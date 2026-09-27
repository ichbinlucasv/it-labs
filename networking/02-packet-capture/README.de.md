# Lab 02 — Analyse von Netzwerkmitschnitten mit tcpdump, tshark & Wireshark

[English](README.md) · **Deutsch**

**Status:** Done — eigener Mitschnitt erzeugt und analysiert, öffentliches Beispiel `dns.cap` mit Kurzbericht analysiert ([`evidence/`](evidence/)); statt Screenshots aus der Wireshark-Oberfläche habe ich die Textentsprechungen in tshark verwendet (Protokollhierarchie, Follow Stream, Anzeigefilter).

## Ziel

Netzwerkverkehr sicher mitschneiden und danach typische SOC-/Helpdesk-Fragen
aus einer pcap-Datei beantworten: *Wer hat mit wem gesprochen, über welche
Protokolle, was wurde angefragt, was ist fehlgeschlagen, und ist etwas
verdächtig?* (Security+ D2 Indikatoren, D4 Monitoring.)

## Aufbau

- Debian/Ubuntu-VM mit `tcpdump`, `tshark`, `wireshark` (`sudo apt install tcpdump tshark wireshark`).
- **Nur in Netzen mitschneiden, die einem gehören oder für die man eine Erlaubnis hat.**
- Zwei Quellen für pcaps:
  1. **Eigener Mitschnitt**, lokal erzeugt mit
     [`generate-capture.sh`](generate-capture.sh): Das Skript legt einen
     isolierten Network Namespace an, startet einen Python-Webserver auf
     Loopback und schneidet einige HTTP-Anfragen mit (einige mit 404).
     Nichts verlässt den Rechner.
  2. **Öffentliche Beispielmitschnitte** (nach `captures/` herunterladen, von git ignoriert):
     - Wireshark-Wiki — Sample Captures: <https://wiki.wireshark.org/SampleCaptures>
       (z. B. `http.cap`, `dns.cap`, `dhcp.pcap`, `smtp.pcap`, `telnet-cooked.pcap`)
     - Trainingsübungen von Malware-Traffic-Analysis.net (passwortgeschützte
       Zips, **enthalten echten Malware-Verkehr — nur in einer isolierten VM**):
       <https://www.malware-traffic-analysis.net/training-exercises.html>
     - NETRESEC-Liste öffentlicher pcap-Sammlungen:
       <https://www.netresec.com/?page=PcapFiles>

## Schritte

### 1. Mitschneiden

```bash
sudo ./generate-capture.sh lab-http.pcap        # own capture (isolated)

# General tcpdump patterns on your own lab interface:
sudo tcpdump -D                                  # list interfaces
sudo tcpdump -i eth0 -nn -c 50 'port 53'         # watch DNS, no name resolution
sudo tcpdump -i eth0 -w lab.pcap -C 50 -W 5      # ring buffer: 5 × 50 MB
sudo tcpdump -i eth0 -nn 'tcp[tcpflags] & (tcp-syn) != 0 and not tcp[tcpflags] & (tcp-ack) != 0'  # SYNs only
```

### 2. Überblick verschaffen

```bash
capinfos lab-http.pcap                           # duration, packet count
tshark -r lab-http.pcap -q -z io,phs             # protocol hierarchy
tshark -r lab-http.pcap -q -z conv,tcp           # TCP conversations
tshark -r lab-http.pcap -q -z endpoints,ip       # top talkers
```

### 3. Ins Detail gehen

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

### 4. Wireshark-Anzeigefilter zum Üben

| Frage | Filter |
|-------|--------|
| Nur Verkehr eines Hosts | `ip.addr == 10.20.30.57` |
| DNS-Fehler | `dns.flags.rcode != 0` |
| TCP-Resets | `tcp.flags.reset == 1` |
| Retransmissions (langsames Netz) | `tcp.analysis.retransmission` |
| Protokolle mit Klartext-Zugangsdaten | `ftp or telnet or pop or imap or http.authorization` |
| HTTP-POSTs | `http.request.method == "POST"` |
| Große DNS-TXT-Antworten (mögliches Tunneling) | `dns.qry.type == 16 and frame.len > 300` |
| Beacons (regelmäßige Rückrufe) | Statistics → Conversations, nach Paketen sortieren; I/O-Graph |

Außerdem: *Follow → TCP Stream*, *File → Export Objects → HTTP*,
*Statistics → Endpoints / Protocol Hierarchy*.

### 5. Eigener Mitschnitt — Ergebnisse

Ausgeführt unter Debian 13, tcpdump 4.99 / TShark 4.4.18. Vollständige
Ausgabe: [`evidence/own-capture.txt`](evidence/own-capture.txt).

