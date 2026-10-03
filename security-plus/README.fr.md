# Notes et cartes CompTIA Security+ (SY0-701)

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** In progress — les notes et un CSV de 99 cartes (il se lit sans erreur) sont écrits ; je continue de préparer l'examen et je ne l'ai pas encore passé (ce lab n'est « Done » que le jour où je réussis le SY0-701).

## Objectif

Préparer le **CompTIA Security+ SY0-701** avec des notes courtes, écrites
avec mes mots, rangées selon les cinq domaines de l'examen, plus un paquet
de cartes que je peux importer dans Anki. Chaque note relie la théorie aux
labs pratiques de ce dépôt.
Les cinq notes existent aussi en français et en allemand. Le CSV reste un
seul paquet en anglais, pour ne pas couper Anki en trois fichiers.

## Mise en place

- Objectifs officiels de l'examen (à télécharger sur la page SY0-701 de
  CompTIA) — la référence pour la liste des sujets.
- Faits d'examen (vérifier le détail à jour chez CompTIA) : jusqu'à 90
  questions (QCM + performance-based), 90 minutes, note de passage 750 sur
  une échelle de 100 à 900.
- Poids des domaines : D1 12 %, D2 22 %, D3 18 %, D4 28 %, D5 20 %.

| Domaine | Notes | Labs liés |
|---------|-------|-----------|
| 1 Concepts généraux de sécurité | [notes/1-general-security-concepts.md](notes/1-general-security-concepts.md) | [Samba AD](../helpdesk/04-samba-ad-lab/), [fim](../rust/), [hashcheck](../python/) |
| 2 Menaces, vulnérabilités et mesures d'atténuation | [notes/2-threats-vulnerabilities-mitigations.md](notes/2-threats-vulnerabilities-mitigations.md) | [Sysmon/auditd](../soc-analyst/02-sysmon-auditd-logs/), [ATT&CK](../soc-analyst/04-attack-mapping/), [nftables](../networking/03-nftables-firewall/) |
| 3 Architecture de sécurité | [notes/3-security-architecture.md](notes/3-security-architecture.md) | [Subnetting](../networking/01-subnetting/), [M365](../helpdesk/05-m365-basics/) |
| 4 Opérations de sécurité | [notes/4-security-operations.md](notes/4-security-operations.md) | [Wazuh](../soc-analyst/01-wazuh-homelab/), [Sigma](../soc-analyst/05-sigma-rules/), [IR write-ups](../soc-analyst/03-incident-writeups/) |
| 5 Gestion et supervision du programme de sécurité | [notes/5-security-program-management.md](notes/5-security-program-management.md) | [Ticket writing](../helpdesk/01-ticket-writing/), [IR reports](../soc-analyst/03-incident-writeups/) |

## Étapes

1. Lire une note de domaine par semaine ; ajouter mes propres exemples tirés des labs.
2. Revoir [`flashcards.csv`](flashcards.csv) tous les jours (colonnes : `front,back,domain`).
   Import dans Anki : *File → Import*, séparateur de champ virgule, « Allow HTML » désactivé,
   associer la colonne 3 à un tag.
3. Faire des examens blancs ; ajouter une carte pour chaque question que je rate.
4. Relire les objectifs officiels avant l'examen et cocher chaque point.

Vérifier que le CSV se parse :

```bash
python3 -c "import csv;r=list(csv.DictReader(open('flashcards.csv',newline='',encoding='utf-8')));print(len(r),'cards');assert all(c['domain'] in {'1','2','3','4','5'} for c in r)"
```

## Preuves

- Notes des examens blancs dans le temps (tableau dans `progress.md`).
- Résultat d'examen / certificat une fois que je l'ai eu.

## Ce que j'ai appris

_À compléter par Lucas._
