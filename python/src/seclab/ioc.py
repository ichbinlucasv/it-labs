"""Extract indicators of compromise (IOCs) from text, with defang/refang helpers.

Supported: IPv4, IPv6, domains, URLs, e-mail addresses, MD5/SHA1/SHA256 hashes.
Defanged input such as ``hxxps://evil[.]example`` or ``198.51.100[.]7`` is
refanged before extraction, so reports from other analysts can be parsed.

Examples::

    python -m seclab.ioc report.txt --defang
    cat alert.json | python -m seclab.ioc --json --exclude-private
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from dataclasses import asdict, dataclass, field

# --- refang / defang --------------------------------------------------------

_REFANG_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bhxxp(s?)\b", re.I), r"http\1"),
    (re.compile(r"\bfxp\b", re.I), "ftp"),
    (re.compile(r"\[://\]"), "://"),
    (re.compile(r"\[:\]"), ":"),
    (re.compile(r"\[\.\]|\(\.\)|\{\.\}|\[dot\]|\(dot\)", re.I), "."),
    (re.compile(r"\[@\]|\(@\)|\[at\]|\(at\)", re.I), "@"),
]


def refang(text: str) -> str:
    """Turn common defanged notations back into live indicators (for parsing only)."""
    for pattern, repl in _REFANG_RULES:
        text = pattern.sub(repl, text)
    return text


def defang(value: str) -> str:
    """Make an indicator non-clickable: ``https://a.example`` -> ``hxxps://a[.]example``."""
    v = re.sub(r"^http", "hxxp", value, flags=re.I)
    v = re.sub(r"^ftp", "fxp", v, flags=re.I)
    v = v.replace("@", "[@]")
    if "://" in v:
        scheme, rest = v.split("://", 1)
        host, sep, path = rest.partition("/")
        return f"{scheme}://{host.replace('.', '[.]')}{sep}{path}"
    if ":" in v and v.count(":") >= 2:  # IPv6
        return v.replace(":", "[:]")
    return v.replace(".", "[.]")


# --- extraction ---------------------------------------------------------------

URL_RE = re.compile(r"\b(?:https?|ftp)://[^\s\"'<>\]\[)(]+", re.I)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63}\b")
IPV4_RE = re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])")
IPV6_RE = re.compile(r"(?<![0-9A-Fa-f:])(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}(?![0-9A-Fa-f:])")
DOMAIN_RE = re.compile(r"\b(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}\b")
HASH_RE = {
    "sha256": re.compile(r"\b[A-Fa-f0-9]{64}\b"),
    "sha1": re.compile(r"\b[A-Fa-f0-9]{40}\b"),
    "md5": re.compile(r"\b[A-Fa-f0-9]{32}\b"),
}

# Things that look like domains but are almost always file names in logs.
# (Some are also real TLDs, e.g. .sh or .zip - a known trade-off, documented.)
FILE_EXTENSIONS = {
    "exe", "dll", "sys", "bat", "cmd", "ps1", "psm1", "vbs", "js", "jse", "hta", "lnk",
    "doc", "docx", "docm", "xls", "xlsx", "xlsm", "ppt", "pptx", "pdf", "rtf", "txt",
    "log", "csv", "json", "xml", "yml", "yaml", "ini", "cfg", "conf", "tmp", "dat",
    "jpg", "jpeg", "png", "gif", "bmp", "zip", "rar", "7z", "gz", "tgz", "tar", "iso",
    "img", "sh", "py", "pl", "rb", "php", "jsp", "aspx", "html", "htm", "evtx", "pcap",
    "pcapng", "md", "so", "bin", "elf", "msi", "jar", "apk",
}


# Longer (generic) TLDs accepted by default. Every 2-letter TLD (country codes)
# is accepted. This keeps things like "c.martin" or "Content.Word" (user names,
# Windows paths) out of the results; use any_tld=True / --any-tld to disable.
COMMON_GTLDS = {
    "com", "net", "org", "info", "biz", "edu", "gov", "mil", "int", "arpa",
    "name", "pro", "mobi", "aero", "asia", "coop", "jobs", "museum", "tel", "travel",
    "xyz", "top", "online", "site", "club", "shop", "store", "app", "dev", "cloud",
    "live", "life", "tech", "space", "website", "link", "click", "buzz", "icu", "vip",
    "work", "fun", "win", "bid", "loan", "email", "support", "services", "digital",
    "network", "systems", "solutions", "company", "global", "world", "today", "news",
    "blog", "page", "host", "lol", "monster", "rest", "cyou", "sbs", "cfd", "quest",
    "bond", "pw", "download", "stream", "zip", "mov", "onion",
    # reserved for documentation/testing (RFC 2606 / RFC 6761)
    "test", "example", "invalid", "localhost",
}


