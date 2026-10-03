# PowerShell

[English](powershell.md) · [Français](powershell.fr.md) · **Deutsch**

Ich nutze es für das Windows-Lab. Benutzer, Sperren, ein Ereignis, „erreicht
dieser PC den DC“.

Ich übe als `helpdesk`, wenn die Aufgabe ein Benutzer ist. Domänen-Admin
ist für den Aufbau des Labs da, danach melde ich mich davon ab.

## 25 Minuten

1. 15 Min. Die vier Befehle unten, auf `dc01` oder auf `win11-soc`, sobald
   `win11-soc` beigetreten ist. Ich tippe sie.
2. 10 Min. Ich fülle [password-reset.md](../helpdesk/password-reset.md) oder
   [cant-log-on.md](../helpdesk/cant-log-on.md) anhand der Ausgabe.

## Die tippe ich, bis es sitzt

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, PasswordExpired, Enabled, DistinguishedName, MemberOf

Search-ADAccount -LockedOut | Select-Object Name, SamAccountName

Get-ADComputer -Filter * -Properties OperatingSystem |
  Select-Object Name, OperatingSystem

Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddHours(-4)} -MaxEvents 20 |
  Select-Object TimeCreated, Id, Message
```

Vom Client aus, nicht aus der Erinnerung an die IP:

```powershell
Test-NetConnection dc01.lab.local -Port 389
Resolve-DnsName lab.local
```

`Get-WinEvent` kann in einem ruhigen Lab nichts zurückgeben. „Keine
Ereignisse“ ist eine Antwort. Das schreibe ich hin. Ich lockere den Filter
nicht, bevor ich den ersten verstanden habe.

## Übung

Ich nehme eine 4625 oder eine fehlgeschlagene Anmeldung aus dem Lab. Ich
schreibe: Konto, Zeit des Fehlers, Quelle. Ist die Meldung zu lang, kopiere
ich die drei Zeilen, die die Frage beantwortet haben.

## Das verwechsle ich noch

- `SamAccountName` und UPN
- Entsperren gegen Zurücksetzen
- `Get-EventLog`, wonach ich nicht mehr greifen sollte. `Get-WinEvent` ist
  der richtige.
