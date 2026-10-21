#!/usr/bin/env python3
"""Recompute the subnetting exercises and check them against answer-key.md.

Uses only the Python standard library (ipaddress). Classic IPv4 rules apply:
the network and broadcast addresses are not usable hosts, so a link that
needs two hosts is a /30 (not an RFC 3021 /31).
"""
from __future__ import annotations

import ipaddress
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

PART_A = [
    "192.168.10.77/26",
    "10.4.200.9/20",
    "172.16.35.130/27",
    "198.51.100.200/29",
    "10.0.0.255/23",
    "203.0.113.66/30",
    "172.20.99.1/18",
    "192.0.2.143/28",
]

PART_B = [
    ("10.1.1.130/25", "10.1.1.200/25", True),
    ("192.168.5.14/28", "192.168.5.17/28", False),
    ("172.16.4.1/22", "172.16.7.254/22", True),
]

VLSM = [
    ("Workstations", 300),
    ("Wi-Fi guests", 120),
    ("Servers", 50),
    ("Printers", 20),
    ("Management", 10),
    ("WAN link", 2),
]

# Documented expectations for parts the answer key states in prose.
PART_D = {
    13: "10.8.0.0/22",
    14: 256,
    15: (23, 10),  # prefix, wasted host addresses
    17: {
        "172.32.1.1": False,
        "172.31.255.1": True,
        "192.168.0.1": True,
        "10.255.0.1": True,
        "100.64.0.1": False,
    },
}


def host_facts(cidr: str) -> dict[str, object]:
    iface = ipaddress.ip_interface(cidr)
    net = iface.network
    size = net.num_addresses
    usable = size - 2 if net.prefixlen <= 30 else 0
    first = ipaddress.ip_address(int(net.network_address) + 1) if usable else None
    last = ipaddress.ip_address(int(net.broadcast_address) - 1) if usable else None
    assignable = first is not None and int(first) <= int(iface.ip) <= int(last)
    return {
        "network": f"{net.network_address}/{net.prefixlen}",
        "mask": str(net.netmask),
        "broadcast": str(net.broadcast_address),
        "first": str(first),
        "last": str(last),
        "usable": usable,
        "assignable": assignable,
    }


def smallest_prefix(hosts_needed: int) -> int:
    """Smallest classic subnet (largest prefix length, /30 or shorter)."""
    prefix = 30
    while (1 << (32 - prefix)) - 2 < hosts_needed:
        prefix -= 1
        if prefix < 0:
            raise ValueError(hosts_needed)
    return prefix


def vlsm_plan(supernet: str, segments: list[tuple[str, int]]) -> list[dict[str, object]]:
    block = ipaddress.ip_network(supernet)
    cursor = int(block.network_address)
    end = int(block.broadcast_address)
    plan = []
    for name, needed in segments:
        prefix = smallest_prefix(needed)
        size = 1 << (32 - prefix)
        if cursor % size:
            cursor += size - (cursor % size)
        if cursor + size - 1 > end:
            raise RuntimeError(f"{name} does not fit in {supernet}")
        net = ipaddress.ip_network((cursor, prefix))
        usable = size - 2
        plan.append(
            {
                "segment": name,
                "needed": needed,
                "prefix": prefix,
                "network": str(net),
                "first": str(ipaddress.ip_address(cursor + 1)),
                "last": str(ipaddress.ip_address(cursor + size - 2)),
                "broadcast": str(net.broadcast_address),
                "spare": usable - needed,
            }
        )
        cursor += size
    plan.append({"first_free": str(ipaddress.ip_address(cursor))})
    return plan


def parse_part_a(text: str) -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = {}
    in_part = False
    for line in text.splitlines():
        if line.startswith("## Part A"):
            in_part = True
            continue
        if in_part and line.startswith("## "):
            break
        if not in_part or not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if not cells or not cells[0].isdigit():
            continue
        rows[int(cells[0])] = {
            "address": cells[1],
            "network": cells[2],
            "mask": cells[3],
            "broadcast": cells[4],
            "first": cells[5],
            "last": cells[6],
            "usable": cells[7],
        }
    return rows


