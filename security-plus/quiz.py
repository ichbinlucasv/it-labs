#!/usr/bin/env python3
"""Show what is in flashcards.csv, and optionally print a fixed sample.

Non-interactive on purpose: a portfolio run must finish by itself.
Import the same CSV into Anki for a real review session.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

CSV = Path(__file__).resolve().parent / "flashcards.csv"


def load() -> list[dict[str, str]]:
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or list(rows[0]) != ["front", "back", "domain"]:
        raise SystemExit("flashcards.csv: header must be front,back,domain")
    return rows


def main(argv: list[str]) -> int:
    rows = load()
    counts = Counter(row["domain"] for row in rows)
    print(f"cards: {len(rows)}")
    for domain in ("1", "2", "3", "4", "5"):
        print(f"  domain {domain}: {counts[domain]}")
    bad = [
        i
        for i, row in enumerate(rows, start=2)
        if not row["front"].strip() or not row["back"].strip() or row["domain"] not in {"1", "2", "3", "4", "5"}
    ]
    if bad:
        print("invalid rows:", ", ".join(str(i) for i in bad))
        return 1
    if "--check" in argv:
        if not 60 <= len(rows) <= 100:
            print(f"expected 60-100 cards, found {len(rows)}")
            return 1
        print("self-check: OK")
    if "--sample" in argv:
        print("")
        print("sample (first card of each domain):")
        seen = set()
        for row in rows:
            if row["domain"] in seen:
                continue
            seen.add(row["domain"])
            front = row["front"].replace("\n", " ")
            back = row["back"].replace("\n", " ")
            print(f"  D{row['domain']}: {front}")
            print(f"       {back}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
