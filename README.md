# IT & Security Home-Lab Portfolio — Lucas

Hands-on labs documenting my path into IT support and security operations.
I am looking for a first role in France as **helpdesk / IT support technician**
or **junior SOC analyst** (alternance or POEI welcome), while preparing
**CompTIA Security+ (SY0-701)** and working through **HTB Academy** modules.

Languages: Portuguese (native), French (C1), English (C1).

> Everything here was built in my own lab. All hostnames, users, companies and
> IP addresses are fictional (`example.com`, RFC 5737 ranges `192.0.2.0/24`,
> `198.51.100.0/24`, `203.0.113.0/24`, and RFC 1918 ranges for the lab LAN).
> No real personal data, no credentials, and no offensive tooling aimed at
> third parties.

---

## Résumé en français

Ce dépôt rassemble mes travaux pratiques en informatique et cybersécurité :
support utilisateur (rédaction de tickets, dépannage Windows/Linux, Active
Directory avec Samba, notions Microsoft 365), réseau (sous-réseaux, analyse de
captures Wireshark/tcpdump, pare-feu nftables), analyse SOC (Wazuh, Sysmon,
auditd, règles Sigma, cartographie MITRE ATT&CK, rapports d'incident à partir
de jeux de données publics), ainsi que de petits outils en Python et en Rust
avec tests automatisés. Je prépare la certification CompTIA Security+ SY0-701
et je recherche un premier poste en **support informatique / technicien
helpdesk** ou **analyste SOC junior**, idéalement en **alternance** ou via une
**POEI**. Chaque lab suit la même structure : objectif, mise en place, étapes,
preuves, et ce que j'ai appris.

---

## Repository map

| Path | What it contains |
|------|------------------|
| [`helpdesk/`](helpdesk/) | Ticket writing, Windows & Linux troubleshooting runbooks, Samba AD DC user-management lab, Microsoft 365 admin basics |
| [`networking/`](networking/) | Subnetting exercises + answer key, packet-capture analysis (Wireshark/tcpdump), nftables host firewall |
| [`soc-analyst/`](soc-analyst/) | Wazuh home lab, Sysmon + auditd log analysis (synthetic samples), incident write-up templates on public datasets, ATT&CK mapping, Sigma rules |
| [`python/`](python/) | `seclab` package: SSH auth.log summariser, IOC extractor (defang/refang), hash checker — stdlib only, pytest suite |
| [`rust/`](rust/) | Cargo workspace: `log-analyzer` and `fim` (file-integrity monitor) crates with unit tests |
| [`security-plus/`](security-plus/) | SY0-701 study notes per domain + flashcards CSV |
| [`.forgejo/workflows/`](.forgejo/workflows/) | Optional CI (Forgejo/Codeberg Actions; GitHub-compatible syntax) |

Every lab README follows the same layout: **Goal · Setup · Steps · Evidence ·
What I learned**.

---

## Skills matrix — labs × Security+ SY0-701 domains

Domains: **D1** General Security Concepts · **D2** Threats, Vulnerabilities &
Mitigations · **D3** Security Architecture · **D4** Security Operations ·
**D5** Security Program Management & Oversight.

`●` = primary focus, `○` = secondary.

| Lab | D1 | D2 | D3 | D4 | D5 | Practical skills |
|-----|:--:|:--:|:--:|:--:|:--:|------------------|
| [helpdesk/01 Ticket writing](helpdesk/01-ticket-writing/) | ○ | | | ● | ○ | ITSM, clear communication, escalation |
| [helpdesk/02 Windows troubleshooting](helpdesk/02-windows-troubleshooting/) | | ○ | ○ | ● | | Event Viewer, PowerShell, networking, SFC/DISM |
| [helpdesk/03 Linux troubleshooting](helpdesk/03-linux-troubleshooting/) | | ○ | ○ | ● | | systemd, journalctl, disk/DNS/permissions |
| [helpdesk/04 Samba AD DC](helpdesk/04-samba-ad-lab/) | ● | | ● | ● | | Identity, groups, GPO concepts, least privilege |
| [helpdesk/05 M365 basics](helpdesk/05-m365-basics/) | ● | ○ | ● | ● | ○ | Entra ID, licences, MFA, Conditional Access concepts |
| [networking/01 Subnetting](networking/01-subnetting/) | | | ● | | | CIDR, VLSM, addressing plans |
| [networking/02 Packet capture](networking/02-packet-capture/) | | ● | ○ | ● | | Wireshark filters, tcpdump, protocol analysis |
| [networking/03 nftables firewall](networking/03-nftables-firewall/) | ○ | ● | ● | ○ | | Default-deny, stateful filtering, logging |
| [soc-analyst/01 Wazuh home lab](soc-analyst/01-wazuh-homelab/) | | ○ | ○ | ● | | SIEM/XDR deployment, agents, alert triage |
| [soc-analyst/02 Sysmon + auditd](soc-analyst/02-sysmon-auditd-logs/) | | ● | | ● | | Endpoint telemetry, log correlation |
| [soc-analyst/03 Incident write-ups](soc-analyst/03-incident-writeups/) | | ● | | ● | ○ | IR lifecycle, reporting, evidence handling |
| [soc-analyst/04 ATT&CK mapping](soc-analyst/04-attack-mapping/) | | ● | | ● | | Threat-informed detection coverage |
| [soc-analyst/05 Sigma rules](soc-analyst/05-sigma-rules/) | | ● | | ● | | Detection engineering, pySigma/sigma-cli |
| [python/ seclab tools](python/) | ○ | ● | | ● | | Regex, parsing, hashing, automated testing |
| [rust/ log-analyzer + fim](rust/) | ○ | ○ | ○ | ● | | Integrity monitoring, systems programming |
| [security-plus/ notes & flashcards](security-plus/) | ● | ● | ● | ● | ● | Exam preparation across all domains |

---

## Quick start

```bash
# Python tools + tests
cd python && python3 -m venv .venv && . .venv/bin/activate
pip install -e '.[test]' && pytest

# Rust workspace
cd rust && cargo test && cargo clippy --all-targets -- -D warnings

# Sigma rules
pip install sigma-cli && sigma check soc-analyst/05-sigma-rules/rules/
```

## Current learning

- CompTIA Security+ SY0-701 — in progress
- HTB Academy — SOC Analyst / fundamentals modules in progress

## Licence

Code: [MIT](LICENSE). Documentation (Markdown, notes, flashcards):
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE).
