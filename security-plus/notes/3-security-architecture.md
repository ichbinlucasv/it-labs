# Domain 3 — Security Architecture (≈18 %)

**English** · [Français](3-security-architecture.fr.md) · [Deutsch](3-security-architecture.de.md)

## Architecture models

| Model | Security considerations |
|-------|------------------------|
| Cloud (IaaS/PaaS/SaaS) | **Shared responsibility** — the customer always owns data & identities |
| Hybrid | Consistent policy across on-prem and cloud |
| Infrastructure as Code | Review templates like code; drift detection |
| Serverless / microservices | Many small attack surfaces; API security |
| Network: on-prem, centralised vs decentralised | Single point of failure vs harder management |
| Containers & virtualisation | Image provenance, isolation, patching base images |
| IoT, ICS/SCADA, RTOS, embedded | Hard to patch → segment them |
| High availability | Redundancy, load balancing, clustering |

Considerations: availability, resilience, cost, responsiveness, scalability,
ease of deployment/recovery, patch availability, risk transference, power,
compute.

## Network security

- **Zones / segmentation**: DMZ (screened subnet), VLANs, air gap.
- **Devices**: firewall (stateful, NGFW, WAF, UTM), IDS/IPS (inline vs tap),
  jump server, proxy (forward/reverse), load balancer, 802.1X/NAC, sensors.
- **Failure modes**: fail-open (availability) vs fail-closed (security).
- **Secure communication**: VPN (IPsec, TLS), SD-WAN, SASE (network + security
  as cloud service).
- **Selection of controls** by attack surface, connectivity, device placement.

## Data protection

- **Data types**: regulated, trade secret, intellectual property, legal,
  financial, human- and non-human-readable.
- **Classifications**: public, private, sensitive, confidential, restricted,
  critical.
- **States**: at rest, in transit, in use.
- **Sovereignty / geolocation**: laws of the country where data is stored
  (GDPR / RGPD in France and the EU).
- **Methods**: encryption, hashing, masking, tokenisation, obfuscation,
  segmentation, permission restrictions.

## Resilience & recovery

- **Sites**: hot (ready now), warm (hardware, needs data), cold (space only);
  geographic dispersion.
- **Backups**: onsite/offsite, frequency, encryption, snapshots, replication,
  journaling. Test restores!
- **Power**: UPS (short term), generator (long term).
- **Continuity of operations**, capacity planning (people, technology,
  infrastructure), testing (tabletop, fail-over, simulation, parallel processing).
- **Metrics**: RTO (how fast to restore), RPO (how much data loss acceptable),
  MTTR (mean time to repair), MTBF (mean time between failures).
