# Domain 4 — Security Operations (≈28 %, the biggest domain)

**English** · [Français](4-security-operations.fr.md) · [Deutsch](4-security-operations.de.md)

## Secure baselines & hardening

Establish → deploy → maintain baselines (CIS Benchmarks). Harden mobile
devices, workstations, switches/routers, cloud, servers, ICS, embedded, IoT.
Wireless: WPA3, RADIUS/802.1X (enterprise), site surveys, heat maps.
Mobile: MDM, BYOD / COPE / CYOD, containerisation.
Application security: input validation, secure cookies, static & dynamic
code analysis, code signing, sandboxing.

## Asset management

Acquisition/procurement → assignment (ownership, classification) →
monitoring/tracking (inventory, enumeration) → disposal (sanitisation,
destruction, certification, data retention).

## Vulnerability management

Identify (vulnerability scans, application/code analysis, threat feeds, pen
testing, bug bounty) → analyse (**CVSS** score, **CVE** identifier,
false positive vs false negative, prioritisation, exposure factor,
environmental variables, risk tolerance) → respond (patch, insurance,
segmentation, compensating controls, exceptions) → **validate** (rescan,
audit, verify) → report.

## Monitoring & alerting

Log aggregation, alerting, scanning, reporting, archiving, alert response
(quarantine, **alert tuning**). Tools: **SIEM**, SCAP, benchmarks, agents vs
agentless, antivirus, DLP, SNMP traps, NetFlow, vulnerability scanners.

## Enterprise security capabilities

Firewall rules & ports, IDS/IPS signatures, web filtering (agent-based,
proxy, URL categories, reputation), OS security (GPO, SELinux), secure
protocols (replace Telnet→SSH, HTTP→HTTPS, FTP→SFTP, LDAP→LDAPS, SNMPv1/2→v3),
DNS filtering, email security (**SPF, DKIM, DMARC**, gateway), FIM, DLP,
NAC, EDR/XDR, user behaviour analytics.

## Identity & access management

Provisioning/de-provisioning, permission assignment, identity proofing,
federation, SSO (**LDAP, OAuth, SAML**), interoperability, attestation.
Access control models: **mandatory (MAC)**, **discretionary (DAC)**,
**role-based (RBAC)**, rule-based, attribute-based (ABAC), time-of-day.
MFA factors: something you know / have / are / somewhere you are.
Passwordless, passkeys. **PAM**: just-in-time permissions, password vaulting,
ephemeral credentials.

## Automation & orchestration

Use cases: user provisioning, resource provisioning, guard rails, security
groups, ticket creation, escalation, enabling/disabling services, CI testing,
API integrations. Benefits: efficiency, baseline enforcement, faster reaction,
workforce multiplier. Risks: complexity, cost, single point of failure,
technical debt.

## Incident response

**Process**: Preparation → Detection → Analysis → Containment → Eradication →
Recovery → Lessons learned.
Training, testing (tabletop exercise, simulation), root cause analysis,
threat hunting, **digital forensics**: legal hold, **chain of custody**,
acquisition (order of volatility: CPU/cache → RAM → swap → disk → remote logs
→ backups), reporting, preservation, e-discovery.

## Data sources for investigations

Firewall, application, endpoint, OS-specific security logs, IPS/IDS,
network logs, metadata; vulnerability scans, automated reports, dashboards,
packet captures.
