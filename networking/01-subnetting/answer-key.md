# Answer key

**English** · [Français](answer-key.fr.md) · [Deutsch](answer-key.de.md)

Computed and verified with Python's `ipaddress` module.

## Part A

| # | Address | Network | Mask | Broadcast | First host | Last host | Usable hosts |
|---|---------|---------|------|-----------|------------|-----------|--------------|
| 1 | `192.168.10.77/26` | 192.168.10.64/26 | 255.255.255.192 | 192.168.10.127 | 192.168.10.65 | 192.168.10.126 | 62 |
| 2 | `10.4.200.9/20` | 10.4.192.0/20 | 255.255.240.0 | 10.4.207.255 | 10.4.192.1 | 10.4.207.254 | 4094 |
| 3 | `172.16.35.130/27` | 172.16.35.128/27 | 255.255.255.224 | 172.16.35.159 | 172.16.35.129 | 172.16.35.158 | 30 |
| 4 | `198.51.100.200/29` | 198.51.100.200/29 | 255.255.255.248 | 198.51.100.207 | 198.51.100.201 | 198.51.100.206 | 6 |
| 5 | `10.0.0.255/23` | 10.0.0.0/23 | 255.255.254.0 | 10.0.1.255 | 10.0.0.1 | 10.0.1.254 | 510 |
| 6 | `203.0.113.66/30` | 203.0.113.64/30 | 255.255.255.252 | 203.0.113.67 | 203.0.113.65 | 203.0.113.66 | 2 |
| 7 | `172.20.99.1/18` | 172.20.64.0/18 | 255.255.192.0 | 172.20.127.255 | 172.20.64.1 | 172.20.127.254 | 16382 |
| 8 | `192.0.2.143/28` | 192.0.2.128/28 | 255.255.255.240 | 192.0.2.143 | 192.0.2.129 | 192.0.2.142 | 14 |

Notes:
- **Q4:** the given address is itself the network address (200 is a multiple of 8) — not assignable.
- **Q5:** `10.0.0.255` looks like a broadcast but in a /23 it is a normal host address.
- **Q8:** `192.0.2.143` is the **broadcast** address of its /28 — it cannot be assigned to a host.

## Part B

9.  **Yes** — both in `10.1.1.128/25`.
10. **No** — `192.168.5.14` is in `192.168.5.0/28` (hosts .1–.14); `.17` is in `192.168.5.16/28`.
11. **Yes** — both in `172.16.4.0/22` (172.16.4.0 – 172.16.7.255).

## Part C — VLSM plan for 10.50.0.0/22

| Segment | Hosts needed | Prefix | Network | Usable range | Broadcast | Spare hosts |
|---|---:|---|---|---|---|---:|
| Workstations | 300 | /23 | 10.50.0.0/23 | 10.50.0.1 – 10.50.1.254 | 10.50.1.255 | 210 |
| Wi-Fi guests | 120 | /25 | 10.50.2.0/25 | 10.50.2.1 – 10.50.2.126 | 10.50.2.127 | 6 |
| Servers | 50 | /26 | 10.50.2.128/26 | 10.50.2.129 – 10.50.2.190 | 10.50.2.191 | 12 |
| Printers | 20 | /27 | 10.50.2.192/27 | 10.50.2.193 – 10.50.2.222 | 10.50.2.223 | 10 |
| Management | 10 | /28 | 10.50.2.224/28 | 10.50.2.225 – 10.50.2.238 | 10.50.2.239 | 4 |
| WAN link | 2 | /30 | 10.50.2.240/30 | 10.50.2.241 – 10.50.2.242 | 10.50.2.243 | 0 |

First free address: **10.50.2.244** (the whole `10.50.3.0/24` is also still free).
In production I would leave growth room (e.g. give guests a /24).

## Part D

13. `10.8.0.0/22`
14. **256** (2^(24−16)).
15. **/23** — 510 usable hosts, so 10 unused host addresses (512 total − 2 − 500).
16. **APIPA / link-local** (`169.254.0.0/16`): the client got no DHCP answer —
    check cable/Wi-Fi, VLAN, DHCP server/scope exhaustion, DHCP relay.
17. Private: `172.31.255.1`, `192.168.0.1`, `10.255.0.1`.
    Not RFC 1918: `172.32.1.1` (public; 172.16.0.0/12 ends at 172.31.255.255),
    `100.64.0.1` (RFC 6598 shared address space, used for carrier-grade NAT).
18. They are reserved for documentation (RFC 5737) and never routed on the
    Internet, so examples cannot accidentally point at a real organisation.
