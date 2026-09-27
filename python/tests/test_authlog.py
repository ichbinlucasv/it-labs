from pathlib import Path

from seclab import authlog

SAMPLE = Path(__file__).resolve().parents[1] / "samples" / "auth.log.synthetic"


def summary():
    return authlog.parse_lines(SAMPLE.read_text().splitlines())


def test_counts_failed_including_repeated_messages():
    s = summary()
    # 1 admin + 1 root + 2 repeated root + 1 oracle + 3 deploy + 1 alice + 1 test
    assert s.failed_total == 10
    assert s.failed_by_ip["203.0.113.45"] == 8
    assert s.failed_by_user["root"] == 3


def test_invalid_users_tracked():
    s = summary()
    assert s.invalid_users == {"admin": 1, "oracle": 1, "test": 1}


def test_accepted_and_success_after_failure():
    s = summary()
    assert [a["user"] for a in s.accepted] == ["deploy", "alice"]
    flagged = s.success_after_failures()
    assert {(a["user"], a["ip"]) for a in flagged} == {("deploy", "203.0.113.45"), ("alice", "10.20.30.5")}


def test_threshold():
    s = summary()
    assert s.suspicious_ips(5) == [("203.0.113.45", 8)]
    assert s.suspicious_ips(100) == []


def test_classic_syslog_timestamp_and_empty():
    lines = [
        "Sep  4 08:01:02 host sshd[99]: Failed password for bob from 192.0.2.10 port 2222 ssh2",
        "Sep  4 08:01:09 host sshd[99]: Accepted publickey for bob from 192.0.2.10 port 2223 ssh2",
        "garbage line",
    ]
    s = authlog.parse_lines(lines)
    assert s.failed_total == 1
    assert s.first_seen == "Sep  4 08:01:02"
    assert authlog.parse_lines([]).failed_total == 0


def test_ignores_invalid_ip():
    s = authlog.parse_lines(["2026-01-01T00:00:00 h sshd[1]: Failed password for x from 999.1.1.1 port 1 ssh2"])
    assert s.failed_total == 0


def test_cli_text_and_json(capsys):
    assert authlog.main([str(SAMPLE), "--threshold", "5"]) == 0
    out = capsys.readouterr().out
    assert "Failed attempts     : 10" in out
    assert "!! Successful login from an IP that also failed" in out
    assert authlog.main([str(SAMPLE), "--json"]) == 0
    assert '"failed_total": 10' in capsys.readouterr().out
