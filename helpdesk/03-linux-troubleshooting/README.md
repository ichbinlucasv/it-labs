# Lab 03 — Linux troubleshooting runbook

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**English** · [Deutsch](README.de.md)

**Status:** Done — I broke and fixed scenarios 1–5 and 7 in a Debian 13 systemd container and saved the terminal output in [`evidence/`](evidence/); scenario 6 only partly (the OOM kill could not be reproduced here, see below).

## Goal

A practical runbook for common Linux server/desktop problems on Debian/Ubuntu,
focusing on reading logs and verifying each hypothesis — and proof that I
actually ran it.

## Setup

- Planned: Debian 12 / Ubuntu 24.04 VM with snapshots.
- **What I used:** a Debian 13 (trixie) root filesystem built with
  `debootstrap` and booted with `systemd-nspawn --boot --private-network`, so
  systemd, journald, nginx and sshd run for real, but the container has only a
  loopback interface (nothing reaches my network). See
  [`lab-container.md`](lab-container.md) for the exact commands.
- Host name inside the container: `lab1`. Users `alice` and `bob` and the
  `finance` group are lab accounts. Addresses in the DNS scenario are
  documentation / lab ranges (`192.0.2.53`, `10.20.30.20`).
- Each scenario: break on purpose → observe the symptom as a user would →
  diagnose with the commands below → fix → verify.

## Steps

### 0. First five commands on any box

```bash
uptime                     # load, how long since reboot
df -h; df -i               # disk space AND inodes
free -h                    # memory / swap
systemctl --failed         # failed units
journalctl -p err -b       # errors since boot
```

In a container, `uptime`, `free` and `df /` show the **host's** values
(shared kernel and overlay filesystem) — worth knowing before drawing
conclusions from them. Output: [`evidence/0-first-five-commands.txt`](evidence/0-first-five-commands.txt).

### 1. Service won't start

```bash
systemctl status nginx
journalctl -u nginx -n 50 --no-pager
sudo nginx -t              # config syntax test (most daemons have one)
ss -tlnp | grep ':80'      # port already in use?
```

*How I broke it:* removed the `;` at the end of `listen 80 default_server`
in `/etc/nginx/sites-enabled/default`.

What I saw ([evidence](evidence/1-service-wont-start.txt)):

```text
$ nginx -t
[emerg] 104#104: invalid parameter "listen" in /etc/nginx/sites-enabled/default:23
nginx: configuration file /etc/nginx/nginx.conf test failed
$ sed -n 22,23p /etc/nginx/sites-enabled/default
	listen 80 default_server
	listen [::]:80 default_server;
```

The error points to **line 23**, but the mistake is on **line 22**: without
the semicolon nginx reads both lines as one directive and only complains when
it reaches the second `listen`. Lesson: when a parser reports line N, also
look at line N-1. After restoring the file: `nginx -t` OK, service `active`,
HTTP 200 on `127.0.0.1`.

*Second break — port in use:* I started a Python web server on port 80 as
a transient unit, then started nginx. The journal said
`bind() to 0.0.0.0:80 failed (98: Address already in use)` and
`ss -tlnp` showed `users:(("python3",pid=135,fd=3))` on `:80` — the
process name and PID tell you exactly what to stop.

### 2. Disk full

```bash
df -h /
sudo du -xh / --max-depth=1 2>/dev/null | sort -h | tail
sudo journalctl --disk-usage
sudo journalctl --vacuum-size=200M
sudo lsof +L1              # deleted files still held open by a process
```

*How I broke it:* instead of filling the real disk I mounted a 100 MB tmpfs on
`/srv/data` and ran a service that keeps writing to `/srv/data/app.log`.

What I saw ([evidence](evidence/2-disk-full.txt)): `echo: write error: No
space left on device`, `df` at 100 %, `du` pointing at the 100 MB `app.log`.
Then I made the classic mistake on purpose: `rm app.log`. `df` **stayed at
100 %**, because the process still had the file open:

```text
$ lsof -nP +L1
COMMAND PID USER FD   TYPE DEVICE  SIZE/OFF NLINK NODE NAME
sh      171 root 3w   REG   0,62 104857600     0    2 /srv/data/app.log (deleted)
```

Space came back only after `systemctl stop chatty-app`. Correct fix on a
real server: find the writer, then truncate (`: > app.log`) or rotate the
log with logrotate instead of deleting it under a running process.

### 3. DNS / network

```bash
ip -br addr; ip route
ping -c3 10.20.30.1
resolvectl status          # or cat /etc/resolv.conf
dig example.com +short
dig @10.20.30.10 example.com
curl -I https://example.com
```

*How I broke it:* ran `dnsmasq` on `127.0.0.1` as the "company DNS"
(answers `intranet.lab.example → 10.20.30.20`) and put a wrong static
resolver `nameserver 192.0.2.53` in `/etc/resolv.conf` — the Linux version
of ticket example 1 in [lab 01](../01-ticket-writing/examples.md).

What I saw ([evidence](evidence/3-dns.txt)):

```text
$ getent hosts intranet.lab.example; echo exit=$?
exit=2
$ dig +time=2 +tries=1 intranet.lab.example
;; UDP setup with 192.0.2.53#53(192.0.2.53) for intranet.lab.example failed: network unreachable.
$ dig @127.0.0.1 intranet.lab.example +short
10.20.30.20
```

