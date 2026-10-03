# Lab 01 — Subnetting üben

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Done — Übungen und Lösung geschrieben; jede Antwort wurde mit Pythons `ipaddress` berechnet und geprüft.

## Ziel

Beim IPv4-Subnetting schnell und genau werden: Netz- und Broadcast-Adresse,
Hostbereiche, einen VLSM-Plan bauen und Routen zusammenfassen. Brauche ich
für die Netz-Triage im Helpdesk, Firewall-Regeln und SIEM-Abfragen auf
IP-Bereiche (Security+ D3 — Netzsegmentierung).

## Aufbau

- Zuerst Stift und Papier, dann prüfen mit `ipcalc`
  (`sudo apt install ipcalc`) oder Pythons Modul `ipaddress`:

```python
import ipaddress
n = ipaddress.ip_interface("192.168.10.77/26").network
print(n, n.netmask, n.broadcast_address, n.num_addresses - 2)
```

## Schritte

1. Die Tabelle der „magischen Zahlen“ unten auswendig lernen.
2. [`exercises.md`](exercises.md) ohne Werkzeug lösen und die Zeit nehmen.
3. Mit [`answer-key.md`](answer-key.md) prüfen (die Antworten wurden mit
   Pythons `ipaddress` erzeugt und gegengeprüft).
4. Die falsch gelösten ein paar Tage später noch einmal machen.

| Präfix | Maske | Blockgröße (im relevanten Oktett) | Nutzbare Hosts |
|-------:|-------|:---------------------------------:|---------------:|
| /24 | 255.255.255.0   | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64  | 62  |
| /27 | 255.255.255.224 | 32  | 30  |
| /28 | 255.255.255.240 | 16  | 14  |
| /29 | 255.255.255.248 | 8   | 6   |
| /30 | 255.255.255.252 | 4   | 2   |
| /31 | 255.255.255.254 | 2   | 2 (Punkt-zu-Punkt, RFC 3021) |

Methode: Blockgröße = 256 − Maskenoktett; Netz = größtes Vielfaches der
Blockgröße ≤ Adressoktett; Broadcast = nächstes Netz − 1.

## Nachweise

- Foto oder Scan der handschriftlichen Rechnung für die Übungen 1–8 und meine Zeit.
- Punktzahl pro Versuch (z. B. `attempt 1: 14/18 in 22 min`).

## Was ich gelernt habe

_Noch von Lucas auszufüllen._
