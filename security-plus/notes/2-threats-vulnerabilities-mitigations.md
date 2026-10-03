# Domain 2 — Threats, Vulnerabilities & Mitigations (≈22 %)

**English** · [Français](2-threats-vulnerabilities-mitigations.fr.md) · [Deutsch](2-threats-vulnerabilities-mitigations.de.md)

## Threat actors

| Actor | Motivation | Resources |
|-------|-----------|-----------|
| Nation-state | Espionage, disruption, war | Very high (APT) |
| Organised crime | Money (ransomware, fraud) | High |
| Hacktivist | Ideology | Variable |
| Insider threat | Revenge, money, negligence | Has access already |
| Unskilled attacker | Thrill, reputation | Low — uses others' tools |
| Shadow IT | Convenience (not malicious) | Unmanaged risk |

Attributes: internal/external, resources/funding, sophistication.

## Threat vectors & attack surface

Message-based (email, SMS = smishing, IM), images, files, voice (vishing),
removable devices, vulnerable software (client-based vs agentless),
unsupported systems, unsecure networks (wireless, wired, Bluetooth), open
ports, default credentials, supply chain (MSPs, vendors, suppliers).

**Human vectors / social engineering:** phishing, spear phishing, whaling,
BEC (business email compromise), pretexting, impersonation, watering hole,
brand impersonation, typosquatting, misinformation/disinformation.

## Vulnerability types

- **Application:** memory injection, buffer overflow, race conditions
  (TOC/TOU), malicious update.
- **Web:** SQL injection (SQLi), cross-site scripting (XSS), CSRF, SSRF,
  directory traversal.
- **OS / firmware / hardware:** end-of-life, legacy, unpatched firmware.
- **Virtualisation:** VM escape, resource reuse.
- **Cloud:** misconfiguration (public buckets!), weak IAM.
- **Cryptographic:** weak algorithms, poor key management, downgrade.
- **Mobile:** side loading, jailbreaking/rooting.
- **Zero-day:** no patch exists yet.

## Indicators of malicious activity

Account lockouts, concurrent sessions in impossible places ("impossible
travel"), blocked content, resource consumption spikes, out-of-cycle logging,
missing logs, published/documented breach data.

**Malware families:** ransomware, trojan, worm (self-propagating), spyware,
bloatware, virus, keylogger, logic bomb, rootkit.
**Network attacks:** DDoS (amplified/reflected), DNS attacks, wireless (evil
twin, deauth), on-path (MITM), credential replay.
**Password attacks:** spraying (few passwords × many users), brute force
(many passwords × one user), credential stuffing (reused breached creds).
**Other:** privilege escalation, replay, forgery, downgrade, collision
(hash), birthday attack.

## Mitigations

Segmentation, access control (ACLs, permissions), application allow-listing,
isolation, patching, encryption, monitoring, least privilege, configuration
enforcement, decommissioning, **hardening** (disable unused ports/services,
change defaults, remove unnecessary software, host firewall, EDR/HIPS).
