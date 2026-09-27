//! Parse web server access logs in the Apache/Nginx *combined* format and
//! produce a small security-oriented summary: top clients, status codes,
//! error rates and requests matching simple suspicious patterns
//! (path traversal, probing for admin panels, scanner user agents...).
//!
//! Standard library only. The heuristics are deliberately simple and
//! transparent - they are triage hints, not a WAF.

use std::collections::HashMap;
use std::fmt;

/// One parsed access-log line.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Entry {
    pub client: String,
    pub timestamp: String,
    pub method: String,
    pub path: String,
    pub status: u16,
    pub bytes: u64,
    pub user_agent: String,
}

/// Why a request was flagged.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Finding {
    PathTraversal,
    SensitiveFile,
    AdminProbe,
    ScannerUserAgent,
    InjectionPattern,
}

impl fmt::Display for Finding {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = match self {
            Finding::PathTraversal => "path-traversal",
            Finding::SensitiveFile => "sensitive-file",
            Finding::AdminProbe => "admin-probe",
            Finding::ScannerUserAgent => "scanner-user-agent",
            Finding::InjectionPattern => "injection-pattern",
        };
        f.write_str(s)
    }
}

/// Parse a single combined-log-format line. Returns `None` for malformed lines.
///
/// Format: `client ident user [timestamp] "METHOD path PROTO" status bytes "referer" "user-agent"`
pub fn parse_line(line: &str) -> Option<Entry> {
    let (client, rest) = line.split_once(' ')?;
    let ts_start = rest.find('[')?;
    let ts_end = rest[ts_start..].find(']')? + ts_start;
    let timestamp = rest[ts_start + 1..ts_end].to_string();
    let rest = &rest[ts_end + 1..];

    let mut quoted = rest.split('"');
    let _ = quoted.next()?; // space before request
    let request = quoted.next()?;
    let status_bytes = quoted.next()?.trim();
    let _ = quoted.next(); // referer
    let _ = quoted.next(); // space
    let user_agent = quoted.next().unwrap_or("").to_string();

    let mut req_parts = request.split_whitespace();
    let method = req_parts.next()?.to_string();
    let path = req_parts.next().unwrap_or("").to_string();

    let mut sb = status_bytes.split_whitespace();
    let status: u16 = sb.next()?.parse().ok()?;
    let bytes: u64 = sb.next().and_then(|b| b.parse().ok()).unwrap_or(0);

    Some(Entry {
        client: client.to_string(),
        timestamp,
        method,
        path,
        status,
        bytes,
        user_agent,
    })
}

/// Minimal percent-decoding (enough to catch `%2e%2e%2f` style evasion).
pub fn percent_decode(input: &str) -> String {
    let bytes = input.as_bytes();
    let mut out = Vec::with_capacity(bytes.len());
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i] == b'%' && i + 2 < bytes.len() {
            if let (Some(h), Some(l)) = (hex_val(bytes[i + 1]), hex_val(bytes[i + 2])) {
                out.push(h * 16 + l);
                i += 3;
                continue;
            }
        }
        out.push(if bytes[i] == b'+' { b' ' } else { bytes[i] });
        i += 1;
    }
    String::from_utf8_lossy(&out).into_owned()
}

fn hex_val(b: u8) -> Option<u8> {
    match b {
        b'0'..=b'9' => Some(b - b'0'),
        b'a'..=b'f' => Some(b - b'a' + 10),
        b'A'..=b'F' => Some(b - b'A' + 10),
        _ => None,
    }
}

const SENSITIVE: &[&str] = &[
    "/etc/passwd",
    "/etc/shadow",
    "/.env",
    "/.git/",
    "/.ssh/",
    "web.config",
    "/.htpasswd",
    "/server-status",
    "/phpinfo.php",
    "/backup.zip",
    "/.aws/",
];
const ADMIN: &[&str] = &[
    "/wp-login.php",
    "/wp-admin",
    "/phpmyadmin",
    "/admin",
    "/manager/html",
    "/xmlrpc.php",
    "/cgi-bin/",
    "/actuator",
];
const SCANNER_UA: &[&str] = &[
    "sqlmap",
    "nikto",
    "nmap",
    "masscan",
    "zgrab",
    "gobuster",
    "dirbuster",
    "wpscan",
    "nuclei",
    "acunetix",
    "python-requests",
    "curl/",
];
const INJECTION: &[&str] = &[
    "' or '1'='1",
    "union select",
    "<script",
    "${jndi:",
    "; cat ",
    "|id",
    "sleep(",
    "../../",
    "cmd.exe",
    "/bin/sh",
];

