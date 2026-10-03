# PowerShell

[English](powershell.md) · **Français** · [Deutsch](powershell.de.md)

Je m'en sers pour le lab Windows. Utilisateurs, verrouillages, un
événement, « est-ce que ce PC atteint le DC ».

Je m'exerce en `helpdesk` quand la tâche est un utilisateur. L'admin du
domaine sert à construire le lab, ensuite je quitte cette session.

## 25 minutes

1. 15 min. Les quatre commandes ci-dessous, sur `dc01` ou sur `win11-soc`
   une fois celui-ci joint au domaine. Je les tape.
2. 10 min. Je remplis [password-reset.md](../helpdesk/password-reset.md) ou
   [cant-log-on.md](../helpdesk/cant-log-on.md) à partir de la sortie.

## Je les retape jusqu'à ce que ça tienne

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, PasswordExpired, Enabled, DistinguishedName, MemberOf

Search-ADAccount -LockedOut | Select-Object Name, SamAccountName

Get-ADComputer -Filter * -Properties OperatingSystem |
  Select-Object Name, OperatingSystem

Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddHours(-4)} -MaxEvents 20 |
  Select-Object TimeCreated, Id, Message
```

Depuis le client, pas depuis le souvenir de l'IP :

```powershell
Test-NetConnection dc01.lab.local -Port 389
Resolve-DnsName lab.local
```

`Get-WinEvent`, sur un lab calme, peut ne rien renvoyer. « Aucun
événement » est une réponse. Je l'écris. Je n'élargis pas le filtre avant
d'avoir compris le premier.

## Exercice

J'en prends un : un 4625, ou une ouverture de session échouée dans le lab.
J'écris : compte, heure de l'échec, source. Si le message est trop long, je
copie les trois lignes qui ont répondu à la question.

## Je mélange encore

- `SamAccountName` et le UPN
- déverrouiller, contre réinitialiser
- `Get-EventLog`, que je dois arrêter d'attraper. `Get-WinEvent` est le bon.
