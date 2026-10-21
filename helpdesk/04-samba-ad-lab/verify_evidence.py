#!/usr/bin/env python3
"""Re-read the saved Samba AD evidence and confirm the checks that were recorded.

This does not provision a domain. It fails if a future edit drops a result
the lab README treats as done (DNS SRV, OUs, lockout, helpdesk delegation).
"""
from __future__ import annotations

import sys
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parent / "evidence"

CHECKS = {
    "2-verify-ous-groups-users.txt": [
        "_ldap._tcp.corp.example.com has SRV record",
        "_kerberos._udp.corp.example.com has SRV record",
        "dc01.corp.example.com has address 10.20.30.10",
        "administrator@CORP.EXAMPLE.COM",
        "OU=Staff,DC=corp,DC=example,DC=com",
        "OU=Disabled,DC=corp,DC=example,DC=com",
    ],
    "3-password-policy-lockout.txt": [
        "Account lockout threshold (attempts): 5",
        "Minimum password length: 12",
    ],
    "4-helpdesk-tasks-delegation.txt": [
        "GG_Helpdesk",
        "OU=Disabled,DC=corp,DC=example,DC=com",
    ],
}


def main() -> int:
    failures = 0
    for name, needles in CHECKS.items():
        path = EVIDENCE / name
        if not path.is_file():
            print(f"FAIL  missing {name}")
            failures += 1
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        missing = [needle for needle in needles if needle not in text]
        if missing:
            print(f"FAIL  {name}: missing {missing}")
            failures += 1
        else:
            print(f"PASS  {name}: {len(needles)} markers present ({len(text.splitlines())} lines)")
    print("note: a Windows client join to this Samba domain is not in the evidence")
    print(f"result: {'OK' if failures == 0 else f'{failures} failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
