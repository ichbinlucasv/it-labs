# bash

**English** · [Français](bash.fr.md) · [Deutsch](bash.de.md)

What I use it for: the Linux host, every day. Packages, services, disks,
"why is SSH failing", a quick look at a log.

## 25 minutes

1. 10 min. Type the block below from memory. Check with `man` only after.
2. 10 min. Break one thing in the lab container from
   [helpdesk/03](../../helpdesk/03-linux-troubleshooting/) and write the
   command that showed it.
3. 5 min. One line in the daily sheet: the flag I forgot.

## Type these until they stick

```bash
systemctl status ssh --no-pager
journalctl -u ssh -S today --no-pager
ss -lntup
df -hT
ip -br addr
ip route
getent hosts example.com
id
find /var/log -type f -mtime -1 -printf '%TY-%Tm-%Td %p\n'
```

A log line, not the whole file:

```bash
journalctl -u ssh --since "1 hour ago" --no-pager | tail -n 40
grep -E 'Failed|Accepted' /var/log/auth.log | tail
```

Debian and Fedora do not use the same log path. If the file is missing,
I say so. I do not invent lines.

## Exercise

On paper, write what `ss -lntup` is telling me about one listening port:
program, user, address, port. Then run it and mark what I misread.

## I still mix up

- `ss` and `netstat`
- `--since` on journalctl versus `tail -f` when I need history
- running a fix as root before I have read the error
