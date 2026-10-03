# Python-Sicherheitswerkzeuge (`seclab`)

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Done — drei Werkzeuge mit 35 bestandenen pytest-Tests.

## Ziel

Drei kleine, aber echte Analystenaufgaben mit sauberem, getestetem Python
automatisieren, nur mit der Standardbibliothek:

| Modul | Was es tut |
|-------|------------|
| `seclab.authlog` | Fasst SSH-Fehlschläge und Erfolge aus `auth.log` (oder einer `journalctl`-Ausgabe) zusammen: häufigste IPs, angegriffene Benutzer, nicht vorhandene Benutzer, Schwellwert-Alarme und **erfolgreiche Anmeldungen von IPs, die auch fehlgeschlagen sind** |
| `seclab.ioc` | Zieht IPv4/IPv6, Domänen, URLs, E-Mails, MD5/SHA1/SHA256 aus beliebigem Text; macht defanged Eingaben wieder scharf (`hxxp`, `[.]`, `[@]`…) und kann die Ausgabe zum sicheren Teilen defangen |
| `seclab.hashcheck` | Hasht Dateien (MD5/SHA1/SHA256 in einem Durchgang, in Blöcken) und vergleicht sie mit einer Liste bekannter schlechter Hashes; Exit-Code 1 bei Treffer |

(Security+ D4 — Automatisierung und Skripte, Loganalyse; D2 — Indikatoren.)

## Aufbau

```bash
cd python
python3 -m venv .venv && . .venv/bin/activate
pip install -e '.[test]'      # pytest is the only (test) dependency
pytest
```

Python ≥ 3.10. Keine Abhängigkeiten von Drittbibliotheken zur Laufzeit.

## Schritte

### authlog

```bash
python -m seclab.authlog samples/auth.log.synthetic --threshold 5
sudo python -m seclab.authlog /var/log/auth.log --json
journalctl -u ssh --no-pager -o short-iso | python -m seclab.authlog -
```

Auszug der Ausgabe am synthetischen Beispiel:

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

(Die zweite Zeile ist ein typischer harmloser Fall — der Benutzer hat sich
einmal vertippt und dann seinen Schlüssel benutzt. Der Kontext zählt: das
ist Eingabe für die Triage, kein Urteil.)

### ioc

```bash
python -m seclab.ioc samples/threat-report.synthetic.txt
python -m seclab.ioc samples/threat-report.synthetic.txt --defang --json
python -m seclab.ioc --refang-only < defanged-report.txt
cat ../soc-analyst/02-sysmon-auditd-logs/samples/*.jsonl | python -m seclab.ioc --defang
```

Entwurfsentscheidungen / Grenzen:

- Domänen, deren letztes Label eine übliche Dateiendung ist (`.exe`, `.ps1`,
  `.docm`, `.sh`, `.zip`…), werden ignoriert, auch wenn ein paar davon echte
  TLDs sind.
- Standardmäßig werden nur TLDs mit 2 Buchstaben (Ländercodes) und eine Liste
  üblicher oder missbrauchter generischer TLDs akzeptiert, und Tokens direkt
  nach einem `\` werden übersprungen, damit `CORP\c.martin` oder
  `Content.Word` nicht als Domänen gemeldet werden. `--any-tld` lockert das.
- `--exclude-private` lässt RFC 1918, Loopback, verbindungslokal **und**
  Dokumentationsbereiche weg (Pythons `ipaddress` behandelt RFC-5737-Bereiche
  als nicht global erreichbar).
- Hash-Erkennung nur über die Länge — jede Hex-Zeichenkette mit 32/40/64
  Zeichen trifft.

### hashcheck

```bash
python -m seclab.hashcheck samples/fake_dropper.txt              # just print hashes
python -m seclab.hashcheck -k samples/known_bad.example.txt samples/ ; echo "exit=$?"
python -m seclab.hashcheck -k my_iocs.txt ~/Downloads -r --json
```

`samples/known_bad.example.txt` enthält den SHA256 der harmlosen Datei
`fake_dropper.txt`, die Demo liefert also einen Treffer und Exit-Code 1.

### Tests

```text
$ pytest
35 passed
```

Die Tests decken Randfälle beim Einlesen ab (klassische gegen ISO-Zeitstempel,
rsyslog „message repeated N times“, ungültige IPs), Defang/Refang hin und
zurück, das Filtern von Fehlalarmen, Hashen in Blöcken (> 1 MiB), das
Einlesen der Liste bekannter schlechter Hashes und die Exit-Codes der CLI.

## Nachweise

- Ausgabe von `pytest` (oben; CI ist abgeschaltet, bis ein Runner da ist).
- (Geplant) Screenshot von `authlog` auf dem `auth.log` einer Lab-VM nach dem
  Wazuh-Brute-Force-Test ([SOC-Analyst-Lab 01](../soc-analyst/01-wazuh-homelab/)).

## Was ich gelernt habe

_Noch von Lucas auszufüllen._
