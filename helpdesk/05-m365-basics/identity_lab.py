#!/usr/bin/env python3
"""Joiner / mover / leaver checks against a local SQLite model.

This is not a Microsoft 365 tenant and it does not call Microsoft Graph.
It encodes the helpdesk rules from this lab: usage location before a licence,
group-based licensing, block sign-in on leave, and a helpdesk role that is
not Global Administrator. People, addresses, and the tenant name are fictional.
"""
from __future__ import annotations

import sqlite3
import sys

SCHEMA = """
CREATE TABLE users (
    upn TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    department TEXT NOT NULL,
    usage_location TEXT,
    enabled INTEGER NOT NULL,
    mfa_registered INTEGER NOT NULL
);
CREATE TABLE skus (
    sku TEXT PRIMARY KEY,
    seats INTEGER NOT NULL,
    used INTEGER NOT NULL
);
CREATE TABLE groups (
    name TEXT PRIMARY KEY,
    purpose TEXT NOT NULL
);
CREATE TABLE memberships (
    group_name TEXT NOT NULL,
    upn TEXT NOT NULL,
    PRIMARY KEY (group_name, upn)
);
CREATE TABLE licenses (
    upn TEXT NOT NULL,
    sku TEXT NOT NULL,
    PRIMARY KEY (upn, sku)
);
CREATE TABLE sessions (
    upn TEXT PRIMARY KEY,
    revoked INTEGER NOT NULL
);
CREATE TABLE signins (
    id INTEGER PRIMARY KEY,
    ts TEXT NOT NULL,
    upn TEXT NOT NULL,
    ip TEXT NOT NULL,
    location TEXT NOT NULL,
    client_app TEXT NOT NULL,
    result TEXT NOT NULL,
    reason TEXT NOT NULL
);
CREATE TABLE roles (
    upn TEXT NOT NULL,
    role TEXT NOT NULL,
    PRIMARY KEY (upn, role)
);
"""


def connect() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    db.execute("INSERT INTO skus VALUES ('M365_BUSINESS_PREMIUM', 10, 0)")
    db.execute("INSERT INTO groups VALUES ('LIC_M365_BP', 'group-based licensing')")
    db.execute("INSERT INTO groups VALUES ('TEAM_SALES', 'department')")
    db.execute("INSERT INTO groups VALUES ('TEAM_SUPPORT', 'department')")
    db.execute(
        "INSERT INTO roles VALUES ('helpdesk@example.com', 'Helpdesk Administrator')"
    )
    return db


def assign_license(db: sqlite3.Connection, upn: str, sku: str) -> str:
    user = db.execute("SELECT usage_location, enabled FROM users WHERE upn = ?", (upn,)).fetchone()
    if user is None:
        return "no such user"
    if not user["usage_location"]:
        return "blocked: set usage location before licensing"
    if not user["enabled"]:
        return "blocked: account disabled"
    db.execute("INSERT OR IGNORE INTO licenses VALUES (?, ?)", (upn, sku))
    db.execute("UPDATE skus SET used = (SELECT COUNT(*) FROM licenses WHERE sku = ?)", (sku,))
    return "licensed"


def joiner(db: sqlite3.Connection, upn: str, name: str, department: str, location: str) -> None:
    db.execute(
        "INSERT INTO users VALUES (?, ?, ?, NULL, 1, 0)",
        (upn, name, department),
    )
    db.execute("INSERT INTO sessions VALUES (?, 0)", (upn,))


