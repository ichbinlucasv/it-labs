import hashlib
import json
from pathlib import Path

from seclab import hashcheck

SAMPLES = Path(__file__).resolve().parents[1] / "samples"


def test_hash_file_matches_hashlib(tmp_path):
    f = tmp_path / "a.bin"
    data = b"lab data" * 200_000  # > 1 MiB, exercises chunking
    f.write_bytes(data)
    h = hashcheck.hash_file(f)
    assert h["sha256"] == hashlib.sha256(data).hexdigest()
    assert h["md5"] == hashlib.md5(data).hexdigest()
    assert h["sha1"] == hashlib.sha1(data).hexdigest()


def test_parse_known_bad_formats():
    lines = [
        "# comment",
        "",
        "D41D8CD98F00B204E9800998ECF8427E, empty md5",
        "da39a3ee5e6b4b0d3255bfef95601890afd80709 empty sha1",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "nothex!, bad",
        "abcd, too short",
    ]
    known = hashcheck.parse_known_bad(lines)
    assert known == {
        "d41d8cd98f00b204e9800998ecf8427e": "empty md5",
        "da39a3ee5e6b4b0d3255bfef95601890afd80709": "empty sha1",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "(no label)",
    }


def test_scan_finds_match_and_clean(tmp_path):
    bad = tmp_path / "bad.txt"
    bad.write_text("pretend malware")
    good = tmp_path / "sub" / "good.txt"
    good.parent.mkdir()
    good.write_text("benign")
    known = {hashlib.sha256(b"pretend malware").hexdigest(): "TEST-BAD"}

    flat = hashcheck.scan([tmp_path], known, recursive=False)
    assert [Path(r.path).name for r in flat] == ["bad.txt"]

    results = {Path(r.path).name: r for r in hashcheck.scan([tmp_path], known, recursive=True)}
    assert results["bad.txt"].is_bad and results["bad.txt"].label == "TEST-BAD"
    assert results["bad.txt"].match == "sha256"
    assert not results["good.txt"].is_bad


def test_md5_match(tmp_path):
    f = tmp_path / "empty"
    f.write_bytes(b"")
    r = hashcheck.check_file(f, {"d41d8cd98f00b204e9800998ecf8427e": "empty"})
    assert r.is_bad and r.match == "md5"


def test_example_list_matches_fake_dropper():
    known = hashcheck.load_known_bad(SAMPLES / "known_bad.example.txt")
    r = hashcheck.check_file(SAMPLES / "fake_dropper.txt", known)
    assert r.is_bad and "fake dropper" in r.label


def test_cli_exit_codes(tmp_path, capsys):
    f = tmp_path / "x.txt"
    f.write_text("x")
    kb = tmp_path / "kb.txt"
    kb.write_text("0" * 64 + ",nothing\n")
    assert hashcheck.main([str(f), "-k", str(kb)]) == 0
    assert "clean" in capsys.readouterr().out
    kb.write_text(hashlib.sha256(b"x").hexdigest() + ",hit\n")
    assert hashcheck.main([str(f), "-k", str(kb), "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert data[0]["is_bad"] is True and data[0]["label"] == "hit"


def test_missing_path_is_ignored(tmp_path):
    assert hashcheck.scan([tmp_path / "does-not-exist"], {}) == []
