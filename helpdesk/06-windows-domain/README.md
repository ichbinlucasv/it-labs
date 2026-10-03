# Lab 06 — Windows Server domain on my PC

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**Status:** In progress — `win11-soc` is in `lab.local` (checked 4 Oct 2026). A helpdesk password reset is written up. An unlock is still open because the lockout threshold is 0.

## Goal

Have one Windows domain I built myself, on the same PC I use for Linux,
so I can practise helpdesk and AD without a second machine. Samba
([lab 04](../04-samba-ad-lab/)) is a different domain. This one is
Windows Server.

## Setup

Host: my Linux PC, libvirt, NAT `192.168.122.0/24`.

| Guest | Role | Address |
| --- | --- | --- |
| `dc01` | Windows Server 2025 eval, AD DS | 192.168.122.10 |
| `win11-soc` | Windows 11 Enterprise eval | 192.168.122.20 |

Domain `lab.local`, NetBIOS `LAB`. DNS on the DC is itself, then the
libvirt gateway `192.168.122.1`.

OUs: Admins, Helpdesk, SOC, Staff, Workstations, Servers, Service
Accounts, Disabled.

Accounts that showed up in the inventory: a domain admin, `helpdesk`,
`soc.analyst`, three staff users, two service accounts. `helpdesk` is in
Helpdesk-T1 and Password-Reset. `soc.analyst` is in SOC-Analysts. I am
not putting the passwords in git.

ADUC (`dsa.msc`) and GPMC are on the DC. Defender was running. Sysmon,
Wireshark, Hayabusa and the rest of the SOC tool list were **not** on
the DC when I looked. Those belong on `win11-soc`. The 4 Oct 2026 check
of that guest covered the domain, DNS, RSAT, gpresult, and one helpdesk
reset. It did not inventory those SOC tools.

## Steps

What is already done:

1. Install Server 2025 evaluation as `dc01`.
2. Promote it. Forest `lab.local`. Confirmed 5 Sep 2026 (`SETUP_DONE`
   on the guest).
3. Create the OUs, the helpdesk and SOC groups, and the lab users.
4. Inventory over the guest agent on 7 Sep 2026. NTDS, DNS, ADWS and
   Netlogon were running. Output: [`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt).

Checked on 4 Oct 2026, both guests on. Output:
[`evidence/win11-2026-10-04.txt`](evidence/win11-2026-10-04.txt).

1. `win11-soc` was already in `lab.local`. Computer object
   `CN=WIN11-SOC,OU=Workstations,DC=lab,DC=local`. Ethernet
   `192.168.122.20`, DNS `192.168.122.10` then `192.168.122.1`.
   RSAT Active Directory tools are installed. I did not have to join it.
2. From that client I reset `jdoe` with the helpdesk credential, not
   the domain admin. `jdoe` cannot reset `asmith` (access denied).
   Helpdesk can. `PasswordLastSet` moved from 5 Sep 2026 19:26:49 to
   4 Oct 2026 00:56:55 on the guest clock. I then put the lab password
   back (00:57:36). The password is not in git. The guest-agent
   process is `NT AUTHORITY\SYSTEM`. This was not a desktop sign-in
   as helpdesk.
3. Computer policy on `win11-soc` came from `DC01.lab.local`. Applied:
   Default Domain Policy, Lab-Logon-Banner, Lab-PowerShell-Logging,
   Lab-Region-Keyboard. `Lab-Workstation-Hardening` is linked on
   `OU=Workstations` and enabled, and the GPO report has no settings
   (`ExtensionData=0`). I expected a hardening setting. There is not
   one in that GPO. That is the ticket below.
4. Domain lockout threshold is 0. `Search-ADAccount -LockedOut` cannot
   show a locked lab user until I set a threshold. I did not fake an
   unlock.

## Ticket from this check

`Lab-Workstation-Hardening` is linked to the workstation OU and looks
enabled. `gpresult /SCOPE COMPUTER /R` on `WIN11-SOC` does not apply it.
`Get-GPOReport` for it has no extension data. `Lab-Logon-Banner` does,
and gpresult lists that one. I left the empty GPO as it is. Filling it
with a guess would make the lab look finished.

Filled in the ticket shape:
[`evidence/HD-2026-10-04.md`](evidence/HD-2026-10-04.md).
The helpdesk reset and the domain check are the same night:
[`evidence/session-2026-10-04.md`](evidence/session-2026-10-04.md),
[`evidence/domain-2026-10-04.md`](evidence/domain-2026-10-04.md).

## Evidence

[`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt) is the
inventory. Short version:

- OS: Windows Server 2025 Datacenter Evaluation, build 26100
- `PartOfDomain=True`, domain and forest `lab.local`
- IPv4 `192.168.122.10`, DNS `127.0.0.1`, `192.168.122.1`
- NTDS, DNS, Netlogon, ADWS, WinDefend: running
- ADUC and GPMC present
- `SETUP_DONE` timestamp: 2026-09-05T19:26:49+02:00

[`evidence/win11-2026-10-04.txt`](evidence/win11-2026-10-04.txt) is the
4 Oct 2026 check of `win11-soc`, the GPO links, and the helpdesk reset.

## What I learned

Promoting the DC is the easy part. The useful check is the boring one:
the client is in the right OU, DNS points at the DC, helpdesk can reset
a staff password, and a staff user cannot reset someone else.

A linked GPO is not a setting. `Lab-Workstation-Hardening` is linked and
empty. I would have told a user the hardening was on. gpresult says it
is not.

Lockout threshold 0 means I still cannot practise an unlock. I will
not write an unlock I did not do. An interactive sign-in as helpdesk
on the desktop is the next session. The reset above used the helpdesk
credential from the guest agent.

I also learned to keep two labs apart. `lab.local` here is Windows
Server on `192.168.122.0/24`. The Samba lab is `corp.example.com` in a
container. Mixing them in one write-up would make both look finished.
They are not.
