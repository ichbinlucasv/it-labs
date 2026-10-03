# Subnetting-Übungen

[English](exercises.md) · [Français](exercises.fr.md) · **Deutsch**

## Teil A — Netzangaben

Für jede Adresse angeben: Netzwerkadresse, Subnetzmaske, Broadcast-Adresse,
erste nutzbare Hostadresse, letzte nutzbare Hostadresse, Anzahl nutzbarer Hosts.

1. `192.168.10.77/26`
2. `10.4.200.9/20`
3. `172.16.35.130/27`
4. `198.51.100.200/29`
5. `10.0.0.255/23`
6. `203.0.113.66/30`
7. `172.20.99.1/18`
8. `192.0.2.143/28` — kann diese Adresse einem Host zugewiesen werden?

## Teil B — Gleiches Subnetz?

Können diese zwei Hosts direkt miteinander sprechen (gleiches Subnetz), ohne Router?

9.  `10.1.1.130/25` und `10.1.1.200/25`
10. `192.168.5.14/28` und `192.168.5.17/28`
11. `172.16.4.1/22` und `172.16.7.254/22`

## Teil C — VLSM-Plan

12. Exemple SARL hat `10.50.0.0/22` bekommen. Subnetze vergeben, **größte
    zuerst**, lückenlos ab dem Anfang des Blocks, mit dem kleinsten Präfix,
    das reicht:

| Segment | Benötigte Hosts |
|---------|----------------:|
| Arbeitsplätze | 300 |
| WLAN-Gäste | 120 |
| Server | 50 |
| Drucker | 20 |
| Verwaltung | 10 |
| WAN-Strecke (Router zu Router) | 2 |

    Danach: was ist die erste freie Adresse, die im /22 übrig bleibt?

## Teil D — Zusammenfassung und Größe

13. `10.8.0.0/24`, `10.8.1.0/24`, `10.8.2.0/24`, `10.8.3.0/24` zu einer
    Route zusammenfassen.
14. Wie viele /24-Subnetze passen in `172.16.0.0/16`?
15. Welches Präfix brauche ich für genau 500 Hosts? Wie viele Adressen bleiben ungenutzt?
16. Ein Benutzer hat die IP `169.254.12.7`. Was bedeutet das?
17. Welche davon sind privat (RFC 1918)? `172.32.1.1`, `172.31.255.1`,
    `192.168.0.1`, `10.255.0.1`, `100.64.0.1`
18. Warum tauchen die RFC-5737-Bereiche (`192.0.2.0/24`, `198.51.100.0/24`,
    `203.0.113.0/24`) in Dokumentation auf?
