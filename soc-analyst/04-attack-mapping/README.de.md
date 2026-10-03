# Lab 04 — MITRE-ATT&CK-Mapping

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Done — Mapping der synthetischen Szenarien gegen die offiziellen STIX-Daten von ATT&CK Enterprise 19.2 geprüft und als Navigator-Layer exportiert ([`coverage-layer.json`](coverage-layer.json), erzeugt mit [`make_layer.py`](make_layer.py)); IR-03 ist bestätigt; die Kandidaten für IR-01/IR-02 bleiben unbestätigt, bis diese [Incident-Berichte](../03-incident-writeups/README.de.md) fertig sind.

## Ziel

Die Verhaltensweisen aus den synthetischen Lab-Szenarien auf MITRE-ATT&CK-
Techniken abbilden, jede mit der Datenquelle verknüpfen, in der sie sichtbar
ist, und mit der Detection, die ich geschrieben habe (oder die noch fehlt),
und so die Lücken in meiner Abdeckung erkennen. (Security+ D2 —
Bedrohungsakteure & TTPs; D4 — Threat Hunting.)

## Aufbau

- MITRE ATT&CK Enterprise: <https://attack.mitre.org/>
- ATT&CK Navigator (für eine Heatmap der Abdeckung): <https://mitre-attack.github.io/attack-navigator/>
- **Versionshinweis:** Mapping gegen ATT&CK Enterprise **v19** geprüft
  (attack.mitre.org, 2026-09-27). In neueren Versionen ist die frühere Taktik
  *Defense Evasion* in **Stealth (TA0005)** und **Defense Impairment
  (TA0112)** aufgeteilt; ältere Unterlagen (und ältere Security+-Bücher)
  sprechen noch von „Defense Evasion“. Alle Technik-IDs wurden zusätzlich
  gegen das offizielle STIX-Bundle 19.2 geprüft (siehe Nachweise).

## Schritte

1. Jede beobachtbare Verhaltensweise aus den synthetischen Szenarien
   ([Lab 02](../02-sysmon-auditd-logs/README.de.md)) und den geplanten
   Incident-Berichten auflisten.
2. Die spezifischste Technik/Sub-Technik finden; die Taktik notieren.
3. Datenquelle und Ereignis notieren, in denen sie sichtbar ist.
4. Die Detection verlinken (Sigma-/Wazuh-Regel) oder als **Lücke (Gap)** markieren.
5. Die Tabelle als ATT&CK-Navigator-Layer exportieren:

   ```bash
   # optional validation source (50 MB, not committed)
   curl -LO https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json
   python3 make_layer.py --stix enterprise-attack.json
   ```

   Danach im ATT&CK Navigator: *Open Existing Layer → Upload from local* →
   `coverage-layer.json`.

Die Tabellen unten bleiben auf Englisch, weil Taktiken und Techniken in
ATT&CK nur englische Namen haben.

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
| IR-03 EVTX password spray | **T1110.003 confirmed** in the [completed write-up](../03-incident-writeups/IR-03-evtx-password-spray.md); T1078.002 possible next step, not in the data; detected by [`win_kerberos_password_spray_correlation`](../05-sigma-rules/rules/win_kerberos_password_spray_correlation.yml) |

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

(Zeile 3 und Zeile 11 zählen jeweils für zwei Taktiken.) Größte Lücke:
**C2 / netzwerkbasierte Detection** → nächster Schritt ist Zeek oder Suricata im Lab.


## Nachweise

- [`coverage-layer.json`](coverage-layer.json): Navigator-Layer mit 15
  Techniken, Score 1 (grün) = Detection in diesem Repo vorhanden, 0 (rot) =
  Lücke; der Kommentar jeder Technik nennt die Tabellenzeilen, aus denen sie stammt.
- Ausgabe von `python3 make_layer.py --stix enterprise-attack.json`:

```text
checked 15 technique IDs against ATT&CK Enterprise 19.2: all valid
wrote coverage-layer.json: 15 techniques, 11 with a detection, 4 gaps
```

  Die 4 Lücken: T1566.001 (keine Mail-Logs im Lab), T1071.001 (C2 über HTTPS
  — Zeile 4 und das 60-s-Beaconing in Zeile 7), T1033 (`whoami`), T1564.001
  (versteckter Dateiname). Die 13 Kandidaten-IDs für die Berichte auf
  öffentlichen Datensätzen existieren ebenfalls und sind in 19.2 nicht
  veraltet, das Mapping selbst ist aber (außer IR-03) unbestätigt.
- Nicht erledigt: Screenshot der Navigator-Heatmap (die Layer-Datei ist die
  Quelle; für den Screenshot fehlt nur der Upload-Schritt oben).

## Was ich gelernt habe

- Eine Verhaltensweise passt oft zu mehr als einer Technik (kodiertes
  PowerShell = T1059.001 + T1027), und dieselbe Technik kann je nach Ort
  erkannt oder übersehen werden (T1105 hat unter Linux eine Regel, unter Windows nicht).
- Technik-IDs und Taktiknamen ändern sich zwischen ATT&CK-Versionen (Defense
  Evasion wurde aufgeteilt); die Prüfung gegen die offiziellen STIX-Daten
  einer genannten Version verhindert, dass man etwas zitiert, das es nicht mehr gibt.
- Zählen pro Technik verdeckt Details: Laut Layer ist T1071.001 eine Lücke,
  aber die Tabelle zeigt, dass zwei verschiedene Verhaltensweisen dahinterstecken
  (erster Kontakt und Beaconing).
- Meine deutlichste Lücke ist netzwerkbasierte Detection (C2 über HTTPS,
  Beaconing), die Host-Logs und Sigma-Regeln auf Prozessereignissen kaum abdecken.
