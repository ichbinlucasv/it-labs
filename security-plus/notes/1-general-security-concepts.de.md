# Domäne 1 — Allgemeine Sicherheitskonzepte (≈12 %)

[English](1-general-security-concepts.md) · [Français](1-general-security-concepts.fr.md) · **Deutsch**

## Kategorien und Typen von Sicherheitskontrollen

| Kategorie | Beispiele |
|-----------|-----------|
| Technisch | Firewall-Regeln, MFA, Verschlüsselung, EDR |
| Management | Richtlinien, Risikobewertungen, Programm zur Sicherheitssensibilisierung |
| Operativ | Wachpersonal, Änderungsmanagement, von Mitarbeitern durchgeführte Backups |
| Physisch | Schlösser, Zäune, Ausweisleser, CCTV |

| Typ | Zweck | Beispiel |
|-----|-------|----------|
| Präventiv | Verhindern, dass es passiert | Kontosperre, Firewall-Deny |
| Abschreckend | Abschrecken | Warnbanner, sichtbare Kamera |
| Detektiv | Merken, dass es passiert ist | IDS, Log-Prüfung, SIEM-Alarm |
| Korrektiv | Nach dem Ereignis reparieren | Backup zurückspielen, patchen |
| Kompensierend | Ersatz, wenn die ideale Kontrolle nicht möglich ist | Netzisolation für eine Maschine, die man nicht patchen kann |
| Direktiv | Den Leuten sagen, was sie tun sollen | Richtlinie, Schild „nur befugtes Personal“ |

## Grundprinzipien

- **CIA-Triade**: Vertraulichkeit (Verschlüsselung, Zugriffskontrolle),
  Integrität (Hashing, Signaturen), Verfügbarkeit (Redundanz, Backups,
  DDoS-Schutz).
- **Nichtabstreitbarkeit**: der Absender kann es nicht abstreiten — digitale
  Signaturen.
- **AAA**: Authentifizierung (wer bist du), Autorisierung (was darfst du),
  Accounting (was hast du getan — Logs).
- **Zero Trust**: niemals wegen des Standorts vertrauen; jede Anfrage
  ausdrücklich prüfen. Die *Control Plane* (Policy Engine, Policy
  Administrator) entscheidet; die *Data Plane* (Policy Enforcement Point)
  setzt durch. Adaptive Identität, Verkleinerung des Bedrohungsbereichs,
  implizite Vertrauenszonen.
- **Gap-Analyse**: Ist-Zustand gegen Soll-Zustand (z. B. gegen ein Framework).
- **Physisch**: Poller, Zugangsschleuse (Mantrap), Beleuchtung, Sensoren
  (Infrarot, Druck, Mikrowelle, Ultraschall).
- **Täuschung**: Honeypot (ein Host), Honeynet (ein Netz), Honeyfile,
  Honeytoken (gefälschte Zugangsdaten oder Daten, die beim Benutzen alarmieren).

## Änderungsmanagement

Genehmigungsprozess, Verantwortung, Beteiligte, Auswirkungsanalyse,
Testergebnisse, **Backout-Plan**, Wartungsfenster, SOP. Technische Folgen:
Allow-/Deny-Listen, eingeschränkte Tätigkeiten, Ausfallzeit, Neustarts von
Diensten/Anwendungen, Altanwendungen, Abhängigkeiten. Dokumentation und
Diagramme aktualisieren; Versionskontrolle.

## Kryptografie, das Wichtige

| Begriff | Merken |
|---------|--------|
| Symmetrisch | Ein gemeinsamer Schlüssel, schnell (AES). Problem: Schlüsselverteilung |
| Asymmetrisch | Paar aus öffentlichem und privatem Schlüssel (RSA, ECC). Für Schlüsselaustausch und Signaturen |
| Hashing | Einweg, feste Länge (SHA-256). Integrität, Passwortspeicherung (+ Salt) |
| Salt | Zufallswert pro Passwort → macht Rainbow Tables unbrauchbar |
| Key Stretching | PBKDF2, bcrypt, Argon2 — absichtlich langsam |
| Digitale Signatur | Hash, signiert mit dem **privaten** Schlüssel des Absenders, geprüft mit seinem **öffentlichen** Schlüssel |
| Für jemanden verschlüsseln | **Seinen öffentlichen** Schlüssel benutzen; er entschlüsselt mit seinem privaten Schlüssel |
| PKI | Die CA stellt Zertifikate aus; CRL / OCSP (Stapling) für den Widerruf; Wildcard- und SAN-Zertifikate |
| Key Escrow | Ein Dritter verwahrt die Schlüssel für die Wiederherstellung |
| TPM / HSM / Secure Enclave | Hardwareschutz der Schlüssel (TPM = auf der Platine, HSM = eigenes Gerät) |
| Verschleierung | Steganografie, Tokenisierung (Wert durch einen Token ersetzen), Datenmaskierung |
| Blockchain | Verteiltes Register, an dem man eine Änderung erkennt |
| Verschlüsselungsebenen | Ganze Platte, Partition, Volume, Datei, Datenbank, Datensatz; Transport (TLS, IPsec) |
