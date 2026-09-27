# SOC analyst labs

| Lab | Focus |
|-----|-------|
| [01-wazuh-homelab](01-wazuh-homelab/) | Deploy Wazuh (SIEM/XDR) with Windows + Linux agents; optional ELK comparison |
| [02-sysmon-auditd-logs](02-sysmon-auditd-logs/) | Investigate endpoint telemetry using **synthetic** Sysmon, Windows Security and auditd samples |
| [03-incident-writeups](03-incident-writeups/) | Three structured investigation write-ups on **public** datasets (sources cited) |
| [04-attack-mapping](04-attack-mapping/) | MITRE ATT&CK mapping of lab scenarios, detections and data sources |
| [05-sigma-rules](05-sigma-rules/) | Sigma detection rules, validated with `sigma check` and replayed on the samples |

> Safety: public malware-traffic datasets contain real malicious artefacts.
> Analyse them only inside an isolated VM, never on a work or personal machine,
> and never re-host the samples.
