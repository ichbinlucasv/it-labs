# Lösung

[English](answer-key.md) · [Français](answer-key.fr.md) · **Deutsch**

Berechnet und mit Pythons Modul `ipaddress` geprüft.

## Teil A

| # | Adresse | Netz | Maske | Broadcast | Erster Host | Letzter Host | Nutzbare Hosts |
|---|---------|------|-------|-----------|-------------|--------------|----------------|
| 1 | `192.168.10.77/26` | 192.168.10.64/26 | 255.255.255.192 | 192.168.10.127 | 192.168.10.65 | 192.168.10.126 | 62 |
| 2 | `10.4.200.9/20` | 10.4.192.0/20 | 255.255.240.0 | 10.4.207.255 | 10.4.192.1 | 10.4.207.254 | 4094 |
| 3 | `172.16.35.130/27` | 172.16.35.128/27 | 255.255.255.224 | 172.16.35.159 | 172.16.35.129 | 172.16.35.158 | 30 |
| 4 | `198.51.100.200/29` | 198.51.100.200/29 | 255.255.255.248 | 198.51.100.207 | 198.51.100.201 | 198.51.100.206 | 6 |
| 5 | `10.0.0.255/23` | 10.0.0.0/23 | 255.255.254.0 | 10.0.1.255 | 10.0.0.1 | 10.0.1.254 | 510 |
| 6 | `203.0.113.66/30` | 203.0.113.64/30 | 255.255.255.252 | 203.0.113.67 | 203.0.113.65 | 203.0.113.66 | 2 |
| 7 | `172.20.99.1/18` | 172.20.64.0/18 | 255.255.192.0 | 172.20.127.255 | 172.20.64.1 | 172.20.127.254 | 16382 |
| 8 | `192.0.2.143/28` | 192.0.2.128/28 | 255.255.255.240 | 192.0.2.143 | 192.0.2.129 | 192.0.2.142 | 14 |

Hinweise:
- **Q4:** die angegebene Adresse ist selbst die Netzwerkadresse (200 ist ein Vielfaches von 8) — nicht vergebbar.
- **Q5:** `10.0.0.255` sieht aus wie ein Broadcast, ist in einem /23 aber eine normale Hostadresse.
- **Q8:** `192.0.2.143` ist die **Broadcast**-Adresse ihres /28 — sie kann keinem Host zugewiesen werden.

## Teil B

9.  **Ja** — beide in `10.1.1.128/25`.
10. **Nein** — `192.168.5.14` liegt in `192.168.5.0/28` (Hosts .1–.14); `.17` liegt in `192.168.5.16/28`.
11. **Ja** — beide in `172.16.4.0/22` (172.16.4.0 – 172.16.7.255).

## Teil C — VLSM-Plan für 10.50.0.0/22

| Segment | Benötigte Hosts | Präfix | Netz | Nutzbarer Bereich | Broadcast | Reserve |
|---|---:|---|---|---|---|---:|
| Arbeitsplätze | 300 | /23 | 10.50.0.0/23 | 10.50.0.1 – 10.50.1.254 | 10.50.1.255 | 210 |
| WLAN-Gäste | 120 | /25 | 10.50.2.0/25 | 10.50.2.1 – 10.50.2.126 | 10.50.2.127 | 6 |
| Server | 50 | /26 | 10.50.2.128/26 | 10.50.2.129 – 10.50.2.190 | 10.50.2.191 | 12 |
| Drucker | 20 | /27 | 10.50.2.192/27 | 10.50.2.193 – 10.50.2.222 | 10.50.2.223 | 10 |
| Verwaltung | 10 | /28 | 10.50.2.224/28 | 10.50.2.225 – 10.50.2.238 | 10.50.2.239 | 4 |
| WAN-Strecke | 2 | /30 | 10.50.2.240/30 | 10.50.2.241 – 10.50.2.242 | 10.50.2.243 | 0 |

Erste freie Adresse: **10.50.2.244** (das ganze `10.50.3.0/24` ist ebenfalls noch frei).
In Produktion würde ich Wachstum lassen (zum Beispiel den Gästen ein /24 geben).

## Teil D

13. `10.8.0.0/22`
14. **256** (2^(24−16)).
15. **/23** — 510 nutzbare Hosts, also 10 ungenutzte Hostadressen (512 gesamt − 2 − 500).
16. **APIPA / verbindungslokal** (`169.254.0.0/16`): der Client hat keine DHCP-Antwort bekommen —
    Kabel/WLAN, VLAN, DHCP-Server/erschöpfter Bereich, DHCP-Relay prüfen.
17. Privat: `172.31.255.1`, `192.168.0.1`, `10.255.0.1`.
    Nicht RFC 1918: `172.32.1.1` (öffentlich; 172.16.0.0/12 endet bei 172.31.255.255),
    `100.64.0.1` (gemeinsamer Adressraum nach RFC 6598, genutzt für Carrier-Grade-NAT).
18. Sie sind für Dokumentation reserviert (RFC 5737) und werden im Internet
    nie geroutet, damit ein Beispiel nicht aus Versehen auf eine echte Organisation zeigt.
