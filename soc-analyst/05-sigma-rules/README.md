# Lab 05 — Sigma detection rules

**Status:** Done — `sigma check` reports 0 errors/issues and every rule fires on the synthetic samples via `validate_rules.py`; not yet deployed on real SIEM telemetry.

## Goal

Write vendor-neutral detection rules in **Sigma**, validate them with the
official tooling, convert them to a SIEM query language, and prove they fire
on the lab's synthetic data (and stay quiet on the benign noise).
(Security+ D4 — alerting and monitoring, detection tuning.)

## Setup

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install sigma-cli pyyaml
sigma plugin install sqlite      # used by validate_rules.py
sigma plugin install splunk      # optional, to see Splunk SPL output
```

- Sigma specification & docs: <https://sigmahq.io/docs/basics/rules.html>
- Community rules for inspiration (not copied): <https://github.com/SigmaHQ/sigma>

### Rules

| File | Detects | ATT&CK | Level |
|------|---------|--------|-------|
| [`win_office_spawns_script_interpreter.yml`](rules/win_office_spawns_script_interpreter.yml) | Office app → PowerShell/cmd/wscript/mshta | T1566.001, T1204.002, T1059.001 | high |
| [`win_powershell_encoded_hidden.yml`](rules/win_powershell_encoded_hidden.yml) | PowerShell `-enc` + hidden window | T1059.001, T1027 | medium |
| [`win_registry_run_key_user_writable_path.yml`](rules/win_registry_run_key_user_writable_path.yml) | Run/RunOnce value pointing to AppData/Temp/Public/ProgramData | T1547.001 | medium |
| [`win_net_domain_admins_enumeration.yml`](rules/win_net_domain_admins_enumeration.yml) | `net group "Domain Admins" /domain` | T1069.002 | low |
| [`win_bruteforce_failed_logons_correlation.yml`](rules/win_bruteforce_failed_logons_correlation.yml) | **Correlation rule** (Sigma v2): ≥10 × 4625 from one IP in 5 min | T1110.001 | medium |
| [`lnx_execution_from_tmp.yml`](rules/lnx_execution_from_tmp.yml) | Binary or script run from /tmp, /var/tmp, /dev/shm | T1059.004 | medium |
| [`lnx_download_to_tmp_with_curl_wget.yml`](rules/lnx_download_to_tmp_with_curl_wget.yml) | curl/wget writing into temp dirs | T1105 | medium |
| [`lnx_auditd_shadow_file_access.yml`](rules/lnx_auditd_shadow_file_access.yml) | auditd PATH record for /etc/shadow | T1003.008 | medium |

## Steps

1. **YAML parses:**

   ```bash
   python -c "import yaml,glob;[list(yaml.safe_load_all(open(f))) for f in glob.glob('rules/*.yml')];print('YAML OK')"
   ```

2. **Sigma validation** (schema, ATT&CK tags, identifiers, conditions):

   ```bash
   sigma check rules/
   ```

3. **Convert** to a SIEM language, e.g. Splunk:

   ```bash
   sigma convert -t splunk --without-pipeline rules/
   ```

   (`--without-pipeline` keeps generic field names; in production use the
   pipeline matching your log source, e.g. `-p sysmon` or `-p splunk_windows`.)

4. **Replay against the synthetic samples** — converts each rule to SQLite SQL
   and runs it on the logs in [`../02-sysmon-auditd-logs/samples/`](../02-sysmon-auditd-logs/samples/):

   ```bash
   python validate_rules.py
   ```

5. Tune: read the `falsepositives` field of each rule and think about how I
   would allow-list legitimate activity in a real environment.

### Validation results (2026-09-27, sigma-cli 3.1.0)

```text
$ sigma check rules/
Found 0 errors, 0 condition errors and 0 issues.

$ python validate_rules.py
[HIT ] lnx_auditd_shadow_file_access.yml: 1 result row(s) (events or correlation alerts) in linux samples
[HIT ] lnx_download_to_tmp_with_curl_wget.yml: 1 result row(s) (events or correlation alerts) in linux samples
[HIT ] lnx_execution_from_tmp.yml: 1 result row(s) (events or correlation alerts) in linux samples
[HIT ] win_bruteforce_failed_logons_correlation.yml: 3 result row(s) (events or correlation alerts) in windows samples
[HIT ] win_net_domain_admins_enumeration.yml: 1 result row(s) (events or correlation alerts) in windows samples
[HIT ] win_office_spawns_script_interpreter.yml: 1 result row(s) (events or correlation alerts) in windows samples
[HIT ] win_powershell_encoded_hidden.yml: 1 result row(s) (events or correlation alerts) in windows samples
[HIT ] win_registry_run_key_user_writable_path.yml: 1 result row(s) (events or correlation alerts) in windows samples
```

The correlation rule produces 3 alerts, all for `203.0.113.45` (the 10th,
11th and 12th failure inside the 5-minute window); the internal host with 2
typos does not trigger. The benign Chrome events do not match any rule.

> One early lesson: `sigma check` rejected the tag `attack.defense-evasion`
> because current ATT&CK splits that tactic into **Stealth** and
> **Defense Impairment** — the rule now uses `attack.stealth`.

## Evidence

- `sigma check` output (above) and converted Splunk queries.
- `validate_rules.py` output (above).
- Later: screenshots of the same rules imported into Wazuh / Splunk and
  firing on real lab telemetry.

## What I learned

_To be completed by Lucas._
