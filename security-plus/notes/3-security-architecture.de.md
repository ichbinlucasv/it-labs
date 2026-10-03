# Domäne 3 — Sicherheitsarchitektur (≈18 %)

[English](3-security-architecture.md) · [Français](3-security-architecture.fr.md) · **Deutsch**

## Architekturmodelle

| Modell | Sicherheitsaspekte |
|--------|--------------------|
| Cloud (IaaS/PaaS/SaaS) | **Geteilte Verantwortung** — der Kunde bleibt immer Eigentümer der Daten und Identitäten |
| Hybrid | Dieselbe Richtlinie on-prem und in der Cloud |
| Infrastructure as Code | Vorlagen wie Code prüfen; Drift erkennen |
| Serverless / Microservices | Viele kleine Angriffsflächen; API-Sicherheit |
| Netz: on-prem, zentral oder dezentral | Einzelner Ausfallpunkt, oder schwerer zu verwalten |
| Container und Virtualisierung | Herkunft der Images, Isolation, Basis-Images patchen |
| IoT, ICS/SCADA, RTOS, Embedded | Schwer zu patchen → segmentieren |
| Hochverfügbarkeit | Redundanz, Lastverteilung, Clustering |

Zu bedenken: Verfügbarkeit, Belastbarkeit, Kosten, Reaktionsfähigkeit,
Skalierbarkeit, einfaches Ausrollen und Wiederherstellen, ob es Patches
gibt, Risikoübertragung, Strom, Rechenleistung.

## Netzsicherheit

- **Zonen / Segmentierung**: DMZ (Screened Subnet), VLANs, Air Gap.
- **Geräte**: Firewall (stateful, NGFW, WAF, UTM), IDS/IPS (inline oder per
  Tap), Jump-Server, Proxy (Forward/Reverse), Load Balancer, 802.1X/NAC,
  Sensoren.
- **Fehlerverhalten**: Fail-open (Verfügbarkeit) gegen Fail-closed (Sicherheit).
- **Sichere Kommunikation**: VPN (IPsec, TLS), SD-WAN, SASE (Netz + Sicherheit
  als Cloud-Dienst).
- **Auswahl der Kontrollen** nach Angriffsfläche, Anbindung, Platzierung der
  Geräte.

## Datenschutz

- **Datenarten**: reguliert, Geschäftsgeheimnis, geistiges Eigentum,
  rechtlich, finanziell, von Menschen lesbar oder nicht.
- **Einstufungen**: öffentlich, privat, sensibel, vertraulich, eingeschränkt,
  kritisch.
- **Zustände**: ruhend, bei der Übertragung, in Benutzung.
- **Souveränität / Geolokation**: Recht des Landes, in dem die Daten liegen
  (GDPR / RGPD in Frankreich und der EU).
- **Verfahren**: Verschlüsselung, Hashing, Maskierung, Tokenisierung,
  Verschleierung, Segmentierung, Einschränkung der Rechte.

## Belastbarkeit und Wiederherstellung

- **Standorte**: heiß (sofort bereit), warm (Hardware da, Daten fehlen), kalt
  (nur der Raum); geografisch verteilt.
- **Backups**: vor Ort/außerhalb, Häufigkeit, Verschlüsselung, Snapshots,
  Replikation, Journaling. Wiederherstellungen testen!
- **Strom**: USV (kurz), Generator (lang).
- **Betriebskontinuität**, Kapazitätsplanung (Personen, Technik,
  Infrastruktur), Tests (Tabletop, Failover, Simulation, Parallelbetrieb).
- **Kennzahlen**: RTO (wie schnell wiederhergestellt), RPO (wie viel
  Datenverlust ist hinnehmbar), MTTR (mittlere Reparaturzeit), MTBF (mittlere
  Zeit zwischen Ausfällen).
