# IR-02 — Splunk Boss of the SOC v1 investigation

**English** · [Français](IR-02-splunk-bots-v1.fr.md) · [Deutsch](IR-02-splunk-bots-v1.de.md)

| Field | Value |
|-------|-------|
| Analyst | Lucas |
| Date of analysis | TBD |
| Dataset & URL | Splunk BOTS v1 — <https://github.com/splunk/botsv1> (full pre-indexed app ~6 GB, or `botsv1-attack-only.tgz` ~135 MB "just the needles, no haystack") |
| Scenario / CTF platform | Splunk BOTS portal <https://bots.splunk.com/> and the CTF scoreboard app <https://github.com/splunk/SA-ctf_scoreboard> (scenario questions) |
| Dataset file SHA256 | TBD |
| Severity | TBD |
| Status | Draft — investigation plan, no findings yet |

## 1. Executive summary

TBD.

## 2. Scope & questions

BOTS v1 contains two scenarios at the fictional company Wayne Enterprises:
**(A)** a compromise and defacement of a company web site, and **(B)** a
ransomware infection on a user workstation. I will work scenario A first,
then B, and answer the investigation questions myself before comparing with
any public write-up.

Data sources available (from the dataset README): Windows Event Logs,
Sysmon, IIS, Fortigate (`fgt_*`), Suricata, Splunk Stream (`stream:dns`,
`stream:http`, `stream:smb`...), Nessus, Windows registry.

## 3. Investigation plan (scenario A — web server compromise)

| # | Question | Starting SPL (generic) | Result |
|---|----------|------------------------|--------|
| 1 | Which sourcetypes/hosts exist? | `index=botsv1 earliest=0 \| stats count by sourcetype, host` | TBD |
| 2 | Who scanned the web site? | `index=botsv1 sourcetype=stream:http dest_ip=<web server> \| stats count by src_ip, http_user_agent \| sort -count` | TBD |
| 3 | Which IDS alerts fired on the web server? | `index=botsv1 sourcetype=suricata dest_ip=<web server> \| stats count by alert.signature` | TBD |
| 4 | Brute-force attempts against the login page? | `index=botsv1 sourcetype=stream:http http_method=POST uri="*login*" \| stats count by src_ip` | TBD |
| 5 | Was a file uploaded / executed? | `index=botsv1 sourcetype=stream:http http_method=POST \| search part_filename=*` and Sysmon EventCode=1 on the server | TBD |
| 6 | What outbound connections did the server make? | `index=botsv1 src_ip=<web server> sourcetype=fgt_traffic \| stats count by dest_ip, dest_port` | TBD |

## 3b. Investigation plan (scenario B — workstation ransomware)

| # | Question | Starting SPL (generic) | Result |
|---|----------|------------------------|--------|
| 1 | Victim host IP on the day in question | `index=botsv1 sourcetype=stream:dhcp` / `WinEventLog:Security` | TBD |
| 2 | What process chain started the infection? | `index=botsv1 sourcetype=XmlWinEventLog:Microsoft-Windows-Sysmon/Operational EventCode=1 host=<victim> \| table _time ParentImage Image CommandLine` | TBD |
| 3 | Removable media involved? | `index=botsv1 sourcetype=winregistry host=<victim>` | TBD |
| 4 | Domains contacted | `index=botsv1 sourcetype=stream:dns src_ip=<victim> \| stats count by query` | TBD |
| 5 | Files encrypted locally / on shares | Sysmon EventCode=2/11 and `stream:smb` / `WinEventLog:Security` 5145 | TBD |

## 4. Timeline

TBD

## 5. IOCs (defanged)

TBD

## 6. ATT&CK mapping

TBD — candidates to verify: T1595 Active Scanning, T1110 Brute Force,
T1190 Exploit Public-Facing Application, T1505.003 Web Shell,
T1491.002 External Defacement (scenario A); T1091 Replication Through
Removable Media, T1204.002 Malicious File, T1486 Data Encrypted for Impact
(scenario B).

## 7–8. Impact & recommendations

TBD

## 9. Evidence

`evidence/IR-02/` — SPL queries (saved as text) + screenshots of results.
