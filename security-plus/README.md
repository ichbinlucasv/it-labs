# CompTIA Security+ (SY0-701) study notes & flashcards

## Goal

Prepare for **CompTIA Security+ SY0-701** with concise notes written in my
own words, organised by the five exam domains, plus a flashcard deck I can
import into Anki. Each note links theory to the hands-on labs in this repo.

## Setup

- Official exam objectives (download from CompTIA's SY0-701 page) — the
  source of truth for the topic list.
- Exam facts (check CompTIA for current details): up to 90 questions
  (multiple choice + performance-based), 90 minutes, passing score 750 on a
  100–900 scale.
- Domain weights: D1 12 %, D2 22 %, D3 18 %, D4 28 %, D5 20 %.

| Domain | Notes | Related labs |
|--------|-------|--------------|
| 1 General Security Concepts | [notes/1-general-security-concepts.md](notes/1-general-security-concepts.md) | [Samba AD](../helpdesk/04-samba-ad-lab/), [fim](../rust/), [hashcheck](../python/) |
| 2 Threats, Vulnerabilities & Mitigations | [notes/2-threats-vulnerabilities-mitigations.md](notes/2-threats-vulnerabilities-mitigations.md) | [Sysmon/auditd](../soc-analyst/02-sysmon-auditd-logs/), [ATT&CK](../soc-analyst/04-attack-mapping/), [nftables](../networking/03-nftables-firewall/) |
| 3 Security Architecture | [notes/3-security-architecture.md](notes/3-security-architecture.md) | [Subnetting](../networking/01-subnetting/), [M365](../helpdesk/05-m365-basics/) |
| 4 Security Operations | [notes/4-security-operations.md](notes/4-security-operations.md) | [Wazuh](../soc-analyst/01-wazuh-homelab/), [Sigma](../soc-analyst/05-sigma-rules/), [IR write-ups](../soc-analyst/03-incident-writeups/) |
| 5 Security Program Management & Oversight | [notes/5-security-program-management.md](notes/5-security-program-management.md) | [Ticket writing](../helpdesk/01-ticket-writing/), [IR reports](../soc-analyst/03-incident-writeups/) |

## Steps

1. Read one domain note per week; add my own examples from the labs.
2. Review [`flashcards.csv`](flashcards.csv) daily (columns: `front,back,domain`).
   Import into Anki: *File → Import*, field separator comma, "Allow HTML" off,
   map column 3 to a tag.
3. Take practice exams; add a flashcard for every question I get wrong.
4. Re-read the official objectives before the exam and tick off each item.

Check the CSV parses:

```bash
python3 -c "import csv;r=list(csv.DictReader(open('flashcards.csv',newline='',encoding='utf-8')));print(len(r),'cards');assert all(c['domain'] in {'1','2','3','4','5'} for c in r)"
```

## Evidence

- Practice-exam scores over time (table in `progress.md`).
- Exam result / certificate once passed.

## What I learned

_To be completed by Lucas._
