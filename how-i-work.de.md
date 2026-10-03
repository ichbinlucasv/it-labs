# Wie ich arbeite

[English](how-i-work.md) · [Français](how-i-work.fr.md) · **Deutsch**

Diese Seite ist für jemanden, der das Repo öffnet und sehen will, was
ich wirklich benutze. Die Labs sind der Nachweis. Diese Seite ist der
Rahmen.

## Alltagsrechner

Ich benutze CachyOS jeden Tag. CachyOS ist Arch Linux, mit eigenem
Kernel und eigenen Paketquellen. Ich habe es installiert, ich
aktualisiere es, und ich repariere es selbst. Die Platte ist
verschlüsselt.

Das Windows-Lab läuft auf demselben Rechner. libvirt stellt einen
Windows Server 2025 Evaluation Domain Controller bereit (`dc01`,
Domäne `lab.local`) und einen Windows 11 Evaluation Client
(`win11-soc`). Beschreibung:
[helpdesk/06-windows-domain](helpdesk/06-windows-domain/).

Ein zweites Identitäts-Lab ist Samba AD in einem Debian-Container
(`corp.example.com`). Dieses Lab steht für sich. Die Windows-Gäste
sind dort nicht eingebunden. Beschreibung:
[helpdesk/04-samba-ad-lab](helpdesk/04-samba-ad-lab/).

Ich habe ausserdem Kali- und BlackArch-Gäste auf diesem Rechner. Wenn
ich Zeit habe, mache ich dort kurze Übungen, und auf den
Windows-Gästen, und ich werde langsam besser. Was ich davon
veröffentliche, ist die Seite der Verteidigung: welches Log ich lesen
würde, welche Prüfung ich starte, welche Kontrolle geholfen hätte.
Flags und Angriffsschritte bleiben aus diesem Repo. Die leere Notiz ist
[templates/career/practice-note.de.md](templates/career/practice-note.de.md).

Auf dem Host benutze ich ausserdem git, neovim, rustup, Python,
Wireshark und Podman ohne Root. Der Befehl `docker` auf diesem Rechner
ist Podman. Lab-Passwörter bleiben in einem Passwortmanager. Sie
liegen nicht in diesem Repo.

## Sprachen

