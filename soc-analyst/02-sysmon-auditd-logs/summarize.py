#!/usr/bin/env python3
"""Count the synthetic Sysmon and auditd samples. No external tools."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLES = HERE / "samples"


def main() -> int:
    sysmon = [
        json.loads(line)
        for line in (SAMPLES / "sysmon.synthetic.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    security = [
        json.loads(line)
        for line in (SAMPLES / "security-4625.synthetic.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    audit = (SAMPLES / "auditd.synthetic.log").read_text(encoding="utf-8").splitlines()
    print(f"sysmon events: {len(sysmon)}")
    for eid, n in sorted(Counter(row["EventID"] for row in sysmon).items()):
        print(f"  EventID {eid}: {n}")
    parents = [
        (row.get("ParentImage", "").rsplit("\\", 1)[-1], row.get("Image", "").rsplit("\\", 1)[-1])
        for row in sysmon
        if row.get("EventID") == 1
    ]
    print("process creation:")
    for parent, image in parents:
        print(f"  {parent} -> {image}")
    print(f"security events: {len(security)}")
    print(f"  4625 failures: {sum(1 for row in security if row.get('EventID') == 4625)}")
    print(f"auditd lines: {len([line for line in audit if line.strip()])}")
    print("samples are synthetic; hashes in the JSONL are placeholders")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
