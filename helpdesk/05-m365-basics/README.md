# Lab 05 — Microsoft 365 administration basics

**Status:** Planned — concept notes only; not practised in a Microsoft 365 tenant. Needs a Microsoft 365 trial or developer tenant, which I do not have yet; nothing here is simulated.

## Goal

Understand the Microsoft 365 / Entra ID concepts that come up in helpdesk
roles: user lifecycle, licences, groups, MFA, self-service password reset, and
which admin centre to use for what. This is a **documented concept lab** — no
real tenant data appears here.

## Setup

- Option A: Microsoft 365 Developer Program sandbox (eligibility has changed
  over time — check the current conditions) or a Microsoft 365 Business trial.
- Option B: Microsoft Learn free modules and interactive guides (MS-900 /
  SC-900 learning paths) when no tenant is available.
- Fictional tenant: `exemple-sarl.onmicrosoft.com`, custom domain `example.com`.

## Steps

### 1. Map the admin centres

| Task | Where |
|------|-------|
| Create users, assign licences, reset passwords | Microsoft 365 admin center (`admin.microsoft.com`) |
| Identity, groups, MFA, Conditional Access, sign-in logs | Microsoft Entra admin center (`entra.microsoft.com`) |
| Mailboxes, shared mailboxes, mail flow, message trace | Exchange admin center |
| Teams policies, meeting settings | Teams admin center |
| Devices, compliance policies, app deployment | Intune (`intune.microsoft.com`) |
| Alerts, phishing, quarantine, Defender incidents | Microsoft Defender portal (`security.microsoft.com`) |
| Retention, DLP, eDiscovery | Microsoft Purview portal |

### 2. User lifecycle (joiner / mover / leaver)

- **Joiner:** create user → usage location (required before licensing) →
  assign licence (ideally via group-based licensing) → add to groups →
  MFA registration on first sign-in.
- **Mover:** change groups/department; remove access no longer needed.
- **Leaver:** block sign-in → revoke sessions → reset password → convert
  mailbox to shared or set forwarding per policy → remove licence → delete
  after the retention period.

Equivalent Microsoft Graph PowerShell (documented, fictional values):

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All","Group.ReadWrite.All"
Get-MgUser -Filter "startswith(displayName,'Julien')" | Select DisplayName,UserPrincipalName
Update-MgUser -UserId j.dupont@example.com -AccountEnabled:$false      # block sign-in
Revoke-MgUserSignInSession -UserId j.dupont@example.com
Get-MgSubscribedSku | Select SkuPartNumber,ConsumedUnits
```

### 3. Licensing concepts

- A licence (SKU, e.g. *Microsoft 365 Business Premium*) contains service
  plans (Exchange Online, Teams, Intune, Entra ID P1...).
- **Group-based licensing** reduces errors: add the user to `LIC_M365_BP`.
- Common helpdesk issue: "no mailbox" → licence missing or usage location not set.

### 4. MFA & authentication

- Prefer **Microsoft Authenticator** (number matching) or **FIDO2/passkeys**
  over SMS.
- **Security defaults** (free) vs **Conditional Access** (Entra ID P1):
  CA policies like "require MFA for all users", "block legacy
  authentication", "require compliant device for admins".
- Always keep **two break-glass accounts** excluded from CA, with long
  passwords stored offline and monitored sign-ins.
- **SSPR** lets users reset their own password after proving identity —
  fewer tickets, but only safe with strong registration methods.

### 5. Helpdesk scenarios (worked in the sandbox or on paper)

| Scenario | Checks |
|----------|--------|
| User lost phone with Authenticator | Verify identity out-of-band → require re-register MFA → revoke sessions |
| "Too many sign-in attempts" | Entra sign-in logs: failure reason, IP, location, client app |
| Shared mailbox access | Exchange admin center → mailbox delegation (Full Access / Send As) |
| Suspicious sign-in from abroad | Sign-in logs + risky users → block, reset, revoke, escalate to SOC |
| New hire has no Teams | Licence assigned? Service plan enabled? Wait for provisioning |

### 6. Least-privilege admin roles

Helpdesk agents get **Helpdesk Administrator** or **User Administrator**,
not Global Administrator. Use **PIM** (Entra ID P2) for just-in-time elevation.

## Evidence

- Screenshots from a sandbox/trial (tenant names blurred): user creation,
  licence assignment, CA policy in report-only mode, sign-in log entry.
- Or: Microsoft Learn module completion badges.

## What I learned

_To be completed by Lucas._
