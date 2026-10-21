#!/usr/bin/env python3
"""Check that the worked tickets in my-rewrites.md carry the fields L1 needs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

TEXT = (Path(__file__).resolve().parent / "my-rewrites.md").read_text(encoding="utf-8")
BLOCKS = re.findall(r"```text\n(.*?)```", TEXT, flags=re.S)

# Position in the file, then the fields that block must contain.
EXPECTATIONS = [
    ("internet", ("Title:", "Priority:", "Troubleshooting done:")),
    ("lockout", ("Title:", "Priority:", "Identity verification:", "Resolution:")),
    ("phishing", ("Title:", "Priority:", "defanged")),
    ("nginx", ("Title:", "Priority: P1", "nginx -t", "Resolution:")),
    ("disk", ("Title:", "Priority: P2", "lsof", "deleted")),
    ("share", ("Title:", "Priority: P4", "finance", "chmod 777")),
    ("escalation", ("Escalating to L2", "MemoryMax", "cgroup")),
    ("closure", ("Closing ticket", "Root cause:", "Verified:")),
]


def main() -> int:
    print(f"fenced ticket blocks: {len(BLOCKS)}")
    if len(BLOCKS) < len(EXPECTATIONS):
        print(f"FAIL  expected at least {len(EXPECTATIONS)} blocks")
        return 1
    failures = 0
    for block, (name, needles) in zip(BLOCKS, EXPECTATIONS):
        missing = [needle for needle in needles if needle not in block]
        if missing:
            failures += 1
            print(f"FAIL  {name}: missing {missing}")
        else:
            title = next((line.strip() for line in block.splitlines() if line.strip().lower().startswith("title")), name)
            print(f"PASS  {name}: {title}")
    priorities = ("P1", "P2", "P3", "P4")
    have = [p for p in priorities if p in TEXT]
    if have != list(priorities):
        failures += 1
        print(f"FAIL  priority matrix missing {[p for p in priorities if p not in have]}")
    else:
        print("PASS  priority exercise mentions P1 P2 P3 P4")
    print(f"result: {'OK' if failures == 0 else f'{failures} failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
