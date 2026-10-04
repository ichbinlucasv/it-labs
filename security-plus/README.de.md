# Lernnotizen und Karteikarten CompTIA Security+

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** In progress — die Notizen und ein CSV mit 99 Karten sind für SY0-701 geschrieben. Die Prüfung, die ich ablege, ist SY0-801. Abgelegt habe ich sie nicht. Dieses Lab ist erst Done, wenn ich SY0-801 bestehe.

## Ziel

Die Prüfung, die ich lernen werde, ist **CompTIA Security+ SY0-801**.
CompTIA ersetzt SY0-701 durch diese Version. Die Notizen und Karten in
diesem Ordner folgen den SY0-701-Zielen, in meinen eigenen Worten, nach
den fünf Domänen, plus ein Stapel, den ich in Anki importieren kann.
Die SY0-801-Ziele lese ich und diese Notizen passe ich an, während ich
lerne. Gebucht habe ich die Prüfung nicht. Jede Notiz verbindet die
Theorie mit den praktischen Labs in diesem Repo.
Die fünf Notizen gibt es auch auf Französisch und Deutsch. Die CSV bleibt
ein englisches Deck, damit Anki nicht in drei Dateien zerfällt.

## Aufbau

- Die offiziellen SY0-801-Ziele bei CompTIA sind die Liste, die ich
  lernen werde. Die Notizen unten sind gegen die SY0-701-Liste geschrieben.
- SY0-701-Fakten, die ich schon notiert hatte (die SY0-801-Seite prüfe
  ich vor der Buchung): bis zu 90 Fragen (Multiple Choice und
  Performance-Based), 90 Minuten, Bestehensgrenze 750 auf einer Skala
  von 100–900.
- SY0-701-Gewichte für diese Notizen: D1 12 %, D2 22 %, D3 18 %,
  D4 28 %, D5 20 %.

| Domäne | Notizen | Verwandte Labs |
|--------|---------|----------------|
| 1 Allgemeine Sicherheitskonzepte | [notes/1-general-security-concepts.md](notes/1-general-security-concepts.md) | [Samba AD](../helpdesk/04-samba-ad-lab/), [fim](../rust/), [hashcheck](../python/) |
| 2 Bedrohungen, Schwachstellen und Gegenmaßnahmen | [notes/2-threats-vulnerabilities-mitigations.md](notes/2-threats-vulnerabilities-mitigations.md) | [Sysmon/auditd](../soc-analyst/02-sysmon-auditd-logs/), [ATT&CK](../soc-analyst/04-attack-mapping/), [nftables](../networking/03-nftables-firewall/) |
| 3 Sicherheitsarchitektur | [notes/3-security-architecture.md](notes/3-security-architecture.md) | [Subnetting](../networking/01-subnetting/), [M365](../helpdesk/05-m365-basics/) |
| 4 Sicherheitsbetrieb | [notes/4-security-operations.md](notes/4-security-operations.md) | [Wazuh](../soc-analyst/01-wazuh-homelab/), [Sigma](../soc-analyst/05-sigma-rules/), [IR write-ups](../soc-analyst/03-incident-writeups/) |
| 5 Management und Aufsicht des Sicherheitsprogramms | [notes/5-security-program-management.md](notes/5-security-program-management.md) | [Ticket writing](../helpdesk/01-ticket-writing/), [IR reports](../soc-analyst/03-incident-writeups/) |

## Schritte

1. Pro Woche eine Domänennotiz lesen; eigene Beispiele aus den Labs ergänzen.
2. [`flashcards.csv`](flashcards.csv) täglich wiederholen (Spalten: `front,back,domain`).
   Import in Anki: *File → Import*, Feldtrenner Komma, „Allow HTML“ aus,
   Spalte 3 einem Tag zuordnen.
3. Übungsprüfungen machen; für jede Frage, die ich falsch habe, eine Karte anlegen.
4. Die offiziellen Ziele vor der Prüfung noch einmal lesen und jeden Punkt abhaken.

Prüfen, dass das CSV parst:

```bash
python3 -c "import csv;r=list(csv.DictReader(open('flashcards.csv',newline='',encoding='utf-8')));print(len(r),'cards');assert all(c['domain'] in {'1','2','3','4','5'} for c in r)"
```

## Nachweise

- Ergebnisse der Übungsprüfungen über die Zeit (Tabelle in `progress.md`).
- Prüfungsergebnis / Zertifikat, sobald ich bestanden habe.

## Was ich gelernt habe

_Von Lucas noch zu ergänzen._
