# Lab 01 — Subnetting practice

## Goal

Be fast and accurate at IPv4 subnetting: finding network/broadcast addresses,
host ranges, designing a VLSM plan, and summarising routes. Needed for
helpdesk network triage, firewall rules, and SIEM queries on IP ranges
(Security+ D3 — network segmentation).

## Setup

- Pen and paper first, then check with `ipcalc` (`sudo apt install ipcalc`) or
  Python's `ipaddress` module:

```python
import ipaddress
n = ipaddress.ip_interface("192.168.10.77/26").network
print(n, n.netmask, n.broadcast_address, n.num_addresses - 2)
```

## Steps

1. Memorise the "magic numbers" table below.
2. Solve [`exercises.md`](exercises.md) without tools, timing yourself.
3. Check with [`answer-key.md`](answer-key.md) (answers were generated and
   double-checked with Python `ipaddress`).
4. Redo the ones you got wrong a few days later.

| Prefix | Mask | Block size (in the interesting octet) | Usable hosts |
|-------:|------|:-------------------------------------:|-------------:|
| /24 | 255.255.255.0   | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64  | 62  |
| /27 | 255.255.255.224 | 32  | 30  |
| /28 | 255.255.255.240 | 16  | 14  |
| /29 | 255.255.255.248 | 8   | 6   |
| /30 | 255.255.255.252 | 4   | 2   |
| /31 | 255.255.255.254 | 2   | 2 (point-to-point, RFC 3021) |

Method: block size = 256 − mask octet; network = largest multiple of block
size ≤ the address octet; broadcast = next network − 1.

## Evidence

- Photo/scan of hand-written working for exercises 1–8 and my time.
- Score per attempt (e.g. `attempt 1: 14/18 in 22 min`).

## What I learned

_To be completed by Lucas._
