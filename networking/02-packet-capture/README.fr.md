# Lab 02 — Analyse de captures avec tcpdump, tshark et Wireshark

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — capture perso générée et analysée, exemple public `dns.cap` analysé avec un mini-rapport ([`evidence/`](evidence/)) ; j'ai utilisé les équivalents texte de tshark (hiérarchie des protocoles, follow stream, filtres d'affichage) à la place de captures d'écran de l'interface Wireshark.

## Objectif

Capturer du trafic sans risque, puis répondre aux questions habituelles
SOC ou helpdesk à partir d'un pcap : *qui a parlé à qui, avec quels
protocoles, qu'est-ce qui a été demandé, qu'est-ce qui a échoué, et est-ce
qu'il y a quelque chose de suspect ?* (Security+ D2 indicateurs, D4 surveillance.)

## Mise en place

- VM Debian/Ubuntu avec `tcpdump`, `tshark`, `wireshark`
  (`sudo apt install tcpdump tshark wireshark`).
- **Je ne capture que sur des réseaux à moi, ou que j'ai le droit de surveiller.**
- Deux sources de pcaps :
  1. **Ma propre capture**, générée en local avec
     [`generate-capture.sh`](generate-capture.sh) : le script crée un network
     namespace isolé, lance un serveur web Python sur le loopback, et capture
     quelques requêtes HTTP (certaines renvoient 404). Rien ne sort de la machine.
  2. **Captures d'exemple publiques** (à télécharger dans `captures/`, ignoré par git) :
     - Wiki Wireshark — Sample Captures : <https://wiki.wireshark.org/SampleCaptures>
       (par exemple `http.cap`, `dns.cap`, `dhcp.pcap`, `smtp.pcap`, `telnet-cooked.pcap`)
     - Exercices de formation Malware-Traffic-Analysis.net (zip protégés par
       mot de passe, **ils contiennent du vrai trafic malveillant — VM isolée**) :
       <https://www.malware-traffic-analysis.net/training-exercises.html>
     - Liste NETRESEC de dépôts publics de pcaps :
       <https://www.netresec.com/?page=PcapFiles>

## Étapes

### 1. Capturer

```bash
sudo ./generate-capture.sh lab-http.pcap        # own capture (isolated)

# General tcpdump patterns on your own lab interface:
sudo tcpdump -D                                  # list interfaces
sudo tcpdump -i eth0 -nn -c 50 'port 53'         # watch DNS, no name resolution
sudo tcpdump -i eth0 -w lab.pcap -C 50 -W 5      # ring buffer: 5 × 50 MB
sudo tcpdump -i eth0 -nn 'tcp[tcpflags] & (tcp-syn) != 0 and not tcp[tcpflags] & (tcp-ack) != 0'  # SYNs only
```

### 2. Vue d'ensemble

```bash
capinfos lab-http.pcap                           # duration, packet count
tshark -r lab-http.pcap -q -z io,phs             # protocol hierarchy
tshark -r lab-http.pcap -q -z conv,tcp           # TCP conversations
tshark -r lab-http.pcap -q -z endpoints,ip       # top talkers
```

### 3. Zoomer

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

### 4. Filtres d'affichage Wireshark à pratiquer

| Question | Filtre |
|----------|--------|
| Seulement le trafic d'un hôte | `ip.addr == 10.20.30.57` |
| Échecs DNS | `dns.flags.rcode != 0` |
| Reset TCP | `tcp.flags.reset == 1` |
| Retransmissions (réseau lent) | `tcp.analysis.retransmission` |
| Protocoles d'identifiants en clair | `ftp or telnet or pop or imap or http.authorization` |
| POST HTTP | `http.request.method == "POST"` |
| Grandes réponses DNS TXT (tunnel possible) | `dns.qry.type == 16 and frame.len > 300` |
| Beacons (rappels réguliers) | Statistics → Conversations, tri par paquets ; I/O graph |

Aussi : *Follow → TCP Stream*, *File → Export Objects → HTTP*, *Statistics →
Endpoints / Protocol Hierarchy*.

### 5. Ma propre capture — résultats

Lancé sur Debian 13, tcpdump 4.99 / TShark 4.4.18. Sortie complète :
[`evidence/own-capture.txt`](evidence/own-capture.txt).

