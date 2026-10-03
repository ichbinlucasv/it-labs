#!/usr/bin/env python3
"""Repository hygiene checks (standard library only).

- every lab README contains the sections Goal, Setup, Steps, Evidence, What I learned
  (What I learned may be the placeholder "_To be completed by Lucas._" but not empty)
- every lab README has a "**Status:** Done|In progress|Planned" line near the top,
  and it matches the Status column of the skills matrix in the root README
- every lab README appears in the skills matrix (and vice versa)
- flashcards CSV parses, has front/back/domain and domains 1-5
- Sigma rule files are at least valid YAML if PyYAML is installed
- no obvious secrets / private keys committed
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ["## Goal", "## Setup", "## Steps", "## Evidence", "## What I learned"]
# Index pages that only list labs (no lab content of their own)
INDEX_PAGES = {"README.md", "helpdesk/README.md", "networking/README.md", "soc-analyst/README.md",
               "soc-analyst/02-sysmon-auditd-logs/samples/README.md",
               "templates/README.md"}
STATUSES = ("Done", "In progress", "Planned")
STATUS_RE = re.compile(r"^\*\*Status:\*\* (Done|In progress|Planned)\b", re.M)
MATRIX_ROW_RE = re.compile(r"^\| \[[^\]]+\]\(([^)]+)\) \| (Done|In progress|Planned) \|", re.M)
SKIP_PARTS = {".git", "target", ".venv", "venv", "__pycache__", ".pytest_cache", "node_modules"}


def _skipped(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts)


SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
]


def check_readmes() -> list[str]:
    errors = []
    for readme in sorted(ROOT.rglob("README.md")):
        rel = readme.relative_to(ROOT).as_posix()
        if rel in INDEX_PAGES or _skipped(readme):
            continue
        text = readme.read_text(encoding="utf-8")
        missing = [s for s in SECTIONS if s not in text]
        if missing:
            errors.append(f"{rel}: missing sections {missing}")
        elif not text.split("## What I learned", 1)[1].strip():
            errors.append(f"{rel}: 'What I learned' is empty (write it or keep the placeholder)")
    return errors


def lab_readmes() -> list[Path]:
    return [r for r in sorted(ROOT.rglob("README.md"))
            if r.relative_to(ROOT).as_posix() not in INDEX_PAGES and not _skipped(r)]


def readme_status(readme: Path) -> str | None:
    """Status from a '**Status:** X' line within the first 10 lines."""
    head = "\n".join(readme.read_text(encoding="utf-8").splitlines()[:10])
    m = STATUS_RE.search(head)
    return m.group(1) if m else None


def matrix_statuses() -> dict[str, str]:
    """{lab dir relative path: status} parsed from the root README skills matrix."""
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    section = text.split("## Skills matrix", 1)[-1].split("\n## ", 1)[0]
    return {link.rstrip("/"): status for link, status in MATRIX_ROW_RE.findall(section)}


def check_statuses() -> list[str]:
    errors = []
    matrix = matrix_statuses()
    if not matrix:
        return ["README.md: could not find a skills matrix with a Status column"]
    seen = set()
    for readme in lab_readmes():
        rel = readme.relative_to(ROOT).as_posix()
        lab = readme.parent.relative_to(ROOT).as_posix()
        status = readme_status(readme)
        if status is None:
            errors.append(f"{rel}: missing '**Status:** Done|In progress|Planned' line near the top")
            continue
        if lab not in matrix:
            errors.append(f"{rel}: lab not listed in the README skills matrix")
        elif matrix[lab] != status:
            errors.append(f"{rel}: status '{status}' but skills matrix says '{matrix[lab]}'")
        seen.add(lab)
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(r"Current count: (\d+) Done, (\d+) In progress, (\d+) Planned", text)
    counts = [sum(1 for v in matrix.values() if v == st) for st in STATUSES]
    if m and [int(x) for x in m.groups()] != counts:
        errors.append(f"README.md: 'Current count' says {m.groups()} but matrix has {tuple(counts)}")
    for lab in sorted(set(matrix) - seen):
        errors.append(f"README.md skills matrix: '{lab}' has no lab README with a status")
    return errors


def check_flashcards() -> list[str]:
    path = ROOT / "security-plus" / "flashcards.csv"
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    errors = []
    if not rows or list(rows[0].keys()) != ["front", "back", "domain"]:
        errors.append("flashcards.csv: header must be front,back,domain")
    for i, r in enumerate(rows, start=2):
        if not r.get("front") or not r.get("back") or r.get("domain") not in {"1", "2", "3", "4", "5"}:
            errors.append(f"flashcards.csv line {i}: invalid row {r}")
    if not 60 <= len(rows) <= 100:
        errors.append(f"flashcards.csv: expected 60-100 cards, found {len(rows)}")
    return errors


def check_yaml() -> list[str]:
    try:
        import yaml  # type: ignore
    except ImportError:
        return []
    errors = []
    for f in sorted((ROOT / "soc-analyst" / "05-sigma-rules" / "rules").glob("*.yml")):
        try:
            list(yaml.safe_load_all(f.read_text(encoding="utf-8")))
        except yaml.YAMLError as exc:
            errors.append(f"{f.name}: {exc}")
    return errors


def check_secrets() -> list[str]:
    errors = []
    for f in ROOT.rglob("*"):
        if not f.is_file() or _skipped(f) or f.resolve() == Path(__file__).resolve():
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                errors.append(f"{f.relative_to(ROOT)}: matches secret pattern {pat.pattern}")
    return errors


def main() -> int:
    errors = check_readmes() + check_statuses() + check_flashcards() + check_yaml() + check_secrets()
    for e in errors:
        print("FAIL", e)
    counts = {st: 0 for st in STATUSES}
    for r in lab_readmes():
        st = readme_status(r)
        if st:
            counts[st] += 1
    print("lab status: " + ", ".join(f"{n} {st}" for st, n in counts.items()))
    print(f"check_repo: {'OK' if not errors else f'{len(errors)} problem(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