/// Return every heuristic the entry matches (sorted, de-duplicated).
pub fn classify(e: &Entry) -> Vec<Finding> {
    let path = percent_decode(&e.path).to_ascii_lowercase();
    let ua = e.user_agent.to_ascii_lowercase();
    let mut f = Vec::new();
    if path.contains("../") || path.contains("..\\") {
        f.push(Finding::PathTraversal);
    }
    if SENSITIVE.iter().any(|s| path.contains(s)) {
        f.push(Finding::SensitiveFile);
    }
    if ADMIN.iter().any(|s| path.starts_with(s)) {
        f.push(Finding::AdminProbe);
    }
    if SCANNER_UA.iter().any(|s| ua.contains(s)) {
        f.push(Finding::ScannerUserAgent);
    }
    if INJECTION.iter().any(|s| path.contains(s)) {
        f.push(Finding::InjectionPattern);
    }
    f.sort();
    f.dedup();
    f
}

/// Aggregated statistics for a log.
#[derive(Debug, Default)]
pub struct Summary {
    pub total: usize,
    pub malformed: usize,
    pub by_client: HashMap<String, usize>,
    pub by_status: HashMap<u16, usize>,
    pub errors_by_client: HashMap<String, usize>,
    pub flagged: Vec<(Entry, Vec<Finding>)>,
    pub bytes: u64,
}

impl Summary {
    /// Feed lines into a new summary.
    pub fn from_lines<'a, I: IntoIterator<Item = &'a str>>(lines: I) -> Self {
        let mut s = Summary::default();
        for line in lines {
            if line.trim().is_empty() {
                continue;
            }
            match parse_line(line) {
                Some(e) => s.add(e),
                None => s.malformed += 1,
            }
        }
        s
    }

    fn add(&mut self, e: Entry) {
        self.total += 1;
        self.bytes += e.bytes;
        *self.by_client.entry(e.client.clone()).or_default() += 1;
        *self.by_status.entry(e.status).or_default() += 1;
        if e.status >= 400 {
            *self.errors_by_client.entry(e.client.clone()).or_default() += 1;
        }
        let findings = classify(&e);
        if !findings.is_empty() {
            self.flagged.push((e, findings));
        }
    }

