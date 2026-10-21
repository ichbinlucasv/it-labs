#!/usr/bin/env python3
"""Answer the IR-02 investigation questions with SQL.

The rows are a small synthetic stand-in for a multi-source SOC dataset.
They are not the Splunk BOTS v1 archive (that download is several gigabytes
and needs Splunk). Addresses are documentation ranges. No exploit payload
is stored — only log fields an analyst would query.
"""
from __future__ import annotations

import sqlite3
import sys

SCHEMA = """
CREATE TABLE http (
    ts TEXT, src_ip TEXT, dest_ip TEXT, method TEXT, uri TEXT,
    user_agent TEXT, filename TEXT
);
CREATE TABLE ids (
    ts TEXT, src_ip TEXT, dest_ip TEXT, signature TEXT
);
CREATE TABLE dns (
    ts TEXT, src_ip TEXT, query TEXT
);
CREATE TABLE process (
    ts TEXT, host TEXT, parent_image TEXT, image TEXT, command_line TEXT
);
CREATE TABLE traffic (
    ts TEXT, src_ip TEXT, dest_ip TEXT, dest_port INTEGER
);
"""

ROWS = {
    "http": [
        ("2026-10-20T14:01:00Z", "198.51.100.23", "203.0.113.10", "GET", "/", "lab-scanner/1.0", ""),
        ("2026-10-20T14:01:02Z", "198.51.100.23", "203.0.113.10", "GET", "/login", "lab-scanner/1.0", ""),
        ("2026-10-20T14:01:04Z", "198.51.100.23", "203.0.113.10", "GET", "/admin", "lab-scanner/1.0", ""),
        ("2026-10-20T14:05:01Z", "198.51.100.23", "203.0.113.10", "POST", "/login", "lab-scanner/1.0", ""),
        ("2026-10-20T14:05:03Z", "198.51.100.23", "203.0.113.10", "POST", "/login", "lab-scanner/1.0", ""),
        ("2026-10-20T14:05:05Z", "198.51.100.23", "203.0.113.10", "POST", "/login", "lab-scanner/1.0", ""),
        ("2026-10-20T14:05:07Z", "198.51.100.23", "203.0.113.10", "POST", "/login", "lab-scanner/1.0", ""),
        ("2026-10-20T14:12:00Z", "198.51.100.23", "203.0.113.10", "POST", "/upload", "lab-scanner/1.0", "notes.txt"),
        ("2026-10-20T15:00:00Z", "198.51.100.50", "203.0.113.10", "GET", "/", "Mozilla/5.0", ""),
    ],
    "ids": [
        ("2026-10-20T14:01:01Z", "198.51.100.23", "203.0.113.10", "ET SCAN lab web probe"),
        ("2026-10-20T14:05:02Z", "198.51.100.23", "203.0.113.10", "ET BRUTE FORCE lab login"),
    ],
    "dns": [
        ("2026-10-20T16:10:00Z", "198.51.100.50", "intranet.example"),
        ("2026-10-20T16:11:00Z", "198.51.100.50", "beacon.example"),
        ("2026-10-20T16:12:00Z", "198.51.100.50", "beacon.example"),
    ],
    "process": [
        ("2026-10-20T16:09:00Z", "ws-04", "explorer.exe", "WINWORD.EXE", "WINWORD.EXE /n report.docm"),
        ("2026-10-20T16:09:05Z", "ws-04", "WINWORD.EXE", "powershell.exe", "powershell.exe -NoP -W Hidden -enc ZQBjAGgAbwAgAHQAZQBzAHQA"),
    ],
    "traffic": [
        ("2026-10-20T14:20:00Z", "203.0.113.10", "203.0.113.80", 443),
        ("2026-10-20T14:20:30Z", "203.0.113.10", "203.0.113.80", 443),
        ("2026-10-20T16:11:05Z", "198.51.100.50", "203.0.113.80", 443),
    ],
}

QUERIES = [
    (
        "sources",
        "Which tables and hosts are in the set?",
        """
        SELECT 'http' AS src, dest_ip AS host, COUNT(*) AS n FROM http GROUP BY dest_ip
        UNION ALL
        SELECT 'ids', dest_ip, COUNT(*) FROM ids GROUP BY dest_ip
        UNION ALL
        SELECT 'process', host, COUNT(*) FROM process GROUP BY host
        UNION ALL
        SELECT 'dns', src_ip, COUNT(*) FROM dns GROUP BY src_ip
        ORDER BY src, host
        """,
    ),
    (
        "web-scan",
        "Who requested the most paths on the web server?",
        """
        SELECT src_ip, user_agent, COUNT(*) AS n
        FROM http WHERE dest_ip = '203.0.113.10'
        GROUP BY src_ip, user_agent ORDER BY n DESC
        """,
    ),
    (
        "ids-alerts",
        "Which IDS signatures fired toward the web server?",
        """
        SELECT signature, COUNT(*) AS n
        FROM ids WHERE dest_ip = '203.0.113.10'
        GROUP BY signature ORDER BY n DESC
        """,
    ),
    (
        "login-posts",
        "How many POSTs hit /login, and from where?",
        """
        SELECT src_ip, COUNT(*) AS n
        FROM http WHERE method = 'POST' AND uri = '/login'
        GROUP BY src_ip ORDER BY n DESC
        """,
    ),
    (
        "upload",
        "Was a file name recorded on a POST?",
        """
        SELECT ts, src_ip, uri, filename FROM http
        WHERE method = 'POST' AND filename != ''
        """,
    ),
    (
        "egress",
        "Where did the web server connect outbound?",
        """
        SELECT dest_ip, dest_port, COUNT(*) AS n
        FROM traffic WHERE src_ip = '203.0.113.10'
        GROUP BY dest_ip, dest_port
        """,
    ),
    (
        "process-chain",
        "Which process chain ran on the workstation?",
        """
        SELECT ts, parent_image, image, command_line
        FROM process WHERE host = 'ws-04' ORDER BY ts
        """,
    ),
    (
        "dns-names",
        "Which names did the workstation look up?",
        """
        SELECT query, COUNT(*) AS n FROM dns
        WHERE src_ip = '198.51.100.50' GROUP BY query ORDER BY n DESC
        """,
    ),
]


def build() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    for table, rows in ROWS.items():
        marks = ", ".join("?" for _ in rows[0])
        db.executemany(f"INSERT INTO {table} VALUES ({marks})", rows)
    return db


def render(db: sqlite3.Connection) -> str:
    lines = ["Synthetic multi-source log investigation", ""]
    for key, question, sql in QUERIES:
        lines.append(f"## {key}")
        lines.append(question)
        rows = db.execute(sql).fetchall()
        headers = rows[0].keys() if rows else []
        if headers:
            lines.append(" | ".join(headers))
            for row in rows:
                lines.append(" | ".join(str(row[h]) for h in headers))
        else:
            lines.append("(no rows)")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    db = build()
    if "--check" in sys.argv:
        posts = db.execute("SELECT COUNT(*) AS n FROM http WHERE uri = '/login' AND method = 'POST'").fetchone()["n"]
        chain = db.execute("SELECT image FROM process ORDER BY ts").fetchall()
        images = [row["image"] for row in chain]
        assert posts == 4, posts
        assert images == ["WINWORD.EXE", "powershell.exe"], images
        assert db.execute("SELECT filename FROM http WHERE filename != ''").fetchone()["filename"] == "notes.txt"
        print("self-check: OK")
    sys.stdout.write(render(db))
    return 0


if __name__ == "__main__":
    sys.exit(main())
