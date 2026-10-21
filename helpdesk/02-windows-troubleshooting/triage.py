#!/usr/bin/env python3
"""Triage a synthetic Windows Security log the way an L1 ticket would.

The sample is invented (documentation addresses, fictional accounts). This is
not a substitute for Event Viewer on a Windows guest: it is the part of the
runbook that can be repeated on Linux — group the failures, name the lockout,
and separate it from a normal successful logon.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "samples" / "security-events.synthetic.jsonl"

NAMES = {
    4624: "successful logon",
    4625: "failed logon",
    4740: "account locked out",
    4771: "Kerberos pre-authentication failed",
}


def load(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def report(rows: list[dict]) -> str:
    lines = [
        f"events: {len(rows)}",
        f"computers: {', '.join(sorted({r['Computer'] for r in rows}))}",
        "",
        "by event id:",
    ]
    counts = Counter((r["EventId"], NAMES.get(r["EventId"], "other")) for r in rows)
    for (eid, name), n in sorted(counts.items()):
        lines.append(f"  {eid} {name}: {n}")

    fails = [r for r in rows if r["EventId"] == 4625]
    by_user: dict[str, list[dict]] = defaultdict(list)
    for row in fails:
        by_user[row["TargetUserName"]].append(row)
    lines.append("")
    lines.append("failed logons (4625):")
    for user, events in sorted(by_user.items()):
        ips = Counter(e["IpAddress"] for e in events)
        ip_text = ", ".join(f"{ip} x{n}" for ip, n in ips.most_common())
        lines.append(f"  {user}: {len(events)} from {ip_text}")

    lines.append("")
    lines.append("lockouts (4740):")
    lockouts = [r for r in rows if r["EventId"] == 4740]
    for row in lockouts:
        lines.append(
            f"  {row['TimeCreated']} {row['TargetUserName']} "
            f"via {row['IpAddress']} on {row['Computer']}"
        )

    lines.append("")
    lines.append("successful logons (4624):")
    for row in rows:
        if row["EventId"] == 4624:
            lines.append(
                f"  {row['TimeCreated']} {row['TargetUserName']} "
                f"from {row['IpAddress']} type {row['LogonType']}"
            )

    lines.append("")
    lines.append("ticket notes:")
    if any(r["TargetUserName"] == "a.martin" and r["EventId"] == 4740 for r in rows):
        martin = [r for r in fails if r["TargetUserName"] == "a.martin"]
        src = martin[0]["IpAddress"] if martin else "?"
        lines.append(
            f"  a.martin locked after {len(martin)} bad passwords from {src}."
        )
        lines.append("  Verify the person out of band, then unlock. Do not only reset the password.")
        lines.append("  Find what on the source keeps retrying, or the account locks again.")
    if any(r["EventId"] == 4771 for r in rows):
        lines.append("  4771 is a Kerberos failure on the DC. Status 0x18 means the password was wrong.")
    benign = [
        r for r in rows if r["EventId"] == 4624 and r["IpAddress"].startswith("10.20.30.")
    ]
    if benign:
        lines.append(
            "  j.doe's type-3 success from 10.20.30.5 is inside the lab LAN."
        )
        lines.append("  One later failure from the same host is a mistype, not the lockout.")
    return "\n".join(lines)


def self_check(rows: list[dict]) -> None:
    assert sum(1 for r in rows if r["EventId"] == 4625 and r["TargetUserName"] == "a.martin") == 5
    assert any(r["EventId"] == 4740 and r["TargetUserName"] == "a.martin" for r in rows)
    assert any(r["EventId"] == 4624 and r["TargetUserName"] == "j.doe" for r in rows)
    text = report(rows)
    assert "a.martin locked after 5 bad passwords from 203.0.113.45." in text
    assert "4771" in text


def main(argv: list[str]) -> int:
    positional = [arg for arg in argv[1:] if not arg.startswith("-")]
    path = Path(positional[0]) if positional else DEFAULT
    rows = load(path)
    if "--check" in argv:
        self_check(rows)
        print("self-check: OK")
    print(report(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
