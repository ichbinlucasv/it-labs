# Domäne 5 — Management und Aufsicht des Sicherheitsprogramms (≈20 %)

[English](5-security-program-management.md) · [Français](5-security-program-management.fr.md) · **Deutsch**

## Governance

- **Richtlinien** (grob, verbindlich): AUP, Informationssicherheit,
  Geschäftskontinuität, Disaster Recovery, Incident Response, SDLC,
  Änderungsmanagement.
- **Standards**: Passwörter, Zugriffskontrolle, physische Sicherheit,
  Verschlüsselung.
- **Verfahren**: Änderungsmanagement, Eintritt/Austritt, Playbooks.
- **Leitlinien**: Empfehlungen, nicht verbindlich.
- Äußere Vorgaben: regulatorisch, rechtlich, Branche, lokal/regional,
  national, global. Überwachung und Überarbeitung.
- Strukturen: Vorstände, Ausschüsse, staatliche Stellen, zentral gegen
  dezentral.
- Rollen für Systeme und Daten: **Owner** (rechenschaftspflichtig),
  **Verantwortlicher** (entscheidet, warum und wie personenbezogene Daten
  verarbeitet werden), **Auftragsverarbeiter** (verarbeitet im Auftrag des
  Verantwortlichen), **Custodian/Steward** (die tägliche Pflege).

## Risikomanagement

- Identifikation → Bewertung (ad hoc, wiederkehrend, einmalig, fortlaufend)
  → Analyse → Register → Behandlung → Bericht.
- **Qualitativ** (hoch/mittel/niedrig, Heatmap) gegen **quantitativ**:
  - SLE = Wert des Assets × Exposure-Faktor
  - ARO = erwartete Ereignisse pro Jahr
  - **ALE = SLE × ARO**
- Risikoregister: zentrale Risikoindikatoren, Risikoverantwortliche,
  Risikoschwelle.
- Risikotoleranz gegen **Risikoappetit** (expansiv, konservativ, neutral).
- Strategien: **übertragen** (Versicherung), **akzeptieren**
  (Ausnahme/Befreiung), **vermeiden** (die Tätigkeit einstellen),
  **mindern** (Kontrollen).
- Business-Impact-Analyse: RTO, RPO, MTTR, MTBF.

## Drittparteienrisiko

Anbieterbewertung (Pentest, Recht auf Audit, Nachweise interner Audits,
unabhängige Bewertungen, Lieferkettenanalyse), Auswahl (Due Diligence,
Interessenkonflikt), Vereinbarungen: **SLA** (Service-Level), **MOA/MOU**
(Absicht), **MSA** (Rahmenbedingungen), **WO/SOW** (die konkrete Arbeit),
**NDA**, **BPA** (Geschäftspartner). Überwachung der Anbieter, Fragebögen,
Rules of Engagement.

## Compliance

Interne/externe Berichte, Folgen von Non-Compliance (Bußgelder, Sanktionen,
Reputationsschaden, Verlust der Lizenz, vertragliche Folgen), Überwachung
der Compliance (Sorgfalt, Attestierung, Automatisierung). **Privatsphäre**:
rechtliche Folgen, betroffene Person, Verantwortlicher gegen
Auftragsverarbeiter, Eigentum, Dateninventar und Aufbewahrung, **Recht auf
Vergessenwerden** (GDPR). In Frankreich: die CNIL ist die
Datenschutzbehörde; die ANSSI ist die nationale Cybersicherheitsagentur;
NIS2 weitet die Pflichten auf mehr Sektoren aus.

## Audits und Bewertungen

Attestierung, intern (Compliance, Prüfungsausschuss, Selbstbewertung),
extern (regulatorisch, Prüfungen, unabhängiger Dritter).
**Penetrationstest**: physisch, offensiv (Red), defensiv (Blue), integriert
(Purple); bekannte Umgebung (White Box), teilweise bekannt (Grey), unbekannt
(Black Box); Aufklärung passiv gegen aktiv.

## Sicherheitssensibilisierung

Phishing-Kampagnen und Meldungen, auffälliges Verhalten erkennen (riskant,
unerwartet, unbeabsichtigt), Hinweise für Benutzer (Richtlinienhandbücher,
Lagebewusstsein, Innentäter, Passwortverwaltung, Wechselmedien, Social
Engineering, operative Sicherheit, hybrides/entferntes Arbeiten), Meldung und
Überwachung (zu Beginn, dann wiederkehrend), Ausarbeitung und Durchführung.
