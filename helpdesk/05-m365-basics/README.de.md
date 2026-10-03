# Lab 05 — Grundlagen der Microsoft-365-Administration

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Planned — nur Konzeptnotizen; nicht in einem Microsoft-365-Mandanten geübt. Ich brauche einen Microsoft-365-Test oder einen Entwicklermandanten, den ich noch nicht habe; hier ist nichts simuliert.

## Ziel

Die Microsoft-365- / Entra-ID-Begriffe verstehen, die im Helpdesk vorkommen:
Lebenszyklus der Benutzer, Lizenzen, Gruppen, MFA, Selbstbedienung beim
Zurücksetzen des Passworts, und welches Admin Center wofür da ist. Das ist
ein **dokumentiertes Konzept-Lab** — hier stehen keine echten Mandantendaten.

## Aufbau

- Option A: Sandbox des Microsoft-365-Entwicklerprogramms (die Teilnahme hat
  sich mit der Zeit geändert — die aktuellen Bedingungen prüfen) oder ein
  Microsoft-365-Business-Test.
- Option B: kostenlose Module und interaktive Anleitungen auf Microsoft Learn
  (Lernpfade MS-900 / SC-900), wenn kein Mandant da ist.
- Fiktiver Mandant: `exemple-sarl.onmicrosoft.com`, eigene Domäne `example.com`.

## Schritte

### 1. Die Admin Center zuordnen

| Aufgabe | Wo |
|---------|----|
| Benutzer anlegen, Lizenzen zuweisen, Passwörter zurücksetzen | Microsoft 365 Admin Center (`admin.microsoft.com`) |
| Identität, Gruppen, MFA, bedingter Zugriff, Anmeldeprotokolle | Microsoft Entra Admin Center (`entra.microsoft.com`) |
| Postfächer, freigegebene Postfächer, Nachrichtenfluss, Nachrichtenverfolgung | Exchange Admin Center |
| Teams-Richtlinien, Besprechungseinstellungen | Teams Admin Center |
| Geräte, Compliancerichtlinien, App-Bereitstellung | Intune (`intune.microsoft.com`) |
| Warnungen, Phishing, Quarantäne, Defender-Incidents | Microsoft Defender-Portal (`security.microsoft.com`) |
| Aufbewahrung, DLP, eDiscovery | Microsoft Purview-Portal |

### 2. Lebenszyklus (Eintritt / Wechsel / Austritt)

- **Eintritt:** Benutzer anlegen → Nutzungsstandort (nötig vor der Lizenz) →
  Lizenz zuweisen (am besten gruppenbasiert) → in Gruppen aufnehmen →
  MFA-Registrierung bei der ersten Anmeldung.
- **Wechsel:** Gruppen/Abteilung ändern; Zugriff entziehen, der nicht mehr
  gebraucht wird.
- **Austritt:** Anmeldung sperren → Sitzungen widerrufen → Passwort
  zurücksetzen → Postfach in ein freigegebenes umwandeln oder Weiterleitung
  nach Richtlinie setzen → Lizenz entfernen → nach der Aufbewahrungsfrist
  löschen.

Dasselbe in Microsoft Graph PowerShell (dokumentiert, fiktive Werte):

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All","Group.ReadWrite.All"
Get-MgUser -Filter "startswith(displayName,'Julien')" | Select DisplayName,UserPrincipalName
Update-MgUser -UserId j.dupont@example.com -AccountEnabled:$false      # block sign-in
Revoke-MgUserSignInSession -UserId j.dupont@example.com
Get-MgSubscribedSku | Select SkuPartNumber,ConsumedUnits
```

### 3. Lizenzbegriffe

- Eine Lizenz (SKU, z. B. *Microsoft 365 Business Premium*) enthält
  Dienstpläne (Exchange Online, Teams, Intune, Entra ID P1 …).
- **Gruppenbasierte Lizenzierung** macht weniger Fehler: den Benutzer in
  `LIC_M365_BP` aufnehmen.
- Häufiger Helpdesk-Fall: „kein Postfach“ → Lizenz fehlt oder
  Nutzungsstandort ist nicht gesetzt.

### 4. MFA und Authentifizierung

- Lieber **Microsoft Authenticator** (Zahlenabgleich) oder
  **FIDO2/Passkeys** als SMS.
- **Sicherheitsstandards** (kostenlos) gegen **bedingten Zugriff** (Entra ID
  P1): Richtlinien wie „MFA für alle Benutzer“, „Legacyauthentifizierung
  sperren“, „konformes Gerät für Admins verlangen“.
- Immer **zwei Break-Glass-Konten** vom bedingten Zugriff ausnehmen, mit
  langen Passwörtern offline und überwachten Anmeldungen.
- **Selbstbedienungs-Kennwortzurücksetzung** lässt Benutzer ihr Passwort
  selbst zurücksetzen, nachdem sie die Identität nachgewiesen haben —
  weniger Tickets, aber nur sicher mit starken Registrierungsmethoden.

### 5. Helpdesk-Szenarien (in der Sandbox oder auf Papier)

| Szenario | Prüfungen |
|----------|-----------|
| Benutzer hat das Telefon mit Authenticator verloren | Identität außer Band prüfen → MFA neu registrieren lassen → Sitzungen widerrufen |
| „Zu viele Anmeldeversuche“ | Entra-Anmeldeprotokolle: Fehlergrund, IP, Ort, Client-App |
| Zugriff auf ein freigegebenes Postfach | Exchange Admin Center → Postfachdelegation (Vollzugriff / Senden als) |
| Verdächtige Anmeldung aus dem Ausland | Anmeldeprotokolle + riskante Benutzer → sperren, zurücksetzen, widerrufen, an den SOC eskalieren |
| Neueinstellung hat kein Teams | Lizenz zugewiesen? Dienstplan aktiv? Auf die Bereitstellung warten |

### 6. Admin-Rollen mit geringsten Rechten

Helpdesk-Agenten bekommen **Helpdesk Administrator** oder **User
Administrator**, nicht Global Administrator. **PIM** (Entra ID P2) für
Erhöhung nur bei Bedarf.

## Nachweise

- Screenshots aus Sandbox oder Test (Mandantennamen unkenntlich): Benutzer
  anlegen, Lizenz zuweisen, Richtlinie für bedingten Zugriff nur im
  Berichtsmodus, Eintrag im Anmeldeprotokoll.
- Oder: Abschlussabzeichen von Microsoft-Learn-Modulen.

## Was ich gelernt habe

_Noch von Lucas auszufüllen._
