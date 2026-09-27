# Lab 03 — Incident write-ups on public datasets

## Goal

Practise the full analyst loop on **real, public** training datasets: scope
the question, investigate with the right tool, record evidence, map to
ATT&CK, and write a report a manager and an L2/L3 analyst can both use.
(Security+ D4 — incident response process; D2 — indicators; D5 — reporting.)

## Setup

| Write-up | Dataset | Source | Tools |
|----------|---------|--------|-------|
| [IR-01](IR-01-malware-traffic-pcap.md) | A Malware-Traffic-Analysis.net training exercise (pcap) | <https://www.malware-traffic-analysis.net/training-exercises.html> | Wireshark, tshark, Zeek (optional) |
| [IR-02](IR-02-splunk-bots-v1.md) | Splunk Boss of the SOC v1 | <https://github.com/splunk/botsv1> | Splunk Enterprise (free trial / dev licence) |
| [IR-03](IR-03-evtx-password-spray.md) | EVTX-ATTACK-SAMPLES — `Credential Access/kerberos_pwd_spray_4771.evtx` | <https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES> | EvtxECmd / `evtx_dump`, Event Viewer, Chainsaw or Hayabusa (optional) |

Alternative/extra dataset: **OTRF Security-Datasets** (formerly Mordor) —
<https://github.com/OTRF/Security-Datasets> / <https://securitydatasets.com/> —
JSON exports of simulated ATT&CK techniques, easy to load into Wazuh/ELK/Splunk.

- Work inside an isolated analysis VM (snapshots, no shared folders, no
  credentials). Malware-traffic zips are password-protected for a reason.
- Record the SHA256 of every file analysed (chain of custody habit).
- Each write-up follows [`TEMPLATE.md`](TEMPLATE.md).

> **Honesty note:** these write-ups are *investigation plans and report
> skeletons*. The analysis steps are based on how these datasets are
> structured, but **no findings are filled in** — they are left as `TBD` until
> I have actually analysed the data. No answers from other people's
> write-ups are copied here.

## Steps

1. Download one dataset into the analysis VM, verify its hash, note the URL and date.
2. Copy `TEMPLATE.md` sections into the write-up and work through the
   investigation steps.
3. Fill evidence tables with exact queries/filters and results (screenshots in `evidence/`).
4. Map confirmed behaviour to ATT&CK and update the
   [mapping table](../04-attack-mapping/).
5. Write the executive summary **last**.

## Evidence

- Completed write-ups with query outputs and screenshots (`evidence/IR-0x/`).
- File hashes of the datasets analysed.

## What I learned

_To be completed by Lucas._
