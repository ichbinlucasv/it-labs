//! Minimal file-integrity monitoring (FIM), the idea behind tools like
//! AIDE, Tripwire or Wazuh syscheck:
//!
//! 1. `baseline`: walk a directory, record SHA-256 + size of every regular file.
//! 2. `check`: walk it again and report files that were **added**, **removed**
//!    or **modified** compared to the baseline.
//!
//! Baseline format is a simple, diff-friendly TSV: `sha256<TAB>size<TAB>relative/path`.
//! Symlinks are not followed (a symlink loop or a link to /dev must not hang the scan).

use sha2::{Digest, Sha256};
use std::collections::BTreeMap;
use std::fmt;
use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Read, Write};
use std::path::{Path, PathBuf};

/// Hash + size of one file.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FileRecord {
    pub sha256: String,
    pub size: u64,
}

/// Relative path -> record. `BTreeMap` keeps output sorted and deterministic.
pub type Baseline = BTreeMap<String, FileRecord>;

/// Result of comparing the current state with a baseline.
#[derive(Debug, Default, PartialEq, Eq)]
pub struct Report {
    pub added: Vec<String>,
    pub removed: Vec<String>,
    pub modified: Vec<String>,
    pub unchanged: usize,
}

impl Report {
    pub fn is_clean(&self) -> bool {
        self.added.is_empty() && self.removed.is_empty() && self.modified.is_empty()
    }
}

impl fmt::Display for Report {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for p in &self.added {
            writeln!(f, "ADDED     {p}")?;
        }
        for p in &self.removed {
            writeln!(f, "REMOVED   {p}")?;
        }
        for p in &self.modified {
            writeln!(f, "MODIFIED  {p}")?;
        }
        write!(
            f,
            "{} added, {} removed, {} modified, {} unchanged",
            self.added.len(),
            self.removed.len(),
            self.modified.len(),
            self.unchanged
        )
    }
}

/// SHA-256 of a file, streamed in 64 KiB chunks.
pub fn hash_file(path: &Path) -> io::Result<FileRecord> {
    let mut file = File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buf = [0u8; 64 * 1024];
    let mut size = 0u64;
    loop {
        let n = file.read(&mut buf)?;
        if n == 0 {
            break;
        }
        size += n as u64;
        hasher.update(&buf[..n]);
    }
    Ok(FileRecord {
        sha256: format!("{:x}", hasher.finalize()),
        size,
    })
}

fn walk(dir: &Path, out: &mut Vec<PathBuf>) -> io::Result<()> {
    let mut entries: Vec<_> = fs::read_dir(dir)?.collect::<Result<_, _>>()?;
    entries.sort_by_key(|e| e.file_name());
    for entry in entries {
        let ft = entry.file_type()?; // does not follow symlinks
        let path = entry.path();
        if ft.is_dir() {
            walk(&path, out)?;
        } else if ft.is_file() {
            out.push(path);
        }
    }
    Ok(())
}

/// Path relative to `root`, always with `/` separators.
fn rel(root: &Path, path: &Path) -> String {
    let r = path.strip_prefix(root).unwrap_or(path);
    r.components()
        .map(|c| c.as_os_str().to_string_lossy())
        .collect::<Vec<_>>()
        .join("/")
}

/// Build a baseline for every regular file under `root`.
/// `exclude` holds relative paths to skip (e.g. the baseline file itself).
pub fn build_baseline(root: &Path, exclude: &[String]) -> io::Result<Baseline> {
    let mut files = Vec::new();
    walk(root, &mut files)?;
    let mut baseline = Baseline::new();
    for path in files {
        let key = rel(root, &path);
        if exclude.iter().any(|e| e == &key) {
            continue;
        }
        baseline.insert(key, hash_file(&path)?);
    }
    Ok(baseline)
}

/// Compare two baselines (`old` = trusted, `new` = current).
pub fn compare(old: &Baseline, new: &Baseline) -> Report {
    let mut r = Report::default();
    for (path, rec) in new {
        match old.get(path) {
            None => r.added.push(path.clone()),
            Some(o) if o != rec => r.modified.push(path.clone()),
            Some(_) => r.unchanged += 1,
        }
    }
    r.removed = old
        .keys()
        .filter(|p| !new.contains_key(*p))
        .cloned()
        .collect();
    r
}

/// Serialise a baseline as TSV.
pub fn write_baseline<W: Write>(baseline: &Baseline, mut w: W) -> io::Result<()> {
    writeln!(w, "# fim baseline v1: sha256<TAB>size<TAB>path")?;
    for (path, rec) in baseline {
        if path.contains('\t') || path.contains('\n') {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                format!("unsupported character in file name: {path:?}"),
            ));
        }
        writeln!(w, "{}\t{}\t{}", rec.sha256, rec.size, path)?;
    }
    Ok(())
}

