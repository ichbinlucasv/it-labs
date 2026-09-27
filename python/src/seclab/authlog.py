"""Summarise SSH authentication events from a Linux auth.log / secure log.

Handles both classic syslog timestamps (``Sep 14 21:40:00``) and the RFC 3339
timestamps used by default on recent Debian/Ubuntu (``2026-09-14T21:40:00.123+00:00``).

Example::

    python -m seclab.authlog /var/log/auth.log --threshold 5
    journalctl -u ssh --no-pager -o short-iso | python -m seclab.authlog -
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable, TextIO

# Timestamp + host + sshd[pid]:  (host/pid parts are optional-tolerant)
_PREFIX = r"^(?P<ts>\S+(?:\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})?)\s+(?P<host>\S+)\s+sshd(?:-session)?\[\d+\]:\s+"

FAILED_RE = re.compile(
    _PREFIX + r"(?:message repeated (?P<rep>\d+) times: \[ ?)?Failed (?P<method>password|publickey|keyboard-interactive/pam) for "
    r"(?P<invalid>invalid user )?(?P<user>\S*) from (?P<ip>\S+) port \d+"
)
INVALID_RE = re.compile(_PREFIX + r"Invalid user (?P<user>\S*) from (?P<ip>\S+)(?: port \d+)?")
ACCEPTED_RE = re.compile(
    _PREFIX + r"Accepted (?P<method>password|publickey|keyboard-interactive/pam) for "
    r"(?P<user>\S+) from (?P<ip>\S+) port \d+"
)


@dataclass
class AuthSummary:
    """Aggregated view of SSH authentication activity."""

    failed_total: int = 0
    failed_by_ip: Counter = field(default_factory=Counter)
    failed_by_user: Counter = field(default_factory=Counter)
    invalid_users: Counter = field(default_factory=Counter)
    accepted: list[dict] = field(default_factory=list)
    first_seen: str | None = None
    last_seen: str | None = None

    def _touch(self, ts: str) -> None:
        if self.first_seen is None:
            self.first_seen = ts
        self.last_seen = ts

    def suspicious_ips(self, threshold: int) -> list[tuple[str, int]]:
        """IPs with at least ``threshold`` failures, most active first."""
        return [(ip, n) for ip, n in self.failed_by_ip.most_common() if n >= threshold]

    def success_after_failures(self) -> list[dict]:
        """Accepted logins from an IP that previously failed - worth a closer look."""
        return [a for a in self.accepted if self.failed_by_ip.get(a["ip"], 0) > 0]

    def to_dict(self, threshold: int = 5, top: int = 10) -> dict:
        return {
            "failed_total": self.failed_total,
            "unique_source_ips": len(self.failed_by_ip),
            "first_seen": self.first_seen,
            "last_seen": self.last_seen,
            "top_ips": self.failed_by_ip.most_common(top),
            "top_users": self.failed_by_user.most_common(top),
            "invalid_users": self.invalid_users.most_common(top),
            "accepted": self.accepted,
            "suspicious_ips": self.suspicious_ips(threshold),
            "success_after_failures": self.success_after_failures(),
        }


def _valid_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def parse_lines(lines: Iterable[str]) -> AuthSummary:
    """Parse auth log lines and return an :class:`AuthSummary`."""
    s = AuthSummary()
    for raw in lines:
        line = raw.rstrip("\n")
        if m := FAILED_RE.search(line):
            if not _valid_ip(m["ip"]):
                continue
            n = int(m["rep"] or 1)  # rsyslog "message repeated N times"
            s._touch(m["ts"])
            s.failed_total += n
            s.failed_by_ip[m["ip"]] += n
            s.failed_by_user[m["user"]] += n
            if m["invalid"]:
                s.invalid_users[m["user"]] += n
        elif m := ACCEPTED_RE.search(line):
            if not _valid_ip(m["ip"]):
                continue
            s._touch(m["ts"])
            s.accepted.append({"ts": m["ts"], "user": m["user"], "ip": m["ip"], "method": m["method"]})
        elif m := INVALID_RE.search(line):
            # "Invalid user" lines precede the "Failed password for invalid user"
            # line; we count the failure there, so only record the timestamp here.
            if _valid_ip(m["ip"]):
                s._touch(m["ts"])
    return s


def format_report(s: AuthSummary, threshold: int = 5, top: int = 10) -> str:
    out = [
        "SSH authentication summary",
        "==========================",
        f"Time range          : {s.first_seen or '-'}  ->  {s.last_seen or '-'}",
        f"Failed attempts     : {s.failed_total}",
        f"Unique source IPs   : {len(s.failed_by_ip)}",
        f"Accepted logins     : {len(s.accepted)}",
        "",
        f"Top {top} source IPs (failures):",
    ]
    out += [f"  {n:>6}  {ip}" for ip, n in s.failed_by_ip.most_common(top)] or ["  (none)"]
    out += ["", f"Top {top} targeted users:"]
    out += [f"  {n:>6}  {u}" for u, n in s.failed_by_user.most_common(top)] or ["  (none)"]
    if s.invalid_users:
        out += ["", "Non-existent users tried:"]
        out += [f"  {n:>6}  {u}" for u, n in s.invalid_users.most_common(top)]
    out += ["", f"IPs at or above threshold ({threshold}):"]
    out += [f"  {ip} ({n})" for ip, n in s.suspicious_ips(threshold)] or ["  (none)"]
    saf = s.success_after_failures()
    out += ["", "!! Successful login from an IP that also failed:" if saf else "Successful logins after failures: none"]
    out += [f"  {a['ts']}  {a['user']}@{a['ip']} via {a['method']}" for a in saf]
    return "\n".join(out)


def _open(path: str) -> TextIO:
    return sys.stdin if path == "-" else open(path, encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Summarise failed/accepted SSH logins from auth.log")
    p.add_argument("logfile", nargs="?", default="-", help="auth.log path, or - for stdin (default)")
    p.add_argument("--threshold", type=int, default=5, help="failures per IP to flag (default 5)")
    p.add_argument("--top", type=int, default=10, help="entries to show per list (default 10)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args(argv)

    with _open(args.logfile) as fh:
        summary = parse_lines(fh)
    if args.json:
        print(json.dumps(summary.to_dict(args.threshold, args.top), indent=2))
    else:
        print(format_report(summary, args.threshold, args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
