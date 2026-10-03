# IT- & Security-Lab-Portfolio — Lucas

[English](README.md) · [Français](README.fr.md) · **Deutsch**

Ich bin Lucas. Ich studiere Cybersicherheit und suche in Frankreich eine
erste Stelle im Helpdesk oder als Junior-SOC-Analyst (Alternance oder POEI).
Linux ist das System, auf dem ich täglich arbeite. Windows ist ein Lab auf
demselben Rechner.

Zuerst schaue ich in Frankreich. Deutschland ist die andere Möglichkeit.
Dort kann ich auf Englisch arbeiten, und ich lerne Deutsch. Sobald ich
arbeite, beginne ich ein Fernstudium an der IU (Internationale
Hochschule). Die Seiten gibt es auf Englisch, Französisch und Deutsch,
damit jemand in beiden Ländern sie öffnen kann. Englisch aktualisiere
ich zuerst. Wenn eine Übersetzung abweicht, gilt die englische Seite.

**Done** heisst: die Prüfung in diesem Repo ist gelaufen und die Ausgabe
liegt bei. Es heisst nicht, dass ich an einem echten Ticket schon schnell
bin.

Täglich bash, im Windows-Lab PowerShell, dazu kleine Werkzeuge in Python
und Rust. C steht auf der Lernliste. Ein C-Projekt liegt hier noch nicht.

Portugiesisch ist meine Muttersprache. Französisch und Englisch sind C1.
Security+ SY0-701 und HTB Academy laufen nebenher.

Rechner, Sprachen und die KI-Werkzeuge stehen in
[Wie ich arbeite](how-i-work.de.md). Kurz: täglich CachyOS (Arch),
Windows nur als virtuelle Maschinen, Grok für einen zweiten Durchgang,
und ein lokales Qwen-Modell über Ollama, geteilt von Hermes, OpenClaw
und Odysseus. Ein Lab ist **Done**, wenn ich die Prüfung selbst laufen
lasse.

### Lab-Status

| Status | Bedeutung |
|--------|-----------|
| **Done** | Code oder Konfiguration läuft und die Prüfungen in diesem Repo sind erfolgreich |
| **In progress** | Teilweise verifiziert — z. B. Syntax geprüft oder mit synthetischen Daten ausgeführt, aber nicht vollständig in einer realen Umgebung getestet |
| **Planned** | Schriftliche Anleitung, die noch nicht in einer realen Umgebung ausgeführt wurde |

Aktueller Stand: 10 Done, 4 In progress, 3 Planned (siehe Skills-Matrix unten).

> Firmennamen, Benutzernamen und Adressen in den Übungen sind Beispiele
> (`example.com`, RFC 5737 `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`).
> Das Windows-Domänen-Lab ist ein echtes Lab auf diesem PC, im
> Standard-NAT von libvirt `192.168.122.0/24`. Dieser Bereich ist nicht
> mein Heimnetz, und er ist im Internet nicht geroutet. Öffentliche
> Trainingsdaten (Wireshark-Beispiele, EVTX-ATTACK-SAMPLES) stehen mit
> den Originalwerten und der Quelle. Keine Passwörter, keine öffentliche
> IP, und keine Angriffsschritte gegen jemand anderen.

---

## Repository-Übersicht

