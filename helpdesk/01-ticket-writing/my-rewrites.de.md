# Meine Umschreibungen, die Prioritätsübung und Tickets aus meiner eigenen Lab-Arbeit

[English](my-rewrites.md) · [Français](my-rewrites.fr.md) · **Deutsch**

Fiktive Organisation: *Exemple SARL* (40 Benutzer, Domäne `example.com`).
Alle Personen, Hosts und Ticketnummern sind erfunden. Abschnitt 3 stützt sich
auf die Störungen, die ich in
[helpdesk lab 03](../03-linux-troubleshooting/) wirklich durchgespielt habe —
die Befehle und Fehlermeldungen sind aus den Nachweisen dieses Labs kopiert,
nur der „Benutzer“ und der Ticket-Rahmen sind fiktiv.

---

## 1. Umschreibungen der schlechten Tickets

### „internet broken“

Was ich zuerst fragen müsste: wer, welches Gerät, was genau
fehlschlägt (alle Seiten? eine App?), seit wann, was sich geändert hat, ist
noch jemand betroffen?

```text
Title:      [Network] One user cannot open any website since this morning — Teams OK
Requester:  <name>, <team>, <phone/Teams>
Asset:      <hostname>, Windows 11
Category:   Network   Impact: Single user   Urgency: Degraded   Priority: P3 (see matrix)
Description:
  User reports "no internet" in the browser since ~08:40. Teams still works,
  so the link and the network are up -> suspect DNS or proxy.
Troubleshooting done:
  - [time] ipconfig /all -> <IP/GW/DNS values>
  - [time] Resolve-DnsName <internal name> -> <result>
Next action: compare DNS server with the standard; check proxy settings.
```

Verglichen mit der Referenzfassung: die Referenz hält auch fest, dass der
Laptop gerade **angedockt** worden war (neuer Netzwerkadapter = andere
Einstellungen). „Was hat sich geändert?“ gehört auf die Checkliste.

### „password / reset done“

```text
Title:      [Account] <user> locked out — unlocked, cause found
Requester:  <name>, <team>, contact used for callback
Category:   Account/Access   Impact: Single user   Urgency: Cannot work   Priority: P3
Identity verification: <how, per procedure>
Troubleshooting done:
  - [time] account status: locked, badPwdCount=<n>, source=<device>
  - [time] unlocked / reset (with forced change at next logon)
Resolution: root cause <...>; verified with user at <time>; KB <link>
```

Verglichen mit der Referenzfassung: ein Zurücksetzen ist oft der Reflex, aber
die Referenz zeigt, dass keins nötig war — nur ein Entsperren, plus das
Telefon, das das alte Passwort weiter versucht hat. Entsperren, ohne die
Quelle zu finden, und das Konto sperrt sich 10 Minuten später wieder.

### „weird email / deleted it“

```text
Title:      [Security] Suspected phishing — link clicked? credentials entered?
Category:   Security   Impact: Single user (possibly more)   Urgency: High   Priority: P2
Description: sender, subject, time received, did the user click / type anything
Indicators (defanged): sender, URL, attachment name/hash
Actions: do NOT delete; report as attachment to security; escalate to SOC
```

Verglichen mit der Referenzfassung: die Referenz ergänzt auf L1 die Prüfung
der **Anmeldeprotokolle** des Benutzers — eine kurze Prüfung, die die
Priorität ändert, wenn es eine verdächtige Anmeldung gibt.

---

## 2. Prioritätsübung (Matrix Auswirkung × Dringlichkeit aus dem Lab-README)

| Ticket | Auswirkung | Dringlichkeit | Priorität | Warum |
|--------|------------|---------------|-----------|-------|
| Bsp. 1 — ein PC kann nicht surfen, Teams geht | Niedrig (ein Benutzer, Workaround vorhanden) | Mittel (eingeschränkt) | **P4** nach der Matrix → ich würde auf **P3** anheben | Das statische DNS kann von unerwünschter Software kommen, das ist eine Sicherheitsfrage |
| Bsp. 2 — Konto gesperrt | Niedrig (ein Benutzer) | Hoch (kann nicht arbeiten) | **P3** | Entspricht der Referenz |
| Bsp. 3 — Phishing-Link angeklickt | Mittel (möglicherweise mehr Benutzer) | Hoch | **P2** | Andere Postfächer haben dieselbe Mail vielleicht auch |
| Eskalation — 6 Benutzer in Etage 2 verlieren alle 20 min das Netz | Mittel (Team eingeschränkt) | Hoch | **P2** | Die ganze Etage ist betroffen, nur Wi-Fi als Workaround |
| 3.1 unten — Intranet-Webserver down | Hoch (ganze Site) | Hoch | **P1** | Der Betrieb steht für alle |
| 3.2 unten — Dateiserver-Freigabe voll | Mittel (Team) | Hoch | **P2** | Die Buchhaltung kann keine Dateien speichern |
| 3.3 unten — einem Benutzer die Freigabe verweigert | Niedrig | Mittel | **P4** | Zugriffsanfrage, kein Ausfall |

