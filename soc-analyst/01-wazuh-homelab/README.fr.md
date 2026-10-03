# Lab 01 — Homelab Wazuh (SIEM / XDR)

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Planned — procédure de déploiement et de triage écrite. Aucun serveur Wazuh n'a encore été déployé.

## Objectif

Déployer un petit SIEM auto-hébergé avec Wazuh, enrôler un endpoint Windows
et un endpoint Linux, produire une activité bénigne « qui ressemble à une
attaque », et m'entraîner au triage d'alertes comme le ferait un analyste
SOC junior. (Security+ D4 — SIEM, agrégation de journaux, alertes, FIM,
détection de vulnérabilités.)

## Mise en place

| VM | Rôle | Ressources (lab) | IP |
|----|------|------------------|----|
| `wazuh01` | Serveur Wazuh + indexeur + tableau de bord (tout-en-un) | 4 vCPU, 8 GB RAM, 50 GB de disque (minimum du quickstart Wazuh pour ~1–25 agents) | 10.20.30.30 |
| `ws01` | Windows 11 + Sysmon + agent Wazuh | 2 vCPU, 4 GB | 10.20.30.50 |
| `web01` | Ubuntu 24.04 + auditd + agent Wazuh | 1 vCPU, 2 GB | 10.20.30.40 |

- Réseau isolé host-only / interne ; NAT seulement pour télécharger les paquets.
- Docs officielles : <https://documentation.wazuh.com/current/quickstart.html>
  (au moment de l'écriture, le quickstart installe Wazuh **4.14** — toujours
  prendre la version des docs en cours).

## Étapes

### 1. Installer le serveur tout-en-un

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
less wazuh-install.sh                 # read scripts before piping them to bash
sudo bash ./wazuh-install.sh -a
# The admin password is printed at the end; store it in a password manager,
# never in this repo. Dashboard: https://10.20.30.30
```

### 2. Enrôler les agents

Depuis le tableau de bord : **Agents → Deploy new agent**, choisir l'OS,
mettre l'adresse du serveur `10.20.30.30`, copier la commande générée.
Vérifier sur le serveur :

```bash
sudo /var/ossec/bin/agent_control -l
```

### 3. Améliorer la télémétrie

- **Windows :** installer Sysmon avec une config communautaire
  ([SwiftOnSecurity/sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config)
  ou [olafhartong/sysmon-modular](https://github.com/olafhartong/sysmon-modular)),
  puis ajouter dans le `ossec.conf` de l'agent :

  ```xml
  <localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
  </localfile>
  ```

  Activer la journalisation des blocs de script PowerShell (événement 4104)
  par GPO ou stratégie locale.
- **Linux :** installer `auditd`, ajouter des règles (exemples dans le
  [lab 02](../02-sysmon-auditd-logs/)), et vérifier que l'agent lit
  `/var/log/audit/audit.log`.
- **FIM :** ajouter `<directories check_all="yes" realtime="yes">/etc</directories>`
  au bloc `syscheck` sur `web01`.

### 4. Produire une activité de test bénigne (mon lab seulement)

| Activité | Famille d'alerte attendue |
|----------|---------------------------|
| 10 mauvais mots de passe SSH vers `web01` depuis une autre VM du lab | échecs d'authentification sshd / force brute |
| `sudo` avec un mauvais mot de passe | échecs PAM / sudo |
| Créer puis supprimer un utilisateur local sur `web01` | utilisateur ajouté / retiré |
| Modifier `/etc/hosts` | somme de contrôle d'intégrité FIM changée |
| Sur `ws01` : `powershell -EncodedCommand` qui lance `Write-Output test` | règles Sysmon/PowerShell |
| Ajouter une valeur `HKCU\...\Run` qui pointe vers `notepad.exe` | persistance dans le registre (Sysmon 13) |

En option, des tests **Atomic Red Team** dans la VM de lab *seulement*,
après avoir lu chaque test.

### 5. Triage de chaque alerte

1. Quelle règle a tiré, quel niveau, quel agent ?
2. Qui (utilisateur), quoi (processus/commande), où (hôte/IP), quand (horodatages, UTC) ?
3. Est-ce attendu ? (ticket de changement, activité d'admin, logiciel connu)
4. Pivoter : autres événements du même hôte / utilisateur / de la même IP à ±15 min.
5. Verdict : vrai positif / vrai positif bénin / faux positif → documenter.
6. Ajuster : exceptions pour les faux positifs confirmés (avec justification).

### 6. Option — comparaison avec ELK

La pile Elastic (Elasticsearch + Kibana + Elastic Agent/Fleet) peut collecter
les mêmes journaux. Wazuh livre son propre indexeur et son tableau de bord
(forks d'OpenSearch), donc faire tourner les deux sur une petite VM n'est
pas recommandé ; essayer ELK sur une VM à part et comparer : langage de
règles, tableaux de bord, consommation de ressources.

## Preuves

- Capture du tableau de bord avec les deux agents **Active**.
- Captures des alertes pour chaque activité du tableau ci-dessus, avec mes
  notes de triage.
- Événement FIM pour `/etc/hosts` montrant les anciennes et nouvelles sommes.

## Ce que j'ai appris

_À compléter par Lucas._
