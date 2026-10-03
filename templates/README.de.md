# Vorlagen für den Alltag

[English](README.md) · [Français](README.fr.md) · **Deutsch**

Die Formulare neben jeder Datei sind `.fr.md` und `.de.md`.

Ich kopiere eine Datei, fülle die Lücken und behalte die Kopie in meinen
Notizen. Die Lücken bleiben in git leer.

Ich öffne nicht jeden Tag alle. Ein nützlicher Tag ist ein Helpdesk- oder
SOC-Blatt, plus **ein** Sprachblock. Die Sprachenliste ist lang, damit ich
eine Sprache nicht sechs Monate liegen lasse. Es ist keine Liste, die ich
vor dem Frühstück fertig mache.

## Heute Morgen

1. [career/daily.md](career/daily.md) kopieren.
2. Die Spalte für heute nehmen.
3. Aufhören, wenn der Timer endet. Eine Zeile schreiben zu dem, was ich aus
   dem Gedächtnis nicht konnte.

| Tag | Beruf üben | Sprache (25 Min.) |
| --- | --- | --- |
| Mo | [Helpdesk-Ticket](helpdesk/ticket.md) | [bash](languages/bash.md) |
| Di | [Anmeldung geht nicht](helpdesk/cant-log-on.md) oder [Passwort zurücksetzen](helpdesk/password-reset.md) | [PowerShell](languages/powershell.md) |
| Mi | [Alert-Triage](soc/alert-triage.md) | [Python](languages/python.md) |
| Do | [Zeitstrahl](soc/timeline.md) zu einem alten Alert | [Rust](languages/rust.md) oder [C](languages/c.md), abwechselnde Wochen |
| Fr | [Wochenrückblick](career/weekly.md) | Eine von [C++](languages/cpp.md), [C#](languages/csharp.md), [Java](languages/java.md), [Kotlin](languages/kotlin.md), [Haskell](languages/haskell.md). Ich wechsle. Nicht alle fünf. |
| Sa | Labor, wenn die Gäste an sind. [Lab 06](../helpdesk/06-windows-domain/) oder ein Linux-Break/Fix. | Nur wenn die Sprache von Freitag noch unklar ist. |
| So | Frei, oder [Geschichte fürs Gespräch](career/story.md) aus einer echten Labornotiz. | Frei. |

## Helpdesk

Die lange Form des Tickets steht schon in
[helpdesk/01-ticket-writing/template.md](../helpdesk/01-ticket-writing/template.md).
Das hier sind die, die ich in der Schicht will.

| Formular | Wann ich es nutze |
| --- | --- |
| [ticket.md](helpdesk/ticket.md) | Jede neue Anfrage |
| [ticket.fr.md](helpdesk/ticket.fr.md) | Dasselbe Ticket auf Französisch, für einen Desk in Frankreich |
| [shift-start.md](helpdesk/shift-start.md) | Die ersten 15 Minuten |
| [cant-log-on.md](helpdesk/cant-log-on.md) | „Ich komme nicht rein“ |
| [password-reset.md](helpdesk/password-reset.md) | Zurücksetzen oder entsperren. Prüfen, wer fragt. |
| [new-user.md](helpdesk/new-user.md) | Neue Person |
| [leaver.md](helpdesk/leaver.md) | Jemand ist gegangen |
| [escalation.md](helpdesk/escalation.md) | Ich hänge fest und gebe es weiter |
| [remote-session.md](helpdesk/remote-session.md) | Ich bin auf dem Bildschirm der Person |
| [kb.md](helpdesk/kb.md) | Dieselbe Lösung kam zweimal |

## SOC

| Formular | Wann ich es nutze |
| --- | --- |
| [shift-handover.md](soc/shift-handover.md) | Ich übernehme die Warteschlange, oder ich gebe sie ab |
| [alert-triage.md](soc/alert-triage.md) | Ein Alert. Nicht fünf Werkzeuge. |
| [timeline.md](soc/timeline.md) | Zeiten in UTC, das älteste zuerst |
| [ioc-note.md](soc/ioc-note.md) | Etwas zum Nachsehen, entschärft |
| [detection-idea.md](soc/detection-idea.md) | Wofür ich einen Alert will, und was Rauschen wäre |
| [end-of-shift.md](soc/end-of-shift.md) | Was noch offen ist |

## Karriere

| Formular | Wann ich es nutze |
| --- | --- |
| [daily.md](career/daily.md) | Jeder Lerntag |
| [weekly.md](career/weekly.md) | Freitag |
| [story.md](career/story.md) | Eine echte Geschichte für ein Vorstellungsgespräch. Erst nachdem ich die Arbeit gemacht habe. |
| [practice-note.de.md](career/practice-note.de.md) | Eine Übung auf TryHackMe, HTB, Boot.dev, Kali oder BlackArch. Nur die Notiz der Verteidigung. |
| [helpdesk-session.de.md](career/helpdesk-session.de.md) | Eine echte Sitzung auf win11-soc mit dem Helpdesk-Konto. Leer, bis ich sie laufen lasse. |
| [domain-join.de.md](career/domain-join.de.md) | Schriftlicher Nachweis, dass der Windows-11-Gast lab.local beigetreten ist. Leer, bis ich ihn laufen lasse. |
| [lab-ticket.de.md](career/lab-ticket.de.md) | Ein echtes Ticket aus diesem Lab. Leer, bis die Arbeit passiert ist. |
| [application.de.md](career/application.de.md) | Der kurze Text für eine Alternance oder ein POEI. Ich schicke ihn selbst. |

## Regeln, die ich immer wieder breche

- Keine Passwörter, keine Cookies und keine Kundennamen in einer Notiz, die
  ich vielleicht in git einfüge.
- Den Fehler zitieren. Nicht „es ist fehlgeschlagen“ schreiben.
- Eine Änderung, dann prüfen. Danach die nächste Änderung.
- Wenn ich ein Werkzeug nur installiert habe, steht in der Notiz:
  installiert. Sie sagt nicht, dass ich es kann.
- UTC in SOC-Notizen. Ortszeit geht auf einem Helpdesk-Ticket, wenn ich die
  Zone dazuschreibe.
- Eine Übungsnotiz hat keine Flags und keine Angriffsschritte. Sie sagt,
  was ich prüfen würde.
