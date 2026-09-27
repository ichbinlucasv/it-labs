# Lab 02 — Packet capture analysis with tcpdump, tshark & Wireshark

**English** · [Deutsch](README.de.md)

**Status:** Done — own capture generated and analysed, public sample `dns.cap` analysed with a mini-report ([`evidence/`](evidence/)); I used tshark's text equivalents (protocol hierarchy, follow stream, display filters) instead of Wireshark GUI screenshots.

## Goal

Capture traffic safely, then answer typical SOC/helpdesk questions from a
pcap: *who talked to whom, over which protocols, what was requested, what
failed, and is anything suspicious?* (Security+ D2 indicators, D4 monitoring.)

## Setup

- Debian/Ubuntu VM with `tcpdump`, `tshark`, `wireshark` (`sudo apt install tcpdump tshark wireshark`).
- **Only capture on networks you own or are authorised to monitor.**
- Two sources of pcaps:
  1. **Your own capture**, generated locally with
     [`generate-capture.sh`](generate-capture.sh): it creates an isolated
     network namespace, runs a Python web server on loopback, and captures a
     few HTTP requests (some returning 404). Nothing leaves the machine.
  2. **Public sample captures** (download into `captures/`, which is git-ignored):
     - Wireshark wiki — Sample Captures: <https://wiki.wireshark.org/SampleCaptures>
       (e.g. `http.cap`, `dns.cap`, `dhcp.pcap`, `smtp.pcap`, `telnet-cooked.pcap`)
     - Malware-Traffic-Analysis.net training exercises (password-protected
       zips, **contain real malware traffic — use an isolated VM**):
       <https://www.malware-traffic-analysis.net/training-exercises.html>
     - NETRESEC list of public pcap repositories:
       <https://www.netresec.com/?page=PcapFiles>

## Steps

### 1. Capture

```bash
sudo ./generate-capture.sh lab-http.pcap        # own capture (isolated)

# General tcpdump patterns on your own lab interface:
sudo tcpdump -D                                  # list interfaces
sudo tcpdump -i eth0 -nn -c 50 'port 53'         # watch DNS, no name resolution
sudo tcpdump -i eth0 -w lab.pcap -C 50 -W 5      # ring buffer: 5 × 50 MB
sudo tcpdump -i eth0 -nn 'tcp[tcpflags] & (tcp-syn) != 0 and not tcp[tcpflags] & (tcp-ack) != 0'  # SYNs only
```

### 2. Get the big picture

```bash
capinfos lab-http.pcap                           # duration, packet count
tshark -r lab-http.pcap -q -z io,phs             # protocol hierarchy
tshark -r lab-http.pcap -q -z conv,tcp           # TCP conversations
tshark -r lab-http.pcap -q -z endpoints,ip       # top talkers
```

### 3. Drill down

```bash
# HTTP requests: time, method, host, URI, user agent
tshark -r lab-http.pcap -Y http.request \
  -T fields -e frame.time_relative -e http.request.method \
  -e http.host -e http.request.uri -e http.user_agent

# Errors
tshark -r lab-http.pcap -Y 'http.response.code >= 400' \
  -T fields -e ip.src -e http.response.code -e http.request.uri
# (on a response, Wireshark 4.x fills http.request.uri with the URI of the
#  matching request; the older field http.response_for.uri no longer exists)

# DNS queries (use dns.cap from the Wireshark wiki)
tshark -r dns.cap -Y 'dns.flags.response == 0' -T fields -e ip.src -e dns.qry.name

# TLS server names (SNI) in HTTPS traffic
tshark -r capture.pcap -Y 'tls.handshake.type == 1' -T fields -e ip.dst -e tls.handshake.extensions_server_name
```

### 4. Wireshark display filters to practise

| Question | Filter |
|----------|--------|
| Only traffic of one host | `ip.addr == 10.20.30.57` |
| DNS failures | `dns.flags.rcode != 0` |
| TCP resets | `tcp.flags.reset == 1` |
| Retransmissions (slow network) | `tcp.analysis.retransmission` |
| Clear-text credentials protocols | `ftp or telnet or pop or imap or http.authorization` |
| HTTP POSTs | `http.request.method == "POST"` |
| Large DNS TXT answers (possible tunnelling) | `dns.qry.type == 16 and frame.len > 300` |
| Beacons (regular callbacks) | Statistics → Conversations, sort by packets; I/O graph |

Also: *Follow → TCP Stream*, *File → Export Objects → HTTP*, *Statistics →
Endpoints / Protocol Hierarchy*.

### 5. My own capture — results

Run on Debian 13, tcpdump 4.99 / TShark 4.4.18. Full output:
[`evidence/own-capture.txt`](evidence/own-capture.txt).

- `capinfos`: 48 packets in 0.034 s, all on loopback (`127.0.0.1`).
- Protocol hierarchy: `eth → ip → tcp` (48 frames) → `http` (8 frames = 4
  requests + 4 responses). The other 40 frames are TCP handshakes, ACKs and
  teardowns — most packets of a short HTTP exchange are not HTTP.
