# Lab 02 — Analyse von Sysmon- und auditd-Logs

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Done — alle Befehle aus Teil A/B/C liefen gegen die synthetischen Beispiele, meine Antworten, die UTC-Zeitleiste und die IOC-Liste stehen in [`my-timeline.md`](my-timeline.md) (Englisch). Echtes Sysmon auf dem Windows-Gast kommt später. Den Gast gibt es ([Lab 06](../../helpdesk/06-windows-domain/)). Auf dem DC war Sysmon beim Inventory nicht installiert.

## Ziel

Lernen, aus roher Telemetrie zu rekonstruieren, was auf einem Endpoint
passiert ist: Windows **Sysmon** (Prozess-, Netzwerk-, Datei-, Registry- und
DNS-Ereignisse), Windows-**Security**-Anmeldeereignisse und Linux-**auditd**-
Einträge. Eine Zeitleiste erstellen und Indikatoren extrahieren. (Security+
D2 Indikatoren bösartiger Aktivität; D4 Log-Datenquellen und Untersuchung.)

## Aufbau

- Beispiele in [`samples/`](samples/) — **alle synthetisch**, siehe die
  [README der Beispiele](samples/README.md).
- Werkzeuge: `jq`, Python 3 und die Audit-Userspace-Tools (`sudo apt install jq auditd`).
  `ausearch`/`aureport` können mit `-if` eine Logdatei lesen, ohne dass der
  Audit-Daemon läuft.
- Um echte Telemetrie in einem Lab zu erzeugen (noch nicht erledigt):
  - **Sysmon** (Microsoft Sysinternals):
    <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon> —
    `sysmon64.exe -accepteula -i sysmonconfig.xml`
  - Beispielregeln für **auditd** (`/etc/audit/rules.d/lab.rules`):

    ```text
    -w /etc/shadow -p r -k shadow_read
    -w /etc/passwd -p wa -k identity
    -w /var/spool/cron/ -p wa -k cron_mod
    -w /etc/crontab -p wa -k cron_mod
    -a always,exit -F arch=b64 -S execve -F dir=/tmp -k exec_tmp
    -a always,exit -F arch=b64 -S execve -F exe=/usr/bin/curl -k net_download
    ```

    Laden mit `sudo augenrules --load`; siehe auch das Community-Regelwerk
    <https://github.com/Neo23x0/auditd>.

### Hier verwendete Sysmon-Event-IDs

| ID | Bedeutung |
|---:|-----------|
| 1 | Prozesserstellung (Image, Kommandozeile, Elternprozess, Hashes) |
| 3 | Netzwerkverbindung |
| 11 | Datei erstellt |
| 13 | Registry-Wert gesetzt |
| 22 | DNS-Abfrage |

## Schritte

### Teil A — Windows (Sysmon-JSONL)

```bash
cd samples
# 1. Overview: count events by ID
jq -r '.EventID' sysmon.synthetic.jsonl | sort | uniq -c

# 2. Process tree: who started what?
jq -r 'select(.EventID==1) | [.UtcTime, .ParentImage, "->", .Image, .CommandLine] | @tsv' sysmon.synthetic.jsonl

# 3. Decode the encoded PowerShell (UTF-16LE base64)
jq -r 'select((.CommandLine // "") | test("-enc ")) | .CommandLine | split("-enc ")[1]' sysmon.synthetic.jsonl \
  | base64 -d | iconv -f UTF-16LE -t UTF-8; echo

# 4. Network: destinations and regularity (beaconing?)
jq -r 'select(.EventID==3) | [.UtcTime, .Image, .DestinationIp, .DestinationPort] | @tsv' sysmon.synthetic.jsonl

# 5. Persistence
jq -r 'select(.EventID==13) | [.TargetObject, .Details] | @tsv' sysmon.synthetic.jsonl

# 6. Failed logons grouped by source (Security log)
jq -r 'select(.EventID==4625) | .IpAddress' security-4625.synthetic.jsonl | sort | uniq -c | sort -rn
```

Fragen für meine Notizen:

1. Welches Dokument hat die Kette gestartet, und welcher Benutzer hat es geöffnet?
2. Wie sieht die Kette Elternprozess → Kindprozess aus?
3. Welche Domain/IP hat PowerShell kontaktiert, und was wurde abgelegt?
4. Wie bleibt die Malware persistent? Welcher Registry-Wert genau?
5. In welchem Abstand verbindet sich `synchelper.exe`?
6. Welche Discovery-Befehle liefen danach? Warum ist `net group "Domain Admins"` interessant?
7. Was bedeuten bei 4625-Ereignissen `SubStatus` `0xc0000064` und
   `0xc000006a` (unbekannter Benutzer vs. falsches Passwort), und was lässt das vermuten?

### Teil B — Linux (auditd)

