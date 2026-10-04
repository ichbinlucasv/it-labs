# Notes et cartes CompTIA Security+

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** In progress — les notes et un CSV de 99 cartes ont été écrits pour le SY0-701. L'examen que je passerai est le SY0-801. Je ne l'ai pas passé. Ce lab n'est Done que le jour où je réussis le SY0-801.

## Objectif

L'examen que je vais étudier est le **CompTIA Security+ SY0-801**.
CompTIA remplace le SY0-701 par cette version. Les notes et les cartes
déjà dans ce dossier suivent les objectifs du SY0-701, avec mes mots,
par les cinq domaines, plus un paquet que je peux importer dans Anki.
Je lirai les objectifs du SY0-801 et je mettrai ces notes à jour en
étudiant. Je n'ai pas réservé l'examen. Chaque note relie la théorie
aux labs pratiques de ce dépôt.
Les cinq notes existent aussi en français et en allemand. Le CSV reste un
seul paquet en anglais, pour ne pas couper Anki en trois fichiers.

## Mise en place

- Les objectifs officiels du SY0-801, chez CompTIA, sont la liste que je
  vais étudier. Les notes ci-dessous ont été écrites sur la liste SY0-701.
- Faits du SY0-701 que j'avais déjà notés (je vérifierai la page SY0-801
  avant de réserver) : jusqu'à 90 questions (QCM et performance-based),
  90 minutes, note de passage 750 sur une échelle de 100 à 900.
- Poids des domaines SY0-701 utilisés pour ces notes : D1 12 %, D2 22 %,
  D3 18 %, D4 28 %, D5 20 %.

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
