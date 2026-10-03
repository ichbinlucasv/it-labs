# Subnetting exercises

**English** · [Français](exercises.fr.md) · [Deutsch](exercises.de.md)

## Part A — Network facts

For each address, give: network address, subnet mask, broadcast address, first
usable host, last usable host, number of usable hosts.

1. `192.168.10.77/26`
2. `10.4.200.9/20`
3. `172.16.35.130/27`
4. `198.51.100.200/29`
5. `10.0.0.255/23`
6. `203.0.113.66/30`
7. `172.20.99.1/18`
8. `192.0.2.143/28` — can this address be assigned to a host?

## Part B — Same subnet?

Can these two hosts talk directly (same subnet) without a router?

9.  `10.1.1.130/25` and `10.1.1.200/25`
10. `192.168.5.14/28` and `192.168.5.17/28`
11. `172.16.4.1/22` and `172.16.7.254/22`

## Part C — VLSM design

12. Exemple SARL received `10.50.0.0/22`. Allocate subnets, **largest first**,
    contiguous from the start of the block, using the smallest prefix that fits:

| Segment | Hosts needed |
|---------|-------------:|
| Workstations | 300 |
| Wi-Fi guests | 120 |
| Servers | 50 |
| Printers | 20 |
| Management | 10 |
| WAN link (router-to-router) | 2 |

    Then: what is the first free address left in the /22?

## Part D — Summarisation & sizing

13. Summarise `10.8.0.0/24`, `10.8.1.0/24`, `10.8.2.0/24`, `10.8.3.0/24` into
    one route.
14. How many /24 subnets fit in `172.16.0.0/16`?
15. What prefix do you need for exactly 500 hosts? How many addresses are wasted?
16. A user has IP `169.254.12.7`. What does it mean?
17. Which of these are private (RFC 1918)? `172.32.1.1`, `172.31.255.1`,
    `192.168.0.1`, `10.255.0.1`, `100.64.0.1`
18. Why do RFC 5737 ranges (`192.0.2.0/24`, `198.51.100.0/24`,
    `203.0.113.0/24`) appear in documentation?