/// Parse a TSV baseline. Comment lines start with `#`.
pub fn read_baseline<R: Read>(r: R) -> io::Result<Baseline> {
    let mut baseline = Baseline::new();
    for (no, line) in BufReader::new(r).lines().enumerate() {
        let line = line?;
        if line.trim().is_empty() || line.starts_with('#') {
            continue;
        }
        let mut parts = line.splitn(3, '\t');
        let bad = || {
            io::Error::new(
                io::ErrorKind::InvalidData,
                format!("bad baseline line {}", no + 1),
            )
        };
        let sha256 = parts.next().ok_or_else(bad)?.to_string();
        let size = parts
            .next()
            .ok_or_else(bad)?
            .parse::<u64>()
            .map_err(|_| bad())?;
        let path = parts.next().ok_or_else(bad)?.to_string();
        if sha256.len() != 64 || !sha256.bytes().all(|b| b.is_ascii_hexdigit()) {
            return Err(bad());
        }
        baseline.insert(path, FileRecord { sha256, size });
    }
    Ok(baseline)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::time::{SystemTime, UNIX_EPOCH};

    /// Self-cleaning temporary directory (std only, no extra crates).
    struct TempDir(PathBuf);
    impl TempDir {
        fn new(tag: &str) -> Self {
            let nanos = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_nanos();
            let p =
                std::env::temp_dir().join(format!("fim-test-{tag}-{}-{nanos}", std::process::id()));
            fs::create_dir_all(&p).unwrap();
            TempDir(p)
        }
    }
    impl Drop for TempDir {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }

    #[test]
    fn known_sha256_vectors() {
        let t = TempDir::new("vec");
        let empty = t.0.join("empty");
        fs::write(&empty, b"").unwrap();
        assert_eq!(
            hash_file(&empty).unwrap().sha256,
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        );
        let abc = t.0.join("abc");
        fs::write(&abc, b"abc").unwrap();
        let rec = hash_file(&abc).unwrap();
        assert_eq!(
            rec.sha256,
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
        );
        assert_eq!(rec.size, 3);
    }

    #[test]
    fn detects_added_removed_modified() {
        let t = TempDir::new("cmp");
        let root = &t.0;
        fs::create_dir_all(root.join("etc/ssh")).unwrap();
        fs::write(root.join("etc/hosts"), "127.0.0.1 localhost\n").unwrap();
        fs::write(root.join("etc/ssh/sshd_config"), "PermitRootLogin no\n").unwrap();
        fs::write(root.join("etc/motd"), "welcome\n").unwrap();

        let before = build_baseline(root, &[]).unwrap();
        assert_eq!(before.len(), 3);
        assert!(before.contains_key("etc/ssh/sshd_config"));

        fs::write(root.join("etc/ssh/sshd_config"), "PermitRootLogin yes\n").unwrap();
        fs::remove_file(root.join("etc/motd")).unwrap();
        fs::write(root.join("etc/cron.evil"), "* * * * * root /tmp/x\n").unwrap();

        let after = build_baseline(root, &[]).unwrap();
        let report = compare(&before, &after);
        assert_eq!(report.added, vec!["etc/cron.evil"]);
        assert_eq!(report.removed, vec!["etc/motd"]);
        assert_eq!(report.modified, vec!["etc/ssh/sshd_config"]);
        assert_eq!(report.unchanged, 1);
        assert!(!report.is_clean());
        assert!(report
            .to_string()
            .contains("1 added, 1 removed, 1 modified, 1 unchanged"));
    }

    #[test]
    fn unchanged_tree_is_clean_and_exclude_works() {
        let t = TempDir::new("clean");
        fs::write(t.0.join("a.txt"), "a").unwrap();
        fs::write(t.0.join("baseline.tsv"), "ignored").unwrap();
        let b1 = build_baseline(&t.0, &["baseline.tsv".to_string()]).unwrap();
        assert_eq!(b1.keys().collect::<Vec<_>>(), vec!["a.txt"]);
        let b2 = build_baseline(&t.0, &["baseline.tsv".to_string()]).unwrap();
        assert!(compare(&b1, &b2).is_clean());
    }

    #[test]
    fn baseline_roundtrip_and_validation() {
        let mut b = Baseline::new();
        b.insert(
            "dir/file name.txt".into(),
            FileRecord {
                sha256: "a".repeat(64),
                size: 42,
            },
        );
        let mut buf = Vec::new();
        write_baseline(&b, &mut buf).unwrap();
        let text = String::from_utf8(buf.clone()).unwrap();
        assert!(text.starts_with("# fim baseline v1"));
        assert_eq!(read_baseline(&buf[..]).unwrap(), b);

        assert!(read_baseline("zz\t1\tx\n".as_bytes()).is_err());
        assert!(read_baseline(format!("{}\tNaN\tx\n", "a".repeat(64)).as_bytes()).is_err());
        assert!(read_baseline(format!("{}\t1\n", "a".repeat(64)).as_bytes()).is_err());
    }

    #[cfg(unix)]
    #[test]
    fn symlinks_are_not_followed() {
        let t = TempDir::new("link");
        fs::write(t.0.join("real.txt"), "x").unwrap();
        std::os::unix::fs::symlink(&t.0, t.0.join("loop")).unwrap();
        let b = build_baseline(&t.0, &[]).unwrap();
        assert_eq!(b.keys().collect::<Vec<_>>(), vec!["real.txt"]);
    }
}
