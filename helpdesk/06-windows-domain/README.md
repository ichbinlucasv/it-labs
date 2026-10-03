# Lab 06 — Windows Server domain on my PC

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**Status:** In progress — the domain controller is real. A helpdesk session on the Windows 11 client is not written up yet.

## Goal

Have one Windows domain I built myself, on the same PC I use for Linux,
so I can practise helpdesk and AD without a second machine. Samba
([lab 04](../04-samba-ad-lab/)) is a different domain. This one is
Windows Server.

## Setup

Host: my Linux PC, libvirt, NAT `192.168.122.0/24`.

| Guest | Role | RAM | vCPU | Address |
| --- | --- | --- | --- | --- |
| `dc01` | Windows Server 2025 eval, AD DS | 8 GB | 4 | 192.168.122.10 |
| `win11-soc` | Windows 11 Enterprise eval | 32 GB | 8 | 192.168.122.20 |

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
the DC when I looked. Those belong on `win11-soc`, and I have not
checked that guest since I built it.

## Steps

What is already done:

1. Install Server 2025 evaluation as `dc01`.
2. Promote it. Forest `lab.local`. Confirmed 5 Sep 2026 (`SETUP_DONE`
   on the guest).
3. Create the OUs, the helpdesk and SOC groups, and the lab users.
4. Inventory over the guest agent on 7 Sep 2026. NTDS, DNS, ADWS and
   Netlogon were running. Output: [`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt).

What I still have to do, and write down when I do it:

1. Turn both guests on. Confirm `win11-soc` is in the domain. If it is
   not, join it, and say so here.
2. From the Windows 11 client, with the helpdesk account, reset one
   staff password and unlock one account. Not with the domain admin.
3. Open GPMC and name one GPO that applies, and one place I expected a
   setting and did not find it.
4. Run one PowerShell check from memory, then fix whatever I got wrong:

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, MemberOf
Search-ADAccount -LockedOut
```

## Evidence

[`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt) is the
inventory. Short version:

- OS: Windows Server 2025 Datacenter Evaluation, build 26100
- `PartOfDomain=True`, domain and forest `lab.local`
- IPv4 `192.168.122.10`, DNS `127.0.0.1`, `192.168.122.1`
- NTDS, DNS, Netlogon, ADWS, WinDefend: running
- ADUC and GPMC present
- `SETUP_DONE` timestamp: 2026-09-05T19:26:49+02:00

The Windows 11 guest exists in libvirt and was shut off the last time I
looked. I do not have an inventory for it, so I am not claiming it is
domain-joined.

## What I learned

Promoting the DC is the easy part. The useful practice is the boring
repetition afterwards: find the user, reset the password, check the
group, as helpdesk, not as admin. I have the domain. I have not logged
that repetition yet.

I also learned to keep two labs apart. `lab.local` here is Windows
Server on `192.168.122.0/24`. The Samba lab is `corp.example.com` in a
container. Mixing them in one write-up would make both look finished.
They are not.
