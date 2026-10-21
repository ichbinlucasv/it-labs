# Lab 02 — Windows troubleshooting runbook

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**Status:** Done — failed-logon triage and a DNS break/fix both run from this repo. `sfc`, DISM, BitLocker, and the print spooler were not executed: there is no Windows guest in this environment.

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

### Runnable checks (no Windows required)

Scenario 4, on a synthetic Security export (fictional accounts, documentation addresses):

```bash
python3 triage.py --check
```

Scenario 1, reduced to the DNS decision in the runbook. A resolver on
`127.0.0.1` is down, then it answers `example.com` and NXDOMAIN for anything else:

```bash
bash dns-break.sh
```

`sfc /scannow`, DISM, BitLocker recovery, and `Restart-Service Spooler` still
need a Windows machine. The commands stay in the steps above as the runbook.

## Evidence

- [`samples/security-events.synthetic.jsonl`](samples/security-events.synthetic.jsonl) — five 4625s, one 4740, one 4771, one 4624, one later mistype.
- `python3 triage.py` prints the lockout of `a.martin` from `203.0.113.45` and separates it from `j.doe`'s successful lab logon.
- `dns-break.sh` shows `dig` failing, then `example.com` → `203.0.113.10`, then NXDOMAIN.

## What I learned

- Five bad passwords and a 4740 are the ticket. A later 4624 for a different user on the lab LAN is not part of that lockout.
- 4771 status `0x18` is a wrong Kerberos password on the DC, which is a different queue from a local 4625.
- Unlocking without finding the source that keeps retrying just locks the account again. The runbook says that; the sample is there so the sentence has events under it.
- When the path to the resolver is the thing that fails, fixing DNS is the test. The lab resolver answers only `example.com`, so a second name (NXDOMAIN) proves the service is up.