- `capinfos`: 48 Pakete in 0,034 s, alle auf Loopback (`127.0.0.1`).
- Protokollhierarchie: `eth → ip → tcp` (48 Frames) → `http` (8 Frames = 4
  Anfragen + 4 Antworten). Die übrigen 40 Frames sind TCP-Handshakes, ACKs und
  Verbindungsabbau — die meisten Pakete eines kurzen HTTP-Austauschs sind kein HTTP.
- `-z conv,tcp`: 4 Verbindungen, eine pro Anfrage (`curl` öffnet jedes Mal
  eine neue Verbindung; Pythons `http.server` antwortet mit HTTP/1.0 und schließt).
- Anfragen und Fehler:

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

- `-z follow,tcp,ascii,1` (die Textfassung von *Follow → TCP Stream*) zeigt
  die vollständige Anfrage `GET /admin` und die Antwort
  `HTTP/1.0 404 File not found` mit dem Server-Banner
  `SimpleHTTP/0.6 Python/3.13.5` — ein Banner, das die genaue Softwareversion verrät.

Hinweis zur Fehleranalyse: Der Fehler-Befehl in einer früheren Version dieses
Labs verwendete `-e http.response_for.uri`; TShark 4.4 brach mit `Some fields
aren't valid` ab. Ich habe die verfügbaren Felder mit
`tshark -G fields | awk -F'\t' '$3 ~ /^http\./ {print $3}'` aufgelistet und
`http.request.uri` verwendet, das Wireshark auch bei Antworten setzt.

### 5b. Öffentliches Beispiel `dns.cap` — Kurzbericht

Heruntergeladen aus den Wireshark-Wiki-Beispielmitschnitten
(`https://wiki.wireshark.org/uploads/__moin_import__/attachments/SampleCaptures/dns.cap`)
in den von git ignorierten Ordner `captures/`. Vollständige Ausgabe:
[`evidence/dns-cap.txt`](evidence/dns-cap.txt). Die Adressen unten stammen
aus diesem öffentlichen Beispiel von 2005, nicht aus meinem Netz.

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

Kurz auf Deutsch: Der Mitschnitt ist harmlos. Auffällig ist nur der
Windows-Host `192.168.170.56`, der einen externen DNS-Server nach den
SRV-Einträgen seines Active Directory fragt und daher seinen Domain
Controller nicht findet — Domänenanmeldung, GPOs und Zeitsynchronisation
schlagen so fehl. Lösung: Client ausschließlich auf den internen AD-DNS
zeigen lassen. Das ist dieselbe Ursache wie in Ticket-Beispiel 1 im
[Helpdesk-Lab 01](../../helpdesk/01-ticket-writing/examples.md).

### 6. Vorlage für den Kurzbericht (pro pcap)

```text
Pcap:            <file, SHA256, source URL>
Time range:      <first – last packet, UTC>
Hosts of interest: <internal IP / MAC / hostname (DHCP, NBNS, Kerberos)>
Summary:         <2–3 sentences>
Indicators:      <domains / IPs / URLs / hashes, defanged>
Timeline:        <time – event>
Conclusion:      <benign / suspicious / malicious + confidence>
```

## Nachweise

- [`evidence/own-capture.txt`](evidence/own-capture.txt): `capinfos`,
  Protokollhierarchie, TCP-Verbindungen, Endpunkte, HTTP-Anfragen,
  404-Filter und verfolgter TCP-Stream für meinen eigenen Mitschnitt.
- [`evidence/dns-cap.txt`](evidence/dns-cap.txt): Hash, Zeitraum, Endpunkte,
  alle Anfragen/Antworten, NXDOMAIN-Filter, TXT-Prüfung und `-z dns,tree` für
  das öffentliche Beispiel `dns.cap` sowie der Kurzbericht oben.
- Nicht erledigt: Screenshots aus der Wireshark-Oberfläche (ich habe dieses
  Lab nur auf der Kommandozeile gemacht; jede geplante GUI-Ansicht hat oben
  eine tshark-Entsprechung). Die pcaps selbst werden nicht committet
  (`*.pcap` wird von git ignoriert).

## Was ich gelernt habe

- Mit den Statistiken beginnen (`capinfos`, `-z io,phs`, `-z conv`,
  `-z endpoints`), bevor man einzelne Pakete ansieht: Sie zeigen, wo man suchen muss.
- Die meisten Frames eines kurzen HTTP-Austauschs sind TCP-Overhead; ein
  TCP-Stream pro Anfrage ist bei HTTP/1.0 normal.
- Feldnamen ändern sich zwischen Wireshark-Versionen — die Referenz ist
  `tshark -G fields`, nicht ein Blogartikel.
- Ein DNS-Mitschnitt allein kann ein Helpdesk-Problem erklären: Ein
  Windows-Client, der einen öffentlichen Resolver nach `_ldap._tcp.dc._msdcs`
  fragt, wird seinen Domain Controller nie finden.
- Server-Banner in Antworten (`SimpleHTTP/0.6 Python/3.13.5`) sind kostenlose
  Informationen für einen Angreifer.
