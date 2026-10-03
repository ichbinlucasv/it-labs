# Passwort zurücksetzen oder entsperren

[English](password-reset.md) · [Français](password-reset.fr.md) · **Deutsch**

```text
Ticket:
Konto:
Anrufer:
Wie ich den Anrufer geprüft habe:
    [ ] Rückruf auf die Nummer am Konto
    [ ] Vorgesetzter auf einer bekannten Nummer
    [ ] persönlich, ich kenne die Person
    [ ] habe ich nicht, also habe ich aufgehört

Vorher:
- LockedOut:
- PasswordExpired:
- Enabled:
- OU:

Aktion:
- [ ] Nur Unlock-ADAccount
- [ ] Zurücksetzen, ChangePasswordAtLogon = true
- [ ] Konto stattdessen deaktiviert (Verdacht auf Missbrauch)

Temporäres Geheimnis im Ticket gespeichert?  NEIN

Danach:
- Benutzer hat sich angemeldet?  ja / nein
- Hat die Person das Passwort selbst geändert?  ja / nein / noch nicht

Befehl, den ich getippt habe (kein Geheimnis darin):
```

Laborübung, auf `lab.local`, Helpdesk-Konto, nur OU Staff:

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, PasswordExpired, Enabled, MemberOf
Unlock-ADAccount jdoe
```

Das Reset-Cmdlet schlage ich noch nach. Wenn ich es tippen kann, lösche ich
diese Erinnerung aus meiner eigenen Kopie. Bis dahin bleibt sie.
