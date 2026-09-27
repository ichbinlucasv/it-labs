# Lab 02 — Packet capture analysis with tcpdump, tshark & Wireshark

**Status:** In progress — the capture script ran on this machine in an isolated network namespace and the tshark commands produced the documented output; analysis of the public sample captures, the Wireshark GUI work and the mini-report are not done yet.

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
  -T fields -e ip.src -e http.response.code -e http.response_for.uri

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

### 5. Reference output from the locally generated capture (ran on this machine)

Running the commands above against a capture made with the script
(4 requests; the server's directory has no `admin`, `robots.txt` or
`index.html`, so 3 of them return 404 and `/` returns a directory listing) gave:

```text
$ tshark -r lab-http.pcap -Y http.request -T fields -e http.request.method -e http.request.uri -e http.user_agent
GET	/	lab-client/1.0
GET	/admin	lab-client/1.0
GET	/robots.txt	lab-client/1.0
GET	/index.html	lab-client/1.0
$ tshark -r lab-http.pcap -Y 'http.response.code >= 400' -T fields -e http.response.code
404
404
404
```

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

- `capinfos` and `-z conv,tcp` output for my own capture.
- Wireshark screenshots: protocol hierarchy, a followed TCP stream, a display
  filter for 404s.
- One mini-report for a Wireshark wiki sample (e.g. `dns.cap`).

## What I learned

_To be completed by Lucas._
