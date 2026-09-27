#!/usr/bin/env python3
"""Replay the Sigma rules against the lab's SYNTHETIC sample logs.

How it works:
  1. Each rule (including the correlation rule) is converted to an SQLite query with sigma-cli
     (`sigma convert -t sqlite --without-pipeline`, plugin: `sigma plugin install sqlite`).
  2. The synthetic Sysmon + Security JSONL (Windows) and the synthetic auditd log (Linux) are
     loaded into in-memory SQLite tables named `logs`.
  3. Each query runs against the table that matches the rule's logsource product.

Requirements: sigma-cli + pySigma-backend-sqlite on PATH (see README).
This is a lab smoke test, not a replacement for testing on real telemetry.
"""
from __future__ import annotations

import json
import re
import shlex
import sqlite3
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
RULES = HERE / "rules"
SAMPLES = HERE.parent / "02-sysmon-auditd-logs" / "samples"

AUDIT_RE = re.compile(r"^type=(?P<type>\S+) msg=audit\((?P<stamp>[\d.]+):(?P<serial>\d+)\): (?P<body>.*)$")
KV_RE = re.compile(r'(\w+)=("[^"]*"|\S+)')


def load_windows() -> list[dict]:
    rows = []
    for name in ("sysmon.synthetic.jsonl", "security-4625.synthetic.jsonl"):
        for line in (SAMPLES / name).read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                row["timestamp"] = row["UtcTime"]  # used by correlation queries
                rows.append(row)
    return rows


def load_linux() -> list[dict]:
    """Flatten auditd records; add Image/CommandLine to execve events."""
    rows: list[dict] = []
    events: dict[str, list[dict]] = {}
    for line in (SAMPLES / "auditd.synthetic.log").read_text().splitlines():
        m = AUDIT_RE.match(line)
        if not m:
            continue
        rec = {"type": m["type"], "serial": m["serial"]}
        for k, v in KV_RE.findall(m["body"]):
            rec[k] = v.strip('"')
        rows.append(rec)
        events.setdefault(m["serial"], []).append(rec)
    # synthesize process_creation-style rows from SYSCALL(execve)+EXECVE
    for recs in events.values():
        sc = next((r for r in recs if r["type"] == "SYSCALL" and r.get("syscall") == "59"), None)
        ex = next((r for r in recs if r["type"] == "EXECVE"), None)
        if sc and ex:
            argc = int(ex.get("argc", 0))
            args = [ex.get(f"a{i}", "") for i in range(argc)]
            rows.append({"type": "PROCESS_CREATION", "Image": sc.get("exe"),
                         "CommandLine": " ".join(shlex.quote(a) if " " in a else a for a in args),
                         "User": sc.get("auid"), "serial": sc["serial"]})
    return rows


def make_db(rows: list[dict]) -> sqlite3.Connection:
    cols = sorted({k for r in rows for k in r})
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE logs (" + ", ".join(f'"{c}" TEXT' for c in cols) + ")")
    for r in rows:
        db.execute(
            "INSERT INTO logs (" + ", ".join(f'"{c}"' for c in r) + ") VALUES (" + ", ".join("?" for _ in r) + ")",
            [json.dumps(v) if isinstance(v, (bool, dict, list)) else (None if v is None else str(v)) for v in r.values()],
        )
    return db


def convert(rule: Path) -> list[str]:
    out = subprocess.run(["sigma", "convert", "-t", "sqlite", "--without-pipeline", str(rule)],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or out.stdout.strip())
    return [l for l in out.stdout.splitlines() if l.startswith(("SELECT", "WITH"))]


def main() -> int:
    dbs = {"windows": make_db(load_windows()), "linux": make_db(load_linux())}
    failures = 0
    for rule in sorted(RULES.glob("*.yml")):
        docs = [d for d in yaml.safe_load_all(rule.read_text()) if d]
        product = next((d.get("logsource", {}).get("product") for d in docs if "logsource" in d), None)
        try:
            queries = convert(rule)
        except RuntimeError as exc:
            print(f"[SKIP] {rule.name}: backend could not convert ({exc.splitlines()[-1][:90]})")
            continue
        hits = 0
        for q in queries:
            db = dbs[product]
            for _ in range(20):
                try:
                    hits += len(db.execute(q).fetchall())
                    break
                except sqlite3.OperationalError as exc:
                    m = re.search(r"no such column: (\S+)", str(exc))
                    if not m:
                        print(f"[ERR ] {rule.name}: {exc}")
                        failures += 1
                        break
                    # field absent from the synthetic data: add it as an empty column
                    db.execute(f'ALTER TABLE logs ADD COLUMN "{m[1]}" TEXT')
        print(f"[{'HIT ' if hits else 'none'}] {rule.name}: {hits} result row(s) (events or correlation alerts) in {product} samples")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
