#!/usr/bin/env python3
"""Re-read the saved Windows domain notes and confirm the recorded facts.

Does not talk to a domain controller. The lockout threshold is part of the
check on purpose: the lab is still open because that value is 0.
"""
from __future__ import annotations

import sys
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent / "evidence"
NOTES = EVIDENCE / "win11-2026-10-04.txt"

NEEDLES = [
    "Name=WIN11-SOC",
    "Domain=lab.local",
    "PartOfDomain=True",
    "IPv4=192.168.122.20",
    "Name=DC01",
    "LOCKOUT_THRESHOLD=0",
    "Lab-Workstation-Hardening",
    "helpdesk",
]


def main() -> int:
    if not NOTES.is_file():
        print(f"FAIL  missing {NOTES.name}")
        return 1
    text = NOTES.read_text(encoding="utf-8", errors="replace")
    missing = [needle for needle in NEEDLES if needle not in text]
    if missing:
        print(f"FAIL  missing {missing}")
        return 1
    print(f"PASS  {NOTES.name}: domain join, DNS, helpdesk reset, and lockout threshold recorded")
    print("open: lockout threshold is 0, so an unlock has nothing to undo")
    print("open: Lab-Workstation-Hardening is linked and has no settings in this note")
    siblings = sorted(p.name for p in EVIDENCE.iterdir() if p.is_file())
    print(f"evidence files: {len(siblings)}")
    print("result: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
