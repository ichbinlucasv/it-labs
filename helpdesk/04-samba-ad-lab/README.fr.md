# Lab 04 — Gestion des utilisateurs Active Directory avec Samba AD DC

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** In progress — le côté Samba AD DC (étapes 1 à 6 et 8) a vraiment tourné dans un conteneur Debian 13 et la sortie est dans [`evidence/`](evidence/). L'étape 7 est encore ouverte : joindre un client Windows 11 à *ce* domaine Samba. J'ai des invités Windows maintenant, mais ils sont dans un autre domaine ([lab 06](../06-windows-domain/), `lab.local` sur Windows Server). Je n'en ai joint aucun à Samba.

## Objectif

Faire tourner un petit domaine Active Directory à la maison, sans licence
Windows Server. M'entraîner aux tâches d'identité qu'un helpdesk fait tous
les jours : créer des utilisateurs, ranger des OU et des groupes,
réinitialiser des mots de passe, déverrouiller ou désactiver des comptes,
appliquer une politique de mot de passe, et joindre un client Windows. Ça
correspond à Security+ D1/D3 (IAM, moindre privilège) et D4 (cycle de vie
des comptes).

## Mise en place

| Hôte | Rôle | IP (LAN du lab) | OS |
|------|------|-----------------|----|
| `dc01.corp.example.com` | Samba AD DC + DNS | 10.20.30.10/24 | Debian 12 |
| `ws01` | Membre du domaine | DHCP / 10.20.30.50 | Windows 11 (eval Pro/Enterprise) |

- Réseau VirtualBox host-only ou interne, pour que le DNS du lab ne fuite
  jamais vers le réseau de la maison.
