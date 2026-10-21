# Lab 01 — Subnetting practice

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**Status:** Done — exercises and answer key written; every answer was computed and checked with Python `ipaddress`.

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

Check the answer key from the repository root:

```bash
python3 networking/01-subnetting/check_answers.py
```

The script recomputes every question with `ipaddress` and compares Part A
with the table in [`answer-key.md`](answer-key.md).

## What I learned

- A `/23` makes `10.0.0.255` a normal host. The dotted decimal is not a broadcast by itself.
- `192.0.2.143/28` is the broadcast, and `198.51.100.200/29` is the network address. Neither can be assigned.
- VLSM largest-first, packed from the start of the block, leaves the first free address at `10.50.2.244`.
- Two hosts need a `/30` under the classic "subtract network and broadcast" rule. RFC 3021 `/31` is a different design.
- `100.64.0.1` is shared address space (RFC 6598), not RFC 1918. `172.32.1.1` is outside `172.16.0.0/12`.
