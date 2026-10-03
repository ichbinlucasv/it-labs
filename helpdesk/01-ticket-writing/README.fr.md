# Lab 01 — Écrire des tickets utiles

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — réécritures, exercice de priorité, notes d'escalade et de clôture dans [`my-rewrites.md`](my-rewrites.md), y compris des tickets tirés de mes propres preuves du lab Linux ; faits en Markdown, pas encore dans un outil ITSM comme GLPI.

## Objectif

Je m'entraîne à écrire des tickets qu'un autre technicien peut reprendre sans
poser de questions : résumé clair, impact, étapes pour reproduire, ce qui a
déjà été tenté, et une prochaine action. Un bon ticket réduit le temps de
résolution. Il sert aussi de preuve pendant les audits et les revues
d'incident (Security+ D4 — documentation des incidents et des changements).

## Mise en place

- N'importe quel outil ITSM, ou du Markdown simple. Outil prévu :
  [GLPI](https://glpi-project.org/), libre et auto-hébergé (très utilisé en
  France). Les modèles de ce dossier sont du Markdown simple.
- Organisation fictive : *Exemple SARL*, 40 utilisateurs, portables Windows 11,
  Microsoft 365, un serveur de fichiers Linux.

## Étapes

1. Lire le modèle dans [`template.md`](template.md).
2. Comparer les mauvais et les bons exemples dans [`examples.md`](examples.md)
   et noter ce qui rend chaque bon ticket exploitable.
3. Réécrire chaque mauvais ticket moi-même, avant de lire la version améliorée.
4. Écrire une note d'escalade (L1 → L2) et une note de clôture pour un ticket.
5. Classer chaque ticket par **impact** et par **urgence**, pour en tirer une
   priorité avec la matrice ci-dessous.

| Impact \ Urgence | Haute | Moyenne | Faible |
|------------------|-------|---------|--------|
| **Élevé** (beaucoup d'utilisateurs / l'activité est arrêtée) | P1 | P2 | P3 |
| **Moyen** (une équipe ou un VIP dégradé) | P2 | P3 | P4 |
| **Faible** (un seul utilisateur, un contournement existe) | P3 | P4 | P4 |

## Preuves

- [`my-rewrites.md`](my-rewrites.md) : mes réécritures des trois mauvais
  tickets (comparées aux versions de référence), le tableau de priorité, trois
  tickets écrits à partir de vraies sorties de dépannage du
  [lab 03](../03-linux-troubleshooting/), une escalade L1 → L2 et une note de clôture.
- Pas fait : capture d'écran d'un ticket dans GLPI. Le modèle marche dans
  n'importe quel outil, mais je n'ai pas encore installé GLPI.

## Ce que j'ai appris

- Un ticket qui note seulement l'action (« reset fait ») ne sert plus après.
  Un ticket utile note la preuve et la cause. La personne suivante ne repart
  pas de zéro.
- « Qu'est-ce qui a changé ? » (nouveau dock, changement de config récent)
  est la question qui mène le plus souvent à la cause.
- Écrire des tickets à partir de mes propres sorties de lab était bien plus
  simple que les inventer. Les commandes exactes et les messages d'erreur
  rendent le ticket exploitable.
- La matrice de priorité donne une base. L'impact sécurité peut justifier de
  la monter, et la raison va dans le ticket.
- Une note d'escalade doit dire ce que j'ai fait, ce que je pense, et ce
  qu'il me faut. Pas seulement « ça ne marche pas, regardez ».