def main() -> int:
    failures = 0

    def check(label: str, ok: bool, detail: str) -> None:
        nonlocal failures
        print(f"{'PASS' if ok else 'FAIL'}  {label}: {detail}")
        if not ok:
            failures += 1

    print("Part A — network facts")
    key = parse_part_a((HERE / "answer-key.md").read_text(encoding="utf-8"))
    if len(key) != 8:
        check("answer-key table", False, f"parsed {len(key)} rows, expected 8")
    for number, cidr in enumerate(PART_A, start=1):
        got = host_facts(cidr)
        row = key.get(number)
        if row is None:
            check(f"Q{number}", False, "missing from answer key")
            continue
        ok = (
            row["address"] == cidr
            and row["network"] == got["network"]
            and row["mask"] == got["mask"]
            and row["broadcast"] == got["broadcast"]
            and row["first"] == got["first"]
            and row["last"] == got["last"]
            and int(row["usable"]) == got["usable"]
        )
        note = ""
        if number == 8:
            note = "  assignable=" + ("yes" if got["assignable"] else "no (broadcast)")
        elif number == 4 and not got["assignable"]:
            note = "  assignable=no (network address)"
        elif number == 5:
            note = "  .255 is a host inside this /23"
        check(
            f"Q{number} {cidr}",
            ok,
            f"{got['network']} mask {got['mask']} usable {got['usable']}{note}",
        )

    print("\nPart B — same subnet?")
    for number, (left, right, expected) in enumerate(PART_B, start=9):
        same = ipaddress.ip_interface(left).network == ipaddress.ip_interface(right).network
        check(f"Q{number}", same is expected, f"{left} vs {right} -> {'yes' if same else 'no'}")

    print("\nPart C — VLSM for 10.50.0.0/22")
    plan = vlsm_plan("10.50.0.0/22", VLSM)
    expected_plan = {
        "Workstations": "10.50.0.0/23",
        "Wi-Fi guests": "10.50.2.0/25",
        "Servers": "10.50.2.128/26",
        "Printers": "10.50.2.192/27",
        "Management": "10.50.2.224/28",
        "WAN link": "10.50.2.240/30",
    }
    for row in plan:
        if "first_free" in row:
            check("Q12 first free", row["first_free"] == "10.50.2.244", str(row["first_free"]))
            continue
        name = str(row["segment"])
        ok = row["network"] == expected_plan[name]
        check(
            f"Q12 {name}",
            ok,
            f"/{row['prefix']} {row['network']} spare {row['spare']}",
        )

    print("\nPart D — summary, sizing, special ranges")
    summary = list(
        ipaddress.collapse_addresses(
            [
                ipaddress.ip_network("10.8.0.0/24"),
                ipaddress.ip_network("10.8.1.0/24"),
                ipaddress.ip_network("10.8.2.0/24"),
                ipaddress.ip_network("10.8.3.0/24"),
            ]
        )
    )
    check("Q13 summary", [str(n) for n in summary] == [PART_D[13]], str(summary[0]))
    slash24s = 2 ** (24 - 16)
    check("Q14 /24s in a /16", slash24s == PART_D[14], str(slash24s))
    prefix, wasted = PART_D[15]
    usable = (1 << (32 - prefix)) - 2
    check("Q15 500 hosts", prefix == 23 and usable - 500 == wasted, f"/{prefix}, wasted {usable - 500}")
    apipa = ipaddress.ip_address("169.254.12.7") in ipaddress.ip_network("169.254.0.0/16")
    check("Q16 APIPA", apipa, "169.254.12.7 is link-local (no DHCP lease)")
    for addr, is_rfc1918 in PART_D[17].items():
        got = ipaddress.ip_address(addr).is_private
        check(f"Q17 {addr}", got is is_rfc1918, "RFC 1918" if got else "not RFC 1918")
    doc_nets = ["192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24"]
    reserved = all(not ipaddress.ip_network(n).is_global for n in doc_nets)
    check("Q18 documentation ranges", reserved, "RFC 5737 blocks are not globally routable")

    print(f"result: {'OK' if failures == 0 else f'{failures} failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
