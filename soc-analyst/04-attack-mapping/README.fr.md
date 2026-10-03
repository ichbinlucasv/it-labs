# Lab 04 — Correspondance MITRE ATT&CK

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — correspondance des scénarios synthétiques vérifiée contre les données STIX officielles d'ATT&CK Enterprise 19.2, et exportée en layer Navigator ([`coverage-layer.json`](coverage-layer.json), produit par [`make_layer.py`](make_layer.py)) ; IR-03 est confirmé ; les candidats IR-01/IR-02 restent non confirmés tant que ces [rapports d'incident](../03-incident-writeups/) ne sont pas faits.

## Objectif

Faire correspondre les comportements des scénarios synthétiques du lab à des
techniques MITRE ATT&CK. Lier chacun à la source de données qui le montre,
et à la détection que j'ai écrite (ou qu'il me manque encore). Voir où ma
couverture a des trous. (Security+ D2 — acteurs de menace et TTP ;
D4 — threat hunting.)

## Mise en place

- MITRE ATT&CK Enterprise : <https://attack.mitre.org/>
- ATT&CK Navigator (pour une carte de chaleur de la couverture) : <https://mitre-attack.github.io/attack-navigator/>
- **Note de version :** correspondance vérifiée contre ATT&CK Enterprise **v19**
  (attack.mitre.org, 2026-09-27). Dans les versions récentes, l'ancienne
  tactique *Defense Evasion* a été coupée en **Stealth (TA0005)** et
  **Defense Impairment (TA0112)**. Les anciens supports (et les anciens livres
  Security+) disent encore « Defense Evasion ». Tous les ID de techniques
  ci-dessous ont été vérifiés contre les données ATT&CK livrées avec pySigma
  (v19.2).

## Étapes

1. Lister chaque comportement observable des scénarios synthétiques
   ([lab 02](../02-sysmon-auditd-logs/)) et des rapports d'incident prévus.
2. Trouver la technique ou la sous-technique la plus précise. Noter la tactique.
3. Noter la source de données et l'événement qui le montre.
4. Lier la détection (règle Sigma / règle Wazuh) ou marquer comme **lacune**.
5. Exporter le tableau vers un layer ATT&CK Navigator :

   ```bash
   # optional validation source (50 MB, not committed)
   curl -LO https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json
   python3 make_layer.py --stix enterprise-attack.json
   ```

   Puis dans ATT&CK Navigator : *Open Existing Layer → Upload from local* →
   `coverage-layer.json`.

### Tableau de correspondance — scénarios synthétiques

| # | Comportement observé (synthétique) | Tactique | Technique | Source de données / événement | Détection |
|---|-------------------------------|--------|-----------|---------------------|-----------|
| 1 | L'utilisateur ouvre un document à macros depuis Downloads | Initial Access | T1566.001 Phishing: Spearphishing Attachment | Passerelle mail, Sysmon 1 (WINWORD avec `.docm`) | Lacune (pas de journaux mail dans le lab) |
| 2 | Word lance PowerShell | Execution | T1204.002 User Execution: Malicious File | Sysmon 1 (ParentImage) | [`win_office_spawns_script_interpreter`](../05-sigma-rules/rules/win_office_spawns_script_interpreter.yml) |
| 3 | PowerShell avec `-enc` et fenêtre cachée | Execution / Stealth | T1059.001 PowerShell; T1027 Obfuscated Files or Information | Sysmon 1 CommandLine, PowerShell 4104 | [`win_powershell_encoded_hidden`](../05-sigma-rules/rules/win_powershell_encoded_hidden.yml) |
| 4 | PowerShell résout un hôte externe et le contacte en 443 | Command and Control | T1071.001 Web Protocols | Sysmon 22, Sysmon 3, journaux proxy/pare-feu | Lacune — il faut une logique de réputation / nouveau domaine |
| 5 | Exécutable écrit dans `%APPDATA%` | Command and Control | T1105 Ingress Tool Transfer | Sysmon 11 | Lacune (règle candidate) |
| 6 | Clé Run → `%APPDATA%\SyncHelper\synchelper.exe` | Persistence | T1547.001 Registry Run Keys / Startup Folder | Sysmon 13 | [`win_registry_run_key_user_writable_path`](../05-sigma-rules/rules/win_registry_run_key_user_writable_path.yml) |
| 7 | Connexions sortantes régulières toutes les ~60 s | Command and Control | T1071.001 Web Protocols (beaconing) | Sysmon 3, pare-feu/NetFlow | Lacune — il faut une analyse de série temporelle |
| 8 | `whoami /all` | Discovery | T1033 System Owner/User Discovery | Sysmon 1 | Lacune (bruyant tout seul ; à utiliser en corrélation) |
| 9 | `net group "Domain Admins" /domain` | Discovery | T1069.002 Permission Groups Discovery: Domain Groups | Sysmon 1, Security 4688 | [`win_net_domain_admins_enumeration`](../05-sigma-rules/rules/win_net_domain_admins_enumeration.yml) |
| 10 | 12 ouvertures de session échouées depuis une seule IP externe en moins de 3 min | Credential Access | T1110.001 Brute Force: Password Guessing | Security 4625 | [`win_bruteforce_failed_logons_correlation`](../05-sigma-rules/rules/win_bruteforce_failed_logons_correlation.yml) |
| 11 | Échecs SSH puis succès pour `deploy` depuis la même IP | Credential Access / Initial Access | T1110.001 Password Guessing → T1078 Valid Accounts | auditd USER_AUTH/USER_LOGIN, `auth.log` | Règles sshd Wazuh ; mon résumé Python [`authlog`](../../python/) |
| 12 | `curl -o /tmp/.cache-upd.sh http://…` | Command and Control | T1105 Ingress Tool Transfer | auditd EXECVE | [`lnx_download_to_tmp_with_curl_wget`](../05-sigma-rules/rules/lnx_download_to_tmp_with_curl_wget.yml) |
| 13 | `bash /tmp/.cache-upd.sh` | Execution | T1059.004 Unix Shell | auditd EXECVE (clé `exec_tmp`) | [`lnx_execution_from_tmp`](../05-sigma-rules/rules/lnx_execution_from_tmp.yml) |
| 14 | `crontab /tmp/.c` | Persistence | T1053.003 Scheduled Task/Job: Cron | auditd (clé `cron_mod`), FIM sur `/var/spool/cron` | FIM Wazuh ; lacune Sigma |
| 15 | `cat /etc/shadow` (refusé) | Credential Access | T1003.008 OS Credential Dumping: /etc/passwd and /etc/shadow | auditd PATH + SYSCALL (clé `shadow_read`) | [`lnx_auditd_shadow_file_access`](../05-sigma-rules/rules/lnx_auditd_shadow_file_access.yml) |
| 16 | Nom de fichier caché `.cache-upd.sh` | Stealth | T1564.001 Hide Artifacts: Hidden Files and Directories | auditd EXECVE / FIM | Lacune |

