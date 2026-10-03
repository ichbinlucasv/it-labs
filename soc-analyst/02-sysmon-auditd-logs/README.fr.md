# Lab 02 — Analyse de journaux Sysmon et auditd

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — toutes les commandes des parties A, B et C ont tourné sur les exemples synthétiques, et mes réponses, la chronologie UTC et la liste d'IOC sont dans [`my-timeline.md`](my-timeline.md). Le vrai Sysmon sur l'invité Windows est une étape plus tard. L'invité existe ([lab 06](../../helpdesk/06-windows-domain/)), et Sysmon n'était pas installé sur le DC quand je l'ai inventorié.

## Objectif

Apprendre à reconstruire ce qui s'est passé sur un poste à partir de la
télémétrie brute : événements **Sysmon** Windows (processus, réseau, fichier,
registre, DNS), événements d'ouverture de session du journal **Security**
Windows, et enregistrements **auditd** Linux. Construire une chronologie et
extraire des indicateurs. (Security+ D2 indicateurs d'activité malveillante ;
D4 sources de journaux et enquête.)

## Mise en place

- Exemples dans [`samples/`](samples/) — **tous synthétiques**, voir le
  [README des exemples](samples/README.md).
- Outils : `jq`, Python 3, et les outils audit en espace utilisateur
  (`sudo apt install jq auditd`). `ausearch` et `aureport` peuvent lire un
  fichier de journal avec `-if`, sans faire tourner le démon audit.
- Pour produire de la vraie télémétrie dans un lab (pas encore fait) :
  - **Sysmon** (Microsoft Sysinternals) :
    <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon> —
    `sysmon64.exe -accepteula -i sysmonconfig.xml`
  - Exemple de règles **auditd** (`/etc/audit/rules.d/lab.rules`) :

    ```text
    -w /etc/shadow -p r -k shadow_read
    -w /etc/passwd -p wa -k identity
    -w /var/spool/cron/ -p wa -k cron_mod
    -w /etc/crontab -p wa -k cron_mod
    -a always,exit -F arch=b64 -S execve -F dir=/tmp -k exec_tmp
    -a always,exit -F arch=b64 -S execve -F exe=/usr/bin/curl -k net_download
    ```

    Charger avec `sudo augenrules --load` ; voir aussi le jeu de règles
    communautaire <https://github.com/Neo23x0/auditd>.

### ID d'événements Sysmon utilisés ici

| ID | Sens |
|---:|------|
| 1 | Création de processus (image, ligne de commande, parent, hash) |
| 3 | Connexion réseau |
| 11 | Fichier créé |
| 13 | Valeur de registre écrite |
| 22 | Requête DNS |

## Étapes

### Partie A — Windows (JSONL Sysmon)

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

Questions à répondre dans mes notes :

1. Quel document a démarré la chaîne, et quel utilisateur l'a ouvert ?
2. Quelle est la chaîne de processus parent → enfant ?
3. Quel domaine ou quelle IP PowerShell a contacté, et qu'est-ce qu'il a déposé ?
4. Comment le malware persiste-t-il ? Quelle valeur de registre exacte ?
5. Quel est l'intervalle entre les connexions de `synchelper.exe` ?
6. Quelles commandes de découverte ont tourné ensuite ? Pourquoi
   `net group "Domain Admins"` est intéressant ?
7. Pour les événements 4625 : que veulent dire les `SubStatus` `0xc0000064`
   et `0xc000006a` (utilisateur inconnu contre mauvais mot de passe), et
   qu'est-ce que ça suggère ?

### Partie B — Linux (auditd)

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

Questions :

1. Depuis quelle IP y a-t-il eu des ouvertures échouées puis une réussie, et pour quel compte ?
2. Reconstruire la suite de commandes de la session 7 (`id`, `curl`, `chmod`, `bash`, `crontab`, `cat`).
3. Pourquoi `auid` est plus utile que `uid` pour l'attribution ?
4. Quelle étape a échoué, et pourquoi une action *échouée* mérite quand même une alerte ?
5. Qu'est-ce que je vérifierais ensuite sur le vrai hôte ? (contenu de la crontab, hash du fichier dans `/tmp`, connexions sortantes, autres hôtes contactés par la même IP)

### Partie C — Chronologie et IOC

Construire un seul tableau de chronologie UTC (heure, hôte, source,
événement, pourquoi c'est significatif) et une liste d'IOC. Mon
[outil `ioc`](../../python/) peut les extraire et les passer en defang :

```bash
cat samples/*.jsonl samples/auditd.synthetic.log | python -m seclab.ioc --defang
```

## Preuves

- [`my-timeline.md`](my-timeline.md) : arbre de processus `jq` et commande
  décodée, événements réseau et registre, analyse des 4625, sortie de
  `aureport -au` et de `ausearch --session 7`, réponses à chaque question,
  la chronologie UTC combinée et la liste d'IOC.
- Pas fait : les mêmes événements dans Wazuh ([lab 01](../01-wazuh-homelab/))
  et de vraies règles auditd. Sur ma machine de lab, `auditctl -s` échoue avec
  `Operation not permitted` (pas de capacité audit dans ce conteneur). Donc
  `ausearch` / `aureport -if` sur un fichier était la seule option.

## Ce que j'ai appris

- Les liens parent → enfant (Word → PowerShell) disent souvent plus qu'un
  événement isolé.
- Des connexions parfaitement régulières (toutes les 60 s) sont un signal
  fort de beaconing.
- `auid` garde l'identité d'ouverture d'origine à travers `sudo` et `su`.
  C'est ce qu'il faut pour l'attribution.
- Les codes SubStatus 4625 séparent les noms d'utilisateur valides des
  invalides. Utile pour comprendre ce qu'un attaquant a appris.
- Les fuseaux comptent. `aureport` affiche l'heure locale, sauf si `TZ=UTC`
  est posé.
- Un extracteur d'IOC trouve des chaînes. Décider lesquelles sont
  malveillantes (et laisser de côté les hôtes internes et les binaires
  légitimes) est le travail de l'analyste.
