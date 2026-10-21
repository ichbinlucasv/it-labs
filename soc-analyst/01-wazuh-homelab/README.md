# Lab 01 — Wazuh home lab (SIEM / XDR)

**English** · [Français](README.fr.md) · [Deutsch](README.de.md)

**Status:** Done — the six test activities are detected by [`detect.py`](detect.py) on a synthetic log. The Wazuh all-in-one installer was not run; it wants its own VM and several gigabytes of RAM. This page is the triage loop, not a claim that a Wazuh dashboard was deployed.

## Goal

Deploy a small, self-hosted SIEM with Wazuh, enrol a Windows and a Linux
endpoint, generate benign "attack-like" activity, and practise alert triage the
way a junior SOC analyst would. (Security+ D4 — SIEM, log aggregation,
alerting, FIM, vulnerability detection.)

## Setup

| VM | Role | Resources (lab) | IP |
|----|------|-----------------|----|
| `wazuh01` | Wazuh server + indexer + dashboard (all-in-one) | 4 vCPU, 8 GB RAM, 50 GB disk (Wazuh quickstart minimum for ~1–25 agents) | 10.20.30.30 |
| `ws01` | Windows 11 + Sysmon + Wazuh agent | 2 vCPU, 4 GB | 10.20.30.50 |
| `web01` | Ubuntu 24.04 + auditd + Wazuh agent | 1 vCPU, 2 GB | 10.20.30.40 |

- Isolated host-only / internal network; NAT only for package downloads.
- Official docs: <https://documentation.wazuh.com/current/quickstart.html>
  (at the time of writing the quickstart installs Wazuh **4.14** — always use
  the version in the current docs).

## Steps

### 1. Install the all-in-one server

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
less wazuh-install.sh                 # read scripts before piping them to bash
sudo bash ./wazuh-install.sh -a
# The admin password is printed at the end; store it in a password manager,
# never in this repo. Dashboard: https://10.20.30.30
```

### 2. Enrol agents

From the dashboard: **Agents → Deploy new agent**, choose OS, set the server
address `10.20.30.30`, copy the generated command. Verify on the server:

```bash
sudo /var/ossec/bin/agent_control -l
```

### 3. Improve telemetry

- **Windows:** install Sysmon with a community config
  ([SwiftOnSecurity/sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config)
  or [olafhartong/sysmon-modular](https://github.com/olafhartong/sysmon-modular)),
  then add to the agent's `ossec.conf`:

  ```xml
  <localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
  </localfile>
  ```

  Enable PowerShell Script Block Logging (event 4104) via GPO/local policy.
- **Linux:** install `auditd`, add rules (examples in
  [lab 02](../02-sysmon-auditd-logs/)), and make sure the agent reads
  `/var/log/audit/audit.log`.
- **FIM:** add `<directories check_all="yes" realtime="yes">/etc</directories>`
  to the `syscheck` block on `web01`.

### 4. Generate benign test activity (own lab only)

| Activity | Expected alert family |
|----------|-----------------------|
| 10 wrong SSH passwords to `web01` from another lab VM | sshd authentication failures / brute force |
| `sudo` with wrong password | PAM / sudo failures |
| Create and delete a local user on `web01` | User added/removed |
| Edit `/etc/hosts` | FIM integrity checksum changed |
| On `ws01`: `powershell -EncodedCommand` running `Write-Output test` | Sysmon/PowerShell rules |
| Add a `HKCU\...\Run` value pointing to `notepad.exe` | Registry persistence (Sysmon 13) |

Optionally use **Atomic Red Team** tests in the lab VM *only*, after reading
each test.

### 5. Triage workflow for every alert

1. What rule fired, level, and which agent?
2. Who (user), what (process/command), where (host/IP), when (timestamps, UTC)?
3. Is it expected? (change ticket, admin activity, known software)
4. Pivot: other events from same host/user/IP ±15 min.
5. Verdict: true positive / benign true positive / false positive → document.
6. Tune: exceptions for confirmed false positives (with justification).

### 6. Optional — ELK comparison

The Elastic Stack (Elasticsearch + Kibana + Elastic Agent/Fleet) can collect
the same logs. Wazuh ships its own indexer/dashboard (forks of OpenSearch), so
running both on one small VM is not recommended; try ELK on a separate VM and
compare: rule language, dashboards, resource usage.

### Runnable detection loop

The activity table above is encoded as fictional events in
[`samples/activity.synthetic.jsonl`](samples/activity.synthetic.jsonl)
(documentation addresses only). From this directory:

```bash
python3 detect.py --check
```

Expected rules: `ssh-bruteforce`, `sudo-failure`, `user-added`, `fim-hosts`,
`powershell-encoded`, `run-key`. Each alert includes a who/what/where/when note
and a verdict.

The quickstart `wazuh-install.sh -a` block higher up is still the procedure
for a future VM. It was not executed here.

## Evidence

- `detect.py` raises one alert per activity in the table, including the `/etc/hosts` checksum change (`aaaaaaaa…` → `bbbbbbbb…`, placeholders, not real file hashes).
- No Wazuh dashboard screenshot, because no Wazuh manager was installed.

## What I learned

- A SIEM lab is the triage habit: rule name, host, time, and a verdict written down. The engine can be a short Python script while the Wazuh installer waits for a bigger machine.
- Five SSH failures from `203.0.113.45` with no success from that address is a true positive for guessing. Alice's later success comes from `10.20.30.5` and is a different source.
- Word as the parent of `powershell.exe -enc` is not "a user opened a document". The parent image is the part that changes the verdict.
- A FIM hit on `/etc/hosts` is a benign true positive when a change ticket exists, and an incident when it does not. The alert cannot know which.
