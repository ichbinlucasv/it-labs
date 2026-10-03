# Domäne 2 — Bedrohungen, Schwachstellen und Gegenmaßnahmen (≈22 %)

[English](2-threats-vulnerabilities-mitigations.md) · [Français](2-threats-vulnerabilities-mitigations.fr.md) · **Deutsch**

## Bedrohungsakteure

| Akteur | Motivation | Mittel |
|--------|------------|--------|
| Staat | Spionage, Störung, Krieg | Sehr hoch (APT) |
| Organisierte Kriminalität | Geld (Ransomware, Betrug) | Hoch |
| Hacktivist | Ideologie | Unterschiedlich |
| Innentäter | Rache, Geld, Nachlässigkeit | Hat schon Zugriff |
| Ungeschulter Angreifer | Nervenkitzel, Ansehen | Gering — benutzt die Werkzeuge anderer |
| Shadow IT | Bequemlichkeit (nicht böswillig) | Nicht verwaltetes Risiko |

Merkmale: intern/extern, Mittel/Finanzierung, Raffinesse.

## Bedrohungsvektoren und Angriffsfläche

Über Nachrichten (E-Mail, SMS = Smishing, Chat), Bilder, Dateien, Sprache
(Vishing), Wechselmedien, anfällige Software (mit Client oder ohne Agent),
nicht mehr unterstützte Systeme, unsichere Netze (Funk, Kabel, Bluetooth),
offene Ports, Standardzugangsdaten, Lieferkette (MSPs, Hersteller,
Lieferanten).

**Menschliche Vektoren / Social Engineering:** Phishing, Spear-Phishing,
Whaling, BEC (Kompromittierung der Geschäfts-E-Mail), Pretexting,
Impersonation, Watering Hole, Markenimitation, Typosquatting,
Fehlinformation/Desinformation.

## Arten von Schwachstellen

- **Anwendung:** Speicher-Injection, Pufferüberlauf, Race Conditions
  (TOC/TOU), bösartiges Update.
- **Web:** SQL-Injection (SQLi), Cross-Site-Scripting (XSS), CSRF, SSRF,
  Directory Traversal.
- **OS / Firmware / Hardware:** End of Life, Legacy, ungepatchte Firmware.
- **Virtualisierung:** VM Escape, Wiederverwendung von Ressourcen.
- **Cloud:** Fehlkonfiguration (öffentliche Buckets!), schwaches IAM.
- **Kryptografie:** schwache Algorithmen, schlechte Schlüsselverwaltung,
  Downgrade.
- **Mobil:** Sideloading, Jailbreak/Rooting.
- **Zero-Day:** es gibt noch keinen Patch.

## Anzeichen böswilliger Aktivität

Kontosperren, gleichzeitige Sitzungen an unmöglichen Orten („Impossible
Travel“), blockierte Inhalte, Spitzen beim Ressourcenverbrauch,
Protokollierung außerhalb des üblichen Zyklus, fehlende Logs,
veröffentlichte oder dokumentierte Daten aus einem Einbruch.

**Malware-Familien:** Ransomware, Trojaner, Wurm (verbreitet sich selbst),
Spyware, Bloatware, Virus, Keylogger, logische Bombe, Rootkit.
**Netzangriffe:** DDoS (verstärkt/reflektiert), DNS-Angriffe, Funk (Evil
Twin, Deauth), On-Path (MITM), Wiederholung von Zugangsdaten.
**Passwortangriffe:** Spraying (wenige Passwörter × viele Benutzer), Brute
Force (viele Passwörter × ein Benutzer), Credential Stuffing (wiederverwendete
bereits geleakte Zugangsdaten).
**Sonstiges:** Privilegienerweiterung, Replay, Fälschung, Downgrade,
Kollision (Hash), Birthday-Angriff.

## Gegenmaßnahmen

Segmentierung, Zugriffskontrolle (ACLs, Berechtigungen),
Anwendungs-Allowlist, Isolation, Patchen, Verschlüsselung, Überwachung,
geringste Rechte, Erzwingen der Konfiguration, Außerbetriebnahme,
**Härtung** (ungenutzte Ports/Dienste abschalten, Standardwerte ändern,
unnötige Software entfernen, Host-Firewall, EDR/HIPS).
