# Lab 03 — Linux troubleshooting runbook

## Goal

A practical runbook for common Linux server/desktop problems on Debian/Ubuntu,
focusing on reading logs and verifying each hypothesis.

## Setup

- Debian 12 or Ubuntu 24.04 LTS VM, 2 GB RAM, snapshot before each scenario.
- A non-root user with `sudo`.
- Scenarios are broken on purpose (see "How to break it" hints) then fixed.

## Steps

### 0. First five commands on any box

```bash
uptime                     # load, how long since reboot
df -h; df -i               # disk space AND inodes
free -h                    # memory / swap
systemctl --failed         # failed units
journalctl -p err -b       # errors since boot
```

### 1. Service won't start

```bash
systemctl status nginx
journalctl -u nginx -n 50 --no-pager
sudo nginx -t              # config syntax test (most daemons have one)
ss -tlnp | grep ':80'      # port already in use?
```

*How to break it:* add a typo to `/etc/nginx/sites-enabled/default`.

### 2. Disk full

```bash
df -h /
sudo du -xh / --max-depth=1 2>/dev/null | sort -h | tail
sudo journalctl --disk-usage
sudo journalctl --vacuum-size=200M
sudo lsof +L1              # deleted files still held open by a process
```

*How to break it:* `fallocate -l 5G /var/tmp/bigfile`.

### 3. DNS / network

```bash
ip -br addr; ip route
ping -c3 10.20.30.1
resolvectl status          # or cat /etc/resolv.conf
dig example.com +short
dig @10.20.30.10 example.com
curl -I https://example.com
```

### 4. Permission denied

```bash
ls -l /srv/share/report.txt
namei -l /srv/share/report.txt     # permissions of every path component
id alice                            # groups
getfacl /srv/share                  # ACLs
```

Fix with the **least privilege** needed (add user to a group, set group
ownership) — never `chmod 777`.

### 5. SSH login problems

```bash
sudo journalctl -u ssh -n 50        # "ssh" on Debian/Ubuntu, "sshd" on RHEL
sudo grep 'Failed password' /var/log/auth.log | tail
sudo sshd -t                        # config syntax
ls -ld ~/.ssh; ls -l ~/.ssh/authorized_keys   # 700 / 600 required
```

My Python [`authlog`](../../python/) tool summarises failed SSH logins.

### 6. High CPU / memory

```bash
top -o %CPU          # or htop
ps aux --sort=-%mem | head
dmesg -T | grep -i 'out of memory'
```

### 7. Package problems

```bash
sudo apt update
sudo apt --fix-broken install
sudo dpkg --configure -a
```

## Evidence

- Terminal output (text files or screenshots) of each scenario broken → fixed.
- `journalctl` excerpt showing the root cause for scenario 1.

## What I learned

_To be completed by Lucas._
