# Domäne 4 — Sicherheitsbetrieb (≈28 %, die größte Domäne)

[English](4-security-operations.md) · [Français](4-security-operations.fr.md) · **Deutsch**

## Sichere Baselines und Härtung

Baselines festlegen → ausrollen → pflegen (CIS Benchmarks). Härten: Mobilgeräte,
Arbeitsplätze, Switches/Router, Cloud, Server, ICS, Embedded, IoT. Funk:
WPA3, RADIUS/802.1X (Enterprise), Site Surveys, Heatmaps. Mobil: MDM, BYOD /
COPE / CYOD, Containerisierung. Anwendungssicherheit: Eingabeprüfung, sichere
Cookies, statische und dynamische Codeanalyse, Codesignierung, Sandboxing.

## Asset-Management

Beschaffung → Zuweisung (Verantwortung, Einstufung) → Überwachung/Nachverfolgung
(Inventar, Enumeration) → Entsorgung (Bereinigung, Zerstörung, Bescheinigung,
Datenaufbewahrung).

## Schwachstellenmanagement

Erkennen (Schwachstellenscans, Anwendungs-/Codeanalyse, Threat Feeds,
Pentest, Bug Bounty) → analysieren (**CVSS**-Score, **CVE**-Kennung,
falsch-positiv gegen falsch-negativ, Priorisierung, Exposure-Faktor,
Umgebungsvariablen, Risikotoleranz) → reagieren (Patch, Versicherung,
Segmentierung, kompensierende Kontrollen, Ausnahmen) → **prüfen** (erneut
scannen, auditieren, nachprüfen) → berichten.

## Überwachung und Alarmierung

Log-Sammlung, Alarmierung, Scannen, Berichte, Archivierung, Reaktion auf
Alarme (Quarantäne, **Alert-Tuning**). Werkzeuge: **SIEM**, SCAP, Benchmarks,
Agenten oder agentenlos, Antivirus, DLP, SNMP-Traps, NetFlow,
Schwachstellenscanner.

## Sicherheitsfähigkeiten im Unternehmen

Firewall-Regeln und Ports, IDS/IPS-Signaturen, Webfilter (mit Agent, Proxy,
URL-Kategorien, Reputation), OS-Sicherheit (GPO, SELinux), sichere Protokolle
(ersetzen Telnet→SSH, HTTP→HTTPS, FTP→SFTP, LDAP→LDAPS, SNMPv1/2→v3),
DNS-Filter, E-Mail-Sicherheit (**SPF, DKIM, DMARC**, Gateway), FIM, DLP,
NAC, EDR/XDR, Analyse des Nutzerverhaltens.

## Identitäts- und Zugriffsverwaltung

Provisionierung/Deprovisionierung, Rechtevergabe, Identitätsnachweis,
Föderation, SSO (**LDAP, OAuth, SAML**), Interoperabilität, Attestierung.
Zugriffskontrollmodelle: **verbindlich (MAC)**, **diskretionär (DAC)**,
**rollenbasierend (RBAC)**, regelbasiert, attributbasiert (ABAC), nach
Tageszeit. MFA-Faktoren: etwas, das du weißt / hast / bist / der Ort, an dem
du bist. Passwortlos, Passkeys. **PAM**: Just-in-time-Rechte, Passwort-Tresor,
kurzlebige Zugangsdaten.

## Automatisierung und Orchestrierung

Anwendungsfälle: Benutzer anlegen, Ressourcen bereitstellen, Leitplanken,
Sicherheitsgruppen, Tickets erzeugen, Eskalation, Dienste an- und abschalten,
Tests in der CI, API-Anbindungen. Nutzen: Effizienz, Baselines durchsetzen,
schnellere Reaktion, die Wirkung des Teams vervielfachen. Risiken:
Komplexität, Kosten, einzelner Ausfallpunkt, technische Schulden.

## Incident Response

**Ablauf**: Vorbereitung → Erkennung → Analyse → Eindämmung → Beseitigung →
Wiederherstellung → gewonnene Erkenntnisse. Training, Tests (Tabletop-Übung,
Simulation), Ursachenanalyse, Threat Hunting, **digitale Forensik**: Legal
Hold, **Beweiskette**, Sicherstellung (Reihenfolge der Volatilität: CPU/Cache
→ RAM → Swap → Platte → entfernte Logs → Backups), Bericht, Aufbewahrung,
E-Discovery.

## Datenquellen für Untersuchungen

Firewall, Anwendung, Endpunkt, betriebssystemeigene Sicherheitslogs, IPS/IDS,
Netzlogs, Metadaten; Schwachstellenscans, automatische Berichte, Dashboards,
Paketerfassungen.