### Techniques candidates pour les rapports sur jeux publics (à confirmer)

| Rapport | Techniques candidates |
|---------|------------------------|
| IR-01 pcap malware-traffic | T1189, T1566, T1204, T1105, T1071.001 |
| IR-02 BOTS v1 | T1595, T1110, T1190, T1505.003, T1491.002, T1091, T1204.002, T1486 |
| IR-03 password spray EVTX | **T1110.003 confirmé** dans le [rapport terminé](../03-incident-writeups/IR-03-evtx-password-spray.md) ; T1078.002 étape suivante possible, pas dans les données ; détecté par [`win_kerberos_password_spray_correlation`](../05-sigma-rules/rules/win_kerberos_password_spray_correlation.yml) |

### Résumé de couverture

| Tactique | Comportements | Détectés par mes règles | Lacunes |
|----------|--------------:|------------------------:|--------:|
| Initial Access | 1 | 0 | 1 |
| Execution | 4 | 3 | 1 |
| Persistence | 2 | 1 | 1 |
| Discovery | 2 | 1 | 1 |
| Credential Access | 3 | 3 | 0 |
| Command and Control | 4 | 1 | 3 |
| Stealth | 2 | 1 | 1 |

(La ligne 3 et la ligne 11 comptent chacune pour deux tactiques.) Plus grosse
lacune : **C2 / détection réseau** → prochaine étape, Zeek ou Suricata dans
le lab.

## Preuves

- [`coverage-layer.json`](coverage-layer.json) : layer Navigator, 15 techniques,
  score 1 (vert) = une détection existe dans ce dépôt, 0 (rouge) = lacune.
  Le commentaire de chaque technique liste les lignes du tableau d'où elle vient.
- Sortie de `python3 make_layer.py --stix enterprise-attack.json` :

```text
checked 15 technique IDs against ATT&CK Enterprise 19.2: all valid
wrote coverage-layer.json: 15 techniques, 11 with a detection, 4 gaps
```

  Les 4 lacunes : T1566.001 (pas de journaux mail dans le lab), T1071.001
  (C2 en HTTPS — ligne 4 et le beacon à 60 s de la ligne 7), T1033
  (`whoami`), T1564.001 (nom de fichier caché). Les 13 ID candidats pour les
  rapports sur jeux publics existent aussi, et ils ne sont pas dépréciés en
  19.2, mais la correspondance elle-même n'est pas confirmée.
- Pas fait : capture d'écran de la carte de chaleur Navigator (le fichier de
  layer est la source ; la capture ne demande que l'envoi décrit plus haut).

## Ce que j'ai appris

- Un comportement correspond souvent à plus d'une technique (PowerShell encodé
  = T1059.001 + T1027). Une technique peut être à la fois détectée et ratée,
  selon l'endroit (T1105 a une règle sous Linux, pas sous Windows).
- Les ID de techniques et les noms de tactiques changent entre versions
  d'ATT&CK (Defense Evasion a été coupée). Vérifier contre les données STIX
  officielles d'une version annoncée évite de citer quelque chose qui
  n'existe plus.
- Compter par technique cache du détail. Le layer dit que T1071.001 est une
  lacune, mais le tableau montre deux comportements différents (premier
  contact et beaconing).
- Mon trou le plus clair est la détection réseau (C2 en HTTPS, beaconing).
  Les journaux hôte et les règles Sigma sur les événements de processus ne
  couvrent pas bien ça.