- `capinfos` : 48 paquets en 0.034 s, tous sur le loopback (`127.0.0.1`).
- Hiérarchie des protocoles : `eth → ip → tcp` (48 trames) → `http` (8 trames
  = 4 requêtes + 4 réponses). Les 40 autres trames sont des poignées de main
  TCP, des ACK et des fermetures. La plupart des paquets d'un court échange
  HTTP ne sont pas de l'HTTP.
- `-z conv,tcp` : 4 conversations, une par requête (`curl` ouvre une nouvelle
  connexion à chaque fois ; `http.server` de Python répond en HTTP/1.0 et ferme).
- Requêtes et erreurs :

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

- `-z follow,tcp,ascii,1` (la version texte de *Follow → TCP Stream*) montre
  la requête complète `GET /admin` et la réponse `HTTP/1.0 404 File not found`,
  avec la bannière serveur `SimpleHTTP/0.6 Python/3.13.5`. Cette bannière
  laisse fuir la version exacte du logiciel.

Note de dépannage : la commande d'erreur dans une version précédente de ce
lab utilisait `-e http.response_for.uri`. TShark 4.4 s'est arrêté avec
`Some fields aren't valid`. J'ai listé les champs disponibles avec
`tshark -G fields | awk -F'\t' '$3 ~ /^http\./ {print $3}'` et j'ai utilisé
`http.request.uri`, que Wireshark remplit aussi sur les réponses.

### 5b. Exemple public `dns.cap` — mini-rapport

Téléchargé depuis les captures d'exemple du wiki Wireshark
(`https://wiki.wireshark.org/uploads/__moin_import__/attachments/SampleCaptures/dns.cap`)
dans le dossier `captures/`, ignoré par git. Sortie complète :
[`evidence/dns-cap.txt`](evidence/dns-cap.txt). Les adresses ci-dessous sont
celles de cet exemple public de 2005, pas celles de mon réseau.

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

Ce dernier point est la même cause que l'exemple de ticket 1 dans le
[lab helpdesk 01](../../helpdesk/01-ticket-writing/examples.md).

### 6. Modèle de mini-rapport (par pcap)

```text
Pcap:            <file, SHA256, source URL>
Time range:      <first – last packet, UTC>
Hosts of interest: <internal IP / MAC / hostname (DHCP, NBNS, Kerberos)>
Summary:         <2–3 sentences>
Indicators:      <domains / IPs / URLs / hashes, defanged>
Timeline:        <time – event>
Conclusion:      <benign / suspicious / malicious + confidence>
```

## Preuves

- [`evidence/own-capture.txt`](evidence/own-capture.txt) : `capinfos`,
  hiérarchie des protocoles, conversations TCP, endpoints, requêtes HTTP,
  filtre 404, flux TCP suivi, pour ma propre capture.
- [`evidence/dns-cap.txt`](evidence/dns-cap.txt) : hash, plage de temps,
  endpoints, toutes les requêtes et réponses, filtre NXDOMAIN, contrôle TXT,
  `-z dns,tree` pour l'exemple public `dns.cap`, et le mini-rapport ci-dessus.
- Pas fait : captures d'écran de l'interface Wireshark (j'ai fait ce lab
  seulement en ligne de commande ; chaque vue d'interface que j'avais prévue
  a un équivalent tshark plus haut). Les pcaps eux-mêmes ne sont pas commités
  (`*.pcap` est ignoré par git).

## Ce que j'ai appris

- Je commence par les statistiques (`capinfos`, `-z io,phs`, `-z conv`,
  `-z endpoints`) avant de regarder des paquets un par un. Elles disent où regarder.
- La plupart des trames d'un court échange HTTP sont du surcoût TCP. Un flux
  TCP par requête est normal en HTTP/1.0.
- Les noms de champs changent entre versions de Wireshark. `tshark -G fields`
  est la référence, pas un billet de blog.
- Une capture DNS seule peut expliquer un problème helpdesk. Un client Windows
  qui demande des enregistrements `_ldap._tcp.dc._msdcs` à un résolveur public
  ne trouvera jamais son contrôleur de domaine.
- Les bannières serveur dans les réponses (`SimpleHTTP/0.6 Python/3.13.5`)
  sont des informations gratuites pour un attaquant.
