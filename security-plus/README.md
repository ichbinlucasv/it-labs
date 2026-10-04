# CompTIA Security+ study notes & flashcards

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**Status:** In progress — the notes and a 99-card CSV were written for SY0-701. The exam I will sit is SY0-801. I have not taken it. This lab is Done only when I pass SY0-801.

## Goal

The exam I will study is **CompTIA Security+ SY0-801**. CompTIA is
replacing SY0-701 with that version. The notes and flashcards already
in this folder follow the SY0-701 objectives, in my own words, by the
five domains, plus a deck I can import into Anki. I will read the
SY0-801 objectives and update these notes as I study. I have not booked
the exam. Each note links theory to the hands-on labs in this repo.
The five notes are also in French and German. The CSV stays one English
deck so Anki does not split into three files.

## Setup

- Official SY0-801 objectives, from CompTIA, are the list I will study.
  The notes below were written against the SY0-701 list.
- SY0-701 facts I already wrote down (I will check the SY0-801 page
  before I book): up to 90 questions (multiple choice and
  performance-based), 90 minutes, passing score 750 on a 100–900 scale.
- SY0-701 domain weights used for these notes: D1 12 %, D2 22 %, D3 18 %,
  D4 28 %, D5 20 %.

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