- `-z conv,tcp`: 4 conversations, one per request (`curl` opens a new
  connection each time; Python's `http.server` answers HTTP/1.0 and closes).
- Requests and errors:

```text
$ tshark -r lab-http.pcap -Y http.request -T fields -e http.request.method -e http.request.uri -e http.user_agent
GET	/	lab-client/1.0
GET	/admin	lab-client/1.0
GET	/robots.txt	lab-client/1.0
GET	/index.html	lab-client/1.0
$ tshark -r lab-http.pcap -Y 'http.response.code >= 400' -T fields -e ip.src -e http.response.code -e http.request.uri
127.0.0.1	404	/admin
127.0.0.1	404	/robots.txt
127.0.0.1	404	/index.html
```

- `-z follow,tcp,ascii,1` (the text version of *Follow → TCP Stream*) shows
  the full `GET /admin` request and the `HTTP/1.0 404 File not found`
  response with the server banner `SimpleHTTP/0.6 Python/3.13.5` — a banner
  that leaks the exact software version.

Troubleshooting note: the error command in an earlier version of this lab
used `-e http.response_for.uri`; TShark 4.4 stopped with `Some fields aren't
valid`. I listed the available fields with
`tshark -G fields | awk -F'\t' '$3 ~ /^http\./ {print $3}'` and used
`http.request.uri`, which Wireshark also sets on responses.

### 5b. Public sample `dns.cap` — mini-report

Downloaded from the Wireshark wiki sample captures
(`https://wiki.wireshark.org/uploads/__moin_import__/attachments/SampleCaptures/dns.cap`)
into the git-ignored `captures/` folder. Full output:
[`evidence/dns-cap.txt`](evidence/dns-cap.txt). The addresses below are the
ones inside this public 2005 sample, not from my network.

```text
Pcap:            dns.cap (Wireshark wiki), SHA256 041eeb6f98bb398f1ee8b09651b5b5a84f6a62639f95bf226f9e7b77355d9f28
Time range:      2005-03-30 08:47:46 – 08:52:25 UTC (38 packets, 279 s), UDP/53 only
Hosts of interest:
                 192.168.170.8  -> DNS server 192.168.170.20: 14 queries (test client)
                 192.168.170.56 -> external DNS 217.13.4.24: 5 queries (Windows host)
Summary:         Mostly a test of many record types against one resolver
                 (TXT, MX, LOC, PTR, A, AAAA, CNAME, ANY, NS — 19 queries, 19 answers,
                 all answered). One NXDOMAIN for a typo'd name (www.example.notginh).
                 The second host asks a public resolver for Active Directory SRV
                 records (_ldap._tcp.dc._msdcs.<domain>.local) and its own name
                 (GRIMM.<domain>.local); all 5 answers are NXDOMAIN (rcode 3).
Indicators:      none malicious. Largest answer: 256-byte payload; the only TXT
                 answer is an SPF record (v=spf1 ptr ?all) — no sign of DNS tunnelling.
Timeline:        08:47:46  first query (TXT google.com)
                 08:51:47  NXDOMAIN www.example.notginh
                 08:52:17  4 NXDOMAIN answers for AD SRV records / host name
                 08:52:25  last NXDOMAIN (GRIMM.<domain>.local, retried)
Conclusion:      benign. Helpdesk reading: 192.168.170.56 is configured with an
                 external DNS server, so it cannot find its domain controller —
                 this breaks domain logon, GPOs and time sync. Fix: point the
                 client at the internal AD DNS only. Confidence: high.
```

That last point is the same root cause as ticket example 1 in
[helpdesk lab 01](../../helpdesk/01-ticket-writing/examples.md).

### 6. Mini-report template (per pcap)

```text
Pcap:            <file, SHA256, source URL>
Time range:      <first – last packet, UTC>
Hosts of interest: <internal IP / MAC / hostname (DHCP, NBNS, Kerberos)>
Summary:         <2–3 sentences>
Indicators:      <domains / IPs / URLs / hashes, defanged>
Timeline:        <time – event>
Conclusion:      <benign / suspicious / malicious + confidence>
```

## Evidence

- [`evidence/own-capture.txt`](evidence/own-capture.txt): `capinfos`,
  protocol hierarchy, TCP conversations, endpoints, HTTP requests, 404 filter,
  followed TCP stream for my own capture.
- [`evidence/dns-cap.txt`](evidence/dns-cap.txt): hash, time range,
  endpoints, all queries/answers, NXDOMAIN filter, TXT check, `-z dns,tree`
  for the public `dns.cap` sample, and the mini-report above.
- Not done: Wireshark GUI screenshots (I did this lab on the command line only;
  every GUI view I planned has a tshark equivalent above).
  Pcaps themselves are not committed (`*.pcap` is git-ignored).

## What I learned

- Start with the statistics (`capinfos`, `-z io,phs`, `-z conv`,
  `-z endpoints`) before looking at single packets: they tell you where to look.
- Most frames in a short HTTP exchange are TCP overhead; one TCP stream per
  request is normal for HTTP/1.0.
- Field names change between Wireshark versions — `tshark -G fields` is the
  reference, not a blog post.
- A DNS capture alone can explain a helpdesk problem: a Windows client asking
  a public resolver for `_ldap._tcp.dc._msdcs` records will never find its
  domain controller.
- Server banners in responses (`SimpleHTTP/0.6 Python/3.13.5`) are free
  information for an attacker.