- Domaine `CORP` / realm `CORP.EXAMPLE.COM` (un sous-domaine d'un nom réservé.
  J'évite `.local`, qui entre en conflit avec mDNS).
- IP statique et nom d'hôte posés sur `dc01` **avant** le provisionnement.

> **Autre voie — évaluation Windows Server :** Microsoft fournit des ISO
> d'évaluation gratuites de Windows Server, 180 jours (Evaluation Center).
> Installer le rôle *AD DS* là donne l'expérience ADUC/GPMC « vraie » que
> la plupart des PME françaises utilisent. Samba AD est plus léger (ça tourne
> dans 1 GB de RAM) et parle les mêmes protocoles (LDAP, Kerberos, DNS, SMB).
> Les outils RSAT sur Windows 11 peuvent donc le gérer aussi. Ce lab documente
> Samba. Les concepts se transposent 1 pour 1.

## Étapes

### 1. Préparer dc01

```bash
sudo hostnamectl set-hostname dc01
echo "10.20.30.10 dc01.corp.example.com dc01" | sudo tee -a /etc/hosts
sudo apt update
sudo apt install -y samba winbind krb5-user smbclient dnsutils \
     libpam-winbind libnss-winbind
# Stop and disable the file-server daemons; the AD DC uses the 'samba' service
sudo systemctl disable --now smbd nmbd winbind
sudo mv /etc/samba/smb.conf /etc/samba/smb.conf.orig
```

### 2. Provisionner le domaine

```bash
sudo samba-tool domain provision \
     --use-rfc2307 \
     --realm=CORP.EXAMPLE.COM \
     --domain=CORP \
     --server-role=dc \
     --dns-backend=SAMBA_INTERNAL
# (prompts for the Administrator password — never write it in scripts or git)

sudo cp /var/lib/samba/private/krb5.conf /etc/krb5.conf
sudo systemctl unmask samba-ad-dc
sudo systemctl enable --now samba-ad-dc
```

Pointer le résolveur de `dc01` lui-même vers `127.0.0.1`, et mettre un
redirecteur DNS dans `/etc/samba/smb.conf` (`dns forwarder = 10.20.30.1`).

### 3. Vérifier

```bash
host -t SRV _ldap._tcp.corp.example.com.
host -t SRV _kerberos._udp.corp.example.com.
kinit administrator && klist
smbclient -L localhost -N
sudo samba-tool domain level show
```

### 4. OU, groupes, utilisateurs

```bash
sudo samba-tool ou create "OU=Staff,DC=corp,DC=example,DC=com"
sudo samba-tool ou create "OU=Sales,OU=Staff,DC=corp,DC=example,DC=com"
sudo samba-tool ou create "OU=Accounting,OU=Staff,DC=corp,DC=example,DC=com"

sudo samba-tool group add GG_Sales
sudo samba-tool group add GG_Accounting

# Fictional users; --random-password then force change at first logon
sudo samba-tool user create j.dupont --random-password \
     --given-name=Julien --surname=Dupont \
     --userou="OU=Sales,OU=Staff" --mail-address=j.dupont@example.com
sudo samba-tool user create c.martin --random-password \
     --given-name=Claire --surname=Martin \
     --userou="OU=Accounting,OU=Staff" --mail-address=c.martin@example.com

sudo samba-tool group addmembers GG_Sales j.dupont
sudo samba-tool group addmembers GG_Accounting c.martin
sudo samba-tool group listmembers GG_Sales
```

### 5. Tâches helpdesk du quotidien

```bash
# Password reset with forced change (identity verified first!)
sudo samba-tool user setpassword j.dupont --must-change-at-next-login

# Disable a leaver (joiner-mover-leaver process) and move them
sudo samba-tool user disable c.martin
sudo samba-tool user move c.martin "OU=Disabled,DC=corp,DC=example,DC=com"   # create the OU first

# Temporary contractor account that expires
sudo samba-tool user setexpiry j.dupont --days=30

# Inspect an account
sudo samba-tool user show j.dupont --attributes=lockoutTime,badPwdCount,userAccountControl
```

### 6. Politique de mot de passe et de verrouillage

```bash
sudo samba-tool domain passwordsettings show
sudo samba-tool domain passwordsettings set \
     --min-pwd-length=12 --complexity=on \
     --account-lockout-threshold=5 \
     --account-lockout-duration=15 \
     --reset-account-lockout-after=15
```

Les politiques fines (`samba-tool domain passwordsettings pso create`) peuvent
donner aux admins une politique plus stricte qu'aux utilisateurs normaux.

### 7. Joindre un client Windows 11

1. Mettre le DNS de `ws01` uniquement sur `10.20.30.10`.
2. *Settings → System → About → Domain or workgroup* → joindre
   `corp.example.com` avec un compte délégué, puis redémarrer.
3. Installer **RSAT: Active Directory Domain Services and LDS Tools** et
   **Group Policy Management Tools** (Optional features) → gérer les
   utilisateurs depuis ADUC et créer une GPO (par exemple verrouillage
   d'écran après 10 min).
4. Ouvrir une session `CORP\j.dupont`, vérifier avec `whoami /groups` et
   `gpresult /r`.

### 8. Notes de sécurité

- Séparer les comptes admin (`adm.lucas`) des comptes du quotidien.
- Déléguer le droit de réinitialiser le mot de passe sur `OU=Staff` à un
  groupe `GG_Helpdesk`, au lieu de donner Domain Admin au helpdesk.
- Revoir régulièrement les membres de `Domain Admins`.

## Ce que j'ai vraiment exécuté

Environnement : un système de fichiers racine Debian 13 (debootstrap) démarré
avec `systemd-nspawn --boot --private-network` comme `dc01`, Samba 4.22.11
de Debian. Le conteneur n'a que le loopback, plus une interface veth que
j'ai créée dedans avec `10.20.30.10/24`. Le DNS et Kerberos du lab ne
touchent donc jamais un vrai réseau. Même approche que le
[lab 03](../03-linux-troubleshooting/lab-container.md), avec
`samba samba-ad-dc winbind krb5-user smbclient ldb-tools` installés.
Les mots de passe (Administrator, utilisateurs de test) ont été générés au
hasard dans des fichiers lisibles seulement par root, dans le conteneur, et
passés avec `$(cat file)`. Aucun n'apparaît dans les preuves.

| Étape | Résultat | Preuve |
|-------|----------|--------|
| 1–2 Provisionnement | `samba-tool domain provision` OK ; service `samba-ad-dc` actif | [1-provision.txt](evidence/1-provision.txt) |
| 3 Vérification | enregistrements SRV `_ldap._tcp` → `dc01:389`, `_kerberos._udp` → `dc01:88` ; `kinit administrator` a obtenu un TGT ; partages `sysvol`/`netlogon` listés ; niveau fonctionnel 2008 R2 | [2-verify-ous-groups-users.txt](evidence/2-verify-ous-groups-users.txt) |
| 4 OU, groupes, utilisateurs | `OU=Staff` avec `Sales`/`Accounting`, `OU=Disabled` ; `GG_Sales`, `GG_Accounting`, `GG_Helpdesk` ; utilisateurs `j.dupont`, `c.martin` | même fichier |
| 6 Politique de mot de passe et de verrouillage | les défauts étaient longueur min. 7, **seuil de verrouillage 0 (pas de verrouillage)** ; passé à 12 / complexité / 5 essais / 15 min. Un mot de passe de 7 caractères a ensuite été refusé (`the password is too short ... 12 characters`) | [3-password-policy-lockout.txt](evidence/3-password-policy-lockout.txt) |
| 6 Test de verrouillage | 5 × `NT_STATUS_LOGON_FAILURE` puis `NT_STATUS_ACCOUNT_LOCKED_OUT`, même avec le bon mot de passe ; `badPwdCount: 5`, `lockoutTime` posé ; `samba-tool user unlock` → les deux reviennent à 0 et l'ouverture de session marche | même fichier |
| 5 Tâches helpdesk | reset avec `--must-change-at-next-login` (`pwdLastSet: 0`) ; départ `c.martin` désactivé (`userAccountControl: 514`) et déplacé vers `OU=Disabled` ; prestataire `ext.bernard` avec expiration à 30 jours | [4-helpdesk-tasks-delegation.txt](evidence/4-helpdesk-tasks-delegation.txt) |
| 8 Délégation | `GG_Helpdesk` reçoit le droit étendu *Reset Password* sur `OU=Staff` (pas Domain Admin) — testé avec un compte membre, voir plus bas | même fichier |
| 7 Client Windows | **pas fait** — il faut une VM Windows 11 | — |

**Test de délégation — un vrai problème et son correctif.** Avec seulement
le droit *Reset Password*, le compte helpdesk `h.tech` pouvait réinitialiser
le mot de passe de `j.dupont`, mais la commande helpdesk habituelle échouait :

```text
$ samba-tool user setpassword j.dupont --random-password --must-change-at-next-login -H ldap://dc01... (as h.tech)
ERROR: ... LDAP_INSUFFICIENT_ACCESS_RIGHTS - <00002098: Object CN=Julien Dupont,OU=Sales,OU=Staff,... has no write property access>
```

« Must change at next logon » écrit l'attribut `pwdLastSet`, qui est un
droit à part. Le déverrouillage écrit `lockoutTime`. J'ai ajouté deux ACE
en écriture sur ces attributs, pour les objets utilisateur sous `OU=Staff`.
Ensuite le reset avec changement forcé a marché. Le reset d'`Administrator`
(hors de `OU=Staff`) était encore refusé avec
`LDAP_INSUFFICIENT_ACCESS_RIGHTS`. C'est exactement le moindre privilège que
je voulais. (Sous Windows, la tâche « Delegation of Control »
« Reset user passwords and force password change at next logon » donne le
droit de reset plus la lecture et l'écriture sur `pwdLastSet`. Le
déverrouillage demande `lockoutTime` en plus.)

## Preuves

- [`evidence/`](evidence/) : provisionnement, sortie de `host -t SRV` et de
  `klist`, création des OU, des groupes et des utilisateurs, paramètres de
  mot de passe avant et après, la séquence de verrouillage et de
  déverrouillage, les tâches départ et prestataire, et le test de délégation.
  Les SID de domaine sont raccourcis en `S-1-5-21-<domain>-RID`.
- Encore à capturer (il faut Windows) : capture ADUC de la structure d'OU
  depuis `ws01`, `whoami /groups` et `gpresult /r` pour `CORP\j.dupont`, une
  GPO de verrouillage d'écran.

## Ce que j'ai appris

- Un domaine Samba tout neuf n'a **pas de verrouillage de compte** (seuil 0).
  Le défaut doit être changé exprès, comme sous Windows.
- Une fois le compte verrouillé, même le bon mot de passe est refusé
  (`ACCOUNT_LOCKED_OUT`). C'est pour ça que les utilisateurs appellent le
  helpdesk « alors que je l'ai tapé correctement ».
- Déléguer « reset password » ne suffit pas pour l'action helpdesk habituelle.
  Forcer le changement à la prochaine ouverture, et déverrouiller, sont des
  droits d'attribut à part. Le test de la délégation avec un vrai compte non
  admin l'a montré. Lire seulement la doc ne l'aurait pas montré.
- Passer les mots de passe en ligne de commande les fait fuir vers `ps` et
  l'historique du shell. samba-tool le signale d'ailleurs. Les lire depuis un
  fichier protégé (ou une invite) est mieux.
- L'AD dépend du DNS. Les premiers contrôles après le provisionnement sont
  les enregistrements SRV.