| Sprache | Wie ich sie benutze |
|---------|---------------------|
| bash | Jeden Tag auf CachyOS, und im Linux-Fehleranalyse-Lab |
| PowerShell | Im Windows-Domänen-Lab, und in den Übungen |
| Python | Die `seclab`-Werkzeuge in diesem Repo, mit pytest |
| Rust | `log-analyzer` und `fim` hier. Zwei weitere öffentliche Repos: [Frihart](https://codeberg.org/ichbinlucasv/Frihart) und [HashChat](https://codeberg.org/ichbinlucasv/HashChat) |
| C | Lernen, und kurze Übungen zum Übersetzen und Lesen. Noch kein C-Projekt in diesem Repo |
| C++ | Dieselbe Stufe wie C: Übungen, kein Programm, das ich ausliefere |
| C# | Eine Sprachübung in [templates/](templates/). Keine C#-Anwendung hier |
| Java | Eine Sprachübung |
| Kotlin | Eine Sprachübung |
| Haskell | Eine Sprachübung. Eine ältere HashChat-Notiz nannte Haskell. Der Code, den ich jetzt schreibe, ist Rust |

Die leeren Formulare in [templates/](templates/) sind der Wochenrhythmus:
ein Helpdesk- oder SOC-Blatt, und eine Sprache. Ich kopiere ein Formular
und fülle es, während ich arbeite. Eine geratene Antwort gehört nicht
nach git.

## KI

Ich benutze KI bei dieser Arbeit, und ich sage es.

**Grok** (xAI) ist der Assistent für Planung, für einen zweiten
Durchgang beim Schreiben, und für die schwereren Builds. Ich arbeite
damit im Terminal.

Auf demselben Rechner läuft ein lokales Modell, damit Lernen keine
Cloud-Schlüssel braucht. **Ollama** stellt ein **Qwen**-Modell bereit.
Drei lokale Programme teilen es sich:

- **Hermes** ist der lokale Coding-Assistent. Ich frage nach einer
  Funktion, dann kompiliere ich das Ergebnis oder ich starte es.
- **OpenClaw** ist eine lokale Agenten-App auf demselben Modell, für
  kleinere Aufgaben.
- **Odysseus** ist ein lokaler Browser-Arbeitsplatz (Chat und Notizen)
  auf demselben Modell. Ich benutze ihn als Lerntutor: ein Thema pro
  Antwort, defensiv, auf virtuellen Maschinen auf diesem Rechner.

Ein Lab wird **Done**, wenn ich die Prüfung selbst laufen lasse und die
Ausgabe behalte. Ein Entwurf mit Grok oder Qwen bleibt **Planned** oder
**In progress**, bis dieser Lauf existiert. Die Nachweisdateien sind
Befehlsausgaben.

Das Modell bleibt bei defensivem Lernen und bei Code. In diesem Repo
steht keine Anleitung für einen Angriff.

## Womit anfangen

Für eine Helpdesk-Stelle oder eine Junior-SOC-Stelle zuerst hier:

1. [Windows-Domäne](helpdesk/06-windows-domain/) — ein echtes AD-DS-Lab, noch **In progress**. Am 4. Okt. 2026 war `win11-soc` schon in `lab.local`, ein Helpdesk-Reset ist aufgeschrieben, und die leere Workstation-GPO ist das Ticket. Noch offen: eine interaktive Helpdesk-Anmeldung, und eine Entsperrung (Sperrschwelle 0).
2. [Fehleranalyse Linux](helpdesk/03-linux-troubleshooting/) — **Done**, mit Terminalausgabe in `evidence/`.
3. [Incident-Berichte](soc-analyst/03-incident-writeups/) und [Sigma-Regeln](soc-analyst/05-sigma-rules/) — wie ich ein Log lese, und wie ich eine Erkennung schreibe.
4. [Python](python/) und [Rust](rust/) — kleine Werkzeuge mit Tests.
5. [Vorlagen](templates/) — die Formulare für einen Übungstag.

## Was ich noch lerne

Security+ SY0-701 ist nicht bestanden. HTB Academy läuft. Deutsch ist
in Arbeit. Portugiesisch ist meine Muttersprache. Französisch und
Englisch sind C1. Zuerst schaue ich in Frankreich, Helpdesk oder
Junior-SOC (Alternance oder POEI). Deutschland ist die andere
Möglichkeit, und dort kann ich auf Englisch arbeiten. Sobald ich
arbeite, beginne ich ein Fernstudium an der IU (Internationale
Hochschule).

Weitere Übungskonten, dieselbe Regel (in Arbeit, hier kein Rang):

- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46) — Academy in Arbeit. Kein Rang auf dieser Seite.
- [TryHackMe](https://tryhackme.com/p/ichbinlucasv)
- [Boot.dev](https://www.boot.dev/u/ichbinlucasv) — die öffentliche Seite bleibt bis Level 10 verborgen, deshalb steht hier kein Level

Eine SOC-Meldung ist schon bis zum Ende geschrieben, mit UTC-Zeitlinie:
[IR-03](soc-analyst/03-incident-writeups/IR-03-evtx-password-spray.md).
Am 4. Okt. 2026 habe ich `win11-soc` in `lab.local` geprüft, ein
Staff-Passwort mit dem Helpdesk-Credential zurückgesetzt, und die leere
Workstation-GPO als Ticket aufgeschrieben. Die Ausgabe liegt in
[Lab 06](helpdesk/06-windows-domain/). Die Formulare in
[templates/career/](templates/career/) bleiben leer für das nächste Mal.

## Kontakt

Nur das Öffentliche. Lab-Passwörter bleiben aus diesem Repo.

- E-Mail: ichbinlucas@pm.me
- [LinkedIn](https://www.linkedin.com/in/lucas-nunes-soares-63148637b/)
- [X](https://x.com/ichbinlucasv)
- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46)

Öffentliche Profile:
[codeberg.org/ichbinlucasv](https://codeberg.org/ichbinlucasv) und
[github.com/ichbinlucasv](https://github.com/ichbinlucasv).
