# Lab 06 — Domaine Windows Server sur mon PC

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** In progress — le contrôleur de domaine est réel. Une session helpdesk sur le client Windows 11 n'est pas encore rédigée.

## Objectif

Avoir un domaine Windows que j'ai construit moi-même, sur le même PC que
j'utilise pour Linux, pour pratiquer le helpdesk et l'AD sans une deuxième
machine. Samba ([lab 04](../04-samba-ad-lab/)) est un autre domaine. Celui-ci
est Windows Server.

## Mise en place

Hôte : mon PC Linux, libvirt, NAT `192.168.122.0/24`.

| Invité | Rôle | RAM | vCPU | Adresse |
| --- | --- | --- | --- | --- |
| `dc01` | Windows Server 2025 évaluation, AD DS | 8 GB | 4 | 192.168.122.10 |
| `win11-soc` | Windows 11 Entreprise évaluation | 32 GB | 8 | 192.168.122.20 |

Domaine `lab.local`, NetBIOS `LAB`. Le DNS sur le DC, c'est lui-même, puis
la passerelle libvirt `192.168.122.1`.

OU : Admins, Helpdesk, SOC, Staff, Workstations, Servers, Service
Accounts, Disabled.

Comptes vus dans l'inventaire : un admin du domaine, `helpdesk`,
`soc.analyst`, trois utilisateurs staff, deux comptes de service. `helpdesk`
est dans Helpdesk-T1 et Password-Reset. `soc.analyst` est dans SOC-Analysts.
Je ne mets pas les mots de passe dans git.

ADUC (`dsa.msc`) et la GPMC sont sur le DC. Defender tournait. Sysmon,
Wireshark, Hayabusa et le reste de la liste d'outils SOC n'étaient **pas**
sur le DC quand j'ai regardé. Ils ont leur place sur `win11-soc`, et je n'ai
pas revu cet invité depuis que je l'ai installé.

## Étapes

Ce qui est déjà fait :

1. Installer l'évaluation de Server 2025 en tant que `dc01`.
2. Le promouvoir. Forêt `lab.local`. Confirmé le 5 septembre 2026
   (`SETUP_DONE` sur l'invité).
3. Créer les OU, les groupes helpdesk et SOC, et les utilisateurs du lab.
4. Inventaire via l'agent invité le 7 septembre 2026. NTDS, DNS, ADWS et
   Netlogon tournaient. Sortie : [`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt).

Ce qu'il me reste à faire, et à écrire ici quand ce sera fait :

1. Allumer les deux invités. Vérifier que `win11-soc` est dans le domaine.
   S'il ne l'est pas, le joindre, et le dire ici.
2. Depuis le client Windows 11, avec le compte helpdesk, réinitialiser le
   mot de passe d'un utilisateur staff et déverrouiller un compte. Pas avec
   l'admin du domaine.
3. Ouvrir la GPMC et nommer une GPO qui s'applique, et un endroit où
   j'attendais un paramètre et où je ne l'ai pas trouvé.
4. Lancer un contrôle PowerShell de mémoire, puis corriger ce que j'aurai
   raté :

```powershell
Get-ADUser jdoe -Properties LockedOut, PasswordLastSet, MemberOf
Search-ADAccount -LockedOut
```

## Preuves

[`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt) est
l'inventaire. Version courte :

- OS : Windows Server 2025 Datacenter Evaluation, build 26100
- `PartOfDomain=True`, domaine et forêt `lab.local`
- IPv4 `192.168.122.10`, DNS `127.0.0.1`, `192.168.122.1`
- NTDS, DNS, Netlogon, ADWS, WinDefend : en cours d'exécution
- ADUC et GPMC présents
- horodatage `SETUP_DONE` : 2026-09-05T19:26:49+02:00

L'invité Windows 11 existe dans libvirt et était éteint la dernière fois
que j'ai regardé. Je n'ai pas d'inventaire pour lui, donc je ne prétends pas
qu'il est joint au domaine.

## Ce que j'ai appris

Promouvoir le DC, c'est la partie facile. L'entraînement utile, c'est la
répétition ennuyeuse ensuite : trouver l'utilisateur, réinitialiser le mot
de passe, vérifier le groupe, en helpdesk, pas en admin. J'ai le domaine.
Je n'ai pas encore noté cette répétition.

J'ai aussi appris à garder deux labs séparés. `lab.local` ici, c'est Windows
Server sur `192.168.122.0/24`. Le lab Samba, c'est `corp.example.com` dans
un conteneur. Les mélanger dans un seul compte rendu ferait croire que les
deux sont finis. Ils ne le sont pas.
