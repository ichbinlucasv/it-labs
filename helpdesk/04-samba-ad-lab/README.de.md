# Lab 04 — Benutzerverwaltung im Active Directory mit Samba AD DC

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** In progress — die Seite des Samba AD DC (Schritte 1–6 und 8) lief echt in einem Debian-13-Container, die Ausgaben liegen in [`evidence/`](evidence/). Schritt 7 ist offen: ein Windows-11-Client in *diese* Samba-Domäne. Windows-Gäste habe ich inzwischen, aber die hängen an einer anderen Domäne ([Lab 06](../06-windows-domain/), `lab.local` auf Windows Server). An Samba habe ich noch keinen gejoint.

## Ziel

Zu Hause eine kleine Active-Directory-Domäne ohne Windows-Server-Lizenz
betreiben und die Identitätsaufgaben üben, die ein Helpdesk täglich
erledigt: Benutzer anlegen, OUs und Gruppen organisieren, Passwörter
zurücksetzen, Konten entsperren/deaktivieren, eine Passwortrichtlinie
durchsetzen und einen Windows-Client in die Domäne aufnehmen. Bezug zu
Security+ D1/D3 (IAM, Least Privilege) und D4 (Lebenszyklus von Konten).

## Aufbau

| Host | Rolle | IP (Lab-LAN) | OS |
|------|-------|--------------|----|
| `dc01.corp.example.com` | Samba AD DC + DNS | 10.20.30.10/24 | Debian 12 |
| `ws01` | Domänenmitglied | DHCP / 10.20.30.50 | Windows 11 (Pro/Enterprise Evaluation) |

- Host-only- oder internes VirtualBox-Netz, damit das Lab-DNS nie ins
  Heimnetz gelangt.
- Domäne `CORP` / Realm `CORP.EXAMPLE.COM` (Subdomain eines reservierten
  Namens — `.local` vermeide ich, weil es mit mDNS kollidiert).
- Statische IP und Hostname auf `dc01` **vor** dem Provisionieren setzen.

> **Alternative — Windows Server Evaluation:** Microsoft bietet kostenlose
> 180-Tage-Evaluations-ISOs von Windows Server (Evaluation Center) an. Mit der
> Rolle *AD DS* bekommt man die „echte“ ADUC/GPMC-Erfahrung, die die meisten
> KMU nutzen. Samba AD ist schlanker (läuft mit 1 GB RAM) und spricht
> dieselben Protokolle (LDAP, Kerberos, DNS, SMB), sodass auch die RSAT-Tools
> unter Windows 11 es verwalten können. Dieses Lab dokumentiert Samba; die
> Konzepte lassen sich 1:1 übertragen.

## Schritte

### 1. dc01 vorbereiten

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

### 2. Domäne provisionieren

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

Den eigenen Resolver von `dc01` auf `127.0.0.1` setzen und einen
DNS-Forwarder in `/etc/samba/smb.conf` eintragen (`dns forwarder = 10.20.30.1`).

### 3. Prüfen

```bash
host -t SRV _ldap._tcp.corp.example.com.
host -t SRV _kerberos._udp.corp.example.com.
kinit administrator && klist
smbclient -L localhost -N
sudo samba-tool domain level show
```

### 4. OUs, Gruppen, Benutzer

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

### 5. Tägliche Helpdesk-Aufgaben

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

### 6. Passwort- und Sperrrichtlinie

```bash
sudo samba-tool domain passwordsettings show
sudo samba-tool domain passwordsettings set \
     --min-pwd-length=12 --complexity=on \
     --account-lockout-threshold=5 \
     --account-lockout-duration=15 \
     --reset-account-lockout-after=15
```

Mit Fine-Grained Password Policies (`samba-tool domain passwordsettings pso create`)
kann man Admins eine strengere Richtlinie geben als normalen Benutzern.

### 7. Windows-11-Client aufnehmen

