# Lab 02 — Runbook zur Windows-Fehleranalyse

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Planned — Runbook geschrieben. Die Szenarien habe ich noch nicht ausgeführt. Ich habe jetzt einen Windows-11-Gast und einen Server-2025-DC (siehe [Lab 06](../06-windows-domain/)). Nächster Schritt: auf `win11-soc` eine Sache kaputt machen und den Fix aufschreiben.

## Ziel

Ein wiederholbares Runbook, Schritt für Schritt, für die Windows-Incidents,
die ich in Stufe 1/2 am häufigsten bearbeiten würde, mit den Befehlen und
damit, wie ich ihre Ausgabe lese.

## Aufbau

- Windows-11-VM (kostenlose Evaluierung / Entwickler-VM von Microsoft) in
  VirtualBox, VMware Workstation Player oder Hyper-V.
- Vor jedem Szenario einen **Snapshot**, damit ich etwas kaputt machen und
  zurückrollen kann.
- Werkzeuge: nur mitgelieferte — PowerShell, `cmd`, Ereignisanzeige
  (`eventvwr.msc`), Dienste (`services.msc`), Task-Manager, Ressourcenmonitor,
  Zuverlässigkeitsüberwachung (`perfmon /rel`).

## Schritte

### 0. Allgemeine Methode

1. **Feststellen** — genaues Symptom, Fehlertext, seit wann, was sich geändert hat.
2. **Umfang** — ein Benutzer/Gerät oder viele? Reproduzierbar?
3. **Hypothese** — mit dem Einfachsten anfangen (Kabel, Neustart, Anmeldedaten).
4. **Testen** — eine Änderung nach der anderen; jedes Ergebnis ins Ticket.
5. **Beheben und prüfen** mit dem Benutzer.
6. **Dokumentieren** — Ursache + KB-Artikel.

### 1. Kein Netz / kein Internet

```powershell
ipconfig /all                        # APIPA 169.254.x.x = no DHCP answer
Get-NetAdapter | ft Name,Status,LinkSpeed
Test-NetConnection 10.20.30.1        # gateway (lab LAN)
Test-NetConnection example.com -Port 443
Resolve-DnsName example.com          # DNS works?
ipconfig /release; ipconfig /renew
ipconfig /flushdns
netsh winsock reset                  # last resort, needs reboot
```

Lesen: IP in Ordnung + Gateway schlägt fehl → lokal/Switch; Gateway in
Ordnung + DNS schlägt fehl → DNS; DNS in Ordnung + 443 schlägt fehl →
Proxy/Firewall.

### 2. Langsamer Rechner

```powershell
Get-Process | Sort-Object CPU -Descending | Select -First 10 Name,CPU,WS
Get-CimInstance Win32_LogicalDisk | Select DeviceID,@{n='FreeGB';e={[math]::Round($_.FreeSpace/1GB,1)}}
Get-CimInstance Win32_StartupCommand | Select Name,Command
perfmon /rel                         # Reliability Monitor: crashes timeline
```

Plattenplatz prüfen (< 10 % frei), Autostart, ausstehende Updates und
unbekannte Prozesse (möglicher Schadcode → an Security eskalieren, nicht
nur beenden).

### 3. Anwendungsabstürze / Systemfehler

```powershell
Get-WinEvent -LogName Application -MaxEvents 50 |
  Where-Object LevelDisplayName -eq 'Error' | ft TimeCreated,ProviderName,Id -Auto
sfc /scannow
DISM /Online /Cleanup-Image /RestoreHealth
```

### 4. Konto gesperrt / Anmeldeprobleme

```powershell
whoami /all                          # groups & privileges of current session
nltest /dsgetdc:corp.example.com     # can the PC find a domain controller?
w32tm /query /status                 # time skew > 5 min breaks Kerberos
gpresult /r                          # applied GPOs
```

Ereignisse im Sicherheitsprotokoll, die ich kennen sollte: **4624** Anmeldung
erfolgreich, **4625** Anmeldung fehlgeschlagen, **4740** Konto gesperrt (auf
dem DC), **4771** Kerberos-Vorauthentifizierung fehlgeschlagen.

### 5. Druckerprobleme

```powershell
Get-Printer | ft Name,PrinterStatus,PortName
Restart-Service Spooler
Get-PrintJob -PrinterName "PRN-F2-01" | Remove-PrintJob
```

### 6. Windows Update schlägt fehl

```powershell
Get-WindowsUpdateLog                 # writes WindowsUpdate.log to Desktop
Stop-Service wuauserv,bits
Rename-Item C:\Windows\SoftwareDistribution SoftwareDistribution.old
Start-Service wuauserv,bits
```

### 7. BitLocker-Wiederherstellungsabfrage

- Identität des Benutzers nach Verfahren prüfen, dann den
  Wiederherstellungsschlüssel aus AD / Entra ID holen (nie aus einer E-Mail
  oder einer Chat-Nachricht).
- `manage-bde -status C:` nach dem Start; klären, warum (BIOS-Update,
  TPM-Wechsel), und es ins Ticket schreiben.

## Nachweise

- Screenshots von `ipconfig /all` vorher/nachher für Szenario 1 (kaputt
  machen, indem in der VM ein falscher statischer DNS steht).
- Gefilterte Ansicht der Ereignisanzeige mit Ereignissen 4625/4740 nach
  absichtlich fehlgeschlagenen Anmeldungen an einem Testkonto.
- Ausgabe von `sfc /scannow` nach Abschluss.

## Was ich gelernt habe

_Noch von Lucas auszufüllen._
