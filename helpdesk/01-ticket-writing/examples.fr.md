# Bons et mauvais tickets (fictifs)

[English](examples.md) · **Français** · [Deutsch](examples.de.md)

Tous les noms, hôtes et adresses sont inventés.

---

## Exemple 1 — « Internet doesn't work »

### ❌ Mauvais

> **Title:** internet broken
> **Description:** user says internet doesn't work. pls fix asap

Problèmes : pas d'utilisateur, pas d'appareil, pas de périmètre, pas d'erreur,
pas d'étapes déjà faites, « asap » sans justification.

### ✅ Bon

```text
Title:      [Network] PC-COMPTA-07 cannot reach websites; Teams works
Requester:  Claire Martin (Accounting), ext. 2143
Asset:      PC-COMPTA-07, Windows 11 23H2
Category:   Network        Impact: Single user   Urgency: Degraded   Priority: P3

Description:
  "Since this morning Chrome says DNS_PROBE_FINISHED_NXDOMAIN on every site."
  Started ~08:40 after laptop was docked. Teams chat/calls work.

Troubleshooting done:
  - 09:05 ipconfig /all -> IP 10.20.30.57/24, GW 10.20.30.1, DNS 203.0.113.53 (unexpected; our DNS is 10.20.30.10)
  - 09:07 Resolve-DnsName intranet.example.com -> timeout
  - 09:08 Resolve-DnsName intranet.example.com -Server 10.20.30.10 -> OK
  - 09:10 Adapter "USB-C Dock Ethernet" has static DNS set manually

Workaround:
  Set adapter back to DHCP-assigned DNS; ipconfig /flushdns -> browsing OK.

Next action:
  L2 to check why a static DNS was configured (user says a "helper" app did it).
  Possible unwanted software -> flag to Security for review.
```

---

## Exemple 2 — Mot de passe / problème de compte

### ❌ Mauvais

> **Title:** password
> **Description:** reset done

### ✅ Bon

```text
Title:      [Account] j.dupont locked out after password change — resolved
Requester:  Julien Dupont (Sales), mobile call
Asset:      Account j.dupont@example.com
Category:   Account/Access   Impact: Single user   Urgency: Cannot work   Priority: P3

Description:
  Account locked at 14:02. User changed password yesterday; phone mail app
  still had the old password and kept retrying.

Identity verification:
  Verified via callback to number in HR directory + manager confirmation (per
  procedure IAM-03). No password given over the phone/chat.

Troubleshooting done:
  - 14:10 AD: account locked, badPwdCount=5, source = mobile device (Exchange ActiveSync)
  - 14:12 Unlocked account; user removed and re-added mail account on phone
  - 14:20 No further failed logons in 10 min

Resolution:
  Root cause: stale credential on mobile device. Account unlocked, no reset
  needed. KB-0042 "Update password on mobile mail apps" sent to user.
```

---

## Exemple 3 — Phishing possible (lié à la sécurité)

### ❌ Mauvais

> **Title:** weird email
> **Description:** user got strange email, deleted it

Problèmes : preuve détruite, pas d'indicateurs, pas de périmètre, pas escaladé.

### ✅ Bon

```text
Title:      [Security] Suspected phishing "Facture impayée" — link clicked, no creds entered
Requester:  Sophie Bernard (Purchasing)
Category:   Security   Impact: Single user (possibly more)   Urgency: High   Priority: P2

Description:
  Email from "billing@examp1e-invoices.test" (look-alike domain), subject
  "Facture impayée n°4471", received 10:31. User clicked link at 10:33, page
  asked for M365 login; user closed the tab without typing anything.

Indicators (defanged):
  - Sender: billing[@]examp1e-invoices[.]test
  - URL:    hxxps://login-examp1e[.]test/owa/
  - Sending IP from headers: 198.51.100.23

Actions:
  - 10:40 Asked user NOT to delete; forwarded as attachment to security@example.com
  - 10:42 Checked sign-in logs for user: no unusual sign-ins
  - 10:45 Escalated to Security (L2/SOC) for message trace + purge from other mailboxes

Next action / owner:
  SOC: search for same sender/subject tenant-wide, block domain/URL, decide on
  password reset + session revocation as precaution.
```

---

## Exemple de note d'escalade (L1 → L2)

```text
Escalating to L2 Infrastructure.
Summary: 6 users on floor 2 lose network every ~20 min since 09:00.
Scope: all on switch SW-F2-01 ports 10–24; floor 1 unaffected.
Done: cable/port swap on 2 PCs (no change), switch uptime 3 days,
      port Gi1/0/12 shows err-disabled events in log (screenshot attached).
Hypothesis: loop or failing uplink on SW-F2-01.
Users informed of workaround (Wi-Fi) and that L2 is investigating.
```
