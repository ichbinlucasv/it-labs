# Domain 1 — General Security Concepts (≈12 %)

## Security control categories & types

| Category | Examples |
|----------|----------|
| Technical | Firewall rules, MFA, encryption, EDR |
| Managerial | Policies, risk assessments, security awareness programme |
| Operational | Guards, change management, backups performed by staff |
| Physical | Locks, fences, badge readers, CCTV |

| Type | Purpose | Example |
|------|---------|---------|
| Preventive | Stop it happening | Account lockout, firewall deny |
| Deterrent | Discourage | Warning banner, visible camera |
| Detective | Notice it happened | IDS, log review, SIEM alert |
| Corrective | Fix after the event | Restore backup, patch |
| Compensating | Alternative when the ideal control isn't possible | Network isolation for an unpatchable machine |
| Directive | Tell people what to do | Policy, "authorised personnel only" sign |

## Core principles

- **CIA triad**: Confidentiality (encryption, access control), Integrity
  (hashing, signatures), Availability (redundancy, backups, DDoS protection).
- **Non-repudiation**: the sender can't deny — digital signatures.
- **AAA**: Authentication (who are you), Authorisation (what may you do),
  Accounting (what did you do — logs).
- **Zero Trust**: never trust by location; verify explicitly every request.
  *Control plane* (policy engine, policy administrator) decides; *data plane*
  (policy enforcement point) enforces. Adaptive identity, threat-scope
  reduction, implicit trust zones.
- **Gap analysis**: current state vs desired state (e.g. vs a framework).
- **Physical**: bollards, access control vestibule (mantrap), lighting,
  sensors (infrared, pressure, microwave, ultrasonic).
- **Deception**: honeypot (one host), honeynet (network), honeyfile, honeytoken
  (fake credential/data that alerts when used).

## Change management

Approval process, ownership, stakeholders, impact analysis, test results,
**backout plan**, maintenance window, SOP. Technical implications: allow/deny
lists, restricted activities, downtime, service/application restarts, legacy
applications, dependencies. Update documentation and diagrams; version control.

## Cryptography essentials

| Concept | Remember |
|---------|----------|
| Symmetric | One shared key, fast (AES). Problem: key distribution |
| Asymmetric | Public/private key pair (RSA, ECC). Used for key exchange & signatures |
| Hashing | One-way, fixed length (SHA-256). Integrity, password storage (+ salt) |
| Salt | Random value per password → defeats rainbow tables |
| Key stretching | PBKDF2, bcrypt, Argon2 — slow on purpose |
| Digital signature | Hash signed with sender's **private** key, verified with their **public** key |
| Encrypt for someone | Use **their public** key; they decrypt with their private key |
| PKI | CA issues certificates; CRL / OCSP (stapling) for revocation; wildcard & SAN certs |
| Key escrow | Third party holds keys for recovery |
| TPM / HSM / secure enclave | Hardware protection of keys (TPM = on the board, HSM = dedicated appliance) |
| Obfuscation | Steganography, tokenisation (replace value with token), data masking |
| Blockchain | Distributed, tamper-evident ledger |
| Encryption levels | Full-disk, partition, volume, file, database, record; transport (TLS, IPsec) |
