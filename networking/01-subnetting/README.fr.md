# Lab 01 — Exercices de sous-réseaux

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — exercices et corrigé écrits ; chaque réponse a été calculée et vérifiée avec `ipaddress` de Python.

## Objectif

Être rapide et juste en subnetting IPv4 : trouver les adresses réseau et de
diffusion, les plages d'hôtes, faire un plan VLSM et agréger des routes.
Utile pour le tri réseau au helpdesk, les règles de pare-feu et les requêtes
SIEM sur des plages d'IP (Security+ D3 — segmentation réseau).

## Mise en place

- D'abord papier et crayon, puis vérification avec `ipcalc`
  (`sudo apt install ipcalc`) ou le module `ipaddress` de Python :

```python
import ipaddress
n = ipaddress.ip_interface("192.168.10.77/26").network
print(n, n.netmask, n.broadcast_address, n.num_addresses - 2)
```

## Étapes

1. Retenir le tableau des « nombres magiques » ci-dessous.
2. Faire [`exercises.md`](exercises.md) sans outil, en me chronométrant.
3. Vérifier avec [`answer-key.md`](answer-key.md) (les réponses ont été
   produites et revérifiées avec `ipaddress` de Python).
4. Refaire quelques jours plus tard celles que j'ai ratées.

| Préfixe | Masque | Taille de bloc (dans l'octet qui compte) | Hôtes utilisables |
|--------:|--------|:----------------------------------------:|------------------:|
| /24 | 255.255.255.0   | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64  | 62  |
| /27 | 255.255.255.224 | 32  | 30  |
| /28 | 255.255.255.240 | 16  | 14  |
| /29 | 255.255.255.248 | 8   | 6   |
| /30 | 255.255.255.252 | 4   | 2   |
| /31 | 255.255.255.254 | 2   | 2 (point à point, RFC 3021) |

Méthode : taille de bloc = 256 − octet du masque ; réseau = plus grand
multiple de la taille de bloc ≤ l'octet de l'adresse ; diffusion = réseau
suivant − 1.

## Preuves

- Photo ou scan du brouillon manuscrit pour les exercices 1 à 8, et mon temps.
- Score par essai (par exemple `attempt 1: 14/18 in 22 min`).

## Ce que j'ai appris

_À compléter par Lucas._
