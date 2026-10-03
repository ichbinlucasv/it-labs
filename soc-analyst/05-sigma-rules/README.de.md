# Lab 05 — Sigma-Erkennungsregeln

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Done — `sigma check` meldet 0 Fehler/Hinweise und jede Regel schlägt auf den synthetischen Beispielen über `validate_rules.py` an; noch nicht auf echter SIEM-Telemetrie ausgerollt.

## Ziel

Herstellerneutrale Erkennungsregeln in **Sigma** schreiben, sie mit dem
offiziellen Werkzeug prüfen, in eine SIEM-Abfragesprache umwandeln und
zeigen, dass sie auf den synthetischen Lab-Daten auslösen (und beim
gutartigen Rauschen still bleiben).
(Security+ D4 — Alarmierung und Überwachung, Erkennung nachschärfen.)

## Aufbau

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install sigma-cli pyyaml
sigma plugin install sqlite      # used by validate_rules.py
sigma plugin install splunk      # optional, to see Splunk SPL output
```

- Sigma-Spezifikation und Doku: <https://sigmahq.io/docs/basics/rules.html>
- Community-Regeln als Anregung (nicht kopiert): <https://github.com/SigmaHQ/sigma>

### Regeln

| Datei | Erkennt | ATT&CK | Stufe |
|-------|---------|--------|-------|
| [`win_office_spawns_script_interpreter.yml`](rules/win_office_spawns_script_interpreter.yml) | Office-App → PowerShell/cmd/wscript/mshta | T1566.001, T1204.002, T1059.001 | hoch |
| [`win_powershell_encoded_hidden.yml`](rules/win_powershell_encoded_hidden.yml) | PowerShell `-enc` + verstecktes Fenster | T1059.001, T1027 | mittel |
| [`win_registry_run_key_user_writable_path.yml`](rules/win_registry_run_key_user_writable_path.yml) | Run/RunOnce-Wert, der auf AppData/Temp/Public/ProgramData zeigt | T1547.001 | mittel |
| [`win_net_domain_admins_enumeration.yml`](rules/win_net_domain_admins_enumeration.yml) | `net group "Domain Admins" /domain` | T1069.002 | niedrig |
| [`win_bruteforce_failed_logons_correlation.yml`](rules/win_bruteforce_failed_logons_correlation.yml) | **Korrelationsregel** (Sigma v2): ≥10 × 4625 von einer IP in 5 min | T1110.001 | mittel |
| [`win_kerberos_password_spray_correlation.yml`](rules/win_kerberos_password_spray_correlation.yml) | **Korrelationsregel** (`value_count`): Kerberos 4771 `0x18` / 4768 `0x6` für ≥5 **verschiedene** Benutzer von einer IP in 5 min | T1110.003 | hoch |
| [`lnx_execution_from_tmp.yml`](rules/lnx_execution_from_tmp.yml) | Binary oder Skript aus /tmp, /var/tmp, /dev/shm | T1059.004 | mittel |
| [`lnx_download_to_tmp_with_curl_wget.yml`](rules/lnx_download_to_tmp_with_curl_wget.yml) | curl/wget schreibt in Temp-Verzeichnisse | T1105 | mittel |
| [`lnx_auditd_shadow_file_access.yml`](rules/lnx_auditd_shadow_file_access.yml) | auditd-PATH-Eintrag für /etc/shadow | T1003.008 | mittel |

## Schritte

1. **YAML lässt sich einlesen:**

   ```bash
   python -c "import yaml,glob;[list(yaml.safe_load_all(open(f))) for f in glob.glob('rules/*.yml')];print('YAML OK')"
   ```

2. **Sigma-Prüfung** (Schema, ATT&CK-Tags, Bezeichner, Bedingungen):

   ```bash
   sigma check rules/
   ```

3. **Umwandeln** in eine SIEM-Sprache, zum Beispiel Splunk:

   ```bash
   sigma convert -t splunk --without-pipeline rules/
   ```

   (`--without-pipeline` behält generische Feldnamen; in Produktion die
   Pipeline zur Logquelle nehmen, zum Beispiel `-p sysmon` oder
   `-p splunk_windows`.)

4. **Gegen die synthetischen Beispiele abspielen** — wandelt jede Regel in
   SQLite-SQL um und führt sie auf den Logs in
   [`../02-sysmon-auditd-logs/samples/`](../02-sysmon-auditd-logs/samples/) aus:

   ```bash
   python validate_rules.py
   ```

5. Nachschärfen: das Feld `falsepositives` jeder Regel lesen und überlegen,
   wie ich legitime Aktivität in einer echten Umgebung freigeben würde.

### Validierungsergebnisse (2026-09-27, sigma-cli 3.1.0)

```text
$ sigma check rules/
Found 0 errors, 0 condition errors and 0 issues.

$ python validate_rules.py
[HIT ] lnx_auditd_shadow_file_access.yml: 1 result row(s) (events or correlation alerts) in linux samples
[HIT ] lnx_download_to_tmp_with_curl_wget.yml: 1 result row(s) (events or correlation alerts) in linux samples
[HIT ] lnx_execution_from_tmp.yml: 1 result row(s) (events or correlation alerts) in linux samples
[HIT ] win_bruteforce_failed_logons_correlation.yml: 3 result row(s) (events or correlation alerts) in windows samples
[none] win_kerberos_password_spray_correlation.yml: 0 result row(s) (events or correlation alerts) in windows samples
[HIT ] win_net_domain_admins_enumeration.yml: 1 result row(s) (events or correlation alerts) in windows samples
[HIT ] win_office_spawns_script_interpreter.yml: 1 result row(s) (events or correlation alerts) in windows samples
[HIT ] win_powershell_encoded_hidden.yml: 1 result row(s) (events or correlation alerts) in windows samples
[HIT ] win_registry_run_key_user_writable_path.yml: 1 result row(s) (events or correlation alerts) in windows samples
```

Die Korrelationsregel erzeugt 3 Alerts, alle für `203.0.113.45` (der 10.,
11. und 12. Fehlschlag im 5-Minuten-Fenster); der interne Host mit 2
Tippfehlern löst nicht aus. Die harmlosen Chrome-Ereignisse passen auf keine
Regel.

Die Kerberos-Spray-Regel (später ergänzt) hat in den synthetischen Beispielen
keine passenden Ereignisse (sie enthalten kein 4768/4771), `[none]` ist also
erwartet. Getestet habe ich sie stattdessen am öffentlichen Sample
`kerberos_pwd_spray_4771.evtx`: 3 Alerts für `172.16.66.1` mit 5, 7 und 9
verschiedenen Benutzernamen — siehe
[IR-03](../03-incident-writeups/IR-03-evtx-password-spray.md).

> Eine frühe Lektion: `sigma check` hat den Tag `attack.defense-evasion`
> abgelehnt, weil aktuelles ATT&CK diese Taktik in **Stealth** und
> **Defense Impairment** aufteilt — die Regel nutzt jetzt `attack.stealth`.

## Nachweise

- Ausgabe von `sigma check` (oben) und umgewandelte Splunk-Abfragen.
- Ausgabe von `validate_rules.py` (oben).
- Später: Screenshots derselben Regeln, importiert in Wazuh / Splunk, wie sie
  auf echter Lab-Telemetrie auslösen.

## Was ich gelernt habe

_Noch von Lucas auszufüllen._
