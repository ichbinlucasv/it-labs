# IR-03 — Kerberos-Password-Spraying in Windows-Security-Logs

[English](IR-03-evtx-password-spray.md) · [Français](IR-03-evtx-password-spray.fr.md) · **Deutsch**

| Feld | Wert |
|------|------|
| Analyst | Lucas |
| Datum der Analyse | 2026-09-27 |
| Datensatz und URL | EVTX-ATTACK-SAMPLES von Samir Bousseaden — <https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES> — Datei `Credential Access/kerberos_pwd_spray_4771.evtx` (heruntergeladen am 2026-09-27 von der rohen GitHub-URL) |
| Lizenz | Siehe das Repository (GPL) |
| SHA256 der Datei | `4a0a1c7132e216dbc704c806e9429df9ae3ac00485d5238e50c776e3099ae11d` |
| Zeitraum der Daten (UTC) | 2020-07-22 20:29:27.321 – 20:29:36.437 (12 Ereignisse) |
| Schwere | Hoch (ein gültiges Domänenpasswort wurde gefunden) — in einer echten Umgebung |
| Status | Abgeschlossen |

Die Hostnamen, Kontonamen und Adressen unten stammen aus diesem öffentlichen
Trainingsbeispiel (eine Lab-Domäne `threebeesco.com`), nicht aus einem echten
Incident. Vollständige Befehlsausgabe:
[`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt).

## 1. Zusammenfassung für die Leitung

Auf dem Domänencontroller `01566s-win16-ir.threebeesco.com` hat eine einzige
Quelladresse, `172.16.66.1`, Kerberos-Tickets für **10 verschiedene Konten
innerhalb von 11 Millisekunden** angefragt — das schafft nur ein Tool. Sieben
Namen gab es nicht, zwei vorhandene Konten (`Administrator`, `backdoor`)
wurden wegen eines falschen Passworts abgewiesen, und **ein Konto, `normal`,
hat ein Ticket bekommen**: das probierte Passwort stimmte für dieses Konto.
Das ist Password Spraying (ein Passwort, viele Konten), und es hat für ein
Konto geklappt. Empfohlene Maßnahmen: Passwort von `normal` zurücksetzen,
prüfen, was der Quellhost mit dem Ticket gemacht hat, und das Konto namens
`backdoor` untersuchen.

## 2. Umfang und Fragen — Antworten

| Frage | Antwort |
|-------|---------|
| Wie viele Konten, von wo? | 10 verschiedene Benutzernamen, alle von `172.16.66.1` (das letzte Ereignis zeigt sie als `::ffff:172.16.66.1`, die IPv4-abgebildete IPv6-Form) |
| Zeitfenster und Rate? | 20:29:36.414 → 20:29:36.437 UTC: 11 Anfragen in 23 ms, alle 10 Namen in den ersten 20 ms |
| Kerberos-Fehlercodes? | 4768 `0x6` (KDC_ERR_C_PRINCIPAL_UNKNOWN — Benutzer existiert nicht) × 7; 4771 `0x18` (KDC_ERR_PREAUTH_FAILED — falsches Passwort) × 2 |
| Hat ein Konto Erfolg gehabt? | **Ja** — 4768 mit Status `0x0` für `normal` (zweimal, AES256-Ticket `0x12`), 9 ms nach den Fehlversuchen |
| Spraying oder Brute Force? | Spraying: jeder Name einmal probiert, viele Namen |

Hintergrund: **4768** = ein TGT wurde angefragt (Erfolg oder Fehlschlag, je
nach `Status`); **4771** = die Kerberos-Präauthentifizierung ist fehlgeschlagen.
Ein unbekannter Benutzer kommt nie bis zur Präauthentifizierung, deshalb
erscheint das als Fehlschlag 4768 und nicht als 4771.

## 3. Untersuchungsprotokoll

| # | Werkzeug | Aktion | Ergebnis |
|---|----------|--------|----------|
| 1 | `sha256sum` | EVTX hashen | `4a0a1c71…ae11d` |
| 2 | [`evtx_to_jsonl.py`](evtx_to_jsonl.py) (python-evtx 0.8.1) | In ein JSON-Objekt pro Ereignis umwandeln | 12 Ereignisse. Ich habe python-evtx statt des geplanten `evtx_dump` benutzt, weil nur ein `pip install` gefehlt hat |
| 3 | `jq` | Nach EventID zählen | 1 × 1102, 9 × 4768, 2 × 4771 |
| 4 | `jq` | Verschiedene Zielbenutzer | 10 (`HD01`, `HD02`, `admin`, `admin02`, `svc-01`, `svc-02`, `bob`, `Administrator`, `backdoor`, `normal`) |
| 5 | `jq` | Quelladressen | nur `172.16.66.1` (Quellports 55957–55969 aufsteigend, dann 52559 über IPv6-abgebildet) |
| 6 | `jq` | Statuscodes | `0x6` × 7, `0x18` × 2, `0x0` × 2 |
| 7 | `jq` | Rate | das ganze Spray < 25 ms — ein Diagramm pro Minute ist unnötig |
| 8 | Sigma | Neue Regel [`win_kerberos_password_spray_correlation.yml`](../05-sigma-rules/rules/win_kerberos_password_spray_correlation.yml): `value_count` verschiedener `TargetUserName` ≥ 5 pro `IpAddress` in 5 min über 4771 `0x18` / 4768 `0x6`; `sigma check` sauber; mit dem SQLite-Backend umgewandelt und auf den Ereignissen laufen lassen | 3 Alarme für `172.16.66.1` (5, 7, 9 verschiedene Benutzer) |
| 9 | Hayabusa / Chainsaw | Nicht ausgeführt | — |

## 4. Zeitleiste (UTC, 2020-07-22)

| Zeit | Ereignis | Detail |
|------|----------|--------|
| 20:29:27.321 | 1102 | Security-Log gelöscht von `3B\a-jbrown` |
| 20:29:36.414–.415 | 4768 `0x6` × 7 | Unbekannte Benutzer `HD01`, `admin`, `svc-02`, `HD02`, `svc-01`, `bob`, `admin02` |
| 20:29:36.425 | 4771 `0x18` × 2 | Falsches Passwort für `Administrator`, `backdoor` |
| 20:29:36.434 | 4768 `0x0` | TGT an `normal` ausgestellt |
| 20:29:36.437 | 4768 `0x0` | Zweites TGT für `normal` von `::ffff:172.16.66.1` |

Zum 1102: das Log wurde 9 s vor dem Spray gelöscht. In diesem Beispiel ist
das höchstwahrscheinlich der Autor des Datensatzes, der das Log vor der
Aufnahme zurücksetzt (`a-jbrown` sieht nach einem Admin-Konto aus). In einem
echten Fall wäre ein gelöschtes Log direkt vor einem Angriff selbst ein
ernster Befund (T1070.001); hier notiere ich es, schreibe es aber nicht dem
Angreifer zu.

## 5. IOCs (Beispieldaten)

| Typ | Wert | Hinweis |
|-----|------|---------|
| Quell-IP | `172.16.66.1` | Interne Adresse — der Host selbst muss untersucht werden |
| Kompromittiertes Konto | `normal` | Passwort erraten |
| Vorhandene Konten, die getroffen wurden | `Administrator`, `backdoor` | `backdoor` ist ein verdächtiger Name für ein Konto, das es gibt |
| Probierte Namen, die es nicht gibt | `HD01`, `HD02`, `admin`, `admin02`, `svc-01`, `svc-02`, `bob` | Typische Liste erratener Namen |

## 6. ATT&CK-Zuordnung

- **T1110.003 Brute Force: Password Spraying** (Credential Access) —
  bestätigt: ein Versuch pro Konto über 10 Konten.
- **T1078.002 Valid Accounts: Domain Accounts** — möglicher nächster Schritt:
  das Ticket für `normal` würde den Angreifer als diesen Benutzer handeln
  lassen. Das Beispiel endet dort, also ist das nicht bestätigt.
- T1070.001 Clear Windows Event Logs — notiert, nicht zugeordnet (siehe Zeitleiste).

## 7. Auswirkung

Das Passwort eines Domänenkontos ist demjenigen bekannt, der `172.16.66.1`
kontrolliert. Der Angreifer hat außerdem gelernt, welche der probierten Namen
existieren (`0x6` gegen `0x18` sagt es ihm), darunter `Administrator` und
`backdoor`.

## 8. Empfehlungen

1. Passwort von `normal` zurücksetzen, seine Sitzungen/Tickets widerrufen und
   seine Anmeldungen (4624/4769) nach 20:29:36 auf laterale Bewegung prüfen.
2. Den Host `172.16.66.1` untersuchen (welcher Prozess die Anfragen geschickt hat).
3. Herausfinden, wer `backdoor` angelegt hat und warum (Ereignisse 4720, `whenCreated`).
4. Eine Passwortrichtlinie erzwingen, die gängige Passwörter sperrt, und MFA,
   wo es geht.
5. Die Korrelationsregel auf verschiedene Benutzer ausrollen. Zwei Lehren aus
   dem Test: `::ffff:x.x.x.x` vor dem Gruppieren auf `x.x.x.x` normalisieren
   (sonst zählt derselbe Host als zwei Quellen), und eine Folgeregel
   ergänzen: „Erfolg für eines der Konten aus dem Spray, von derselben Quelle“ —
   meine Regel alarmiert auf die Fehlversuche, aber der **Erfolg** ist das
   Ereignis, auf das es am meisten ankommt.

## 9. Nachweise

- [`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt) — Hash,
  Ereignistabelle, Zählungen und das Ergebnis des Sigma-Replays. Das EVTX
  selbst ist nicht eingecheckt.