```bash
cd samples
# Authentication summary (note the times are displayed in the local timezone)
aureport -if auditd.synthetic.log -au

# Executables summary
aureport -if auditd.synthetic.log -x --summary

# Events by key (key names come from the audit rules)
ausearch -if auditd.synthetic.log -k net_download -i
ausearch -if auditd.synthetic.log -k exec_tmp -i
ausearch -if auditd.synthetic.log -k cron_mod -i

# Failed syscalls (e.g. access denied)
ausearch -if auditd.synthetic.log --success no -i

# Everything done in login session 7, by audit UID (auid survives sudo/su)
ausearch -if auditd.synthetic.log --session 7 -i | grep -E 'proctitle|USER_'
```

Fragen:

1. Von welcher IP gab es erst fehlgeschlagene und dann erfolgreiche Anmeldungen, und für welches Konto?
2. Die Befehlsfolge von Session 7 rekonstruieren (`id`, `curl`, `chmod`, `bash`, `crontab`, `cat`).
3. Warum ist `auid` für die Zuordnung nützlicher als `uid`?
4. Welcher Schritt ist fehlgeschlagen, und warum verdient auch eine *fehlgeschlagene* Aktion einen Alarm?
5. Was würde man als Nächstes auf dem echten Host prüfen? (crontab-Inhalt,
   Hash der Datei in `/tmp`, ausgehende Verbindungen, andere Hosts, die dieselbe IP kontaktiert hat)

### Teil C — Zeitleiste & IOCs

Eine gemeinsame UTC-Zeitleiste (Zeit, Host, Quelle, Ereignis, Bedeutung) und
eine IOC-Liste erstellen — mein [`ioc`-Tool](../../python/) kann sie
extrahieren und entschärfen (defang):

```bash
cat samples/*.jsonl samples/auditd.synthetic.log | python -m seclab.ioc --defang
```

### Meine Ergebnisse in Kürze

Details und alle Ausgaben: [`my-timeline.md`](my-timeline.md).

- **Windows:** `c.martin` öffnet auf `WS-COMPTA-07` die Datei
  `Facture_4471.docm` → Word startet verstecktes, kodiertes PowerShell
  (dekodiert: `Write-Output 'SYNTHETIC LAB EVENT - harmless'`) → Kontakt zu
  `cdn-update.example.net` (198.51.100.77) → `synchelper.exe` in
  `AppData\Roaming` abgelegt und über einen Run-Key persistent gemacht →
  Verbindungen exakt alle **60 s** (Beaconing) → `whoami /all` und
  `net group "Domain Admins" /domain`.
- **4625:** 12 Fehlversuche von `203.0.113.45` in etwa 2,5 Minuten auf 6
  Namen; die SubStatus-Codes verraten, welche Namen existieren. Zwei
  Fehlversuche von `10.20.30.57` sehen nach normalen Tippfehlern aus.
- **Linux:** `203.0.113.45` rät das Passwort von `deploy` (2 Fehlversuche,
  dann Erfolg) → `id` → Download nach `/tmp/.cache-upd.sh` → ausführen →
  `crontab /tmp/.c` → Lesen von `/etc/shadow` mit `EACCES` abgewiesen.
- Dieselbe externe Adresse taucht in beiden Geschichten auf, und
  198.51.100.77 liefert sowohl die Windows-Payload als auch das Linux-Skript.

## Nachweise

- [`my-timeline.md`](my-timeline.md): `jq`-Prozessbaum und dekodierter
  Befehl, Netzwerk-/Registry-Ereignisse, 4625-Analyse, Ausgaben von
  `aureport -au` und `ausearch --session 7`, Antworten auf alle Fragen, die
  gemeinsame UTC-Zeitleiste und die IOC-Liste.
- Nicht erledigt: dieselben Ereignisse in Wazuh ([Lab 01](../01-wazuh-homelab/))
  und echte auditd-Regeln — auf meinem Lab-Rechner schlägt `auditctl -s` mit
  „Operation not permitted“ fehl (keine Audit-Capability in diesem
  Container), daher war `ausearch`/`aureport -if` auf eine Datei die einzige Möglichkeit.

## Was ich gelernt habe

- Beziehungen zwischen Eltern- und Kindprozess (Word → PowerShell) sagen oft
  mehr als jedes einzelne Ereignis.
- Vollkommen regelmäßige Verbindungen (alle 60 s) sind ein starkes Zeichen für Beaconing.
- `auid` behält die ursprüngliche Anmeldeidentität über `sudo`/`su` hinweg —
  genau das braucht man für die Zuordnung.
- Die SubStatus-Codes von 4625 unterscheiden gültige von ungültigen
  Benutzernamen — nützlich, um zu verstehen, was ein Angreifer gelernt hat.
- Zeitzonen sind wichtig: `aureport` zeigt Ortszeit, solange `TZ=UTC` nicht gesetzt ist.
- Ein IOC-Extraktor findet Zeichenketten; zu entscheiden, welche davon
  bösartig sind (und interne Hosts sowie legitime Programme wegzulassen), ist
  Aufgabe des Analysten.
