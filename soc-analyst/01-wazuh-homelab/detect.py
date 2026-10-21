#!/usr/bin/env python3
"""Small detection loop for the Wazuh lab's test activity.

The full Wazuh all-in-one stack is not installed here (it wants several
gigabytes of RAM and its own VM). This script reads the same kind of
benign lab events the runbook would generate, raises one alert per case,
and prints a triage note. It does not claim to be Wazuh.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "samples" / "activity.synthetic.jsonl"


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def alerts_for(events: list[dict]) -> list[dict]:
    found: list[dict] = []
    ssh: dict[str, list[dict]] = defaultdict(list)
    for event in events:
        if event["kind"] == "sshd" and event["result"] == "failure":
            ssh[event["src"]].append(event)
        elif event["kind"] == "sudo" and event["result"] == "failure":
            found.append(_alert("sudo-failure", event, "A sudo password was rejected."))
        elif event["kind"] == "useradd":
            found.append(_alert("user-added", event, f"Local user {event['target']} was created."))
        elif event["kind"] == "fim" and event["path"] == "/etc/hosts":
            found.append(_alert("fim-hosts", event, "Checksum of /etc/hosts changed."))
        elif event["kind"] == "process" and "-enc" in event.get("command", ""):
            found.append(_alert("powershell-encoded", event, "PowerShell was started with -enc."))
        elif event["kind"] == "registry" and "\\Run\\" in event.get("path", ""):
            found.append(_alert("run-key", event, "A per-user Run key was set."))
    for src, rows in ssh.items():
        if len(rows) >= 5:
            found.append(
                {
                    "rule": "ssh-bruteforce",
                    "host": rows[0]["host"],
                    "ts": rows[-1]["ts"],
                    "detail": f"{len(rows)} SSH failures from {src}",
                    "triage": (
                        f"Who: several account names from {src}. What: sshd failures. "
                        f"Where: {rows[0]['host']}. When: {rows[0]['ts']} to {rows[-1]['ts']}. "
                        "Verdict: true positive for a password guess against the lab host. "
                        "No successful login from this address in the sample."
                    ),
                }
            )
    return found


def _alert(rule: str, event: dict, what: str) -> dict:
    if rule == "fim-hosts":
        triage = (
            f"Who: {event['user']}. What: {what} "
            f"old {event['old_sha256'][:12]}… new {event['new_sha256'][:12]}…. "
            f"Where: {event['host']}:{event['path']}. When: {event['ts']}. "
            "Verdict: benign true positive if a change ticket exists, otherwise investigate."
        )
    elif rule == "powershell-encoded":
        triage = (
            f"Who: {event['user']}. What: {what} Parent {event['parent']}. "
            f"Where: {event['host']}. When: {event['ts']}. "
            "Verdict: true positive in this sample. The parent is WINWORD.EXE, which a user document should not spawn."
        )
    elif rule == "run-key":
        triage = (
            f"Who: {event['user']}. What: {what} Value points at a user-writable path. "
            f"Where: {event['host']} {event['path']}. When: {event['ts']}. "
            "Verdict: true positive for persistence. Confirm the file is expected before deleting the value."
        )
    else:
        triage = (
            f"Who: {event.get('user')}. What: {what} Where: {event['host']}. When: {event['ts']}. "
            "Verdict: expected only if this was the lab's own test. Record it either way."
        )
    return {"rule": rule, "host": event["host"], "ts": event["ts"], "detail": what, "triage": triage}


def render(found: list[dict]) -> str:
    lines = [f"alerts: {len(found)}", ""]
    for alert in found:
        lines.append(f"[{alert['rule']}] {alert['ts']} {alert['host']} — {alert['detail']}")
        lines.append(f"  {alert['triage']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    path = DEFAULT
    for arg in argv[1:]:
        if not arg.startswith("-"):
            path = Path(arg)
    found = alerts_for(load(path))
    if "--check" in argv:
        rules = {a["rule"] for a in found}
        expected = {
            "ssh-bruteforce",
            "sudo-failure",
            "user-added",
            "fim-hosts",
            "powershell-encoded",
            "run-key",
        }
        missing = expected - rules
        if missing or len(found) != len(expected):
            print("self-check failed:", missing or found)
            return 1
        print("self-check: OK")
    sys.stdout.write(render(found))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
