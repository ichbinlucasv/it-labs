# IR-02 — Enquête Splunk Boss of the SOC v1

[English](IR-02-splunk-bots-v1.md) · **Français** · [Deutsch](IR-02-splunk-bots-v1.de.md)

| Champ | Valeur |
|-------|--------|
| Analyste | Lucas |
| Date d'analyse | TBD |
| Jeu de données et URL | Splunk BOTS v1 — <https://github.com/splunk/botsv1> (appli pré-indexée complète ~6 GB, ou `botsv1-attack-only.tgz` ~135 MB « just the needles, no haystack ») |
| Scénario / plateforme CTF | Portail Splunk BOTS <https://bots.splunk.com/> et l'appli de scoreboard CTF <https://github.com/splunk/SA-ctf_scoreboard> (questions du scénario) |
| SHA256 du fichier | TBD |
| Gravité | TBD |
| Statut | Brouillon — plan d'enquête, pas encore de constats |

## 1. Résumé pour la direction

TBD.

## 2. Périmètre et questions

BOTS v1 contient deux scénarios dans l'entreprise fictive Wayne Enterprises :
**(A)** une compromission et une défiguration du site web de l'entreprise, et
**(B)** une infection par ransomware sur le poste d'un utilisateur. Je ferai
d'abord le scénario A, puis B, et je répondrai moi-même aux questions de
l'enquête avant de comparer avec un compte rendu public.

Sources disponibles (d'après le README du jeu de données) : journaux
d'événements Windows, Sysmon, IIS, Fortigate (`fgt_*`), Suricata, Splunk
Stream (`stream:dns`, `stream:http`, `stream:smb`...), Nessus, base de
registre Windows.

## 3. Plan d'enquête (scénario A — compromission du serveur web)

| # | Question | SPL de départ (générique) | Résultat |
|---|----------|---------------------------|----------|
| 1 | Quels sourcetypes/hôtes existent ? | `index=botsv1 earliest=0 \| stats count by sourcetype, host` | TBD |
| 2 | Qui a scanné le site web ? | `index=botsv1 sourcetype=stream:http dest_ip=<web server> \| stats count by src_ip, http_user_agent \| sort -count` | TBD |
| 3 | Quelles alertes IDS ont tiré sur le serveur web ? | `index=botsv1 sourcetype=suricata dest_ip=<web server> \| stats count by alert.signature` | TBD |
| 4 | Tentatives de force brute contre la page de connexion ? | `index=botsv1 sourcetype=stream:http http_method=POST uri="*login*" \| stats count by src_ip` | TBD |
| 5 | Un fichier a-t-il été déposé / exécuté ? | `index=botsv1 sourcetype=stream:http http_method=POST \| search part_filename=*` et Sysmon EventCode=1 sur le serveur | TBD |
| 6 | Quelles connexions sortantes le serveur a-t-il faites ? | `index=botsv1 src_ip=<web server> sourcetype=fgt_traffic \| stats count by dest_ip, dest_port` | TBD |

## 3b. Plan d'enquête (scénario B — ransomware sur un poste)

| # | Question | SPL de départ (générique) | Résultat |
|---|----------|---------------------------|----------|
| 1 | IP de l'hôte victime le jour en question | `index=botsv1 sourcetype=stream:dhcp` / `WinEventLog:Security` | TBD |
| 2 | Quelle chaîne de processus a démarré l'infection ? | `index=botsv1 sourcetype=XmlWinEventLog:Microsoft-Windows-Sysmon/Operational EventCode=1 host=<victim> \| table _time ParentImage Image CommandLine` | TBD |
| 3 | Un support amovible est-il en cause ? | `index=botsv1 sourcetype=winregistry host=<victim>` | TBD |
| 4 | Domaines contactés | `index=botsv1 sourcetype=stream:dns src_ip=<victim> \| stats count by query` | TBD |
| 5 | Fichiers chiffrés en local / sur des partages | Sysmon EventCode=2/11 et `stream:smb` / `WinEventLog:Security` 5145 | TBD |

## 4. Chronologie

TBD

## 5. IOC (defanged)

TBD

## 6. Correspondance ATT&CK

TBD — candidats à vérifier : T1595 Active Scanning, T1110 Brute Force,
T1190 Exploit Public-Facing Application, T1505.003 Web Shell,
T1491.002 External Defacement (scénario A) ; T1091 Replication Through
Removable Media, T1204.002 Malicious File, T1486 Data Encrypted for Impact
(scénario B).

## 7–8. Impact et recommandations

TBD

## 9. Preuves

`evidence/IR-02/` — requêtes SPL (enregistrées en texte) + captures d'écran des résultats.
