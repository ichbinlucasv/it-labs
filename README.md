# IT & Security Lab Portfolio — Lucas

A structured lab plan I'm working through on my path into IT support and
security operations; each lab is marked **Status: Done / In progress / Planned**.
I am looking for a first role in France as **helpdesk / IT support technician**
or **junior SOC analyst** (alternance or POEI welcome), while preparing
**CompTIA Security+ (SY0-701)** and working through **HTB Academy** modules.

Languages: Portuguese (native), French (C1), English (C1).

### Lab status

| Status | Meaning |
|--------|---------|
| **Done** | The code or config runs and its checks pass in this repo |
| **In progress** | Partly verified — for example syntax checked or run on synthetic data, but not tested end to end in a real environment |
| **Planned** | A written procedure that hasn't been run in a real environment yet |

Current count: 5 Done, 5 In progress, 6 Planned (see the skills matrix below).

> All hostnames, users, companies and IP addresses are fictional (`example.com`, RFC 5737 ranges `192.0.2.0/24`,
> `198.51.100.0/24`, `203.0.113.0/24`, and RFC 1918 ranges for the lab LAN).
> No real personal data, no credentials, and no offensive tooling aimed at
> third parties.

---

## Résumé en français

Ce dépôt est un plan de labs structuré que je suis en train de réaliser, en
informatique et cybersécurité ; chaque lab porte un statut **Done** (terminé :
le code ou la configuration s'exécute et ses vérifications passent dans ce
dépôt), **In progress** (en cours : vérifié en partie, par exemple syntaxe
validée mais pas testé de bout en bout) ou **Planned** (prévu : procédure
rédigée, pas encore exécutée dans un environnement réel). Thèmes :
support utilisateur (rédaction de tickets, dépannage Windows/Linux, Active
Directory avec Samba, notions Microsoft 365), réseau (sous-réseaux, analyse de
captures Wireshark/tcpdump, pare-feu nftables), analyse SOC (Wazuh, Sysmon,
auditd, règles Sigma, cartographie MITRE ATT&CK, rapports d'incident à partir
de jeux de données publics), ainsi que de petits outils en Python et en Rust
avec tests automatisés. Je prépare la certification CompTIA Security+ SY0-701
et je recherche un premier poste en **support informatique / technicien
helpdesk** ou **analyste SOC junior**, idéalement en **alternance** ou via une
**POEI**. Chaque lab suit la même structure : statut, objectif, mise en place,
étapes, preuves, et ce que j'ai appris.

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
| [`scripts/check_repo.py`](scripts/check_repo.py) | Repo hygiene check: lab README sections, flashcards CSV, Sigma YAML, secret patterns |
| [`.forgejo/workflows-disabled/`](.forgejo/workflows-disabled/) | CI workflow, **disabled** until a runner exists (see [CI](#ci)) |

Every lab README starts with a **Status** line and follows the same layout:
**Goal · Setup · Steps · Evidence · What I learned**.

---

## Skills matrix — labs × Security+ SY0-701 domains

Domains: **D1** General Security Concepts · **D2** Threats, Vulnerabilities &
Mitigations · **D3** Security Architecture · **D4** Security Operations ·
**D5** Security Program Management & Oversight.

`●` = primary focus, `○` = secondary.

| Lab | Status | D1 | D2 | D3 | D4 | D5 | Practical skills |
|-----|--------|:--:|:--:|:--:|:--:|:--:|------------------|
| [helpdesk/01 Ticket writing](helpdesk/01-ticket-writing/) | Planned | ○ | | | ● | ○ | ITSM, clear communication, escalation |
| [helpdesk/02 Windows troubleshooting](helpdesk/02-windows-troubleshooting/) | Planned | | ○ | ○ | ● | | Event Viewer, PowerShell, networking, SFC/DISM |
| [helpdesk/03 Linux troubleshooting](helpdesk/03-linux-troubleshooting/) | Done | | ○ | ○ | ● | | systemd, journalctl, disk/DNS/permissions |
| [helpdesk/04 Samba AD DC](helpdesk/04-samba-ad-lab/) | Planned | ● | | ● | ● | | Identity, groups, GPO concepts, least privilege |
| [helpdesk/05 M365 basics](helpdesk/05-m365-basics/) | Planned | ● | ○ | ● | ● | ○ | Entra ID, licences, MFA, Conditional Access concepts |
| [networking/01 Subnetting](networking/01-subnetting/) | Done | | | ● | | | CIDR, VLSM, addressing plans |
| [networking/02 Packet capture](networking/02-packet-capture/) | In progress | | ● | ○ | ● | | Wireshark filters, tcpdump, protocol analysis |
| [networking/03 nftables firewall](networking/03-nftables-firewall/) | In progress | ○ | ● | ● | ○ | | Default-deny, stateful filtering, logging |
| [soc-analyst/01 Wazuh home lab](soc-analyst/01-wazuh-homelab/) | Planned | | ○ | ○ | ● | | SIEM/XDR deployment, agents, alert triage |
| [soc-analyst/02 Sysmon + auditd](soc-analyst/02-sysmon-auditd-logs/) | In progress | | ● | | ● | | Endpoint telemetry, log correlation |
| [soc-analyst/03 Incident write-ups](soc-analyst/03-incident-writeups/) | Planned | | ● | | ● | ○ | IR lifecycle, reporting, evidence handling |
| [soc-analyst/04 ATT&CK mapping](soc-analyst/04-attack-mapping/) | In progress | | ● | | ● | | Threat-informed detection coverage |
| [soc-analyst/05 Sigma rules](soc-analyst/05-sigma-rules/) | Done | | ● | | ● | | Detection engineering, pySigma/sigma-cli |
| [python/ seclab tools](python/) | Done | ○ | ● | | ● | | Regex, parsing, hashing, automated testing |
| [rust/ log-analyzer + fim](rust/) | Done | ○ | ○ | ○ | ● | | Integrity monitoring, systems programming |
| [security-plus/ notes & flashcards](security-plus/) | In progress | ● | ● | ● | ● | ● | Exam preparation across all domains |

---

## Quick start

```bash
# Python tools + tests
(cd python && python3 -m venv .venv && . .venv/bin/activate \
  && pip install -e '.[test]' && pytest)

# Rust workspace
(cd rust && cargo test && cargo clippy --all-targets -- -D warnings)

# Sigma rules: lint + replay on the synthetic samples
python3 -m venv .venv-sigma && . .venv-sigma/bin/activate
pip install sigma-cli pyyaml && sigma plugin install sqlite
sigma check soc-analyst/05-sigma-rules/rules/
python soc-analyst/05-sigma-rules/validate_rules.py

# Repo hygiene
python3 scripts/check_repo.py
```

## What has been verified

| Item | How |
|------|-----|
| Python tools | `pytest` — 35 tests pass |
| Rust crates | `cargo test` (11 unit tests) and `cargo clippy --all-targets -- -D warnings` clean, `cargo fmt --check` clean |
| Sigma rules | valid YAML; `sigma check` 0 errors/issues (sigma-cli 3.1.0); each rule fires on the synthetic samples via the SQLite backend |
| nftables ruleset | `nft -c -f` OK; loaded in an isolated network namespace |
| Packet-capture script | generated a capture in a network namespace; tshark commands in the lab produce the documented output |
| auditd sample | parsed by `ausearch`/`aureport` |
| Subnetting answers | computed with Python `ipaddress` |
| Flashcards | 99 cards, parsed with Python `csv` |

Things that need a real lab (Windows VMs, Wazuh server, Samba DC, M365
tenant) are documented as procedures, and their **Evidence** sections list
the screenshots/outputs still to capture.

## CI

The workflow lives in `.forgejo/workflows-disabled/ci.yml`, so Forgejo does
**not** pick it up (Codeberg's hosted runners are limited and the job would
sit queued forever). It needs a **self-hosted Forgejo runner labelled
`docker`**. To enable it:

1. Register a [Forgejo runner](https://forgejo.org/docs/latest/admin/actions/)
   with the label `docker` for this repository (Codeberg: repo *Settings →
   Actions → Runners*) and enable Actions for the repo.
2. `git mv .forgejo/workflows-disabled/ci.yml .forgejo/workflows/ci.yml`, then commit and push.

On GitHub, copy the file to `.github/workflows/` and set `runs-on: ubuntu-latest`.

## Current learning

- CompTIA Security+ SY0-701 — in progress
- HTB Academy — SOC Analyst / fundamentals modules in progress

## Licence

Code: [MIT](LICENSE). Documentation (Markdown, notes, flashcards):
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE).
