# IR-02 — Web scan, login posts, and a workstation process chain

**English** · [Français](IR-02-splunk-bots-v1.fr.md) · [Deutsch](IR-02-splunk-bots-v1.de.md)

| Field | Value |
|-------|-------|
| Analyst | Lab analyst |
| Date of analysis | 2026-10-21 |
| Dataset & URL | Synthetic rows loaded by [`investigate_sql.py`](investigate_sql.py). This is **not** Splunk Boss of the SOC v1. That archive is several gigabytes and was not loaded. The questions follow the same analyst loop (who scanned, what did the IDS say, was there a brute force, what ran next). |
| Dataset file SHA256 | Not a single file. The rows live in the script. `sha256sum investigate_sql.py` is the way to pin the version that was queried. |
| Data time range (UTC) | 2026-10-20 14:01:00 – 16:12:00 |
| Severity | Medium for the story in the rows (scan, repeated login posts, Word spawning encoded PowerShell). No production system is involved. |
| Status | Complete |

```bash
python3 investigate_sql.py
```

Full output: [`evidence/IR-02/analysis.txt`](evidence/IR-02/analysis.txt).

## 1. Executive summary

Two things happen in this sample, and the logs do not prove they are the same attacker. Between 14:01 and 14:12 UTC, `198.51.100.23` (user agent `lab-scanner/1.0`) requested eight paths on the web server `203.0.113.10`, including four `POST /login` calls, and uploaded a name `notes.txt`. The IDS rows say "lab web probe" and "lab login". The web server then opened TCP/443 to `203.0.113.80` twice. Later, on workstation `ws-04` (`198.51.100.50`), `explorer.exe` started `WINWORD.EXE` on `report.docm`, and Word started `powershell.exe` with `-enc`. The decoded command is the harmless string `echo test`. The workstation also resolved `beacon.example`. I would escalate the process chain. I would not call the text upload a webshell: the only filename in the log is `notes.txt`.

## 2. Scope & questions

- Who talked to the web server, and with which client?
- Did an IDS signature fire?
- Was `/login` posted repeatedly, and was a filename stored?
- Where did the web server connect afterwards?
- What process chain ran on the workstation, and which names did it resolve?

## 3. Investigation log

Queries are the SQL statements in `investigate_sql.py`. Results below are the rows that came back on 2026-10-21.

| # | Question | Result |
|---|----------|--------|
| 1 | Tables and hosts | `http` 9 rows to `203.0.113.10`; `ids` 2 rows to the same host; `process` 2 rows on `ws-04`; `dns` 3 rows from `198.51.100.50` |
| 2 | Who hit the web server | `198.51.100.23` / `lab-scanner/1.0` × 8; `198.51.100.50` / `Mozilla/5.0` × 1 |
| 3 | IDS signatures | `ET SCAN lab web probe` × 1; `ET BRUTE FORCE lab login` × 1 |
| 4 | `POST /login` | 4, all from `198.51.100.23` |
| 5 | Upload filename | `2026-10-20T14:12:00Z` `POST /upload` filename `notes.txt` |
| 6 | Web server egress | `203.0.113.80:443` × 2 |
| 7 | Process chain | `explorer.exe` → `WINWORD.EXE` (`report.docm`), then `WINWORD.EXE` → `powershell.exe -enc …` |
| 8 | DNS from the workstation | `beacon.example` × 2, `intranet.example` × 1 |

## 4. Timeline

| Time (UTC) | Host | Event | ATT&CK |
|------------|------|-------|--------|
| 14:01:00–14:01:04 | 203.0.113.10 | GET `/`, `/login`, `/admin` from 198.51.100.23 | T1595 |
| 14:01:01 | 203.0.113.10 | IDS: lab web probe | T1595 |
| 14:05:01–14:05:07 | 203.0.113.10 | Four `POST /login` from the same address | T1110 |
| 14:05:02 | 203.0.113.10 | IDS: lab login | T1110 |
| 14:12:00 | 203.0.113.10 | `POST /upload` filename `notes.txt` | – |
| 14:20:00 and 14:20:30 | 203.0.113.10 | Outbound 443 to 203.0.113.80 | T1071.001 |
| 16:09:00 | ws-04 | explorer.exe starts WINWORD.EXE on report.docm | T1204.002 |
| 16:09:05 | ws-04 | WINWORD.EXE starts powershell.exe `-enc` (`echo test`) | T1059.001 |
| 16:11–16:12 | 198.51.100.50 | DNS `beacon.example` | T1071.001 |

The workstation's normal browser GET of `/` at 15:00 is a separate user agent and is not part of the scan.

## 5. Indicators (defanged)

| Type | Value | Context |
|------|-------|---------|
| IPv4 | `198.51.100.23` | Scanner and login posts |
| User-Agent | `lab-scanner/1.0` | All eight scanner requests |
| IPv4 | `203.0.113.80` | Web server egress and the name `beacon.example` in the other lab capture |
| Domain | `beacon[.]example` | Workstation DNS |
| Process | `WINWORD.EXE` → `powershell.exe -enc` | Parent/child that should be rare |
| Filename | `notes.txt` | Upload name only. Not treated as malware. |

The encoded blob `ZQBjAGgAbwAgAHQAZQBzAHQA` decodes as UTF-16LE to `echo test`. It is a lab marker, not a payload to run.

## 6. ATT&CK mapping

| Tactic | Technique | Evidence |
|--------|-----------|----------|
| Reconnaissance | T1595 Active Scanning | Three GETs plus the scan signature |
| Credential Access | T1110 Brute Force | Four posts to `/login` and the brute-force signature |
| Execution | T1204.002 Malicious File | Word opened `report.docm` |
| Execution | T1059.001 PowerShell | `-enc` child of WINWORD.EXE |
| Command and Control | T1071.001 Web Protocols | 443 to 203.0.113.80 and DNS for `beacon.example` |

Not confirmed, because the rows do not show them: T1190, T1505.003, T1486, T1091, T1491.002. A filename of `notes.txt` is not a web shell.

## 7. Impact assessment

The web server accepted four login posts and one upload of a text name. The rows do not say the password was correct. The workstation ran encoded PowerShell as the child of Word, which is the higher-severity fact, even though the decoded text is harmless. No user account is named.

## 8. Recommendations

- **Containment:** isolate `ws-04` in a real environment before collecting the PowerShell console history. Reset any account that authenticated from `198.51.100.23` if a success row appears — none does here.
- **Eradication:** remove the Run-key or scheduled task if a follow-up log shows one. This dataset has no persistence event.
- **Detection:** the existing Sigma rule `win_office_spawns_script_interpreter` matches the Word → PowerShell shape, and `win_powershell_encoded_hidden` matches `-enc` with a hidden window. Replay those rules on real endpoint logs; do not wait for Splunk.
- **Lessons learned:** SQL was enough to answer the triage questions. The tool matters less than writing down the question, the query, and the row count.

## 9. Evidence

- [`evidence/IR-02/analysis.txt`](evidence/IR-02/analysis.txt)
- [`investigate_sql.py`](investigate_sql.py) — schema, rows, and queries.
