# IR-02 — Untersuchung Splunk Boss of the SOC v1

[English](IR-02-splunk-bots-v1.md) · [Français](IR-02-splunk-bots-v1.fr.md) · **Deutsch**

| Feld | Wert |
|------|------|
| Analyst | Lucas |
| Datum der Analyse | TBD |
| Datensatz und URL | Splunk BOTS v1 — <https://github.com/splunk/botsv1> (vollständige vorindexierte App ~6 GB, oder `botsv1-attack-only.tgz` ~135 MB „just the needles, no haystack“) |
| Szenario / CTF-Plattform | Splunk-BOTS-Portal <https://bots.splunk.com/> und die CTF-Scoreboard-App <https://github.com/splunk/SA-ctf_scoreboard> (Fragen zum Szenario) |
| SHA256 der Datei | TBD |
| Schwere | TBD |
| Status | Entwurf — Untersuchungsplan, noch keine Feststellungen |

## 1. Zusammenfassung für die Leitung

TBD.

## 2. Umfang und Fragen

BOTS v1 enthält zwei Szenarien in der fiktiven Firma Wayne Enterprises:
**(A)** Kompromittierung und Verunstaltung der Firmenwebsite, und **(B)** eine
Ransomware-Infektion auf dem Arbeitsplatz eines Benutzers. Ich bearbeite
zuerst Szenario A, dann B, und beantworte die Untersuchungsfragen selbst,
bevor ich mit einem öffentlichen Write-up vergleiche.

Verfügbare Quellen (laut README des Datensatzes): Windows Event Logs,
Sysmon, IIS, Fortigate (`fgt_*`), Suricata, Splunk Stream (`stream:dns`,
`stream:http`, `stream:smb`...), Nessus, Windows-Registry.

## 3. Untersuchungsplan (Szenario A — Kompromittierung des Webservers)

| # | Frage | SPL zum Einstieg (generisch) | Ergebnis |
|---|-------|------------------------------|----------|
| 1 | Welche Sourcetypes/Hosts gibt es? | `index=botsv1 earliest=0 \| stats count by sourcetype, host` | TBD |
| 2 | Wer hat die Website gescannt? | `index=botsv1 sourcetype=stream:http dest_ip=<web server> \| stats count by src_ip, http_user_agent \| sort -count` | TBD |
| 3 | Welche IDS-Alarme sind auf dem Webserver ausgelöst? | `index=botsv1 sourcetype=suricata dest_ip=<web server> \| stats count by alert.signature` | TBD |
| 4 | Brute-Force-Versuche gegen die Anmeldeseite? | `index=botsv1 sourcetype=stream:http http_method=POST uri="*login*" \| stats count by src_ip` | TBD |
| 5 | Wurde eine Datei hochgeladen / ausgeführt? | `index=botsv1 sourcetype=stream:http http_method=POST \| search part_filename=*` und Sysmon EventCode=1 auf dem Server | TBD |
| 6 | Welche ausgehenden Verbindungen hat der Server aufgebaut? | `index=botsv1 src_ip=<web server> sourcetype=fgt_traffic \| stats count by dest_ip, dest_port` | TBD |

## 3b. Untersuchungsplan (Szenario B — Ransomware auf einem Arbeitsplatz)

| # | Frage | SPL zum Einstieg (generisch) | Ergebnis |
|---|-------|------------------------------|----------|
| 1 | IP des Opfer-Hosts am betreffenden Tag | `index=botsv1 sourcetype=stream:dhcp` / `WinEventLog:Security` | TBD |
| 2 | Welche Prozesskette hat die Infektion gestartet? | `index=botsv1 sourcetype=XmlWinEventLog:Microsoft-Windows-Sysmon/Operational EventCode=1 host=<victim> \| table _time ParentImage Image CommandLine` | TBD |
| 3 | Wechselmedium beteiligt? | `index=botsv1 sourcetype=winregistry host=<victim>` | TBD |
| 4 | Kontaktierte Domains | `index=botsv1 sourcetype=stream:dns src_ip=<victim> \| stats count by query` | TBD |
| 5 | Dateien lokal / auf Freigaben verschlüsselt | Sysmon EventCode=2/11 und `stream:smb` / `WinEventLog:Security` 5145 | TBD |

## 4. Zeitleiste

TBD

## 5. IOCs (defanged)

TBD

## 6. ATT&CK-Zuordnung

TBD — Kandidaten zum Prüfen: T1595 Active Scanning, T1110 Brute Force,
T1190 Exploit Public-Facing Application, T1505.003 Web Shell,
T1491.002 External Defacement (Szenario A); T1091 Replication Through
Removable Media, T1204.002 Malicious File, T1486 Data Encrypted for Impact
(Szenario B).

## 7–8. Auswirkung und Empfehlungen

TBD

## 9. Nachweise

`evidence/IR-02/` — SPL-Abfragen (als Text gespeichert) + Screenshots der Ergebnisse.
