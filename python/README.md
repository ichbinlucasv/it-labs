# Python security tools (`seclab`)

## Goal

Automate three small but real analyst chores with clean, tested Python using
only the standard library:

| Module | What it does |
|--------|--------------|
| `seclab.authlog` | Summarises SSH failures/successes from `auth.log` (or `journalctl` output): top IPs, targeted users, non-existent users, threshold alerts, and **successful logins from IPs that also failed** |
| `seclab.ioc` | Extracts IPv4/IPv6, domains, URLs, e-mails, MD5/SHA1/SHA256 from any text; refangs defanged input (`hxxp`, `[.]`, `[@]`…) and can defang output for safe sharing |
| `seclab.hashcheck` | Hashes files (MD5/SHA1/SHA256 in one pass, chunked) and compares them against a known-bad list; exit code 1 on match |

(Security+ D4 — automation & scripting, log analysis; D2 — indicators.)

## Setup

```bash
cd python
python3 -m venv .venv && . .venv/bin/activate
pip install -e '.[test]'      # pytest is the only (test) dependency
pytest
```

Requires Python ≥ 3.10. No third-party runtime dependencies.

## Steps

### authlog

```bash
python -m seclab.authlog samples/auth.log.synthetic --threshold 5
sudo python -m seclab.authlog /var/log/auth.log --json
journalctl -u ssh --no-pager -o short-iso | python -m seclab.authlog -
```

Excerpt of the output on the synthetic sample:

```text
Failed attempts     : 10
Unique source IPs   : 3
...
IPs at or above threshold (5):
  203.0.113.45 (8)

!! Successful login from an IP that also failed:
  2026-09-14T21:40:09.650033+00:00  deploy@203.0.113.45 via password
  2026-09-14T22:02:21.883120+00:00  alice@10.20.30.5 via publickey
```

(The second line is a typical benign case — a user mistyped once, then used
their key. Context matters: this is triage input, not a verdict.)

### ioc

```bash
python -m seclab.ioc samples/threat-report.synthetic.txt
python -m seclab.ioc samples/threat-report.synthetic.txt --defang --json
python -m seclab.ioc --refang-only < defanged-report.txt
cat ../soc-analyst/02-sysmon-auditd-logs/samples/*.jsonl | python -m seclab.ioc --defang
```

Design choices / limitations:

- Domains whose last label is a common file extension (`.exe`, `.ps1`,
  `.docm`, `.sh`, `.zip`…) are ignored, even though a few are real TLDs.
- By default only 2-letter (country-code) TLDs and a list of common/abused
  generic TLDs are accepted, and tokens right after a `\` are skipped, so
  `CORP\c.martin` or `Content.Word` are not reported as domains. Use
  `--any-tld` to relax this.
- `--exclude-private` drops RFC 1918, loopback, link-local **and**
  documentation ranges (Python's `ipaddress` treats RFC 5737 ranges as not
  globally reachable).
- Hash detection is by length only — any 32/40/64-char hex string matches.

### hashcheck

```bash
python -m seclab.hashcheck samples/fake_dropper.txt              # just print hashes
python -m seclab.hashcheck -k samples/known_bad.example.txt samples/ ; echo "exit=$?"
python -m seclab.hashcheck -k my_iocs.txt ~/Downloads -r --json
```

`samples/known_bad.example.txt` contains the SHA256 of the harmless
`fake_dropper.txt`, so the demo produces one match and exit code 1.

### Tests

```text
$ pytest
35 passed
```

Tests cover parsing edge cases (classic vs ISO timestamps, rsyslog "message
repeated N times", invalid IPs), defang/refang round-trips, false-positive
filtering, hash chunking (> 1 MiB), known-bad list parsing, and CLI exit codes.

## Evidence

- `pytest` output (above; also run in CI if enabled).
- Screenshot of `authlog` on my own lab VM's `auth.log` after the Wazuh
  brute-force test ([soc-analyst lab 01](../soc-analyst/01-wazuh-homelab/)).

## What I learned

_To be completed by Lucas._
