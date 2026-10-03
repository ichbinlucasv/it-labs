# IT labs

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

I'm Lucas. I study cybersecurity and I want a first job in France, in
helpdesk or as a junior SOC analyst (alternance or POEI). Linux is the
machine I actually live on. Windows is a lab on that same PC.

France is where I am looking first. Germany is the other option. I can
work there in English, and I am learning German. Once I am working, I
start a distance degree at IU (Internationale Hochschule). The pages
exist in all three languages so a reader in either country can open
them. I update the English page first. If a translation disagrees with
it, the English page wins.

This repo is the practice, not a finished résumé. **Done** means I ran the
check and kept the output. It does not mean I am fast, or that I would
skip the docs on a real ticket.

I use bash every day and PowerShell on the Windows lab. Python is the
small toolkit below. Rust is the language I like building in:
`log-analyzer` and `fim` here, plus [Frihart](https://codeberg.org/ichbinlucasv/Frihart)
and [HashChat](https://codeberg.org/ichbinlucasv/HashChat) in their own
repos. C is on the study list. There is no C project in this repo yet.

Portuguese is my first language. French and English are both C1.
Security+ SY0-701 and HTB Academy are in progress.

The machine, the languages, and the AI tools are in
[How I work](how-i-work.md). Short version: CachyOS (Arch) every day,
Fedora is the other distro I like, Windows only as virtual machines,
Grok for a second pass, and a local Qwen model through Ollama, shared
by Hermes, OpenClaw, and Odysseus. A lab is **Done** when I have run
the check myself.

### Lab status

| Status | Meaning |
|--------|---------|
| **Done** | The code or config runs and its checks pass in this repo |
| **In progress** | Partly verified — for example syntax checked or run on synthetic data, but not tested end to end in a real environment |
| **Planned** | A written procedure that hasn't been run in a real environment yet |

Current count: 10 Done, 4 In progress, 3 Planned (see the skills matrix below).

> Company names, user names, and addresses in the exercises are examples
> (`example.com`, RFC 5737 `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`).
> The Windows domain lab is a real lab on this PC, on the default libvirt
> NAT `192.168.122.0/24`. That range is not my home LAN, and it is not
> routed on the internet. Public training sets (Wireshark samples,
> EVTX-ATTACK-SAMPLES) are quoted with their original values and cited.
> No passwords, no public IP, and no offensive steps aimed at anyone else.

---

## Repository map

| Path | What it contains |
|------|------------------|
| [how-i-work.md](how-i-work.md) | Daily machine (CachyOS / Arch), the Fedora drill, the languages, and Grok plus a local Qwen model |
| [`helpdesk/`](helpdesk/) | Tickets, Linux and Windows troubleshooting, a Samba AD lab, and a Windows Server domain I actually promoted (`lab.local`) |
| [`networking/`](networking/) | Subnetting exercises + answer key, packet-capture analysis (Wireshark/tcpdump), nftables host firewall |
| [`soc-analyst/`](soc-analyst/) | Wazuh home lab, Sysmon + auditd log analysis (synthetic samples), incident write-up templates on public datasets, ATT&CK mapping, Sigma rules |
| [`python/`](python/) | `seclab` package: SSH auth.log summariser, IOC extractor (defang/refang), hash checker — stdlib only, pytest suite |
| [`rust/`](rust/) | Cargo workspace: `log-analyzer` and `fim` (file-integrity monitor) crates with unit tests |
| [`security-plus/`](security-plus/) | SY0-701 study notes per domain + flashcards CSV |
| [`templates/`](templates/) | Blank forms I copy on a work day: helpdesk, SOC, and one language at a time |
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
| [helpdesk/01 Ticket writing](helpdesk/01-ticket-writing/) | Done | ○ | | | ● | ○ | ITSM, clear communication, escalation |
| [helpdesk/02 Windows troubleshooting](helpdesk/02-windows-troubleshooting/) | Planned | | ○ | ○ | ● | | Event Viewer, PowerShell, networking, SFC/DISM |
| [helpdesk/03 Linux troubleshooting](helpdesk/03-linux-troubleshooting/) | Done | | ○ | ○ | ● | | systemd, journalctl, disk/DNS/permissions |
| [helpdesk/04 Samba AD DC](helpdesk/04-samba-ad-lab/) | In progress | ● | | ● | ● | | Identity, groups, GPO concepts, least privilege |
| [helpdesk/05 M365 basics](helpdesk/05-m365-basics/) | Planned | ● | ○ | ● | ● | ○ | Entra ID, licences, MFA, Conditional Access concepts |
| [helpdesk/06 Windows domain](helpdesk/06-windows-domain/) | In progress | ● | | ● | ● | | AD DS, client in the domain, helpdesk reset, GPO check |
| [networking/01 Subnetting](networking/01-subnetting/) | Done | | | ● | | | CIDR, VLSM, addressing plans |
| [networking/02 Packet capture](networking/02-packet-capture/) | Done | | ● | ○ | ● | | Wireshark filters, tcpdump, protocol analysis |
| [networking/03 nftables firewall](networking/03-nftables-firewall/) | Done | ○ | ● | ● | ○ | | Default-deny, stateful filtering, logging |
| [soc-analyst/01 Wazuh home lab](soc-analyst/01-wazuh-homelab/) | Planned | | ○ | ○ | ● | | SIEM/XDR deployment, agents, alert triage |
| [soc-analyst/02 Sysmon + auditd](soc-analyst/02-sysmon-auditd-logs/) | Done | | ● | | ● | | Endpoint telemetry, log correlation |
| [soc-analyst/03 Incident write-ups](soc-analyst/03-incident-writeups/) | In progress | | ● | | ● | ○ | IR lifecycle, reporting, evidence handling |
| [soc-analyst/04 ATT&CK mapping](soc-analyst/04-attack-mapping/) | Done | | ● | | ● | | Threat-informed detection coverage |
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

## What I have actually run

| Item | How |
|------|-----|
| Python tools | `pytest` — 35 tests pass |
| Rust crates | `cargo test` (11 unit tests) and `cargo clippy --all-targets -- -D warnings` clean, `cargo fmt --check` clean |
| Sigma rules | valid YAML; `sigma check` 0 errors/issues (sigma-cli 3.1.0); the 8 original rules fire on the synthetic samples via the SQLite backend; the Kerberos spraying rule fires on a public EVTX sample |
| Linux troubleshooting | 7 break/fix scenarios run in a Debian 13 systemd container (`systemd-nspawn`); terminal output in `helpdesk/03-linux-troubleshooting/evidence/` (OOM kill not reproducible there) |
| Samba AD DC | provisioned in a Debian 13 container; DNS SRV, Kerberos, OUs/groups/users, lockout policy and helpdesk delegation tested; Windows client join not done |
| Windows Server domain | `dc01` promoted to `lab.local` on 5 Sep 2026. On 4 Oct 2026 `win11-soc` was already in that domain (`OU=Workstations`, DNS to the DC). From that client the helpdesk credential reset `jdoe`; `jdoe` could not reset someone else. Output in `helpdesk/06-windows-domain/evidence/win11-2026-10-04.txt`. Lockout threshold is 0, so no unlock yet. `Lab-Workstation-Hardening` is linked and empty |
| nftables ruleset | `nft -c -f` OK; traffic-tested with three network namespaces (admin / outside / blocklisted client), counters and kernel log checked |
| Packet capture | own capture generated in a network namespace and analysed with tshark; public Wireshark `dns.cap` sample analysed with a mini-report |
| Sysmon / auditd samples | every question answered, UTC timeline and IOC list written; `ausearch`/`aureport` on the synthetic auditd log |
| Incident write-up IR-03 | public Kerberos password-spray EVTX parsed with python-evtx and analysed end to end |
| ATT&CK mapping | 15 technique IDs checked against the ATT&CK Enterprise 19.2 STIX bundle; Navigator layer generated |
| Subnetting answers | computed with Python `ipaddress` |
| Flashcards | 99 cards, parsed with Python `csv` |

Still open: an interactive helpdesk sign-in on the Windows 11 desktop,
a real unlock once the lockout threshold is not 0, settings inside
`Lab-Workstation-Hardening`, the Windows troubleshooting scenarios,
joining a Windows client to the Samba domain, Wazuh, an M365 tenant,
an isolated VM for the malware pcaps, and a Splunk box. Those pages
say so.

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
- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46) — profile open. Academy (SOC Analyst / fundamentals) is in progress. No rank on this page.
- [TryHackMe](https://tryhackme.com/p/ichbinlucasv) — account open, in progress. No rank on this page.
- [Boot.dev](https://www.boot.dev/u/ichbinlucasv) — account open. The public profile stays hidden until level 10, so no level here.

One finished SOC write-up with a timeline is
[IR-03](soc-analyst/03-incident-writeups/IR-03-evtx-password-spray.md).
The 4 Oct 2026 domain check, helpdesk reset, and the empty-GPO ticket
are in [lab 06](helpdesk/06-windows-domain/). Forms for the next run:
[templates/career/](templates/career/).

## Contact

These are the public ones. Lab passwords and private notes stay off this repo.

- Email: ichbinlucas@pm.me
- [LinkedIn](https://www.linkedin.com/in/lucas-nunes-soares-63148637b/)
- [X](https://x.com/ichbinlucasv)
- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46)

## Licence

Code: [MIT](LICENSE). Documentation (Markdown, notes, flashcards):
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE).
