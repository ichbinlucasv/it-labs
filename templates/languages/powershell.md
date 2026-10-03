# PowerShell

What I use it for: the Windows lab. Users, lockouts, one event, "can this
PC reach the DC".

I practise as `helpdesk` when the task is a user. Domain admin is for
building the lab, then I log off it.

## 25 minutes

1. 15 min. The four commands below, on `dc01` or `win11-soc` once it is
   joined. Type them.
2. 10 min. Fill [password-reset.md](../helpdesk/password-reset.md) or
   [cant-log-on.md](../helpdesk/cant-log-on.md) from the output.

## Type these until they stick

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, PasswordExpired, Enabled, DistinguishedName, MemberOf

Search-ADAccount -LockedOut | Select-Object Name, SamAccountName

Get-ADComputer -Filter * -Properties OperatingSystem |
  Select-Object Name, OperatingSystem

Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddHours(-4)} -MaxEvents 20 |
  Select-Object TimeCreated, Id, Message
```

From the client, not from memory of the IP:

```powershell
Test-NetConnection dc01.lab.local -Port 389
Resolve-DnsName lab.local
```

`Get-WinEvent` on a quiet lab may return nothing. "No events" is an answer.
I write that down. I do not loosen the filter until I understand the first one.

## Exercise

Pick one 4625 or one failed lab logon. Write: account, failure time, source.
If the message is too long, copy the three lines that answered the question.

## I still mix up

- `SamAccountName` and UPN
- unlocking versus resetting
- `Get-EventLog`, which I should stop reaching for. `Get-WinEvent` is the one.
