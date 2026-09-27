# IR-03 — Kerberos password spraying in Windows Security logs

| Field | Value |
|-------|-------|
| Analyst | Lucas |
| Date of analysis | 2026-09-27 |
| Dataset & URL | EVTX-ATTACK-SAMPLES by Samir Bousseaden — <https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES> — file `Credential Access/kerberos_pwd_spray_4771.evtx` (downloaded 2026-09-27 from the raw GitHub URL) |
| Licence | See the repository (GPL) |
| Dataset file SHA256 | `4a0a1c7132e216dbc704c806e9429df9ae3ac00485d5238e50c776e3099ae11d` |
| Data time range (UTC) | 2020-07-22 20:29:27.321 – 20:29:36.437 (12 events) |
| Severity | High (a valid domain password was found) — in a real environment |
| Status | Complete |

The host names, account names and addresses below come from this public
training sample (a lab domain `threebeesco.com`), not from a real incident.
Full command output: [`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt).

## 1. Executive summary

On the domain controller `01566s-win16-ir.threebeesco.com`, one source
address, `172.16.66.1`, requested Kerberos tickets for **10 different
accounts within 11 milliseconds** — only a tool does that. Seven names did
not exist, two existing accounts (`Administrator`, `backdoor`) were refused
for a wrong password, and **one account, `normal`, received a ticket**:
the password tried was correct for it. This is password spraying (one
password, many accounts), and it succeeded for one account. Recommended
actions: reset `normal`'s password, review what the source host did with the
ticket, and investigate the account named `backdoor`.

## 2. Scope & questions — answers

| Question | Answer |
|----------|--------|
| How many accounts, from where? | 10 distinct user names, all from `172.16.66.1` (the last event shows it as `::ffff:172.16.66.1`, the IPv4-mapped IPv6 form) |
| Time window and rate? | 20:29:36.414 → 20:29:36.437 UTC: 11 requests in 23 ms, all 10 names in the first 20 ms |
| Kerberos failure codes? | 4768 `0x6` (KDC_ERR_C_PRINCIPAL_UNKNOWN — user does not exist) × 7; 4771 `0x18` (KDC_ERR_PREAUTH_FAILED — wrong password) × 2 |
| Did any account succeed? | **Yes** — 4768 with status `0x0` for `normal` (twice, AES256 ticket `0x12`), 9 ms after the failures |
| Spraying or brute force? | Spraying: each name tried once, many names |

Background: **4768** = a TGT was requested (success or failure, depending on
`Status`); **4771** = Kerberos pre-authentication failed. An unknown user
never reaches pre-authentication, which is why it appears as a 4768 failure
and not as a 4771.

## 3. Investigation log

| # | Tool | Action | Result |
|---|------|--------|--------|
| 1 | `sha256sum` | Hash the EVTX | `4a0a1c71…ae11d` |
| 2 | [`evtx_to_jsonl.py`](evtx_to_jsonl.py) (python-evtx 0.8.1) | Convert to one JSON object per event | 12 events. I used python-evtx instead of the planned `evtx_dump` because it was one `pip install` away |
| 3 | `jq` | Count by EventID | 1 × 1102, 9 × 4768, 2 × 4771 |
| 4 | `jq` | Distinct target users | 10 (`HD01`, `HD02`, `admin`, `admin02`, `svc-01`, `svc-02`, `bob`, `Administrator`, `backdoor`, `normal`) |
| 5 | `jq` | Source addresses | only `172.16.66.1` (source ports 55957–55969 increasing, then 52559 over IPv6-mapped) |
| 6 | `jq` | Status codes | `0x6` × 7, `0x18` × 2, `0x0` × 2 |
| 7 | `jq` | Rate | whole spray < 25 ms — per-minute chart unnecessary |
| 8 | Sigma | New rule [`win_kerberos_password_spray_correlation.yml`](../05-sigma-rules/rules/win_kerberos_password_spray_correlation.yml): `value_count` of distinct `TargetUserName` ≥ 5 per `IpAddress` in 5 min over 4771 `0x18` / 4768 `0x6`; `sigma check` clean; converted with the SQLite backend and run on the events | 3 alerts for `172.16.66.1` (5, 7, 9 distinct users) |
| 9 | Hayabusa / Chainsaw | Not run | — |

## 4. Timeline (UTC, 2020-07-22)

| Time | Event | Detail |
|------|-------|--------|
| 20:29:27.321 | 1102 | Security log cleared by `3B\a-jbrown` |
| 20:29:36.414–.415 | 4768 `0x6` × 7 | Unknown users `HD01`, `admin`, `svc-02`, `HD02`, `svc-01`, `bob`, `admin02` |
| 20:29:36.425 | 4771 `0x18` × 2 | Wrong password for `Administrator`, `backdoor` |
| 20:29:36.434 | 4768 `0x0` | TGT issued to `normal` |
| 20:29:36.437 | 4768 `0x0` | Second TGT for `normal` from `::ffff:172.16.66.1` |

About the 1102: the log was cleared 9 s before the spray. In this sample
it is most likely the dataset author resetting the log before recording
(`a-jbrown` looks like an admin account). In a real case a cleared log right
before an attack would itself be a serious finding (T1070.001); here I note
it but do not attribute it to the attacker.

## 5. IOCs (sample data)

| Type | Value | Note |
|------|-------|------|
| Source IP | `172.16.66.1` | Internal address — the host itself must be investigated |
| Compromised account | `normal` | Password guessed |
| Targeted existing accounts | `Administrator`, `backdoor` | `backdoor` is a suspicious name for an account that exists |
| Non-existent names tried | `HD01`, `HD02`, `admin`, `admin02`, `svc-01`, `svc-02`, `bob` | Typical guessed-name list |

## 6. ATT&CK mapping

- **T1110.003 Brute Force: Password Spraying** (Credential Access) —
  confirmed: one attempt per account across 10 accounts.
- **T1078.002 Valid Accounts: Domain Accounts** — possible next step: the
  ticket for `normal` would let the attacker act as that user. The sample ends
  there, so this is not confirmed.
- T1070.001 Clear Windows Event Logs — noted, not attributed (see timeline).

## 7. Impact

One domain account's password is known to whoever controls `172.16.66.1`.
The attacker also learned which of the tried names exist (`0x6` vs `0x18`
tells them), including `Administrator` and `backdoor`.

## 8. Recommendations

1. Reset `normal`'s password, revoke its sessions/tickets, and review its
   logons (4624/4769) after 20:29:36 for lateral movement.
2. Investigate the host at `172.16.66.1` (what process sent the requests).
3. Find out who created `backdoor` and why (4720 events, `whenCreated`).
4. Enforce a password policy that blocks common passwords, and MFA where possible.
5. Deploy the distinct-user correlation rule. Two lessons from testing it:
   normalise `::ffff:x.x.x.x` to `x.x.x.x` before grouping (otherwise the
   same host counts as two sources), and add a follow-up rule "success for
   one of the sprayed accounts from the same source" — my rule alerts on the
   failures but the **success** is the event that matters most.

## 9. Evidence

- [`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt) — hash, event
  table, counts, and the Sigma replay result. The EVTX itself is not committed.
