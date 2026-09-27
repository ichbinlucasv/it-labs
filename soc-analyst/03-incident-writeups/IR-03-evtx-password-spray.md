# IR-03 — Kerberos password spraying in Windows Security logs

| Field | Value |
|-------|-------|
| Analyst | Lucas |
| Date of analysis | TBD |
| Dataset & URL | EVTX-ATTACK-SAMPLES by Samir Bousseaden — <https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES> — file `Credential Access/kerberos_pwd_spray_4771.evtx` (file presence in the repo checked 2026-09-27; contents not yet analysed) |
| Licence | See the repository (GPL) |
| Dataset file SHA256 | TBD |
| Severity | TBD |
| Status | Draft — investigation plan, no findings yet |

## 1. Executive summary

TBD.

## 2. Scope & questions

- How many accounts were targeted and from which source address/host?
- Over what time window, and at what rate?
- Which Kerberos failure codes appear, and what do they tell us?
- Did any account **succeed** (look for 4768 success / 4624 for the same
  accounts and source after the failures)? — if the file contains them.
- Spraying (many users, few passwords) or brute force (one user, many passwords)?

Background — Event **4771** = Kerberos pre-authentication failed (on a DC).
Useful `Failure Code` values: `0x18` wrong password, `0x6` unknown user
(normally logged as 4768 failure), `0x12` account disabled/locked/expired.

## 3. Investigation plan

| # | Tool | Action | Result |
|---|------|--------|--------|
| 1 | `sha256sum` | Hash the EVTX | TBD |
| 2 | `evtx_dump` (<https://github.com/omerbenamram/evtx>) | `evtx_dump -o jsonl kerberos_pwd_spray_4771.evtx > spray.jsonl` | TBD |
| 3 | `jq` | Count events by EventID: `jq -r '.Event.System.EventID' spray.jsonl \| sort \| uniq -c` | TBD |
| 4 | `jq` | Distinct target users: `jq -r '.Event.EventData.TargetUserName' spray.jsonl \| sort -u \| wc -l` | TBD |
| 5 | `jq` | Source addresses: `.Event.EventData.IpAddress` | TBD |
| 6 | `jq` | Failure codes: `.Event.EventData.Status` | TBD |
| 7 | spreadsheet / Python | Events per minute → rate & duration | TBD |
| 8 | My Sigma correlation rule idea | Adapt [`win_bruteforce_failed_logons_correlation.yml`](../05-sigma-rules/rules/win_bruteforce_failed_logons_correlation.yml) to 4771 grouped by `IpAddress` with `value_count` of `TargetUserName` | TBD |
| 9 | Hayabusa / Chainsaw (optional) | Run against the file and compare their detections with mine | TBD |

## 4. Timeline

TBD

## 5. IOCs

TBD (source host/IP, targeted accounts — sample data only).

## 6. ATT&CK mapping

Candidate to confirm: **T1110.003 Brute Force: Password Spraying**
(Credential Access).

## 7–8. Impact & recommendations

TBD — typical: lockout policy review, MFA, detection on distinct-user count
per source, investigate source host.

## 9. Evidence

`evidence/IR-03/` — jq outputs, per-minute chart, tool screenshots.