    /// Top `n` entries of a counter, sorted by count desc then key asc (deterministic).
    pub fn top<K: Clone + Ord>(map: &HashMap<K, usize>, n: usize) -> Vec<(K, usize)> {
        let mut v: Vec<(K, usize)> = map.iter().map(|(k, c)| (k.clone(), *c)).collect();
        v.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0)));
        v.truncate(n);
        v
    }

    /// Clients with at least `min_errors` 4xx/5xx responses (possible scanning).
    pub fn noisy_clients(&self, min_errors: usize) -> Vec<(String, usize)> {
        Self::top(&self.errors_by_client, usize::MAX)
            .into_iter()
            .filter(|(_, c)| *c >= min_errors)
            .collect()
    }

    /// Human-readable report.
    pub fn report(&self, top_n: usize, min_errors: usize) -> String {
        let mut out = String::new();
        out.push_str("Access log summary\n==================\n");
        out.push_str(&format!(
            "Requests: {}  (malformed lines: {})  bytes sent: {}\n\n",
            self.total, self.malformed, self.bytes
        ));
        out.push_str(&format!("Top {top_n} clients:\n"));
        for (c, n) in Self::top(&self.by_client, top_n) {
            out.push_str(&format!("  {n:>6}  {c}\n"));
        }
        out.push_str("\nStatus codes:\n");
        let mut codes: Vec<_> = self.by_status.iter().collect();
        codes.sort();
        for (code, n) in codes {
            out.push_str(&format!("  {code}: {n}\n"));
        }
        out.push_str(&format!(
            "\nClients with >= {min_errors} error responses:\n"
        ));
        let noisy = self.noisy_clients(min_errors);
        if noisy.is_empty() {
            out.push_str("  (none)\n");
        }
        for (c, n) in noisy {
            out.push_str(&format!("  {c} ({n})\n"));
        }
        out.push_str(&format!("\nFlagged requests: {}\n", self.flagged.len()));
        for (e, f) in &self.flagged {
            let tags: Vec<String> = f.iter().map(|x| x.to_string()).collect();
            out.push_str(&format!(
                "  [{}] {} {} {} -> {} ({})\n",
                e.timestamp,
                e.client,
                e.method,
                e.path,
                e.status,
                tags.join(",")
            ));
        }
        out
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const GOOD: &str = r#"192.0.2.10 - - [14/Sep/2026:21:00:01 +0000] "GET /index.html HTTP/1.1" 200 5120 "-" "Mozilla/5.0""#;

    #[test]
    fn parses_combined_line() {
        let e = parse_line(GOOD).expect("should parse");
        assert_eq!(e.client, "192.0.2.10");
        assert_eq!(e.timestamp, "14/Sep/2026:21:00:01 +0000");
        assert_eq!(e.method, "GET");
        assert_eq!(e.path, "/index.html");
        assert_eq!(e.status, 200);
        assert_eq!(e.bytes, 5120);
        assert_eq!(e.user_agent, "Mozilla/5.0");
    }

    #[test]
    fn dash_bytes_is_zero_and_garbage_is_none() {
        let l = r#"198.51.100.5 - - [14/Sep/2026:21:00:02 +0000] "HEAD / HTTP/1.1" 304 - "-" "x""#;
        assert_eq!(parse_line(l).unwrap().bytes, 0);
        assert!(parse_line("not a log line").is_none());
        assert!(parse_line("").is_none());
    }

    #[test]
    fn percent_decoding() {
        assert_eq!(percent_decode("%2e%2e%2fetc%2Fpasswd"), "../etc/passwd");
        assert_eq!(percent_decode("a+b%20c"), "a b c");
        assert_eq!(percent_decode("100%"), "100%");
        assert_eq!(percent_decode("%zz"), "%zz");
    }

    #[test]
    fn classifies_encoded_traversal() {
        let l = r#"203.0.113.45 - - [14/Sep/2026:21:05:00 +0000] "GET /download?file=%2e%2e%2f%2e%2e%2fetc%2fpasswd HTTP/1.1" 400 0 "-" "curl/8.5.0""#;
        let f = classify(&parse_line(l).unwrap());
        assert_eq!(
            f,
            vec![
                Finding::PathTraversal,
                Finding::SensitiveFile,
                Finding::ScannerUserAgent,
                Finding::InjectionPattern
            ]
        );
    }

    #[test]
    fn benign_request_not_flagged() {
        assert!(classify(&parse_line(GOOD).unwrap()).is_empty());
    }

    #[test]
    fn summary_counts_and_noisy_clients() {
        let log = [
            GOOD,
            r#"203.0.113.45 - - [14/Sep/2026:21:05:00 +0000] "GET /wp-login.php HTTP/1.1" 404 0 "-" "Mozilla/5.0""#,
            r#"203.0.113.45 - - [14/Sep/2026:21:05:01 +0000] "GET /.env HTTP/1.1" 404 0 "-" "Mozilla/5.0""#,
            r#"203.0.113.45 - - [14/Sep/2026:21:05:02 +0000] "GET /phpmyadmin/ HTTP/1.1" 404 0 "-" "Mozilla/5.0""#,
            "broken line",
            "",
        ];
        let s = Summary::from_lines(log);
        assert_eq!(s.total, 4);
        assert_eq!(s.malformed, 1);
        assert_eq!(s.by_status[&404], 3);
        assert_eq!(s.noisy_clients(3), vec![("203.0.113.45".to_string(), 3)]);
        assert!(s.noisy_clients(4).is_empty());
        assert_eq!(s.flagged.len(), 3);
        let top = Summary::top(&s.by_client, 1);
        assert_eq!(top, vec![("203.0.113.45".to_string(), 3)]);
        let report = s.report(5, 3);
        assert!(report.contains("Flagged requests: 3"));
        assert!(report.contains("admin-probe"));
    }
}