def main() -> int:
    db = connect()
    checks: list[tuple[str, bool, str]] = []

    def record(name: str, ok: bool, detail: str) -> None:
        checks.append((name, ok, detail))
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {detail}")

    joiner(db, "a.martin@example.com", "A. Martin", "Sales", "FR")
    early = assign_license(db, "a.martin@example.com", "M365_BUSINESS_PREMIUM")
    record("licence before usage location", early.startswith("blocked"), early)

    db.execute(
        "UPDATE users SET usage_location = 'FR' WHERE upn = 'a.martin@example.com'"
    )
    db.execute(
        "INSERT INTO memberships VALUES ('LIC_M365_BP', 'a.martin@example.com')"
    )
    db.execute(
        "INSERT INTO memberships VALUES ('TEAM_SALES', 'a.martin@example.com')"
    )
    licensed = assign_license(db, "a.martin@example.com", "M365_BUSINESS_PREMIUM")
    record("joiner licensed via group", licensed == "licensed", licensed)

    # Mover: Sales -> Support. Drop the sales group, keep the licence group.
    db.execute(
        "UPDATE users SET department = 'Support' WHERE upn = 'a.martin@example.com'"
    )
    db.execute(
        "DELETE FROM memberships WHERE upn = 'a.martin@example.com' AND group_name = 'TEAM_SALES'"
    )
    db.execute(
        "INSERT INTO memberships VALUES ('TEAM_SUPPORT', 'a.martin@example.com')"
    )
    groups = [
        row["group_name"]
        for row in db.execute(
            "SELECT group_name FROM memberships WHERE upn = 'a.martin@example.com' ORDER BY 1"
        )
    ]
    record(
        "mover groups",
        groups == ["LIC_M365_BP", "TEAM_SUPPORT"],
        ", ".join(groups),
    )

    # Lost authenticator: require registration again and revoke sessions.
    db.execute("UPDATE users SET mfa_registered = 0 WHERE upn = 'a.martin@example.com'")
    db.execute("UPDATE sessions SET revoked = 1 WHERE upn = 'a.martin@example.com'")
    mfa = db.execute(
        "SELECT mfa_registered FROM users WHERE upn = 'a.martin@example.com'"
    ).fetchone()["mfa_registered"]
    revoked = db.execute(
        "SELECT revoked FROM sessions WHERE upn = 'a.martin@example.com'"
    ).fetchone()["revoked"]
    record("lost authenticator", mfa == 0 and revoked == 1, f"mfa={mfa} sessions_revoked={revoked}")

    db.executemany(
        "INSERT INTO signins (ts, upn, ip, location, client_app, result, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            ("2026-10-21T09:00:00Z", "a.martin@example.com", "203.0.113.10", "FR", "Browser", "success", "MFA"),
            ("2026-10-21T09:40:00Z", "a.martin@example.com", "198.51.100.23", "ZZ", "Legacy auth", "failure", "blocked legacy authentication"),
            ("2026-10-21T09:41:00Z", "a.martin@example.com", "198.51.100.23", "ZZ", "Legacy auth", "failure", "blocked legacy authentication"),
        ],
    )
    suspicious = db.execute(
        """
        SELECT ip, location, client_app, COUNT(*) AS n
        FROM signins
        WHERE result = 'failure'
        GROUP BY ip, location, client_app
        """
    ).fetchone()
    record(
        "suspicious sign-in",
        suspicious["ip"] == "198.51.100.23" and suspicious["n"] == 2,
        f"{suspicious['n']} failures from {suspicious['ip']} ({suspicious['location']}) via {suspicious['client_app']}",
    )

    # Leaver.
    db.execute("UPDATE users SET enabled = 0 WHERE upn = 'a.martin@example.com'")
    db.execute("DELETE FROM licenses WHERE upn = 'a.martin@example.com'")
    db.execute("UPDATE skus SET used = (SELECT COUNT(*) FROM licenses)")
    db.execute("UPDATE sessions SET revoked = 1 WHERE upn = 'a.martin@example.com'")
    enabled = db.execute(
        "SELECT enabled FROM users WHERE upn = 'a.martin@example.com'"
    ).fetchone()["enabled"]
    seats = db.execute("SELECT used FROM skus").fetchone()["used"]
    record("leaver", enabled == 0 and seats == 0, f"enabled={enabled} licences_used={seats}")

    role = db.execute(
        "SELECT role FROM roles WHERE upn = 'helpdesk@example.com'"
    ).fetchone()["role"]
    record(
        "helpdesk role is not Global Administrator",
        role == "Helpdesk Administrator",
        role,
    )

    failed = [name for name, ok, _ in checks if not ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
