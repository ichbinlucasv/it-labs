# Lab 02 — Windows troubleshooting runbook

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**Status:** Planned — written runbook. The scenarios have not been run yet. I do have a Windows 11 guest and a Server 2025 DC now (see [lab 06](../06-windows-domain/)). Next step is to break one thing on `win11-soc` and write down the fix.

## Goal

Build a repeatable, step-by-step runbook for the Windows incidents I would
handle most often at L1/L2, with the commands to use and how to read
their output.

## Setup

- Windows 11 VM (free evaluation / developer VM from Microsoft) in VirtualBox,
  VMware Workstation Player, or Hyper-V.
- Take a **snapshot** before each scenario so I can break things and roll back.
- Tools: built-in only — PowerShell, `cmd`, Event Viewer (`eventvwr.msc`),
  Services (`services.msc`), Task Manager, Resource Monitor, Reliability Monitor
  (`perfmon /rel`).

## Steps

### 0. General method

1. **Identify** — exact symptom, error text, since when, what changed.
2. **Scope** — one user/device or many? Reproducible?
3. **Hypothesis** — start with the simplest (cable, reboot, credentials).
4. **Test** — one change at a time; record each result in the ticket.
5. **Fix & verify** with the user.
6. **Document** — root cause + KB article.

### 1. No network / no internet

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

Read it: IP OK + gateway fails → local/switch; gateway OK + DNS fails → DNS;
DNS OK + 443 fails → proxy/firewall.

### 2. Slow computer

```powershell
Get-Process | Sort-Object CPU -Descending | Select -First 10 Name,CPU,WS
Get-CimInstance Win32_LogicalDisk | Select DeviceID,@{n='FreeGB';e={[math]::Round($_.FreeSpace/1GB,1)}}
Get-CimInstance Win32_StartupCommand | Select Name,Command
perfmon /rel                         # Reliability Monitor: crashes timeline
```

Check disk space (< 10 % free), startup items, pending updates, and unknown
processes (possible malware → escalate to Security, do not just kill it).

### 3. Application crashes / system errors

```powershell
Get-WinEvent -LogName Application -MaxEvents 50 |
  Where-Object LevelDisplayName -eq 'Error' | ft TimeCreated,ProviderName,Id -Auto
sfc /scannow
DISM /Online /Cleanup-Image /RestoreHealth
```

### 4. Account locked / logon problems

```powershell
whoami /all                          # groups & privileges of current session
nltest /dsgetdc:corp.example.com     # can the PC find a domain controller?
w32tm /query /status                 # time skew > 5 min breaks Kerberos
gpresult /r                          # applied GPOs
```

Security log events worth knowing: **4624** successful logon, **4625** failed
logon, **4740** account locked out (on DC), **4771** Kerberos pre-auth failed.

### 5. Printer problems

```powershell
Get-Printer | ft Name,PrinterStatus,PortName
Restart-Service Spooler
Get-PrintJob -PrinterName "PRN-F2-01" | Remove-PrintJob
```

### 6. Windows Update failing

```powershell
Get-WindowsUpdateLog                 # writes WindowsUpdate.log to Desktop
Stop-Service wuauserv,bits
Rename-Item C:\Windows\SoftwareDistribution SoftwareDistribution.old
Start-Service wuauserv,bits
```

### 7. BitLocker recovery prompt

- Verify identity of the user per procedure, then retrieve the recovery key
  from AD / Entra ID (never from an email or chat message).
- `manage-bde -status C:` after boot; investigate why (BIOS update, TPM
  change) and record it in the ticket.

## Evidence

- Screenshots of `ipconfig /all` before/after for scenario 1 (break it by
  setting a wrong static DNS in the VM).
- Event Viewer filtered view showing 4625/4740 events after deliberately
  failing logons on a test account.
- Output of `sfc /scannow` completion.

## What I learned

_To be completed by Lucas._