@dataclass
class IOCs:
    ipv4: list[str] = field(default_factory=list)
    ipv6: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    emails: list[str] = field(default_factory=list)
    md5: list[str] = field(default_factory=list)
    sha1: list[str] = field(default_factory=list)
    sha256: list[str] = field(default_factory=list)

    def as_dict(self, defanged: bool = False) -> dict[str, list[str]]:
        d = asdict(self)
        if defanged:
            for key in ("ipv4", "ipv6", "domains", "urls", "emails"):
                d[key] = [defang(v) for v in d[key]]
        return d

    def total(self) -> int:
        return sum(len(v) for v in asdict(self).values())


def _unique(items) -> list[str]:
    seen: dict[str, None] = {}
    for i in items:
        seen.setdefault(i, None)
    return list(seen)


def _is_public(ip: ipaddress._BaseAddress) -> bool:
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast
                or ip.is_reserved or ip.is_unspecified)


def _plausible_tld(tld: str, any_tld: bool) -> bool:
    if tld in FILE_EXTENSIONS or tld.isdigit():
        return False
    return any_tld or len(tld) == 2 or tld in COMMON_GTLDS


def extract(text: str, exclude_private: bool = False, any_tld: bool = False) -> IOCs:
    """Extract IOCs from ``text``. Results are de-duplicated, in order of appearance."""
    text = refang(text)
    result = IOCs()

    result.urls = _unique(u.rstrip(".,;:!?'\"") for u in URL_RE.findall(text))
    result.emails = _unique(e.lower() for e in EMAIL_RE.findall(text))

    for cand in IPV4_RE.findall(text):
        try:
            ip = ipaddress.IPv4Address(cand)
        except ValueError:
            continue
        if exclude_private and not _is_public(ip):
            continue
        result.ipv4.append(str(ip))
    result.ipv4 = _unique(result.ipv4)

    for cand in IPV6_RE.findall(text):
        if cand.count(":") < 2:
            continue
        try:
            ip6 = ipaddress.IPv6Address(cand)
        except ValueError:
            continue
        if ip6.is_unspecified or (exclude_private and not _is_public(ip6)):
            continue
        result.ipv6.append(ip6.compressed)
    result.ipv6 = _unique(result.ipv6)

    # hashes: longest first, so a SHA256 is not also reported as something shorter
    for name in ("sha256", "sha1", "md5"):
        setattr(result, name, _unique(h.lower() for h in HASH_RE[name].findall(text)))

    email_domains = {e.split("@", 1)[1] for e in result.emails}
    domains = []
    for m in DOMAIN_RE.finditer(text):
        if m.start() > 0 and text[m.start() - 1] == "\\":
            continue  # Windows path component or DOMAIN\user, not a hostname
        d = m.group(0).lower().rstrip(".")
        if not _plausible_tld(d.rsplit(".", 1)[-1], any_tld):
            continue
        domains.append(d)
    # keep domains that also appear in URLs/e-mails: analysts usually want them listed
    result.domains = _unique(domains + sorted(email_domains - set(domains)))
    return result


def format_text(iocs: IOCs, defanged: bool = False) -> str:
    lines = []
    for key, values in iocs.as_dict(defanged).items():
        if values:
            lines.append(f"[{key}] ({len(values)})")
            lines.extend(f"  {v}" for v in values)
    return "\n".join(lines) if lines else "No IOCs found."


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Extract IOCs (IPs, domains, URLs, e-mails, hashes) from text")
    p.add_argument("files", nargs="*", help="input files (default: stdin)")
    p.add_argument("--defang", action="store_true", help="print network indicators defanged")
    p.add_argument("--exclude-private", action="store_true", help="drop private/loopback/reserved IPs")
    p.add_argument("--any-tld", action="store_true", help="accept any TLD (more false positives)")
    p.add_argument("--json", action="store_true", help="JSON output")
    p.add_argument("--refang-only", action="store_true", help="just refang the input text and print it")
    args = p.parse_args(argv)

    if args.files:
        text = "\n".join(open(f, encoding="utf-8", errors="replace").read() for f in args.files)
    else:
        text = sys.stdin.read()

    if args.refang_only:
        print(refang(text), end="")
        return 0
    iocs = extract(text, exclude_private=args.exclude_private, any_tld=args.any_tld)
    if args.json:
        print(json.dumps(iocs.as_dict(args.defang), indent=2))
    else:
        print(format_text(iocs, args.defang))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
