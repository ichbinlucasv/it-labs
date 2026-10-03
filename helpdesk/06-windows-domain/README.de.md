# Lab 06 — Windows-Server-Domäne auf meinem PC

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** In progress — der Domänencontroller ist echt. Eine Helpdesk-Sitzung auf dem Windows-11-Client ist noch nicht aufgeschrieben.

## Ziel

Eine Windows-Domäne, die ich selbst gebaut habe, auf demselben PC, den ich
für Linux nutze, damit ich Helpdesk und AD üben kann ohne einen zweiten
Rechner. Samba ([Lab 04](../04-samba-ad-lab/)) ist eine andere Domäne. Diese
hier ist Windows Server.

## Aufbau

Host: mein Linux-PC, libvirt, NAT `192.168.122.0/24`.

| Gast | Rolle | RAM | vCPU | Adresse |
| --- | --- | --- | --- | --- |
| `dc01` | Windows Server 2025 Evaluierung, AD DS | 8 GB | 4 | 192.168.122.10 |
| `win11-soc` | Windows 11 Enterprise Evaluierung | 32 GB | 8 | 192.168.122.20 |

Domäne `lab.local`, NetBIOS `LAB`. DNS auf dem DC ist er selbst, danach das
libvirt-Gateway `192.168.122.1`.

OUs: Admins, Helpdesk, SOC, Staff, Workstations, Servers, Service
Accounts, Disabled.

Konten, die im Inventar standen: ein Domänenadmin, `helpdesk`,
`soc.analyst`, drei Staff-Benutzer, zwei Dienstkonten. `helpdesk` ist in
Helpdesk-T1 und Password-Reset. `soc.analyst` ist in SOC-Analysts. Die
Passwörter kommen nicht ins Git.

ADUC (`dsa.msc`) und GPMC liegen auf dem DC. Defender lief. Sysmon,
Wireshark, Hayabusa und der Rest der SOC-Werkzeugliste waren **nicht** auf
dem DC, als ich nachgesehen habe. Die gehören auf `win11-soc`, und diesen
Gast habe ich seit dem Aufbau nicht wieder geprüft.

## Schritte

Was schon erledigt ist:

1. Server 2025 Evaluierung als `dc01` installieren.
2. Heraufstufen. Gesamtstruktur `lab.local`. Bestätigt am 5. September 2026
   (`SETUP_DONE` auf dem Gast).
3. Die OUs, die Helpdesk- und SOC-Gruppen und die Lab-Benutzer anlegen.
4. Inventar über den Gast-Agenten am 7. September 2026. NTDS, DNS, ADWS und
   Netlogon liefen. Ausgabe: [`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt).

Was ich noch machen muss, und hier aufschreibe, wenn ich es mache:

1. Beide Gäste einschalten. Prüfen, ob `win11-soc` in der Domäne ist. Wenn
   nicht, aufnehmen und das hier hinschreiben.
2. Vom Windows-11-Client aus, mit dem Helpdesk-Konto, ein Staff-Passwort
   zurücksetzen und ein Konto entsperren. Nicht mit dem Domänenadmin.
3. GPMC öffnen und eine GPO nennen, die greift, und eine Stelle, an der ich
   eine Einstellung erwartet und nicht gefunden habe.
4. Eine PowerShell-Prüfung aus dem Kopf laufen lassen, dann korrigieren, was
   ich falsch hatte:

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, MemberOf
Search-ADAccount -LockedOut
```

## Nachweise

[`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt) ist das
Inventar. Kurzfassung:

- OS: Windows Server 2025 Datacenter Evaluation, Build 26100
- `PartOfDomain=True`, Domäne und Gesamtstruktur `lab.local`
- IPv4 `192.168.122.10`, DNS `127.0.0.1`, `192.168.122.1`
- NTDS, DNS, Netlogon, ADWS, WinDefend: läuft
- ADUC und GPMC vorhanden
- Zeitstempel `SETUP_DONE`: 2026-09-05T19:26:49+02:00

Der Windows-11-Gast existiert in libvirt und war ausgeschaltet, als ich das
letzte Mal nachgesehen habe. Ich habe kein Inventar davon, also behaupte ich
nicht, dass er in der Domäne ist.

## Was ich gelernt habe

Den DC heraufzustufen ist der leichte Teil. Die nützliche Übung ist die
langweilige Wiederholung danach: den Benutzer finden, das Passwort
zurücksetzen, die Gruppe prüfen, als Helpdesk, nicht als Admin. Ich habe
die Domäne. Diese Wiederholung habe ich noch nicht aufgeschrieben.

Ich habe auch gelernt, zwei Labs auseinanderzuhalten. `lab.local` hier ist
Windows Server auf `192.168.122.0/24`. Das Samba-Lab ist `corp.example.com`
in einem Container. Beides in einem Bericht zu vermischen würde so tun, als
wären beide fertig. Sind sie nicht.