Merksatz: die Matrix ist ein Ausgangspunkt; ein Sicherheitsaspekt kann eine
höhere Priorität begründen, und das gehört ins Ticket.

---

## 3. Tickets aus meinen eigenen Lab-Szenarien

### 3.1 Dienst down nach einer Konfigurationsänderung (P1 — gelöst)

```text
Title:      [Server] Intranet web server returns nothing — nginx fails to start after config edit
Requester:  Monitoring alert + 3 user calls (Accounting, Sales)
Asset:      lab1 (Debian 13, nginx)
Category:   Software   Impact: Whole site   Urgency: Cannot work   Priority: P1

Description:
  Intranet unreachable since 16:43. A config change was deployed a few minutes before.

Troubleshooting done:
  - 16:43 systemctl status nginx -> failed (Result: exit-code), ExecStartPre nginx -t failed
  - 16:43 journalctl -u nginx -> [emerg] invalid parameter "listen" in
          /etc/nginx/sites-enabled/default:23
  - 16:43 nginx -t -> same error; line 22 "listen 80 default_server" is missing its ";"
          (nginx reports the NEXT line)

Resolution:
  Restored previous version of sites-enabled/default, nginx -t OK,
  systemctl restart nginx -> active, HTTP 200 confirmed. Users confirmed at 16:50.
  Root cause: syntax error in change. Follow-up: run "nginx -t" before every
  reload (add to change checklist).
```

### 3.2 Platte voll auf einer Dateifreigabe (P2 — gelöst, mit einem dokumentierten Fehler)

```text
Title:      [Server] /srv/data full — users get "No space left on device"
Asset:      lab1, filesystem /srv/data (100 MB)
Category:   Hardware/Storage   Impact: Team   Urgency: Cannot work   Priority: P2

Troubleshooting done:
  - df -h /srv/data -> 100 %
  - du -xh /srv/data --max-depth=1 -> app.log = 100 MB
  - rm app.log -> df still 100 % (file deleted but still open)
  - lsof -nP +L1 -> sh (PID 171) holds /srv/data/app.log (deleted)
  - systemctl stop chatty-app -> df 0 %

Resolution:
  Space recovered after stopping the writing service. Root cause: application
  log without rotation. Next action / owner: L2 to add logrotate
  (copytruncate) and a disk-usage alert at 80 %.
Note for the team: deleting a log under a running process does not free space;
truncate it (": > file") or stop the writer first.
```

### 3.3 Zugriff auf eine Freigabe verweigert (P4 — zur Freigabe eskaliert)

```text
Title:      [Access] alice cannot read /srv/share/finance/report.txt
Requester:  alice (Sales)
Category:   Account/Access   Impact: Single user   Urgency: Degraded   Priority: P4

Troubleshooting done:
  - namei -l -> blocked at "drwxr-x--- root finance finance"
  - id alice -> not in group "finance"

Next action / owner:
  Access to Finance data needs approval from the data owner (Finance manager).
  Request sent. Options once approved: add alice to "finance" (read only,
  file is 640) or a per-user read ACL. No chmod 777.
```

### 3.4 Eskalationsnotiz (L1 → L2) für ein Problem, das ich selbst nicht beheben konnte

Geschrieben aus Szenario 6 von Lab 03, wo ich das Speicherlimit in meiner
Umgebung nicht testen konnte:

```text
Escalating to L2 Linux.
Summary: A batch job on lab1 was supposed to be limited to 64 MB
         (systemd-run -p MemoryMax=64M) but allocated 500 MB without being stopped.
Done:    Reproduced twice; journal shows the job finished normally (no OOM kill).
         /sys/fs/cgroup/cgroup.controllers is empty -> the memory controller
         is not available to systemd on this host.
Hypothesis: cgroup v2 memory controller not delegated (container / kernel setup),
         so MemoryMax is silently ignored.
Impact:  No outage now; risk that a runaway job exhausts host memory.
Ask:     Confirm cgroup delegation on the host, or move the job to a VM.
```

### 3.5 Abschlussnotiz

```text
Closing ticket 3.2.
Root cause: app.log in /srv/data grew without rotation until the 100 MB
filesystem was full.
Fix: writing service stopped and file removed; space back to 0 % used.
Verified: user saved a file successfully at 16:50.
Prevention: logrotate + 80 % disk alert handed to L2 (linked change request).
KB: "Disk full but du shows nothing — deleted files held open (lsof +L1)".
```
