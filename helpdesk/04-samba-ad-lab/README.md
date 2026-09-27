# Lab 04 — Active Directory user management with Samba AD DC

**English** · [Deutsch](README.de.md)

**Status:** In progress — the Samba AD DC side (steps 1–6 and 8) ran for real in a Debian 13 container and the output is in [`evidence/`](evidence/); step 7 (joining a Windows 11 client, RSAT/ADUC, GPO) is not runnable on my Linux-only lab machine and still needs a Windows VM.

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

## What I actually ran

Environment: a Debian 13 root filesystem (debootstrap) booted with
`systemd-nspawn --boot --private-network` as `dc01`, Samba 4.22.11 from
Debian. The container has only loopback plus a veth interface I created
inside it with `10.20.30.10/24`, so the lab DNS/Kerberos never touches a
real network. Same approach as [lab 03](../03-linux-troubleshooting/lab-container.md),
with `samba samba-ad-dc winbind krb5-user smbclient ldb-tools` installed.
Passwords (Administrator, test users) were generated randomly into
root-only files inside the container and passed with `$(cat file)`; none
appears in the evidence.

| Step | Result | Evidence |
|------|--------|----------|
| 1–2 Provision | `samba-tool domain provision` OK; `samba-ad-dc` service active | [1-provision.txt](evidence/1-provision.txt) |
| 3 Verify | SRV records `_ldap._tcp` → `dc01:389`, `_kerberos._udp` → `dc01:88`; `kinit administrator` got a TGT; `sysvol`/`netlogon` shares listed; function level 2008 R2 | [2-verify-ous-groups-users.txt](evidence/2-verify-ous-groups-users.txt) |
| 4 OUs, groups, users | `OU=Staff` with `Sales`/`Accounting`, `OU=Disabled`; `GG_Sales`, `GG_Accounting`, `GG_Helpdesk`; users `j.dupont`, `c.martin` | same file |
| 6 Password & lockout policy | defaults were min length 7, **lockout threshold 0 (no lockout)**; set to 12 / complexity / 5 attempts / 15 min. A 7-character password was then rejected (`the password is too short ... 12 characters`) | [3-password-policy-lockout.txt](evidence/3-password-policy-lockout.txt) |
| 6 Lockout test | 5 × `NT_STATUS_LOGON_FAILURE` then `NT_STATUS_ACCOUNT_LOCKED_OUT`, even with the right password; `badPwdCount: 5`, `lockoutTime` set; `samba-tool user unlock` → both back to 0 and logon works | same file |
| 5 Helpdesk tasks | reset with `--must-change-at-next-login` (`pwdLastSet: 0`); leaver `c.martin` disabled (`userAccountControl: 514`) and moved to `OU=Disabled`; contractor `ext.bernard` with 30-day expiry | [4-helpdesk-tasks-delegation.txt](evidence/4-helpdesk-tasks-delegation.txt) |
| 8 Delegation | `GG_Helpdesk` gets the *Reset Password* extended right on `OU=Staff` (no Domain Admin) — tested with a member account, see below | same file |
| 7 Windows client | **not done** — needs a Windows 11 VM | — |

**Delegation test — a real problem and its fix.** With only the *Reset
Password* right, the helpdesk account `h.tech` could reset `j.dupont`'s
password, but the normal helpdesk command failed:

```text
$ samba-tool user setpassword j.dupont --random-password --must-change-at-next-login -H ldap://dc01... (as h.tech)
ERROR: ... LDAP_INSUFFICIENT_ACCESS_RIGHTS - <00002098: Object CN=Julien Dupont,OU=Sales,OU=Staff,... has no write property access>
```

"Must change at next logon" writes the `pwdLastSet` attribute, which is a
separate permission; unlocking writes `lockoutTime`. I added two
write-property ACEs for those attributes on user objects under `OU=Staff`,
and then the reset with forced change worked, while resetting
`Administrator` (outside `OU=Staff`) was still refused with
`LDAP_INSUFFICIENT_ACCESS_RIGHTS` — exactly the least-privilege result I wanted.
(On Windows, the "Delegation of Control" task "Reset user passwords and force
password change at next logon" grants the reset right plus read/write on
`pwdLastSet`; unlocking needs `lockoutTime` in addition.)

## Evidence

- [`evidence/`](evidence/): provisioning, `host -t SRV` and `klist` output,
  OU/group/user creation, password settings before/after, the lockout and
  unlock sequence, leaver/contractor tasks, and the delegation test.
  Domain SIDs are shortened to `S-1-5-21-<domain>-RID`.
- Still to capture (needs Windows): ADUC screenshot of the OU structure from
  `ws01`, `whoami /groups` and `gpresult /r` for `CORP\j.dupont`, a screen-lock GPO.

## What I learned

- A fresh Samba domain has **no account lockout** (threshold 0) — the default
  has to be changed deliberately, just like on Windows.
- Once locked, even the correct password is refused (`ACCOUNT_LOCKED_OUT`),
  which is why users call the helpdesk "although I typed it right".
- Delegating "reset password" is not enough for the usual helpdesk action:
  forcing a change at next logon and unlocking are separate attribute
  permissions. Testing the delegation with a real non-admin account showed
  it; reading the documentation alone would not have.
- Passing passwords on the command line leaks them to `ps` and shell
  history; samba-tool even warns about it. Reading them from a protected
  file (or a prompt) is better.
- AD depends on DNS: the first checks after provisioning are the SRV records.