1. DNS von `ws01` ausschließlich auf `10.20.30.10` setzen.
2. *Einstellungen → System → Info → Domäne oder Arbeitsgruppe* → mit einem
   delegierten Konto `corp.example.com` beitreten, neu starten.
3. **RSAT: Active Directory Domain Services and LDS Tools** und **Group
   Policy Management Tools** (optionale Features) installieren → Benutzer in
   ADUC verwalten und eine GPO anlegen (z. B. Bildschirmsperre nach 10 min).
4. Als `CORP\j.dupont` anmelden, mit `whoami /groups` und `gpresult /r` prüfen.

### 8. Sicherheitshinweise

- Admin-Konten (`adm.lucas`) von Alltagskonten trennen.
- Das Recht zum Zurücksetzen von Passwörtern auf `OU=Staff` an eine Gruppe
  `GG_Helpdesk` delegieren, statt dem Helpdesk Domain-Admin-Rechte zu geben.
- Die Mitgliedschaft in `Domain Admins` regelmäßig überprüfen.

## Was ich tatsächlich ausgeführt habe

Umgebung: ein Debian-13-Root-Dateisystem (debootstrap), gestartet mit
`systemd-nspawn --boot --private-network` als `dc01`, Samba 4.22.11 aus
Debian. Der Container hat nur Loopback und ein veth-Interface, das ich darin
mit `10.20.30.10/24` angelegt habe — Lab-DNS und Kerberos berühren also nie
ein echtes Netz. Gleiches Vorgehen wie in
[Lab 03](../03-linux-troubleshooting/lab-container.md), zusätzlich mit
`samba samba-ad-dc winbind krb5-user smbclient ldb-tools`. Die Passwörter
(Administrator, Testbenutzer) wurden zufällig in nur für root lesbare Dateien
im Container erzeugt und mit `$(cat file)` übergeben; keines davon erscheint
in den Nachweisen.

| Schritt | Ergebnis | Nachweis |
|---------|----------|----------|
| 1–2 Provisionieren | `samba-tool domain provision` OK; Dienst `samba-ad-dc` aktiv | [1-provision.txt](evidence/1-provision.txt) |
| 3 Prüfen | SRV-Einträge `_ldap._tcp` → `dc01:389`, `_kerberos._udp` → `dc01:88`; `kinit administrator` erhielt ein TGT; Freigaben `sysvol`/`netlogon` gelistet; Funktionsebene 2008 R2 | [2-verify-ous-groups-users.txt](evidence/2-verify-ous-groups-users.txt) |
| 4 OUs, Gruppen, Benutzer | `OU=Staff` mit `Sales`/`Accounting`, `OU=Disabled`; `GG_Sales`, `GG_Accounting`, `GG_Helpdesk`; Benutzer `j.dupont`, `c.martin` | gleiche Datei |
| 6 Passwort- und Sperrrichtlinie | Standard war Mindestlänge 7 und **Sperrschwelle 0 (keine Sperre)**; gesetzt auf 12 / Komplexität / 5 Versuche / 15 min. Ein Passwort mit 7 Zeichen wurde danach abgelehnt (`the password is too short ... 12 characters`) | [3-password-policy-lockout.txt](evidence/3-password-policy-lockout.txt) |
| 6 Sperrtest | 5 × `NT_STATUS_LOGON_FAILURE`, dann `NT_STATUS_ACCOUNT_LOCKED_OUT`, selbst mit richtigem Passwort; `badPwdCount: 5`, `lockoutTime` gesetzt; `samba-tool user unlock` → beide wieder 0, Anmeldung funktioniert | gleiche Datei |
| 5 Helpdesk-Aufgaben | Reset mit `--must-change-at-next-login` (`pwdLastSet: 0`); ausscheidende Mitarbeiterin `c.martin` deaktiviert (`userAccountControl: 514`) und nach `OU=Disabled` verschoben; externer Mitarbeiter `ext.bernard` mit Ablauf nach 30 Tagen | [4-helpdesk-tasks-delegation.txt](evidence/4-helpdesk-tasks-delegation.txt) |
| 8 Delegation | `GG_Helpdesk` erhält das erweiterte Recht *Reset Password* auf `OU=Staff` (kein Domain Admin) — mit einem Mitgliedskonto getestet, siehe unten | gleiche Datei |
| 7 Windows-Client | **nicht erledigt** — braucht eine Windows-11-VM | — |

