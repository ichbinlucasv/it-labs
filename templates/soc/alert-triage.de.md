# Ein Alert

[English](alert-triage.md) · [Français](alert-triage.fr.md) · **Deutsch**

Ein Alert pro Blatt. UTC. Ich antworte aus dem Log, bevor ich ein zweites
Werkzeug öffne.

```text
Alert-Name / Regel:
ID:
Angekommen (UTC):
Gerät:
Benutzer:
Schweregrad im Werkzeug:

Was die Regel für geschehen hält (ein Satz):

Erstes Ereignis, das ich geöffnet habe (ID, Zeit UTC):
Übergeordneter Prozess, wenn das ein Endpoint ist:
Anmeldetyp, wenn das eine Anmeldung ist:

Auf diesem Gerät schon gesehen?  unbekannt / ja, Ticket / nein

Harmloser Grund, den ich benennen kann:
    [ ] Admin-Werkzeug, das wir nutzen
    [ ] Fenster für Patches / Sicherung
    [ ] der Benutzer hat es getan
    [ ] ich kann keinen nennen

Entscheidung:
    [ ] schließen, Grund:
    [ ] beobachten, was meine Meinung ändern würde:
    [ ] eskalieren, mit dem Zeitstrahl

Was ich nicht getan habe: die Datei ausführen, den Link anklicken oder das Passwort versuchen.
```

Ich übe an den synthetischen Logs in
[soc-analyst/02](../../soc-analyst/02-sysmon-auditd-logs/) oder an IR-03.
Ein Blatt ohne Ereignis-ID zählt nicht.
