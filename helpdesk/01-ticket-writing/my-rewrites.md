# My rewrites, priority exercise and tickets from my own lab work

**English** · [Français](my-rewrites.fr.md) · [Deutsch](my-rewrites.de.md)

Fictional organisation: *Exemple SARL* (40 users, domain `example.com`).
All people, hosts and ticket numbers are invented. Section 3 is based on the
break/fix scenarios I actually ran in
[helpdesk lab 03](../03-linux-troubleshooting/) — the commands and error
messages are copied from that lab's evidence, only the "user" and the
ticket framing are fictional.

---

## 1. Rewrites of the bad tickets

### "internet broken"

What I would have to ask first: who, which device, what exactly fails
(all sites? one app?), since when, what changed, anyone else affected?

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

Compared with the reference version: the reference also records that the
laptop had just been **docked** (new network adapter = different settings).
"What changed?" belongs on the checklist.

### "password / reset done"

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

Compared with the reference version: a reset is often the reflex, but the
reference shows none was needed — only an unlock plus fixing the phone that
kept retrying the old password. Unlocking without finding the source means
the account locks again 10 minutes later.

### "weird email / deleted it"

```text
Title:      [Security] Suspected phishing — link clicked? credentials entered?
Category:   Security   Impact: Single user (possibly more)   Urgency: High   Priority: P2
Description: sender, subject, time received, did the user click / type anything
Indicators (defanged): sender, URL, attachment name/hash
Actions: do NOT delete; report as attachment to security; escalate to SOC
```

Compared with the reference version: the reference adds checking the
user's **sign-in logs** at L1 — a quick check that changes the priority if
there is a suspicious sign-in.

---

## 2. Priority exercise (impact × urgency matrix from the lab README)

| Ticket | Impact | Urgency | Priority | Why |
|--------|--------|---------|----------|-----|
| Ex. 1 — one PC cannot browse, Teams works | Low (single user, workaround exists) | Medium (degraded) | **P4** by the matrix → I would raise to **P3** | The static DNS may come from unwanted software, which is a security question |
| Ex. 2 — account locked | Low (single user) | High (cannot work) | **P3** | Matches the reference |
| Ex. 3 — phishing link clicked | Medium (possibly more users) | High | **P2** | Other mailboxes may have the same mail |
| Escalation — 6 users on floor 2 lose network every 20 min | Medium (team degraded) | High | **P2** | Whole floor affected, Wi-Fi workaround only |
| 3.1 below — intranet web server down | High (whole site) | High | **P1** | Business stopped for everybody |
| 3.2 below — file server share full | Medium (team) | High | **P2** | Accounting cannot save files |
| 3.3 below — one user denied on a share | Low | Medium | **P4** | Access request, not an outage |

Learning point: the matrix is a starting point; a security aspect can justify
raising the priority, and that should be written in the ticket.

---

## 3. Tickets written from my own lab scenarios

### 3.1 Service down after a config change (P1 — resolved)

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

### 3.2 Disk full on a file share (P2 — resolved, with a mistake documented)

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

### 3.3 Access denied to a share (P4 — escalated for approval)

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

### 3.4 Escalation note (L1 → L2) for a problem I could not fix myself

Written from scenario 6 of lab 03, where the memory limit could not be
tested in my environment:

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

### 3.5 Closure note

```text
Closing ticket 3.2.
Root cause: app.log in /srv/data grew without rotation until the 100 MB
filesystem was full.
Fix: writing service stopped and file removed; space back to 0 % used.
Verified: user saved a file successfully at 16:50.
Prevention: logrotate + 80 % disk alert handed to L2 (linked change request).
KB: "Disk full but du shows nothing — deleted files held open (lsof +L1)".
```