**Delegationstest — ein echtes Problem und seine Lösung.** Nur mit dem Recht
*Reset Password* konnte das Helpdesk-Konto `h.tech` das Passwort von
`j.dupont` zurücksetzen, aber der übliche Helpdesk-Befehl schlug fehl:

```text
$ samba-tool user setpassword j.dupont --random-password --must-change-at-next-login -H ldap://dc01... (as h.tech)
ERROR: ... LDAP_INSUFFICIENT_ACCESS_RIGHTS - <00002098: Object CN=Julien Dupont,OU=Sales,OU=Staff,... has no write property access>
```

„Kennwort bei nächster Anmeldung ändern“ schreibt das Attribut `pwdLastSet`,
und dafür braucht es eine eigene Berechtigung; Entsperren schreibt
`lockoutTime`. Ich habe für diese beiden Attribute Schreib-ACEs auf
Benutzerobjekten unter `OU=Staff` ergänzt. Danach funktionierte der Reset mit
erzwungener Änderung, während das Zurücksetzen von `Administrator` (außerhalb
von `OU=Staff`) weiterhin mit `LDAP_INSUFFICIENT_ACCESS_RIGHTS` abgelehnt
wurde — genau das gewünschte Ergebnis nach dem Least-Privilege-Prinzip.
(Unter Windows vergibt die Aufgabe „Setzt Benutzerkennwörter zurück und
erzwingt Kennwortänderung bei der nächsten Anmeldung“ im Assistenten zum
Zuweisen der Objektverwaltung das Reset-Recht plus Lesen/Schreiben auf
`pwdLastSet`; Entsperren braucht zusätzlich `lockoutTime`.)

## Nachweise

- [`evidence/`](evidence/): Provisionierung, Ausgaben von `host -t SRV` und
  `klist`, Anlage von OUs/Gruppen/Benutzern, Passworteinstellungen vorher/
  nachher, Sperr- und Entsperrablauf, Aufgaben für Austritte/Externe und der
  Delegationstest. Domänen-SIDs sind auf `S-1-5-21-<domain>-RID` gekürzt.
- Noch zu erfassen (braucht Windows): ADUC-Screenshot der OU-Struktur von
  `ws01`, `whoami /groups` und `gpresult /r` für `CORP\j.dupont`, eine GPO
  für die Bildschirmsperre.

## Was ich gelernt habe

- Eine frische Samba-Domäne hat **keine Kontosperre** (Schwelle 0) — die
  Voreinstellung muss man bewusst ändern, genau wie unter Windows.
- Ist ein Konto gesperrt, wird selbst das richtige Passwort abgelehnt
  (`ACCOUNT_LOCKED_OUT`) — deshalb rufen Benutzer beim Helpdesk an, „obwohl
  ich es richtig eingegeben habe“.
- „Passwort zurücksetzen“ zu delegieren reicht für die übliche
  Helpdesk-Aktion nicht: Kennwortänderung erzwingen und Entsperren sind
  eigene Attributberechtigungen. Das hat erst der Test mit einem echten
  Nicht-Admin-Konto gezeigt; die Dokumentation allein hätte es nicht.
- Passwörter auf der Kommandozeile landen in `ps` und in der Shell-History;
  samba-tool warnt sogar davor. Besser aus einer geschützten Datei (oder per
  Eingabeaufforderung) lesen.
- AD hängt an DNS: Die ersten Prüfungen nach dem Provisionieren sind die SRV-Einträge.
