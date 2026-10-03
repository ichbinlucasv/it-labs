# bash

[English](bash.md) · [Français](bash.fr.md) · **Deutsch**

Ich nutze es für den Linux-Rechner, jeden Tag. Pakete, Dienste, Platten,
„warum SSH fehlschlägt“, ein kurzer Blick in ein Log.

## 25 Minuten

1. 10 Min. Ich tippe den Block unten aus dem Kopf. `man` erst danach.
2. 10 Min. Ich mache im Lab-Container aus
   [helpdesk/03](../../helpdesk/03-linux-troubleshooting/) eine Sache kaputt
   und schreibe den Befehl auf, der sie gezeigt hat.
3. 5 Min. Eine Zeile auf dem Tageszettel: die Option, die ich vergessen habe.

## Die tippe ich, bis es sitzt

```bash
systemctl status ssh --no-pager
journalctl -u ssh -S today --no-pager
ss -lntup
df -hT
ip -br addr
ip route
getent hosts example.com
id
find /var/log -type f -mtime -1 -printf '%TY-%Tm-%Td %p\n'
```

Eine Logzeile, nicht die ganze Datei:

```bash
journalctl -u ssh --since "1 hour ago" --no-pager | tail -n 40
grep -E 'Failed|Accepted' /var/log/auth.log | tail
```

Debian und Fedora benutzen nicht denselben Log-Pfad. Fehlt die Datei, sage
ich das. Ich erfinde keine Zeilen.

## Übung

Auf Papier schreibe ich, was `ss -lntup` mir über einen lauschenden Port
sagt: Programm, Benutzer, Adresse, Port. Dann führe ich den Befehl aus und
markiere, was ich falsch gelesen habe.

## Das verwechsle ich noch

- `ss` und `netstat`
- `--since` bei journalctl gegen `tail -f`, wenn ich die Vergangenheit brauche
- eine Korrektur als root ausführen, bevor ich den Fehler gelesen habe
