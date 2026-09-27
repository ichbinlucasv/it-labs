# Lab 04 — Active Directory user management with Samba AD DC

**Status:** Planned — written procedure; no Samba AD DC has been provisioned yet and the commands have not been run.

## Goal

Run a small Active Directory domain at home without a Windows Server licence,
and practise the identity tasks a helpdesk handles daily: creating users,
organising OUs and groups, resetting passwords, unlocking/disabling accounts,
enforcing a password policy, and joining a Windows client. Maps to Security+
D1/D3 (IAM, least privilege) and D4 (account lifecycle).

## Setup

| Host | Role | IP (lab LAN) | OS |
|------|------|--------------|----|
| `dc01.corp.example.com` | Samba AD DC + DNS | 10.20.30.10/24 | Debian 12 |
| `ws01` | Domain member | DHCP / 10.20.30.50 | Windows 11 (Pro/Enterprise eval) |

- Host-only or internal VirtualBox network so the lab DNS never leaks to the
  home network.
- Domain `CORP` / realm `CORP.EXAMPLE.COM` (a subdomain of a reserved name — I
  avoid `.local`, which conflicts with mDNS).
- Static IP and hostname set on `dc01` **before** provisioning.

> **Alternative — Windows Server evaluation:** Microsoft provides free
> 180-day evaluation ISOs of Windows Server (Evaluation Center). Installing the
> *AD DS* role there gives the "real" ADUC/GPMC experience that most French
> SMEs use. Samba AD is lighter (runs in 1 GB RAM) and speaks the same
> protocols (LDAP, Kerberos, DNS, SMB), so the RSAT tools on Windows 11 can
> manage it too. This lab documents Samba; the concepts transfer 1:1.

## Steps

### 1. Prepare dc01

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

### 2. Provision the domain

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

Point `dc01`'s own resolver at `127.0.0.1` and set a DNS forwarder in
`/etc/samba/smb.conf` (`dns forwarder = 10.20.30.1`).

### 3. Verify

```bash
host -t SRV _ldap._tcp.corp.example.com.
host -t SRV _kerberos._udp.corp.example.com.
kinit administrator && klist
smbclient -L localhost -N
sudo samba-tool domain level show
```

### 4. OUs, groups, users

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

### 5. Daily helpdesk tasks

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

### 6. Password & lockout policy

```bash
sudo samba-tool domain passwordsettings show
sudo samba-tool domain passwordsettings set \
     --min-pwd-length=12 --complexity=on \
     --account-lockout-threshold=5 \
     --account-lockout-duration=15 \
     --reset-account-lockout-after=15
```

Fine-grained policies (`samba-tool domain passwordsettings pso create`) can
give admins a stricter policy than normal users.

### 7. Join a Windows 11 client

1. Set `ws01` DNS to `10.20.30.10` only.
2. *Settings → System → About → Domain or workgroup* → join `corp.example.com`
   with a delegated account, reboot.
3. Install **RSAT: Active Directory Domain Services and LDS Tools** and
   **Group Policy Management Tools** (Optional features) → manage users from
   ADUC and create a GPO (e.g. screen lock after 10 min).
4. Log on as `CORP\j.dupont`, verify with `whoami /groups` and `gpresult /r`.

### 8. Security notes

- Separate admin accounts (`adm.lucas`) from daily accounts.
- Delegate password-reset rights on `OU=Staff` to a `GG_Helpdesk` group
  instead of giving helpdesk Domain Admin.
- Review `Domain Admins` membership regularly.

## Evidence

- `host -t SRV` and `klist` output after provisioning.
- ADUC screenshot from `ws01` showing the OU structure.
- `samba-tool domain passwordsettings show` after hardening.
- Screenshot of a locked account (`badPwdCount`) and the unlock.

## What I learned

_To be completed by Lucas._
