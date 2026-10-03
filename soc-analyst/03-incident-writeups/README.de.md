# Lab 03 — Incident-Berichte auf öffentlichen Datensätzen

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** In progress — [IR-03](IR-03-evtx-password-spray.md) (Kerberos-Password-Spraying, öffentliches EVTX-Beispiel) ist analysiert und abgeschlossen; IR-01 (Malware-Traffic-pcap, braucht eine isolierte Analyse-VM) und IR-02 (Splunk BOTS v1, braucht eine Splunk-Instanz) sind noch Untersuchungspläne.

## Ziel

Den vollständigen Analyse-Ablauf an **echten, öffentlichen**
Trainingsdatensätzen üben: Fragestellung eingrenzen, mit dem passenden
Werkzeug untersuchen, Nachweise festhalten, auf ATT&CK abbilden und einen
Bericht schreiben, den sowohl eine Führungskraft als auch ein L2/L3-Analyst
nutzen kann. (Security+ D4 — Incident-Response-Prozess; D2 — Indikatoren;
D5 — Berichtswesen.)

## Aufbau

| Bericht | Datensatz | Quelle | Werkzeuge |
|---------|-----------|--------|-----------|
| [IR-01](IR-01-malware-traffic-pcap.md) | Eine Trainingsübung von Malware-Traffic-Analysis.net (pcap) | <https://www.malware-traffic-analysis.net/training-exercises.html> | Wireshark, tshark, Zeek (optional) |
| [IR-02](IR-02-splunk-bots-v1.md) | Splunk Boss of the SOC v1 | <https://github.com/splunk/botsv1> | Splunk Enterprise (Testversion / Entwicklerlizenz) |
| [IR-03](IR-03-evtx-password-spray.md) | EVTX-ATTACK-SAMPLES — `Credential Access/kerberos_pwd_spray_4771.evtx` | <https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES> | python-evtx, `jq`, Sigma (sigma-cli, SQLite-Backend) |

Zusätzlicher Datensatz: **OTRF Security-Datasets** (früher Mordor) —
<https://github.com/OTRF/Security-Datasets> / <https://securitydatasets.com/> —
JSON-Exporte simulierter ATT&CK-Techniken, leicht in Wazuh/ELK/Splunk zu laden.

- In einer isolierten Analyse-VM arbeiten (Snapshots, keine geteilten
  Ordner, keine Zugangsdaten). Malware-Traffic-Zips sind aus gutem Grund passwortgeschützt.
- Von jeder analysierten Datei den SHA256 festhalten (Gewohnheit für die Beweiskette).
- Jeder Bericht folgt [`TEMPLATE.md`](TEMPLATE.md).

> **Hinweis zur Ehrlichkeit:** IR-01 und IR-02 sind noch *Untersuchungspläne
> und Berichtsgerüste*: Ihre Ergebnisse bleiben `TBD`, bis ich die Daten
> analysiert habe. IR-03 enthält meine eigene Analyse des öffentlichen
> Beispiels. Es wurden keine Antworten aus Berichten anderer übernommen.
>
> Warum IR-01/IR-02 noch offen sind: Die Malware-Traffic-pcaps enthalten
> echten bösartigen Verkehr, und meine Regel ist, sie nur in einer eigenen,
> isolierten Analyse-VM zu öffnen — das ist mein aktueller Lab-Rechner nicht;
> BOTS v1 braucht eine Splunk-Instanz mit dem etwa 6 GB großen Datensatz.

## Schritte

1. Einen Datensatz in die Analyse-VM herunterladen, den Hash prüfen, URL und Datum notieren.
2. Die Abschnitte aus `TEMPLATE.md` in den Bericht übernehmen und die
   Untersuchungsschritte durcharbeiten.
3. Nachweistabellen mit den genauen Abfragen/Filtern und Ergebnissen füllen
   (Ausgaben in `evidence/`).
4. Bestätigtes Verhalten auf ATT&CK abbilden und die
   [Mapping-Tabelle](../04-attack-mapping/README.de.md) aktualisieren.
5. Die Management-Zusammenfassung **zuletzt** schreiben.

### IR-03 in Kürze (Bericht auf Englisch)

Auf dem Domain Controller des Beispiels fragte eine einzige Quelladresse,
`172.16.66.1`, innerhalb von **11 Millisekunden** Kerberos-Tickets für **10
verschiedene Konten** an — das schafft nur ein Tool. Sieben Namen
existierten nicht (4768, `0x6`), zwei existierende Konten (`Administrator`,
`backdoor`) wurden wegen eines falschen Passworts abgewiesen (4771, `0x18`),
und **ein Konto, `normal`, erhielt ein Ticket** — das getestete Passwort war
für dieses Konto richtig. Das ist Password Spraying (ein Passwort, viele
Konten, T1110.003) mit einem Treffer. Meine neue Sigma-Korrelationsregel
(Anzahl **verschiedener** Benutzernamen pro Quelle) löste auf den Daten drei
Alarme aus (5, 7 und 9 Benutzer). Zwei Erkenntnisse aus dem Test: Adressen
wie `::ffff:172.16.66.1` vor dem Gruppieren normalisieren, und eine
Folgeregel für den **Erfolg** eines der betroffenen Konten ergänzen — die
Regel alarmiert auf die Fehlversuche, das wichtigste Ereignis ist aber der
Erfolg. Das Löschen des Security-Logs (1102) 9 s vorher stammt in diesem
Beispiel sehr wahrscheinlich vom Autor des Datensatzes; ich notiere es, ordne
es aber nicht dem Angreifer zu.

## Nachweise

- [IR-03](IR-03-evtx-password-spray.md) mit [`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt)
  (SHA256 des EVTX, Ereignistabelle, Sigma-Replay).
- IR-01, IR-02: noch nicht begonnen (siehe Hinweis zur Ehrlichkeit).

## Was ich gelernt habe

- Auch kleine Datensätze können eine vollständige Geschichte erzählen: 12
  Ereignisse reichten, um Enumeration, Spraying und einen erfolgreichen Treffer zu sehen.
- Kerberos-Statuscodes verraten Informationen: `0x6` gegenüber `0x18` zeigt
  einem Angreifer, welche Konten existieren.
- Meine Detection alarmierte auf die Fehlversuche, das wichtigste Ereignis
  war aber der Erfolg direkt danach — ein Detection-Konzept braucht auch die
  Regel für „was danach passiert“.
- Normalisierung von Daten ist wichtig: Derselbe Host erschien als
  `172.16.66.1` und als `::ffff:172.16.66.1`.
- Nicht jedes verdächtige Ereignis gehört zum Angreifer (das Löschen des
  Logs, 1102); „notiert, nicht zugeordnet“ ist besser als eine überzogene Behauptung.
