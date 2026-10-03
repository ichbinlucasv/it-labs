# Exercices de sous-réseaux

[English](exercises.md) · **Français** · [Deutsch](exercises.de.md)

## Partie A — Faits réseau

Pour chaque adresse, donner : adresse réseau, masque de sous-réseau, adresse
de diffusion, premier hôte utilisable, dernier hôte utilisable, nombre
d'hôtes utilisables.

1. `192.168.10.77/26`
2. `10.4.200.9/20`
3. `172.16.35.130/27`
4. `198.51.100.200/29`
5. `10.0.0.255/23`
6. `203.0.113.66/30`
7. `172.20.99.1/18`
8. `192.0.2.143/28` — cette adresse peut-elle être attribuée à un hôte ?

## Partie B — Même sous-réseau ?

Ces deux hôtes peuvent-ils se parler directement (même sous-réseau) sans routeur ?

9.  `10.1.1.130/25` et `10.1.1.200/25`
10. `192.168.5.14/28` et `192.168.5.17/28`
11. `172.16.4.1/22` et `172.16.7.254/22`

## Partie C — Plan VLSM

12. Exemple SARL a reçu `10.50.0.0/22`. Allouer des sous-réseaux, **du plus
    grand au plus petit**, contigus depuis le début du bloc, avec le plus
    petit préfixe qui suffit :

| Segment | Hôtes nécessaires |
|---------|------------------:|
| Postes de travail | 300 |
| Invités Wi-Fi | 120 |
| Serveurs | 50 |
| Imprimantes | 20 |
| Administration | 10 |
| Lien WAN (routeur à routeur) | 2 |

    Ensuite : quelle est la première adresse libre qui reste dans le /22 ?

## Partie D — Agrégation et dimensionnement

13. Agréger `10.8.0.0/24`, `10.8.1.0/24`, `10.8.2.0/24`, `10.8.3.0/24` en
    une seule route.
14. Combien de sous-réseaux /24 tiennent dans `172.16.0.0/16` ?
15. Quel préfixe faut-il pour exactement 500 hôtes ? Combien d'adresses sont perdues ?
16. Un utilisateur a l'IP `169.254.12.7`. Qu'est-ce que ça veut dire ?
17. Lesquelles sont privées (RFC 1918) ? `172.32.1.1`, `172.31.255.1`,
    `192.168.0.1`, `10.255.0.1`, `100.64.0.1`
18. Pourquoi les plages RFC 5737 (`192.0.2.0/24`, `198.51.100.0/24`,
    `203.0.113.0/24`) apparaissent-elles dans la documentation ?
