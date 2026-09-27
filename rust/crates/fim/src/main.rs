use std::fs::File;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

const USAGE: &str = "usage:\n  fim baseline <DIR> <BASELINE_FILE>   record SHA-256 of every file under DIR\n  fim check    <DIR> <BASELINE_FILE>   compare DIR against the baseline\n\n\
Exit codes: 0 = no changes / baseline written, 1 = changes detected, 2 = error.";

fn exclude_for(dir: &Path, baseline: &Path) -> Vec<String> {
    // If the baseline file lives inside the monitored directory, skip it.
    match (dir.canonicalize(), baseline.canonicalize()) {
        (Ok(d), Ok(b)) => b
            .strip_prefix(&d)
            .map(|r| vec![r.to_string_lossy().replace('\\', "/")])
            .unwrap_or_default(),
        _ => Vec::new(),
    }
}

fn run() -> Result<ExitCode, String> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args
        .first()
        .map(|a| a == "-h" || a == "--help")
        .unwrap_or(false)
    {
        println!("{USAGE}");
        return Ok(ExitCode::SUCCESS);
    }
    let [cmd, dir, baseline_path] = args.as_slice() else {
        return Err(USAGE.to_string());
    };
    let dir = PathBuf::from(dir);
    let baseline_path = PathBuf::from(baseline_path);

    match cmd.as_str() {
        "baseline" => {
            // create the file first so it can be excluded by path
            let file =
                File::create(&baseline_path).map_err(|e| format!("cannot create baseline: {e}"))?;
            let exclude = exclude_for(&dir, &baseline_path);
            let b = fim::build_baseline(&dir, &exclude).map_err(|e| format!("scan failed: {e}"))?;
            fim::write_baseline(&b, file).map_err(|e| format!("write failed: {e}"))?;
            println!(
                "baseline of {} file(s) written to {}",
                b.len(),
                baseline_path.display()
            );
            Ok(ExitCode::SUCCESS)
        }
        "check" => {
            let file =
                File::open(&baseline_path).map_err(|e| format!("cannot open baseline: {e}"))?;
            let old = fim::read_baseline(file).map_err(|e| format!("invalid baseline: {e}"))?;
            let exclude = exclude_for(&dir, &baseline_path);
            let new =
                fim::build_baseline(&dir, &exclude).map_err(|e| format!("scan failed: {e}"))?;
            let report = fim::compare(&old, &new);
            println!("{report}");
            Ok(if report.is_clean() {
                ExitCode::SUCCESS
            } else {
                ExitCode::from(1)
            })
        }
        _ => Err(USAGE.to_string()),
    }
}

fn main() -> ExitCode {
    match run() {
        Ok(code) => code,
        Err(msg) => {
            eprintln!("{msg}");
            ExitCode::from(2)
        }
    }
}
