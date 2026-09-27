import json
from pathlib import Path

import pytest

from seclab import ioc

REPORT = Path(__file__).resolve().parents[1] / "samples" / "threat-report.synthetic.txt"


@pytest.mark.parametrize(
    "defanged, live",
    [
        ("hxxps://evil[.]example/path", "https://evil.example/path"),
        ("hXXp://198.51.100[.]7:8080/a", "http://198.51.100.7:8080/a"),
        ("user[@]example[.]com", "user@example.com"),
        ("bad(.)example(dot)net", "bad.example.net"),
        ("fxp://files{.}example[.]org", "ftp://files.example.org"),
        ("https[://]a[.]example", "https://a.example"),
    ],
)
def test_refang(defanged, live):
    assert ioc.refang(defanged) == live


@pytest.mark.parametrize(
    "live, defanged",
    [
        ("https://evil.example/a.b/c", "hxxps://evil[.]example/a.b/c"),
        ("203.0.113.9", "203[.]0[.]113[.]9"),
        ("evil.example.net", "evil[.]example[.]net"),
        ("a@b.example", "a[@]b[.]example"),
        ("2001:db8::1", "2001[:]db8[:][:]1"),
    ],
)
def test_defang(live, defanged):
    assert ioc.defang(live) == defanged


def test_defang_refang_roundtrip():
    for v in ["https://x.example/p?q=1", "198.51.100.1", "mail@x.example", "sub.x.example"]:
        assert ioc.refang(ioc.defang(v)) == v


def test_extract_from_synthetic_report():
    r = ioc.extract(REPORT.read_text())
    assert r.ipv4 == ["10.20.30.57", "198.51.100.77", "203.0.113.45", "10.20.30.20"]
    assert r.ipv6 == ["2001:db8:dead:beef::25"]
    assert r.urls == ["https://cdn-update.example.net/assets/update.bin"]
    assert r.emails == ["billing@examp1e-invoices.test"]
    assert "cdn-update.example.net" in r.domains
    assert "examp1e-invoices.test" in r.domains
    assert "synchelper.exe" not in r.domains  # file names filtered
    assert r.sha256 == ["9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"]
    assert r.md5 == ["098f6bcd4621d373cade4e832627b4f6"]
    assert r.sha1 == []


def test_exclude_private():
    r = ioc.extract(REPORT.read_text(), exclude_private=True)
    # 203.0.113.0/24 and 198.51.100.0/24 are documentation ranges; Python flags them
    # as private (not globally routable), so they are excluded too - expected.
    assert "10.20.30.57" not in r.ipv4
    assert r.ipv6 == []


def test_rejects_invalid_ips_and_times():
    r = ioc.extract("version 1.2.3.4.5 bad 256.1.1.1 time 21:40:00 mac 00:11:22:33:44:55")
    assert r.ipv4 == []
    assert r.ipv6 == []


def test_hash_lengths_do_not_overlap():
    sha1 = "a" * 40
    r = ioc.extract(f"sha1 {sha1}")
    assert r.sha1 == [sha1] and r.md5 == [] and r.sha256 == []


def test_deduplication_preserves_order():
    r = ioc.extract("192.0.2.2 192.0.2.1 192.0.2.2")
    assert r.ipv4 == ["192.0.2.2", "192.0.2.1"]


def test_cli_json_defanged(capsys):
    assert ioc.main([str(REPORT), "--json", "--defang"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "hxxps://cdn-update[.]example[.]net/assets/update.bin" in data["urls"]
    assert "198[.]51[.]100[.]77" in data["ipv4"]


def test_cli_stdin(monkeypatch, capsys):
    import io
    monkeypatch.setattr("sys.stdin", io.StringIO("nothing here"))
    assert ioc.main([]) == 0
    assert "No IOCs found." in capsys.readouterr().out


def test_filters_usernames_and_windows_paths():
    text = r'"User": "CORP\\c.martin", "TargetUserName": "j.dupont", C:\Users\x\Content.Word\a.tmp host intranet.example.com'
    r = ioc.extract(text)
    assert r.domains == ["intranet.example.com"]
    loose = ioc.extract("TargetUserName j.dupont", any_tld=True)
    assert loose.domains == ["j.dupont"]


def test_country_code_tlds_accepted():
    assert ioc.extract("see phish-lab.xx and cdn.lab.zz").domains == ["phish-lab.xx", "cdn.lab.zz"]