Asking the right server directly works, asking the configured one fails →
the resolver configuration is the problem, not the name. After
`nameserver 127.0.0.1`, `getent` and `dig` both return `10.20.30.20`.
(In the container there is no route at all, so dig says "network
unreachable"; on a real LAN the same mistake usually shows as a timeout.)
Side note: `dig nosuchhost.intranet.lab.example` returned `NOERROR`, because
dnsmasq's `address=/domain/` also answers for every sub-domain.

### 4. Permission denied

```bash
ls -l /srv/share/report.txt
namei -l /srv/share/report.txt     # permissions of every path component
id alice                            # groups
getfacl /srv/share                  # ACLs
```

*How I broke it:* `/srv/share/finance` is `root:finance 750`, the report is
`640`, and `alice` is not in `finance`.

What I saw ([evidence](evidence/4-permission-denied.txt)): `namei -l` showed
the blocking component at once (`drwxr-x--- root finance finance`), and
`id alice` showed no `finance` group. Two least-privilege fixes, both tested:

- `usermod -aG finance alice` → alice can read, but **still cannot write**
  (file is `640`) — which is what the group should allow.
- For one person only: `setfacl -m u:alice:rx` on the directory and
  `u:alice:r` on the file → read access without touching the group.

Never `chmod 777`. Note: a new group membership only applies to **new**
logins (`su - alice` starts one; a user must log out and in again).

### 5. SSH login problems

```bash
sudo journalctl -u ssh -n 50        # "ssh" on Debian/Ubuntu, "sshd" on RHEL
sudo grep 'Failed password' /var/log/auth.log | tail
sudo sshd -t                        # config syntax
ls -ld ~/.ssh; ls -l ~/.ssh/authorized_keys   # 700 / 600 required
```

*First break attempt:* `chmod 664 ~/.ssh/authorized_keys`. Key login **still
worked**. OpenSSH tolerates group-write when the group is the user's own
private group (`alice:alice`) — so that break did not reproduce the
problem and I noted it rather than hiding it.

*Second break:* `chmod 777 /home/alice`. Now ([evidence](evidence/5-ssh-login.txt)):

```text
alice@127.0.0.1: Permission denied (publickey,password).
$ journalctl -u ssh ... | grep -i modes
Authentication refused: bad ownership or modes for directory /home/alice
```

`sshd -t` was OK (config is fine), `namei -l` on `authorized_keys` showed
`drwxrwxrwx alice alice alice`. After `chmod 755 /home/alice` the login
worked again. The user only sees "Permission denied"; the real reason is
only in the **server** log.

### 6. High CPU / memory

```bash
top -o %CPU          # or htop
ps aux --sort=-%mem | head
dmesg -T | grep -i 'out of memory'
```

*CPU:* a transient unit running `yes > /dev/null` showed at 100 % CPU in
`top` and `ps --sort=-%cpu`; `systemctl status runaway-job` named the unit
that owns it, and stopping the unit fixed it ([evidence](evidence/6-cpu-memory.txt)).

*Memory — not reproduced:* I ran a Python job with
`systemd-run -p MemoryMax=64M` that allocates 500 MB. It **was not killed**;
`/sys/fs/cgroup/cgroup.controllers` is empty in this container, so the
memory controller is not delegated and the limit is silently ignored. The
OOM-kill part (`dmesg`/journal "Out of memory: Killed process") needs a VM.

### 7. Package problems

```bash
sudo apt update
sudo apt --fix-broken install
sudo dpkg --configure -a
```

*How I broke it:* built a tiny `.deb` (`lab-tool`) that depends on a
package that does not exist, and installed it with `dpkg -i`.

What I saw ([evidence](evidence/7-packages.txt)): `dependency problems -
leaving unconfigured`, `dpkg -l` state `iU` (installed, unpacked, not
configured), and afterwards **every** `apt-get install` refused to run
(`Unmet dependencies. Try 'apt --fix-broken install'`). `apt-get
--fix-broken install` removed `lab-tool`; `dpkg --audit` came back clean.
Lesson: one broken package blocks all installs, so fix that first.

## Evidence

- [`evidence/`](evidence/) — terminal output of every scenario, broken → fixed
  (unit invocation IDs removed, nothing else edited).
- Root cause in the journal for scenario 1: `invalid parameter "listen" in
  /etc/nginx/sites-enabled/default:23` and `bind() to 0.0.0.0:80 failed (98:
  Address already in use)`.
- Not captured: OOM kill (see scenario 6).

## What I learned

- Always read the service's own log and config test (`journalctl -u`,
  `nginx -t`, `sshd -t`) before changing anything; the user-facing error
  ("Job failed", "Permission denied") rarely contains the reason.
- A parser's line number can be one line after the real mistake.
- Deleting a big log does not free space while a process holds it open —
  `lsof +L1` finds it.
- `namei -l` answers "which directory blocks me?" in one command.
- Some "breaks" don't break: OpenSSH accepted a group-writable
  `authorized_keys` with a private group. Testing the theory beats repeating it.
- Containers share the host kernel: resource numbers and cgroup limits can
  behave differently than on a VM, so I note where my environment differs.
