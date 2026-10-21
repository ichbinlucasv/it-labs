# Lab 03 — Incident write-ups on public datasets

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**English** · [Deutsch](README.de.md)

**Status:** Done — [IR-03](IR-03-evtx-password-spray.md) is the public EVTX write-up; [IR-01](IR-01-malware-traffic-pcap.md) is a synthetic pcap analysed with tshark; [IR-02](IR-02-splunk-bots-v1.md) is the same questions answered in SQL. The malware-traffic-analysis.net zip and the Splunk BOTS archive were not opened.

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

> **Honesty note:** IR-03 is an analysis of the public EVTX sample.
> IR-01 and IR-02 were plans for a malware-traffic pcap and for Splunk BOTS.
> Those two downloads were not opened. The pages now record a synthetic pcap
> rebuilt by `generate_lab_pcap.py` and a small SQL log set in
> `investigate_sql.py`. Command output is in `evidence/`. No answers from
> other people's write-ups are copied here.

## Steps

1. Download one dataset into the analysis VM, verify its hash, note the URL and date.
2. Copy `TEMPLATE.md` sections into the write-up and work through the
   investigation steps.
3. Fill evidence tables with exact queries/filters and results (screenshots in `evidence/`).
4. Map confirmed behaviour to ATT&CK and update the
   [mapping table](../04-attack-mapping/).
5. Write the executive summary **last**.

## Evidence

- [IR-03](IR-03-evtx-password-spray.md) with [`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt)
  (SHA256 of the EVTX, event table, Sigma replay).
- [IR-01](IR-01-malware-traffic-pcap.md) with [`evidence/IR-01/analysis.txt`](evidence/IR-01/analysis.txt)
  (tshark on the generated pcap; SHA256 in [`evidence/IR-01/sha256.txt`](evidence/IR-01/sha256.txt)).
- [IR-02](IR-02-splunk-bots-v1.md) with [`evidence/IR-02/analysis.txt`](evidence/IR-02/analysis.txt).

## What I learned

- Small datasets can still tell a complete story: 12 events were enough to
  see enumeration, spraying and one successful guess.
- Kerberos status codes leak information: `0x6` vs `0x18` tells an attacker
  which accounts exist.
- My detection alerted on the failures, but the most important event was the
  success right after — a detection plan needs the "what happened next" rule too.
- Data normalisation matters: the same host appeared as `172.16.66.1` and
  `::ffff:172.16.66.1`.
- Not every suspicious event belongs to the attacker (the 1102 log clear);
  saying "noted, not attributed" is better than over-claiming.
- A 60-second HTTP interval is the finding in the synthetic pcap. Four
  `POST /login` rows are a brute-force question, and `notes.txt` is not a web shell.
- The encoded PowerShell blob in the SQL set decodes to `echo test`. The parent
  process (Word) is what makes it worth escalating, not the decoded text.
