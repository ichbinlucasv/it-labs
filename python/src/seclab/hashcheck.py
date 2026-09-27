"""Compute file hashes and compare them against a known-bad hash list.

Known-bad list format (one entry per line, ``#`` comments allowed)::

    <hash>[,<label>]        or        <hash>  <label>

MD5, SHA1 and SHA256 are recognised by length. Exit code is 1 when at least
one file matches, so the tool can be used in scripts.

Example::

    python -m seclab.hashcheck --known-bad samples/known_bad.example.txt ~/Downloads -r
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

ALGORITHMS = ("md5", "sha1", "sha256")
_LEN_TO_ALGO = {32: "md5", 40: "sha1", 64: "sha256"}
_HEX = re.compile(r"^[0-9a-fA-F]+$")
CHUNK = 1024 * 1024


def hash_file(path: str | Path, algorithms: Iterable[str] = ALGORITHMS) -> dict[str, str]:
    """Hash a file in chunks (constant memory) with several algorithms at once."""
    hashers = {a: hashlib.new(a) for a in algorithms}
    with open(path, "rb") as fh:
        while chunk := fh.read(CHUNK):
            for h in hashers.values():
                h.update(chunk)
    return {a: h.hexdigest() for a, h in hashers.items()}


def parse_known_bad(lines: Iterable[str]) -> dict[str, str]:
    """Return ``{hash_lowercase: label}``. Invalid lines are skipped."""
    known: dict[str, str] = {}
    for raw in lines:
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = re.split(r"[,\s]+", line, maxsplit=1)
        digest = parts[0].strip().lower()
        label = parts[1].strip() if len(parts) > 1 else ""
        if _HEX.match(digest) and len(digest) in _LEN_TO_ALGO:
            known[digest] = label or "(no label)"
    return known


def load_known_bad(path: str | Path) -> dict[str, str]:
    with open(path, encoding="utf-8") as fh:
        return parse_known_bad(fh)


def iter_files(paths: Iterable[str | Path], recursive: bool = False) -> Iterator[Path]:
    for p in map(Path, paths):
        if p.is_file():
            yield p
        elif p.is_dir():
            pattern = p.rglob("*") if recursive else p.glob("*")
            yield from sorted(f for f in pattern if f.is_file())


@dataclass
class Result:
    path: str
    hashes: dict[str, str]
    match: str | None = None      # algorithm that matched
    label: str | None = None

    @property
    def is_bad(self) -> bool:
        return self.match is not None


def check_file(path: str | Path, known_bad: dict[str, str]) -> Result:
    hashes = hash_file(path)
    for algo, digest in hashes.items():
        if digest in known_bad:
            return Result(str(path), hashes, algo, known_bad[digest])
    return Result(str(path), hashes)


def scan(paths: Iterable[str | Path], known_bad: dict[str, str], recursive: bool = False) -> list[Result]:
    results = []
    for f in iter_files(paths, recursive):
        try:
            results.append(check_file(f, known_bad))
        except OSError as exc:  # unreadable file: report, keep going
            print(f"warning: cannot read {f}: {exc}", file=sys.stderr)
    return results


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Hash files and compare against a known-bad list")
    p.add_argument("paths", nargs="+", help="files or directories to check")
    p.add_argument("-k", "--known-bad", help="known-bad hash list (omit to just print hashes)")
    p.add_argument("-r", "--recursive", action="store_true", help="recurse into directories")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args(argv)

    known = load_known_bad(args.known_bad) if args.known_bad else {}
    results = scan(args.paths, known, args.recursive)

    if args.json:
        print(json.dumps([{**r.__dict__, "is_bad": r.is_bad} for r in results], indent=2))
    else:
        for r in results:
            status = f"MATCH ({r.match}: {r.label})" if r.is_bad else ("clean" if known else "")
            print(f"{r.hashes['sha256']}  {r.path}  {status}".rstrip())
        if known:
            bad = sum(r.is_bad for r in results)
            print(f"\n{len(results)} file(s) checked, {bad} match(es) against {len(known)} known-bad hash(es).")
    return 1 if any(r.is_bad for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
