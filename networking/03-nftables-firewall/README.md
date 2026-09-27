# Lab 03 — Host firewall with nftables

**Status:** Done — syntax checked, then traffic-tested with three network namespaces standing in for the server, an admin client and an outside client ([`netns-test.sh`](netns-test.sh), output in [`evidence/`](evidence/)); not yet persisted on a real VM with `nftables.service`.

## Goal

Write a default-deny host firewall for a Linux server with nftables:
stateful filtering, SSH restricted to an admin subnet with rate limiting,
public web ports, essential ICMP/ICMPv6, a blocklist set, and logging.
(Security+ D3 — secure network design; D2 — mitigation/hardening.)

## Setup

- Debian 12 / Ubuntu 24.04 VM with **console access** (in case you lock
  yourself out of SSH), `sudo apt install nftables`.
- Lab LAN `10.20.30.0/24` is the admin subnet. Blocklist uses RFC 5737
  addresses as placeholders.
- Ruleset: [`ruleset.nft`](ruleset.nft).

## Steps

1. **Read** the ruleset and predict what happens to: SSH from `10.20.30.5`,
   SSH from `192.0.2.10`, HTTPS from anywhere, ping, traffic from `198.51.100.66`.
2. **Check syntax without applying** (parses and validates against the kernel,
   but commits nothing):

   ```bash
   sudo nft -c -f ruleset.nft && echo "syntax OK"
   ```

3. **Test safely** — either in a throw-away network namespace:

   ```bash
   sudo ip netns add fwtest
   sudo ip netns exec fwtest nft -f ruleset.nft
   sudo ip netns exec fwtest nft list ruleset
   sudo ip netns del fwtest
   ```

   or on the VM with an automatic rollback in case of lock-out:

   ```bash
   sudo nft list ruleset > /root/nft-backup.nft
   sudo nft -f ruleset.nft
   # if SSH still works, cancel the rollback (Ctrl-C); otherwise it restores:
   sleep 120 && sudo nft -f /root/nft-backup.nft
   ```

4. **Persist**: copy to `/etc/nftables.conf`, `sudo systemctl enable --now nftables`.
5. **Verify** from another lab VM: `nc -zv 10.20.30.10 22` / `curl -I http://10.20.30.10`
   and watch counters/logs:

   ```bash
   sudo nft list chain inet lab_filter input      # counters
   sudo journalctl -k -g 'nft-in-' -f             # log prefixes
   ```

6. **Manage the blocklist at runtime** (no reload needed):

   ```bash
   sudo nft add element inet lab_filter blocklist_v4 '{ 203.0.113.99 }'
   sudo nft list set inet lab_filter blocklist_v4
   ```

### Validation performed

I did not have two VMs, so I used network namespaces: each namespace has its
own interfaces, routes and nftables ruleset, which is enough to test what a
firewall lets through. [`netns-test.sh`](netns-test.sh) builds this, runs
the tests without and with the ruleset, and cleans up:

```text
admin   10.20.30.5      --veth--  fw  10.20.30.10  (server under test, fake services on 22/80/443)
outside 192.0.2.10      --veth--  fw  192.0.2.1 / 198.51.100.1
        198.51.100.66   (in the blocklist)
```

```bash
sudo sysctl -w net.netfilter.nf_log_all_netns=1   # allow log lines from non-host namespaces
sudo ./netns-test.sh
sudo dmesg | grep nft-                              # log prefixes
sudo sysctl -w net.netfilter.nf_log_all_netns=0
```

Results ([full output](evidence/netns-test.txt), nftables v1.1.3):

| Test | Without ruleset | With ruleset | Matches prediction? |
|------|-----------------|--------------|---------------------|
| SSH from admin `10.20.30.5` | open | open | yes |
| SSH from `192.0.2.10` | open | **blocked**, logged `nft-in-ssh-denied` | yes |
| HTTP/HTTPS from `192.0.2.10` | open | open | yes |
| TCP 3306 from `192.0.2.10` | refused (no service) | **blocked** silently, logged `nft-in-drop` | yes |
| Anything from `198.51.100.66` | open | **blocked**, logged `nft-in-blocklist` | yes |
| Ping from `192.0.2.10` | reply | reply (rate-limited accept) | yes |
| 20 SSH connections in a row from admin | — | 8 open, 12 blocked | yes (burst 5 + refill) |
| Add `192.0.2.10` to the blocklist at runtime | — | 443 blocked; open again after removing it | yes |
| Server → `198.51.100.66:443` | — | blocked by the output chain | yes |

Note the difference between **refused** (RST: the port is closed but the
host answers) and **blocked** (no answer at all: the firewall drops). A
scanner sees the first as "closed" and the second as "filtered".

**Problem I found and fixed.** In the first run, the 12 rate-limited SSH
attempts from the *admin* subnet fell through to the generic rule and were
logged as `nft-in-ssh-denied` — the same prefix as an outsider trying SSH.
During an investigation that would look like an attack from inside the admin
network. I added two rules so admin connections over the limit get their own
prefix `nft-in-ssh-ratelimit` (log line rate-limited, drop always applied).
Second run, kernel log summary ([evidence](evidence/kernel-log-summary.txt), MACs redacted):

```text
      8 nft-in-ssh-ratelimit: IN=veth-adm ... SRC=10.20.30.5 DST=10.20.30.10 PROTO=TCP DPT=22
      2 nft-out-blocklist: IN= OUT=veth-out SRC=198.51.100.1 DST=198.51.100.66 PROTO=TCP DPT=443
      2 nft-in-ssh-denied: IN=veth-out ... SRC=192.0.2.10 DST=10.20.30.10 PROTO=TCP DPT=22
      2 nft-in-drop: IN=veth-out ... SRC=192.0.2.10 DST=10.20.30.10 PROTO=TCP DPT=3306
      2 nft-in-blocklist: IN=veth-out ... SRC=198.51.100.66 DST=10.20.30.10 PROTO=TCP DPT=443
```

(Each blocked connection appears twice because the client retransmits its
SYN after 1 s. The drop counter showed 24 packets for the 12 attempts, but
only 8 log lines — the log statement's own rate limit worked.)

Not done here: step 4 (persisting with `nftables.service` on a VM) and a
real SSH daemon behind the rules; the fake services only accept and close.

### Design notes

- `policy drop` on input/forward; output allowed (a stricter egress policy is
  a good next step).
- `ct state invalid drop` before anything else; established/related early for
  performance.
- Logging is rate-limited so an attacker cannot fill the disk with log lines.
- `flush ruleset` wipes rules from other tools (Docker, libvirt) — on such
  hosts, use a dedicated table and `destroy table` / `delete table` instead.

## Evidence

- [`evidence/netns-test.txt`](evidence/netns-test.txt): `nft -c -f` result, test
  matrix without/with the ruleset, rate-limit and runtime-blocklist tests, and
  the rules whose counters increased.
- [`evidence/kernel-log-summary.txt`](evidence/kernel-log-summary.txt): `dmesg`
  lines with the `nft-*` prefixes, counted (MAC addresses redacted).

## What I learned

- Predict first, then test: writing the expected result for each case before
  running the script made the one surprise (the misleading log prefix) obvious.
- Order matters in a chain: a packet that does not match a `limit ... accept`
  rule simply continues to the next rule — here it landed in the "denied" rule.
- "Refused" and "blocked" are different answers and tell an analyst different things.
- Logging needs its own rate limit, otherwise an attacker can fill the disk.
- Network namespaces are a cheap way to test a ruleset without risking
  lock-out on a remote server; `nft -c` only proves syntax, not behaviour.
