# Lab 02 — Sysmon + auditd log analysis

## Goal

Learn to reconstruct what happened on an endpoint from raw telemetry:
Windows **Sysmon** (process, network, file, registry, DNS events), Windows
**Security** logon events, and Linux **auditd** records. Build a timeline and
extract indicators. (Security+ D2 indicators of malicious activity; D4 log
data sources and investigation.)

## Setup

- Samples in [`samples/`](samples/) — **all synthetic**, see the
  [samples README](samples/README.md).
- Tools: `jq`, Python 3, and the audit userspace tools (`sudo apt install jq auditd`).
  `ausearch`/`aureport` can read a log file with `-if` without running the
  audit daemon.
- To produce real telemetry in my own lab:
  - **Sysmon** (Microsoft Sysinternals):
    <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon> —
    `sysmon64.exe -accepteula -i sysmonconfig.xml`
  - **auditd** example rules (`/etc/audit/rules.d/lab.rules`):

    ```text
    -w /etc/shadow -p r -k shadow_read
    -w /etc/passwd -p wa -k identity
    -w /var/spool/cron/ -p wa -k cron_mod
    -w /etc/crontab -p wa -k cron_mod
    -a always,exit -F arch=b64 -S execve -F dir=/tmp -k exec_tmp
    -a always,exit -F arch=b64 -S execve -F exe=/usr/bin/curl -k net_download
    ```

    Load with `sudo augenrules --load`; see also the community rule set
    <https://github.com/Neo23x0/auditd>.

### Sysmon event IDs used here

| ID | Meaning |
|---:|---------|
| 1 | Process creation (image, command line, parent, hashes) |
| 3 | Network connection |
| 11 | File created |
| 13 | Registry value set |
| 22 | DNS query |

## Steps

### Part A — Windows (Sysmon JSONL)

```bash
cd samples
# 1. Overview: count events by ID
jq -r '.EventID' sysmon.synthetic.jsonl | sort | uniq -c

# 2. Process tree: who started what?
jq -r 'select(.EventID==1) | [.UtcTime, .ParentImage, "->", .Image, .CommandLine] | @tsv' sysmon.synthetic.jsonl

# 3. Decode the encoded PowerShell (UTF-16LE base64)
jq -r 'select((.CommandLine // "") | test("-enc ")) | .CommandLine | split("-enc ")[1]' sysmon.synthetic.jsonl \
  | base64 -d | iconv -f UTF-16LE -t UTF-8; echo

# 4. Network: destinations and regularity (beaconing?)
jq -r 'select(.EventID==3) | [.UtcTime, .Image, .DestinationIp, .DestinationPort] | @tsv' sysmon.synthetic.jsonl

# 5. Persistence
jq -r 'select(.EventID==13) | [.TargetObject, .Details] | @tsv' sysmon.synthetic.jsonl

# 6. Failed logons grouped by source (Security log)
jq -r 'select(.EventID==4625) | .IpAddress' security-4625.synthetic.jsonl | sort | uniq -c | sort -rn
```

Questions to answer in my notes:

1. Which document started the chain, and which user opened it?
2. What is the parent → child process chain?
3. Which domain/IP did PowerShell contact, and what did it drop?
4. How does the malware persist? What exact registry value?
5. What is the interval between the `synchelper.exe` connections?
6. What discovery commands ran afterwards? Why is `net group "Domain Admins"` interesting?
7. For 4625 events: what do `SubStatus` `0xc0000064` vs `0xc000006a` mean
   (unknown user vs wrong password), and what does that suggest?

### Part B — Linux (auditd)

```bash
cd samples
# Authentication summary (note the times are displayed in the local timezone)
aureport -if auditd.synthetic.log -au

# Executables summary
aureport -if auditd.synthetic.log -x --summary

# Events by key (key names come from the audit rules)
ausearch -if auditd.synthetic.log -k net_download -i
ausearch -if auditd.synthetic.log -k exec_tmp -i
ausearch -if auditd.synthetic.log -k cron_mod -i

# Failed syscalls (e.g. access denied)
ausearch -if auditd.synthetic.log --success no -i

# Everything done in login session 7, by audit UID (auid survives sudo/su)
ausearch -if auditd.synthetic.log --session 7 -i | grep -E 'proctitle|USER_'
```

Questions:

1. From which IP were there failed then successful logins, and for which account?
2. Rebuild the command sequence of session 7 (`id`, `curl`, `chmod`, `bash`, `crontab`, `cat`).
3. Why is `auid` more useful than `uid` for attribution?
4. Which step failed, and why is a *failed* action still worth an alert?
5. What would you check next on the real host? (crontab contents, `/tmp` file
   hash, outbound connections, other hosts contacted by the same IP)

### Part C — Timeline & IOCs

Build a single UTC timeline table (time, host, source, event, significance)
and an IOC list — my [`ioc` tool](../../python/) can extract and defang them:

```bash
cat samples/*.jsonl samples/auditd.synthetic.log | python -m seclab.ioc --defang
```

## Evidence

- Output of the `jq` process tree and decoded command.
- `aureport -au` and `ausearch -k exec_tmp -i` output.
- My timeline table and IOC list (added as `my-timeline.md`).
- Screenshot of the same events in Wazuh if the samples were re-created in the
  lab ([lab 01](../01-wazuh-homelab/)).

## What I learned

_To be completed by Lucas._
