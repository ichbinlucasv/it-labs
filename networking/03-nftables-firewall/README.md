# Lab 03 — Host firewall with nftables

**Status:** In progress — the ruleset passes `nft -c -f` and loaded in an isolated network namespace; traffic filtering between two VMs has not been tested.

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

- `sudo nft -c -f ruleset.nft` → exit code 0 (nftables v1.1.3).
- Loaded in an isolated network namespace and listed back with `nft list
  ruleset` successfully. Traffic behaviour (steps 5–6) remains to be tested
  on a real two-VM lab.

### Design notes

- `policy drop` on input/forward; output allowed (a stricter egress policy is
  a good next step).
- `ct state invalid drop` before anything else; established/related early for
  performance.
- Logging is rate-limited so an attacker cannot fill the disk with log lines.
- `flush ruleset` wipes rules from other tools (Docker, libvirt) — on such
  hosts, use a dedicated table and `destroy table` / `delete table` instead.

## Evidence

- Output of `nft -c -f ruleset.nft`.
- `nft list ruleset` after applying, with counters incremented after tests.
- `journalctl -k` lines showing `nft-in-ssh-denied:` from a non-admin host.

## What I learned

_To be completed by Lucas._
