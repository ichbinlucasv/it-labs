# Lab 02 — Runbook de dépannage Windows

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Planned — runbook écrit. Je n'ai pas encore joué les scénarios. J'ai maintenant un invité Windows 11 et un DC Server 2025 (voir [lab 06](../06-windows-domain/)). Prochaine étape : casser une chose sur `win11-soc` et noter le correctif.

## Objectif

Un runbook reproductible, étape par étape, pour les incidents Windows que
je traiterais le plus souvent en N1/N2, avec les commandes à utiliser et
comment lire leur sortie.

## Mise en place

- VM Windows 11 (évaluation gratuite / VM développeur Microsoft) dans VirtualBox,
  VMware Workstation Player ou Hyper-V.
- Prendre un **snapshot** avant chaque scénario pour pouvoir casser et revenir
  en arrière.
- Outils : uniquement ceux du système — PowerShell, `cmd`, Observateur
  d'événements (`eventvwr.msc`), Services (`services.msc`), Gestionnaire des
  tâches, Moniteur de ressources, Moniteur de fiabilité (`perfmon /rel`).

## Étapes

### 0. Méthode générale

1. **Identifier** — symptôme exact, texte de l'erreur, depuis quand, ce qui a changé.
2. **Périmètre** — un utilisateur ou un poste, ou plusieurs ? Reproductible ?
3. **Hypothèse** — commencer par le plus simple (câble, redémarrage, identifiants).
4. **Tester** — un changement à la fois ; noter chaque résultat dans le ticket.
5. **Corriger et vérifier** avec l'utilisateur.
6. **Documenter** — cause racine + article de KB.

### 1. Pas de réseau / pas d'Internet

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

Lecture : IP correcte + passerelle en échec → local/commutateur ; passerelle
correcte + DNS en échec → DNS ; DNS correct + 443 en échec → proxy/pare-feu.

### 2. Ordinateur lent

```powershell
Get-Process | Sort-Object CPU -Descending | Select -First 10 Name,CPU,WS
Get-CimInstance Win32_LogicalDisk | Select DeviceID,@{n='FreeGB';e={[math]::Round($_.FreeSpace/1GB,1)}}
Get-CimInstance Win32_StartupCommand | Select Name,Command
perfmon /rel                         # Reliability Monitor: crashes timeline
```

Vérifier l'espace disque (< 10 % libre), les programmes au démarrage, les
mises à jour en attente et les processus inconnus (malware possible →
escalader vers Security, ne pas se contenter de tuer le processus).

### 3. Plantages d'application / erreurs système

```powershell
Get-WinEvent -LogName Application -MaxEvents 50 |
  Where-Object LevelDisplayName -eq 'Error' | ft TimeCreated,ProviderName,Id -Auto
sfc /scannow
DISM /Online /Cleanup-Image /RestoreHealth
```

### 4. Compte verrouillé / problèmes d'ouverture de session

```powershell
whoami /all                          # groups & privileges of current session
nltest /dsgetdc:corp.example.com     # can the PC find a domain controller?
w32tm /query /status                 # time skew > 5 min breaks Kerberos
gpresult /r                          # applied GPOs
```

Événements du journal Sécurité à connaître : **4624** ouverture de session
réussie, **4625** ouverture de session échouée, **4740** compte verrouillé
(sur le DC), **4771** pré-authentification Kerberos échouée.

### 5. Problèmes d'imprimante

```powershell
Get-Printer | ft Name,PrinterStatus,PortName
Restart-Service Spooler
Get-PrintJob -PrinterName "PRN-F2-01" | Remove-PrintJob
```

### 6. Échec de Windows Update

```powershell
Get-WindowsUpdateLog                 # writes WindowsUpdate.log to Desktop
Stop-Service wuauserv,bits
Rename-Item C:\Windows\SoftwareDistribution SoftwareDistribution.old
Start-Service wuauserv,bits
```

### 7. Invite de récupération BitLocker

- Vérifier l'identité de l'utilisateur selon la procédure, puis récupérer la
  clé de récupération dans l'AD / Entra ID (jamais depuis un e-mail ou un
  message de chat).
- `manage-bde -status C:` après le démarrage ; chercher pourquoi (mise à jour
  du BIOS, changement de TPM) et le noter dans le ticket.

## Preuves

- Captures de `ipconfig /all` avant/après pour le scénario 1 (le casser en
  mettant un mauvais DNS statique dans la VM).
- Vue filtrée de l'Observateur d'événements montrant des événements 4625/4740
  après des ouvertures de session ratées volontairement sur un compte de test.
- Sortie de `sfc /scannow` une fois terminé.

## Ce que j'ai appris

_À compléter par Lucas._