| Pfad | Inhalt |
|------|--------|
| [how-i-work.de.md](how-i-work.de.md) | Alltagsrechner (CachyOS), Sprachen, und wie ich Grok plus ein lokales Qwen-Modell benutze |
| [`helpdesk/`](helpdesk/) | Tickets, Fehleranalyse unter Linux und Windows, ein Samba-AD-Lab, und eine Windows-Server-Domäne, die auf meinem PC läuft (`lab.local`) |
| [`networking/`](networking/) | Subnetting-Übungen mit Lösungen, Analyse von Netzwerkmitschnitten (Wireshark/tcpdump), Host-Firewall mit nftables |
| [`soc-analyst/`](soc-analyst/) | Wazuh-Homelab, Analyse von Sysmon- und auditd-Logs (synthetische Beispiele), Incident-Berichte auf öffentlichen Datensätzen, ATT&CK-Mapping, Sigma-Regeln |
| [`python/`](python/) | Paket `seclab`: Auswertung von SSH-`auth.log`, IOC-Extraktor (defang/refang), Hash-Prüfer — nur Standardbibliothek, pytest-Suite |
| [`rust/`](rust/) | Cargo-Workspace: Crates `log-analyzer` und `fim` (File-Integrity-Monitoring) mit Unit-Tests |
| [`security-plus/`](security-plus/) | Lernnotizen SY0-701 pro Domäne + Karteikarten (CSV) |
| [`templates/`](templates/) | Leere Formulare für den Arbeitstag: Helpdesk, SOC, und eine Sprache pro Block |
| [`scripts/check_repo.py`](scripts/check_repo.py) | Hygiene-Prüfung des Repos: Abschnitte der Lab-READMEs, Karteikarten-CSV, Sigma-YAML, Muster für Secrets |
| [`.forgejo/workflows-disabled/`](.forgejo/workflows-disabled/) | CI-Workflow, **deaktiviert**, bis ein Runner existiert (siehe [CI](#ci)) |

Jede Lab-README beginnt mit einer **Status**-Zeile und folgt demselben
Aufbau: **Goal · Setup · Steps · Evidence · What I learned** (in den
deutschen Fassungen: Ziel · Aufbau · Schritte · Nachweise · Was ich gelernt habe).

---

## Skills-Matrix — Labs × Security+-SY0-701-Domänen

Domänen: **D1** General Security Concepts · **D2** Threats, Vulnerabilities &
Mitigations · **D3** Security Architecture · **D4** Security Operations ·
**D5** Security Program Management & Oversight.

`●` = Schwerpunkt, `○` = Nebenaspekt.

| Lab | Status | D1 | D2 | D3 | D4 | D5 | Praktische Fähigkeiten |
|-----|--------|:--:|:--:|:--:|:--:|:--:|------------------------|
| [helpdesk/01 Tickets schreiben](helpdesk/01-ticket-writing/) ([DE](helpdesk/01-ticket-writing/README.de.md)) | Done | ○ | | | ● | ○ | ITSM, klare Kommunikation, Eskalation |
| [helpdesk/02 Fehleranalyse Windows](helpdesk/02-windows-troubleshooting/) | Planned | | ○ | ○ | ● | | Ereignisanzeige, PowerShell, Netzwerk, SFC/DISM |
| [helpdesk/03 Fehleranalyse Linux](helpdesk/03-linux-troubleshooting/) ([DE](helpdesk/03-linux-troubleshooting/README.de.md)) | Done | | ○ | ○ | ● | | systemd, journalctl, Speicherplatz/DNS/Berechtigungen |
| [helpdesk/04 Samba AD DC](helpdesk/04-samba-ad-lab/) ([DE](helpdesk/04-samba-ad-lab/README.de.md)) | In progress | ● | | ● | ● | | Identitäten, Gruppen, GPO-Konzepte, Least Privilege |
| [helpdesk/05 M365-Grundlagen](helpdesk/05-m365-basics/) | Planned | ● | ○ | ● | ● | ○ | Entra ID, Lizenzen, MFA, Conditional-Access-Konzepte |
| [helpdesk/06 Windows-Domäne](helpdesk/06-windows-domain/) | In progress | ● | | ● | ● | | AD DS, Client in der Domäne, Helpdesk-Reset, GPO-Prüfung |
| [networking/01 Subnetting](networking/01-subnetting/) | Done | | | ● | | | CIDR, VLSM, Adresspläne |
| [networking/02 Netzwerkmitschnitte](networking/02-packet-capture/) ([DE](networking/02-packet-capture/README.de.md)) | Done | | ● | ○ | ● | | Wireshark-Filter, tcpdump, Protokollanalyse |
| [networking/03 nftables-Firewall](networking/03-nftables-firewall/) ([DE](networking/03-nftables-firewall/README.de.md)) | Done | ○ | ● | ● | ○ | | Default-Deny, zustandsbehaftete Filterung, Logging |
| [soc-analyst/01 Wazuh-Homelab](soc-analyst/01-wazuh-homelab/) | Planned | | ○ | ○ | ● | | SIEM/XDR-Aufbau, Agents, Alarm-Triage |
| [soc-analyst/02 Sysmon + auditd](soc-analyst/02-sysmon-auditd-logs/) ([DE](soc-analyst/02-sysmon-auditd-logs/README.de.md)) | Done | | ● | | ● | | Endpoint-Telemetrie, Log-Korrelation |
| [soc-analyst/03 Incident-Berichte](soc-analyst/03-incident-writeups/) ([DE](soc-analyst/03-incident-writeups/README.de.md)) | In progress | | ● | | ● | ○ | IR-Lebenszyklus, Berichtswesen, Umgang mit Beweismitteln |
| [soc-analyst/04 ATT&CK-Mapping](soc-analyst/04-attack-mapping/) ([DE](soc-analyst/04-attack-mapping/README.de.md)) | Done | | ● | | ● | | Bedrohungsorientierte Abdeckung von Detections |
| [soc-analyst/05 Sigma-Regeln](soc-analyst/05-sigma-rules/) | Done | | ● | | ● | | Detection Engineering, pySigma/sigma-cli |
| [python/ seclab-Tools](python/) | Done | ○ | ● | | ● | | Regex, Parsing, Hashing, automatisierte Tests |
| [rust/ log-analyzer + fim](rust/) | Done | ○ | ○ | ○ | ● | | Integritätsüberwachung, Systemprogrammierung |
| [security-plus/ Notizen & Karteikarten](security-plus/) | In progress | ● | ● | ● | ● | ● | Prüfungsvorbereitung über alle Domänen |

---

## Schnellstart

```bash
# Python tools + tests
(cd python && python3 -m venv .venv && . .venv/bin/activate \
  && pip install -e '.[test]' && pytest)

# Rust workspace
(cd rust && cargo test && cargo clippy --all-targets -- -D warnings)

# Sigma rules: lint + replay on the synthetic samples
python3 -m venv .venv-sigma && . .venv-sigma/bin/activate
pip install sigma-cli pyyaml && sigma plugin install sqlite
sigma check soc-analyst/05-sigma-rules/rules/
python soc-analyst/05-sigma-rules/validate_rules.py

# Repo hygiene
python3 scripts/check_repo.py
```

## Was verifiziert wurde

| Punkt | Wie |
|-------|-----|
| Python-Tools | `pytest` — 35 Tests erfolgreich |
| Rust-Crates | `cargo test` (11 Unit-Tests), `cargo clippy --all-targets -- -D warnings` ohne Befund, `cargo fmt --check` ohne Befund |
| Sigma-Regeln | gültiges YAML; `sigma check` 0 Fehler (sigma-cli 3.1.0); die 8 ursprünglichen Regeln schlagen über das SQLite-Backend auf den synthetischen Beispielen an; die Kerberos-Spraying-Regel schlägt auf einem öffentlichen EVTX-Beispiel an |
| Fehleranalyse Linux | 7 Break/Fix-Szenarien in einem Debian-13-systemd-Container (`systemd-nspawn`) durchgeführt; Terminalausgaben in `helpdesk/03-linux-troubleshooting/evidence/` (OOM-Kill dort nicht reproduzierbar) |
| Samba AD DC | in einem Debian-13-Container provisioniert; DNS-SRV, Kerberos, OUs/Gruppen/Benutzer, Sperrrichtlinie und Helpdesk-Delegation getestet; Domänenbeitritt eines Windows-Clients noch offen |
| Windows-Server-Domäne | `dc01` am 5. Sep 2026 zu `lab.local` promotet. Am 4. Okt. 2026 war `win11-soc` schon in dieser Domäne (`OU=Workstations`, DNS zum DC). Von diesem Client hat das Helpdesk-Credential `jdoe` zurückgesetzt; `jdoe` konnte niemand anderen zurücksetzen. Ausgabe in `helpdesk/06-windows-domain/evidence/win11-2026-10-04.txt`. Die Sperrschwelle ist 0, also noch keine Entsperrung. `Lab-Workstation-Hardening` ist verknüpft und leer |
| nftables-Regelwerk | `nft -c -f` OK; Datenverkehr mit drei Network Namespaces getestet (Admin / extern / gesperrter Client), Zähler und Kernel-Log geprüft |
| Netzwerkmitschnitte | eigener Mitschnitt in einem Network Namespace erzeugt und mit tshark analysiert; öffentliches Wireshark-Beispiel `dns.cap` mit Kurzbericht analysiert |
| Sysmon-/auditd-Beispiele | alle Fragen beantwortet, UTC-Zeitleiste und IOC-Liste erstellt; `ausearch`/`aureport` auf dem synthetischen auditd-Log |
| Incident-Bericht IR-03 | öffentliches Kerberos-Password-Spray-EVTX mit python-evtx eingelesen und vollständig analysiert |
| ATT&CK-Mapping | 15 Technik-IDs gegen das STIX-Bundle ATT&CK Enterprise 19.2 geprüft; Navigator-Layer erzeugt |
| Subnetting-Lösungen | mit Python `ipaddress` berechnet |
| Karteikarten | 99 Karten, mit Python `csv` eingelesen |

Noch offen: eine interaktive Helpdesk-Anmeldung auf dem Windows-11-Desktop,
eine echte Entsperrung sobald die Sperrschwelle nicht mehr 0 ist,
Einstellungen in `Lab-Workstation-Hardening`, die
Windows-Fehleranalyse-Szenarien, ein Windows-Client in der Samba-Domäne,
Wazuh, ein M365-Tenant, eine isolierte VM für die Malware-Mitschnitte,
und Splunk. Das steht auf den jeweiligen Seiten.

## CI

Der Workflow liegt in `.forgejo/workflows-disabled/ci.yml`, damit Forgejo ihn
**nicht** ausführt (die gehosteten Runner von Codeberg sind begrenzt, der Job
würde endlos in der Warteschlange stehen). Er braucht einen
**selbst gehosteten Forgejo-Runner mit dem Label `docker`**. Aktivieren:

1. Einen [Forgejo-Runner](https://forgejo.org/docs/latest/admin/actions/) mit
   dem Label `docker` für dieses Repository registrieren (Codeberg: Repo
   *Settings → Actions → Runners*) und Actions für das Repo aktivieren.
2. `git mv .forgejo/workflows-disabled/ci.yml .forgejo/workflows/ci.yml`, dann committen und pushen.

Auf GitHub die Datei nach `.github/workflows/` kopieren und `runs-on: ubuntu-latest` setzen.

## Aktuelles Lernen

- CompTIA Security+ SY0-701 — in Vorbereitung
- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46) — Profil offen. Academy (SOC Analyst / Grundlagen) ist in Arbeit. Kein Rang auf dieser Seite.
- [TryHackMe](https://tryhackme.com/p/ichbinlucasv) — Konto offen, in Arbeit. Kein Rang auf dieser Seite.
- [Boot.dev](https://www.boot.dev/u/ichbinlucasv) — Konto offen. Das öffentliche Profil bleibt bis Level 10 verborgen, deshalb kein Level hier.

Ein fertiger SOC-Bericht mit Zeitlinie:
[IR-03](soc-analyst/03-incident-writeups/IR-03-evtx-password-spray.md).
Die Prüfung vom 4. Okt. 2026, der Helpdesk-Reset und das Ticket zur
leeren GPO stehen in [Lab 06](helpdesk/06-windows-domain/).
Formulare für das nächste Mal:
[templates/career/](templates/career/).

## Kontakt

Das hier ist öffentlich. Lab-Passwörter und private Notizen bleiben aus diesem Repo.

- E-Mail: ichbinlucas@pm.me
- [LinkedIn](https://www.linkedin.com/in/lucas-nunes-soares-63148637b/)
- [X](https://x.com/ichbinlucasv)
- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46)

## Lizenz

Code: [MIT](LICENSE). Dokumentation (Markdown, Notizen, Karteikarten):
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Siehe [LICENSE](LICENSE).
