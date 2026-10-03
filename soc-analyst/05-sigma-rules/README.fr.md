# Lab 05 — Règles de détection Sigma

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — `sigma check` signale 0 erreur/problème et chaque règle se déclenche sur les exemples synthétiques via `validate_rules.py` ; pas encore déployé sur de la télémétrie SIEM réelle.

## Objectif

Écrire des règles de détection indépendantes du produit en **Sigma**, les
valider avec l'outillage officiel, les convertir vers un langage de requête
SIEM, et prouver qu'elles se déclenchent sur les données synthétiques du lab
(et qu'elles restent silencieuses sur le bruit bénin).
(Security+ D4 — alertes et supervision, réglage de la détection.)

## Mise en place

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install sigma-cli pyyaml
sigma plugin install sqlite      # used by validate_rules.py
sigma plugin install splunk      # optional, to see Splunk SPL output
```

- Spécification et docs Sigma : <https://sigmahq.io/docs/basics/rules.html>
- Règles communautaires pour s'en inspirer (pas copiées) : <https://github.com/SigmaHQ/sigma>

### Règles

| Fichier | Détecte | ATT&CK | Niveau |
|---------|---------|--------|--------|
| [`win_office_spawns_script_interpreter.yml`](rules/win_office_spawns_script_interpreter.yml) | appli Office → PowerShell/cmd/wscript/mshta | T1566.001, T1204.002, T1059.001 | élevé |
| [`win_powershell_encoded_hidden.yml`](rules/win_powershell_encoded_hidden.yml) | PowerShell `-enc` + fenêtre masquée | T1059.001, T1027 | moyen |
| [`win_registry_run_key_user_writable_path.yml`](rules/win_registry_run_key_user_writable_path.yml) | valeur Run/RunOnce qui pointe vers AppData/Temp/Public/ProgramData | T1547.001 | moyen |
| [`win_net_domain_admins_enumeration.yml`](rules/win_net_domain_admins_enumeration.yml) | `net group "Domain Admins" /domain` | T1069.002 | faible |
| [`win_bruteforce_failed_logons_correlation.yml`](rules/win_bruteforce_failed_logons_correlation.yml) | **règle de corrélation** (Sigma v2) : ≥10 × 4625 depuis une IP en 5 min | T1110.001 | moyen |
| [`win_kerberos_password_spray_correlation.yml`](rules/win_kerberos_password_spray_correlation.yml) | **règle de corrélation** (`value_count`) : Kerberos 4771 `0x18` / 4768 `0x6` pour ≥5 utilisateurs **distincts** depuis une IP en 5 min | T1110.003 | élevé |
| [`lnx_execution_from_tmp.yml`](rules/lnx_execution_from_tmp.yml) | binaire ou script lancé depuis /tmp, /var/tmp, /dev/shm | T1059.004 | moyen |
| [`lnx_download_to_tmp_with_curl_wget.yml`](rules/lnx_download_to_tmp_with_curl_wget.yml) | curl/wget qui écrit dans des répertoires temporaires | T1105 | moyen |
| [`lnx_auditd_shadow_file_access.yml`](rules/lnx_auditd_shadow_file_access.yml) | enregistrement PATH auditd pour /etc/shadow | T1003.008 | moyen |

## Étapes

1. **Le YAML s'analyse :**

   ```bash
   python -c "import yaml,glob;[list(yaml.safe_load_all(open(f))) for f in glob.glob('rules/*.yml')];print('YAML OK')"
   ```

2. **Validation Sigma** (schéma, tags ATT&CK, identifiants, conditions) :

   ```bash
   sigma check rules/
   ```

3. **Convertir** vers un langage SIEM, par exemple Splunk :

   ```bash
   sigma convert -t splunk --without-pipeline rules/
   ```

   (`--without-pipeline` garde des noms de champs génériques ; en production,
   utiliser le pipeline qui correspond à la source de logs, par exemple
   `-p sysmon` ou `-p splunk_windows`.)

4. **Rejouer sur les exemples synthétiques** — convertit chaque règle en SQL
   SQLite et l'exécute sur les journaux de
   [`../02-sysmon-auditd-logs/samples/`](../02-sysmon-auditd-logs/samples/) :

   ```bash
   python validate_rules.py
   ```

5. Régler : lire le champ `falsepositives` de chaque règle et réfléchir à
   comment je mettrais en liste d'autorisation l'activité légitime dans un
   vrai environnement.

### Résultats de validation (2026-09-27, sigma-cli 3.1.0)

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

La règle de corrélation produit 3 alertes, toutes pour `203.0.113.45` (le
10e, le 11e et le 12e échec dans la fenêtre de 5 minutes) ; l'hôte interne
avec 2 fautes de frappe ne déclenche pas. Les événements Chrome bénins ne
matchent aucune règle.

La règle de spray Kerberos (ajoutée plus tard) n'a aucun événement
correspondant dans les exemples synthétiques (ils ne contiennent pas de
4768/4771), donc `[none]` est attendu. Je l'ai testée à la place sur
l'échantillon public `kerberos_pwd_spray_4771.evtx` : 3 alertes pour
`172.16.66.1` avec 5, 7 et 9 noms d'utilisateurs distincts — voir
[IR-03](../03-incident-writeups/IR-03-evtx-password-spray.md).

> Leçon prise au début : `sigma check` a rejeté le tag `attack.defense-evasion`
> parce que l'ATT&CK actuel sépare cette tactique en **Stealth** et
> **Defense Impairment** — la règle utilise maintenant `attack.stealth`.

## Preuves

- Sortie de `sigma check` (ci-dessus) et requêtes Splunk converties.
- Sortie de `validate_rules.py` (ci-dessus).
- Plus tard : captures des mêmes règles importées dans Wazuh / Splunk et
  déclenchées sur de la télémétrie réelle de lab.

## Ce que j'ai appris

_À compléter par Lucas._
