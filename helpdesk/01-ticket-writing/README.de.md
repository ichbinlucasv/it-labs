# Lab 01 — Nützliche Tickets schreiben

[English](README.md) · **Deutsch**

**Status:** Done — Überarbeitungen, Priorisierungsübung, Eskalations- und Abschlussnotizen in [`my-rewrites.md`](my-rewrites.md) (Englisch), darunter Tickets auf Basis meiner eigenen Nachweise aus dem Linux-Lab; in Markdown erstellt, noch nicht in einem ITSM-Tool wie GLPI.

## Ziel

Tickets so schreiben, dass ein anderer Techniker sie ohne Rückfragen
übernehmen kann: klare Zusammenfassung, Auswirkung, Schritte zur
Reproduktion, bereits Versuchtes und eine nächste Aktion. Gute Tickets
verkürzen die Lösungszeit und dienen bei Audits und Incident-Reviews als
Nachweis (Security+ D4 — Dokumentation von Incidents und Changes).

## Aufbau

- Ein beliebiges ITSM-Tool oder reines Markdown. Geplantes Tool: das freie,
  selbst gehostete [GLPI](https://glpi-project.org/) (in Frankreich weit
  verbreitet); die Vorlagen in diesem Ordner sind reines Markdown.
- Fiktive Organisation: *Exemple SARL*, 40 Benutzer, Windows-11-Laptops,
  Microsoft 365, ein Linux-Fileserver.

## Schritte

1. Die Vorlage in [`template.md`](template.md) lesen.
2. Die schlechten und guten Beispiele in [`examples.md`](examples.md)
   vergleichen und notieren, was ein „gutes“ Ticket umsetzbar macht.
3. Jedes „schlechte“ Ticket selbst neu schreiben, bevor man die verbesserte Fassung liest.
4. Für ein Ticket eine Eskalationsnotiz (L1 → L2) und eine Abschlussnotiz schreiben.
5. Jedes Ticket nach **Auswirkung** und **Dringlichkeit** einstufen und
   daraus mit der Matrix unten die Priorität ableiten.

| Auswirkung \ Dringlichkeit | Hoch | Mittel | Niedrig |
|----------------------------|------|--------|---------|
| **Hoch** (viele Benutzer / Betrieb steht) | P1 | P2 | P3 |
| **Mittel** (Team oder VIP beeinträchtigt) | P2 | P3 | P4 |
| **Niedrig** (ein Benutzer, Workaround vorhanden) | P3 | P4 | P4 |

## Nachweise

- [`my-rewrites.md`](my-rewrites.md): meine Überarbeitungen der drei
  schlechten Tickets (verglichen mit den Referenzfassungen), die
  Prioritätentabelle, drei Tickets auf Basis echter Ausgaben aus
  [Lab 03](../03-linux-troubleshooting/README.de.md), eine Eskalation L1 → L2
  und eine Abschlussnotiz.
- Nicht erledigt: Screenshot eines Tickets in GLPI — die Vorlage funktioniert
  in jedem Tool, aber GLPI habe ich noch nicht installiert.

## Was ich gelernt habe

- Ein Ticket, das nur die Aktion festhält („Reset erledigt“), ist später
  nutzlos; ein brauchbares Ticket hält Befunde und Ursache fest, damit die
  nächste Person nicht von vorne anfängt.
- „Was hat sich geändert?“ (neue Dockingstation, kürzliche
  Konfigurationsänderung) ist die Frage, die am häufigsten zur Ursache führt.
- Tickets aus meinen eigenen Lab-Ausgaben zu schreiben war viel einfacher, als
  sie zu erfinden: Exakte Befehle und Fehlermeldungen machen ein Ticket umsetzbar.
- Die Prioritätenmatrix liefert einen Standardwert; ein Sicherheitsaspekt
  kann eine höhere Priorität rechtfertigen, und die Begründung gehört ins Ticket.
- Eine Eskalationsnotiz sollte sagen, was ich getan habe, was ich vermute und
  was ich brauche — nicht nur „geht nicht, bitte prüfen“.
