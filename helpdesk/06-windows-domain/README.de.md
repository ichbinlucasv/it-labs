# Lab 06 — Windows-Server-Domäne auf meinem PC

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** In progress — `win11-soc` ist in `lab.local` (geprüft am 4. Okt. 2026). Ein Helpdesk-Passwortreset ist aufgeschrieben. Eine Entsperrung ist noch offen, weil die Sperrschwelle 0 ist.

## Ziel

Eine Windows-Domäne, die ich selbst gebaut habe, auf demselben PC, den ich
für Linux nutze, damit ich Helpdesk und AD üben kann ohne einen zweiten
Rechner. Samba ([Lab 04](../04-samba-ad-lab/)) ist eine andere Domäne. Diese
hier ist Windows Server.

## Aufbau

Host: mein Linux-PC, libvirt, NAT `192.168.122.0/24`.

| Gast | Rolle | Adresse |
| --- | --- | --- |
| `dc01` | Windows Server 2025 Evaluierung, AD DS | 192.168.122.10 |
| `win11-soc` | Windows 11 Enterprise Evaluierung | 192.168.122.20 |

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
dem DC, als ich nachgesehen habe. Die gehören auf `win11-soc`. Die Prüfung
vom 4. Okt. 2026 an diesem Gast hat Domäne, DNS, RSAT, gpresult und einen
Helpdesk-Reset abgedeckt. Die SOC-Werkzeuge habe ich dabei nicht
inventarisiert.

## Schritte

Was schon erledigt ist:

1. Server 2025 Evaluierung als `dc01` installieren.
2. Heraufstufen. Gesamtstruktur `lab.local`. Bestätigt am 5. September 2026
   (`SETUP_DONE` auf dem Gast).
3. Die OUs, die Helpdesk- und SOC-Gruppen und die Lab-Benutzer anlegen.
4. Inventar über den Gast-Agenten am 7. September 2026. NTDS, DNS, ADWS und
   Netlogon liefen. Ausgabe: [`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt).

Geprüft am 4. Okt. 2026, beide Gäste an. Ausgabe:
[`evidence/win11-2026-10-04.txt`](evidence/win11-2026-10-04.txt).

1. `win11-soc` war schon in `lab.local`. Computerobjekt
   `CN=WIN11-SOC,OU=Workstations,DC=lab,DC=local`. Ethernet
   `192.168.122.20`, DNS `192.168.122.10` und dann `192.168.122.1`.
   Die RSAT-Active-Directory-Werkzeuge sind installiert. Aufnehmen
   musste ich ihn nicht.
2. Von diesem Client habe ich `jdoe` mit dem Helpdesk-Credential
   zurückgesetzt, nicht mit dem Domänenadmin. `jdoe` kann `asmith`
   nicht zurücksetzen (Zugriff verweigert). Helpdesk kann es.
   `PasswordLastSet` ging von 5. Sep. 2026 19:26:49 auf 4. Okt. 2026
   00:56:55, Uhr des Gasts. Danach habe ich das Lab-Passwort zurückgesetzt
   (00:57:36). Das Passwort steht nicht in git. Der Prozess des
   Gast-Agents ist `NT AUTHORITY\SYSTEM`. Das war keine
   Desktop-Anmeldung als Helpdesk.
3. Die Computerrichtlinie auf `win11-soc` kam von `DC01.lab.local`.
   Angewendet: Default Domain Policy, Lab-Logon-Banner,
   Lab-PowerShell-Logging, Lab-Region-Keyboard.
   `Lab-Workstation-Hardening` ist an `OU=Workstations` verknüpft und
   aktiv, und der GPO-Bericht hat keine Einstellung (`ExtensionData=0`).
   Ich hatte eine Härtung erwartet. In dieser GPO ist keine.
4. Die Domänen-Sperrschwelle ist 0. Ich kann keinen gesperrten
   Lab-Benutzer zeigen, bis ich eine Schwelle setze. Eine Entsperrung
   habe ich nicht erfunden.

## Ticket aus dieser Prüfung

`Lab-Workstation-Hardening` ist an die Workstation-OU verknüpft und
sieht aktiv aus. `gpresult /SCOPE COMPUTER /R` auf `WIN11-SOC` wendet
sie nicht an. `Get-GPOReport` hat keine Extension-Daten.
`Lab-Logon-Banner` hat welche, und gpresult listet sie. Die leere GPO
habe ich gelassen. Sie mit einer Vermutung zu füllen würde das Lab
fertig aussehen lassen.

Ausgefüllt in der Ticketform:
[`evidence/HD-2026-10-04.de.md`](evidence/HD-2026-10-04.de.md).
Helpdesk-Reset und Domänenprüfung sind dieselbe Nacht:
[`evidence/session-2026-10-04.de.md`](evidence/session-2026-10-04.de.md),
[`evidence/domain-2026-10-04.de.md`](evidence/domain-2026-10-04.de.md).

## Nachweise

[`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt) ist das
Inventar. Kurzfassung:

- OS: Windows Server 2025 Datacenter Evaluation, Build 26100
- `PartOfDomain=True`, Domäne und Gesamtstruktur `lab.local`
- IPv4 `192.168.122.10`, DNS `127.0.0.1`, `192.168.122.1`
- NTDS, DNS, Netlogon, ADWS, WinDefend: läuft
- ADUC und GPMC vorhanden
- Zeitstempel `SETUP_DONE`: 2026-09-05T19:26:49+02:00

[`evidence/win11-2026-10-04.txt`](evidence/win11-2026-10-04.txt) ist die
Prüfung vom 4. Okt. 2026 von `win11-soc`, den GPO-Links und dem
Helpdesk-Reset.

## Was ich gelernt habe

Den DC heraufzustufen ist der leichte Teil. Die nützliche Prüfung ist
die langweilige: der Client steht in der richtigen OU, DNS zeigt auf
den DC, Helpdesk kann ein Staff-Passwort zurücksetzen, und ein
Staff-Benutzer kann niemand anderen zurücksetzen.

Eine verknüpfte GPO ist keine Einstellung. `Lab-Workstation-Hardening`
ist verknüpft und leer. Ich hätte einer Person gesagt, die Härtung sei
an. gpresult sagt nein.

Sperrschwelle 0 heisst, ich kann eine Entsperrung noch nicht üben.
Eine Entsperrung, die ich nicht gemacht habe, schreibe ich nicht auf.
Eine interaktive Anmeldung als Helpdesk am Desktop ist die nächste
Sitzung. Der Reset oben hat das Helpdesk-Credential über den Gast-Agent
benutzt.

Ich habe auch gelernt, zwei Labs auseinanderzuhalten. `lab.local` hier ist
Windows Server auf `192.168.122.0/24`. Das Samba-Lab ist `corp.example.com`
in einem Container. Beides in einem Bericht zu vermischen würde so tun, als
wären beide fertig. Sind sie nicht.
