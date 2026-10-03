# Lab 06 — Domaine Windows Server sur mon PC

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** In progress — `win11-soc` est dans `lab.local` (vérifié le 4 oct. 2026). Une réinitialisation helpdesk est écrite. Un déverrouillage reste ouvert parce que le seuil de verrouillage est 0.

## Objectif

Avoir un domaine Windows que j'ai construit moi-même, sur le même PC que
j'utilise pour Linux, pour pratiquer le helpdesk et l'AD sans une deuxième
machine. Samba ([lab 04](../04-samba-ad-lab/)) est un autre domaine. Celui-ci
est Windows Server.

## Mise en place

Hôte : mon PC Linux, libvirt, NAT `192.168.122.0/24`.

| Invité | Rôle | Adresse |
| --- | --- | --- |
| `dc01` | Windows Server 2025 évaluation, AD DS | 192.168.122.10 |
| `win11-soc` | Windows 11 Entreprise évaluation | 192.168.122.20 |

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
sur le DC quand j'ai regardé. Ils ont leur place sur `win11-soc`. Le
contrôle du 4 oct. 2026 sur cet invité a couvert le domaine, le DNS,
RSAT, gpresult et une réinitialisation helpdesk. Il n'a pas inventorié
ces outils SOC.

## Étapes

Ce qui est déjà fait :

1. Installer l'évaluation de Server 2025 en tant que `dc01`.
2. Le promouvoir. Forêt `lab.local`. Confirmé le 5 septembre 2026
   (`SETUP_DONE` sur l'invité).
3. Créer les OU, les groupes helpdesk et SOC, et les utilisateurs du lab.
4. Inventaire via l'agent invité le 7 septembre 2026. NTDS, DNS, ADWS et
   Netlogon tournaient. Sortie : [`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt).

Vérifié le 4 oct. 2026, les deux invités allumés. Sortie :
[`evidence/win11-2026-10-04.txt`](evidence/win11-2026-10-04.txt).

1. `win11-soc` était déjà dans `lab.local`. Objet ordinateur
   `CN=WIN11-SOC,OU=Workstations,DC=lab,DC=local`. Ethernet
   `192.168.122.20`, DNS `192.168.122.10` puis `192.168.122.1`.
   Les outils RSAT Active Directory sont installés. Je n'ai pas eu à
   le joindre.
2. Depuis ce client j'ai réinitialisé `jdoe` avec le credential
   helpdesk, pas l'admin du domaine. `jdoe` ne peut pas réinitialiser
   `asmith` (accès refusé). Helpdesk peut. `PasswordLastSet` est passé
   du 5 sept. 2026 19:26:49 au 4 oct. 2026 00:56:55, heure de l'invité.
   J'ai ensuite remis le mot de passe du lab (00:57:36). Le mot de passe
   n'est pas dans git. Le processus de l'agent invité est
   `NT AUTHORITY\SYSTEM`. Ce n'était pas une ouverture de session bureau
   en helpdesk.
3. La stratégie ordinateur sur `win11-soc` venait de `DC01.lab.local`.
   Appliquées : Default Domain Policy, Lab-Logon-Banner,
   Lab-PowerShell-Logging, Lab-Region-Keyboard.
   `Lab-Workstation-Hardening` est liée sur `OU=Workstations` et activée,
   et le rapport de GPO n'a pas de paramètre (`ExtensionData=0`).
   J'attendais un durcissement. Il n'y en a pas dans cette GPO.
4. Le seuil de verrouillage du domaine est 0. Je ne peux pas montrer
   un compte verrouillé tant que je n'ai pas mis un seuil. Je n'ai pas
   inventé un déverrouillage.

## Ticket de ce contrôle

`Lab-Workstation-Hardening` est liée à l'OU des postes et a l'air
activée. `gpresult /SCOPE COMPUTER /R` sur `WIN11-SOC` ne l'applique pas.
`Get-GPOReport` n'a pas de données d'extension. `Lab-Logon-Banner` en a,
et gpresult la liste. J'ai laissé la GPO vide. La remplir au hasard
ferait croire que le lab est fini.

Rempli dans la forme d'un ticket :
[`evidence/HD-2026-10-04.fr.md`](evidence/HD-2026-10-04.fr.md).
La réinitialisation helpdesk et le contrôle du domaine sont le même soir :
[`evidence/session-2026-10-04.fr.md`](evidence/session-2026-10-04.fr.md),
[`evidence/domain-2026-10-04.fr.md`](evidence/domain-2026-10-04.fr.md).

## Preuves

[`evidence/dc01-2026-09-07.txt`](evidence/dc01-2026-09-07.txt) est
l'inventaire. Version courte :

- OS : Windows Server 2025 Datacenter Evaluation, build 26100
- `PartOfDomain=True`, domaine et forêt `lab.local`
- IPv4 `192.168.122.10`, DNS `127.0.0.1`, `192.168.122.1`
- NTDS, DNS, Netlogon, ADWS, WinDefend : en cours d'exécution
- ADUC et GPMC présents
- horodatage `SETUP_DONE` : 2026-09-05T19:26:49+02:00

[`evidence/win11-2026-10-04.txt`](evidence/win11-2026-10-04.txt) est le
contrôle du 4 oct. 2026 de `win11-soc`, des liens GPO, et de la
réinitialisation helpdesk.

## Ce que j'ai appris

Promouvoir le DC, c'est la partie facile. Le contrôle utile est ennuyeux :
le client est dans la bonne OU, le DNS pointe vers le DC, helpdesk peut
réinitialiser un mot de passe staff, et un utilisateur staff ne peut pas
réinitialiser quelqu'un d'autre.

Une GPO liée n'est pas un paramètre. `Lab-Workstation-Hardening` est liée
et vide. J'aurais dit à un utilisateur que le durcissement était en place.
gpresult dit que non.

Un seuil de verrouillage à 0 veut dire que je ne peux pas encore
m'entraîner à un déverrouillage. Je n'écrirai pas un déverrouillage que
je n'ai pas fait. Une ouverture de session interactive en helpdesk sur
le bureau est la prochaine session. La réinitialisation ci-dessus a
utilisé le credential helpdesk depuis l'agent invité.

J'ai aussi appris à garder deux labs séparés. `lab.local` ici, c'est Windows
Server sur `192.168.122.0/24`. Le lab Samba, c'est `corp.example.com` dans
un conteneur. Les mélanger dans un seul compte rendu ferait croire que les
deux sont finis. Ils ne le sont pas.
