# Corrigé

[English](answer-key.md) · **Français** · [Deutsch](answer-key.de.md)

Calculé et vérifié avec le module `ipaddress` de Python.

## Partie A

| # | Adresse | Réseau | Masque | Diffusion | Premier hôte | Dernier hôte | Hôtes utilisables |
|---|---------|--------|--------|-----------|--------------|--------------|-------------------|
| 1 | `192.168.10.77/26` | 192.168.10.64/26 | 255.255.255.192 | 192.168.10.127 | 192.168.10.65 | 192.168.10.126 | 62 |
| 2 | `10.4.200.9/20` | 10.4.192.0/20 | 255.255.240.0 | 10.4.207.255 | 10.4.192.1 | 10.4.207.254 | 4094 |
| 3 | `172.16.35.130/27` | 172.16.35.128/27 | 255.255.255.224 | 172.16.35.159 | 172.16.35.129 | 172.16.35.158 | 30 |
| 4 | `198.51.100.200/29` | 198.51.100.200/29 | 255.255.255.248 | 198.51.100.207 | 198.51.100.201 | 198.51.100.206 | 6 |
| 5 | `10.0.0.255/23` | 10.0.0.0/23 | 255.255.254.0 | 10.0.1.255 | 10.0.0.1 | 10.0.1.254 | 510 |
| 6 | `203.0.113.66/30` | 203.0.113.64/30 | 255.255.255.252 | 203.0.113.67 | 203.0.113.65 | 203.0.113.66 | 2 |
| 7 | `172.20.99.1/18` | 172.20.64.0/18 | 255.255.192.0 | 172.20.127.255 | 172.20.64.1 | 172.20.127.254 | 16382 |
| 8 | `192.0.2.143/28` | 192.0.2.128/28 | 255.255.255.240 | 192.0.2.143 | 192.0.2.129 | 192.0.2.142 | 14 |

Notes :
- **Q4 :** l'adresse donnée est elle-même l'adresse réseau (200 est un multiple de 8) — pas attribuable.
- **Q5 :** `10.0.0.255` ressemble à une diffusion, mais dans un /23 c'est une adresse d'hôte normale.
- **Q8 :** `192.0.2.143` est l'adresse de **diffusion** de son /28 — elle ne peut pas être attribuée à un hôte.

## Partie B

9.  **Oui** — les deux dans `10.1.1.128/25`.
10. **Non** — `192.168.5.14` est dans `192.168.5.0/28` (hôtes .1–.14) ; `.17` est dans `192.168.5.16/28`.
11. **Oui** — les deux dans `172.16.4.0/22` (172.16.4.0 – 172.16.7.255).

## Partie C — Plan VLSM pour 10.50.0.0/22

| Segment | Hôtes nécessaires | Préfixe | Réseau | Plage utilisable | Diffusion | Hôtes en réserve |
|---|---:|---|---|---|---|---:|
| Postes de travail | 300 | /23 | 10.50.0.0/23 | 10.50.0.1 – 10.50.1.254 | 10.50.1.255 | 210 |
| Invités Wi-Fi | 120 | /25 | 10.50.2.0/25 | 10.50.2.1 – 10.50.2.126 | 10.50.2.127 | 6 |
| Serveurs | 50 | /26 | 10.50.2.128/26 | 10.50.2.129 – 10.50.2.190 | 10.50.2.191 | 12 |
| Imprimantes | 20 | /27 | 10.50.2.192/27 | 10.50.2.193 – 10.50.2.222 | 10.50.2.223 | 10 |
| Administration | 10 | /28 | 10.50.2.224/28 | 10.50.2.225 – 10.50.2.238 | 10.50.2.239 | 4 |
| Lien WAN | 2 | /30 | 10.50.2.240/30 | 10.50.2.241 – 10.50.2.242 | 10.50.2.243 | 0 |

Première adresse libre : **10.50.2.244** (tout le `10.50.3.0/24` est encore libre aussi).
En production je laisserais de la marge (par exemple un /24 pour les invités).

## Partie D

13. `10.8.0.0/22`
14. **256** (2^(24−16)).
15. **/23** — 510 hôtes utilisables, donc 10 adresses d'hôtes inutilisées (512 au total − 2 − 500).
16. **APIPA / lien-local** (`169.254.0.0/16`) : le client n'a pas eu de réponse DHCP —
    vérifier câble/Wi-Fi, VLAN, serveur DHCP / épuisement de l'étendue, relais DHCP.
17. Privées : `172.31.255.1`, `192.168.0.1`, `10.255.0.1`.
    Pas RFC 1918 : `172.32.1.1` (publique ; 172.16.0.0/12 s'arrête à 172.31.255.255),
    `100.64.0.1` (espace d'adresses partagé RFC 6598, utilisé pour le NAT opérateur).
18. Elles sont réservées à la documentation (RFC 5737) et jamais routées sur
    Internet, donc un exemple ne peut pas viser une vraie organisation par accident.
