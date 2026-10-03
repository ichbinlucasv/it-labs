# Labs IT

[English](README.md) · **Français** · [Deutsch](README.de.md)

Je suis Lucas. J'étudie la cybersécurité. Je cherche un premier poste en
France, au helpdesk ou comme analyste SOC junior (alternance ou POEI).
Linux est la machine que j'utilise vraiment. Windows est un lab sur le même PC.

Je cherche d'abord en France. L'Allemagne est l'autre option. Je peux y
travailler en anglais, j'apprends l'allemand, et ma femme est allemande.
Les pages sont en anglais, en français et en allemand. Je mets l'anglais
à jour en premier. Si une traduction ne dit pas la même chose, c'est
l'anglais qui compte.

Ce dépôt, c'est la pratique, pas un CV fini. **Done** veut dire que j'ai
lancé la vérification et gardé la sortie. Ça ne veut pas dire que je suis
rapide, ni que je sauterais la doc sur un vrai ticket.

J'utilise bash tous les jours, PowerShell sur le lab Windows, et Python et
Rust pour les petits outils plus bas. Le C est sur la liste d'étude. Il n'y
a pas encore de projet C dans ce dépôt.

Le portugais est ma langue maternelle. Le français et l'anglais sont tous
les deux C1. Security+ SY0-701 et HTB Academy sont en cours.

La machine, les langages et les outils d'IA sont dans
[Comment je travaille](how-i-work.fr.md). Version courte : CachyOS (Arch)
tous les jours, Windows seulement en machines virtuelles, Grok pour une
relecture, et un modèle Qwen local via Ollama, partagé par Hermes,
OpenClaw et Odysseus. Un lab est **Done** quand j'ai lancé la
vérification moi-même.

### Statut des labs

| Statut | Sens |
|--------|------|
| **Done** | Le code ou la config tourne, et les vérifications passent dans ce dépôt |
| **In progress** | Vérifié en partie — par exemple la syntaxe est contrôlée, ou ça a tourné sur des données synthétiques, mais pas de bout en bout dans un vrai environnement |
| **Planned** | Une procédure écrite, pas encore lancée dans un vrai environnement |

Décompte actuel : 10 Done, 4 In progress, 3 Planned (voir la matrice de compétences ci-dessous).

> Tous les noms d'hôtes, les utilisateurs, les sociétés et les adresses IP sont fictifs (`example.com`, plages RFC 5737 `192.0.2.0/24`,
> `198.51.100.0/24`, `203.0.113.0/24`, et plages RFC 1918 pour le LAN du lab).
> Exception : les jeux de données publics de formation (captures d'exemple Wireshark,
> EVTX-ATTACK-SAMPLES) sont cités avec leurs valeurs d'origine et leur source.
> Pas de vraies données personnelles, pas d'identifiants, et pas d'outils
> offensifs visant des tiers.

---

## Plan du dépôt

| Chemin | Contenu |
|--------|---------|
| [how-i-work.fr.md](how-i-work.fr.md) | Machine du quotidien (CachyOS), langages, et comment j'utilise Grok plus un modèle Qwen local |
| [`helpdesk/`](helpdesk/) | Tickets, dépannage Linux et Windows, un lab Samba AD, et un domaine Windows Server que j'ai vraiment promu (`lab.local`) |
| [`networking/`](networking/) | Exercices de subnetting + corrigé, analyse de captures (Wireshark/tcpdump), pare-feu hôte nftables |
| [`soc-analyst/`](soc-analyst/) | Homelab Wazuh, analyse de journaux Sysmon + auditd (exemples synthétiques), modèles de rapports d'incident sur des jeux publics, correspondance ATT&CK, règles Sigma |
| [`python/`](python/) | Paquet `seclab` : résumé d'`auth.log` SSH, extracteur d'IOC (defang/refang), vérificateur de hash — bibliothèque standard seulement, suite pytest |
| [`rust/`](rust/) | Workspace Cargo : crates `log-analyzer` et `fim` (contrôle d'intégrité des fichiers) avec tests unitaires |
| [`security-plus/`](security-plus/) | Notes d'étude SY0-701 par domaine + CSV de fiches |
| [`templates/`](templates/) | Formulaires vides que je copie un jour de travail : helpdesk, SOC, et une langue à la fois |
| [`scripts/check_repo.py`](scripts/check_repo.py) | Contrôle d'hygiène du dépôt : sections des README de lab, CSV des fiches, YAML Sigma, motifs de secrets |
| [`.forgejo/workflows-disabled/`](.forgejo/workflows-disabled/) | Workflow CI, **désactivé** tant qu'il n'y a pas de runner (voir [CI](#ci)) |

Chaque README de lab commence par une ligne **Status** et suit le même plan :
**Goal · Setup · Steps · Evidence · What I learned** (dans les versions
françaises : Objectif · Mise en place · Étapes · Preuves · Ce que j'ai appris).

---

## Matrice de compétences — labs × domaines Security+ SY0-701

Domaines : **D1** Concepts généraux de sécurité · **D2** Menaces, vulnérabilités
et atténuations · **D3** Architecture de sécurité · **D4** Opérations de
sécurité · **D5** Gestion du programme de sécurité et supervision.

`●` = sujet principal, `○` = sujet secondaire.

| Lab | Statut | D1 | D2 | D3 | D4 | D5 | Compétences pratiques |
|-----|--------|:--:|:--:|:--:|:--:|:--:|------------------------|
| [helpdesk/01 Écriture de tickets](helpdesk/01-ticket-writing/) | Done | ○ | | | ● | ○ | ITSM, communication claire, escalade |
| [helpdesk/02 Dépannage Windows](helpdesk/02-windows-troubleshooting/) | Planned | | ○ | ○ | ● | | Observateur d'événements, PowerShell, réseau, SFC/DISM |
| [helpdesk/03 Dépannage Linux](helpdesk/03-linux-troubleshooting/) | Done | | ○ | ○ | ● | | systemd, journalctl, disque/DNS/droits |
| [helpdesk/04 Samba AD DC](helpdesk/04-samba-ad-lab/) | In progress | ● | | ● | ● | | Identité, groupes, concepts de GPO, moindre privilège |
| [helpdesk/05 Bases M365](helpdesk/05-m365-basics/) | Planned | ● | ○ | ● | ● | ○ | Entra ID, licences, MFA, concepts de Conditional Access |
| [helpdesk/06 Domaine Windows](helpdesk/06-windows-domain/) | In progress | ● | | ● | ● | | Windows Server AD DS, OU, groupe helpdesk, RSAT sur le DC |
| [networking/01 Subnetting](networking/01-subnetting/) | Done | | | ● | | | CIDR, VLSM, plans d'adressage |
| [networking/02 Capture de paquets](networking/02-packet-capture/) | Done | | ● | ○ | ● | | Filtres Wireshark, tcpdump, analyse de protocoles |
| [networking/03 Pare-feu nftables](networking/03-nftables-firewall/) | Done | ○ | ● | ● | ○ | | Refus par défaut, filtrage à état, journalisation |
| [soc-analyst/01 Homelab Wazuh](soc-analyst/01-wazuh-homelab/) | Planned | | ○ | ○ | ● | | Déploiement SIEM/XDR, agents, triage des alertes |
| [soc-analyst/02 Sysmon + auditd](soc-analyst/02-sysmon-auditd-logs/) | Done | | ● | | ● | | Télémétrie des postes, corrélation de journaux |
| [soc-analyst/03 Rapports d'incident](soc-analyst/03-incident-writeups/) | In progress | | ● | | ● | ○ | Cycle de réponse à incident, rapports, gestion des preuves |
| [soc-analyst/04 Correspondance ATT&CK](soc-analyst/04-attack-mapping/) | Done | | ● | | ● | | Couverture de détection guidée par la menace |
| [soc-analyst/05 Règles Sigma](soc-analyst/05-sigma-rules/) | Done | | ● | | ● | | Ingénierie de détection, pySigma/sigma-cli |
| [python/ outils seclab](python/) | Done | ○ | ● | | ● | | Regex, parsing, hachage, tests automatisés |
| [rust/ log-analyzer + fim](rust/) | Done | ○ | ○ | ○ | ● | | Surveillance d'intégrité, programmation système |
| [security-plus/ notes et fiches](security-plus/) | In progress | ● | ● | ● | ● | ● | Préparation de l'examen sur tous les domaines |

---

## Démarrage rapide

```bash
# Python tools + tests
(cd python && python3 -m venv .venv && . .venv/bin/activate \
  && pip install -e '.[test]' && pytest)

# Rust workspace
(cd rust && cargo test && cargo clippy --all-targets -- -D warnings)

# Sigma rules: lint + replay on the synthetic samples
python3 -m venv .venv-sigma && . .venv-sigma/bin/activate
pip install sigma-cli pyyaml && sigma plugin install sqlite
sigma check soc-analyst/05-sigma-rules/rules/
python soc-analyst/05-sigma-rules/validate_rules.py

# Repo hygiene
python3 scripts/check_repo.py
```

## Ce que j'ai vraiment exécuté

| Élément | Comment |
|---------|---------|
| Outils Python | `pytest` — 35 tests passent |
| Crates Rust | `cargo test` (11 tests unitaires) et `cargo clippy --all-targets -- -D warnings` propres, `cargo fmt --check` propre |
| Règles Sigma | YAML valide ; `sigma check` 0 erreur, 0 problème (sigma-cli 3.1.0) ; les 8 règles d'origine se déclenchent sur les exemples synthétiques via le backend SQLite ; la règle de spraying Kerberos se déclenche sur un exemple EVTX public |
| Dépannage Linux | 7 scénarios cassé/réparé dans un conteneur systemd Debian 13 (`systemd-nspawn`) ; sortie du terminal dans `helpdesk/03-linux-troubleshooting/evidence/` (kill OOM pas reproductible là) |
| Samba AD DC | provisionné dans un conteneur Debian 13 ; DNS SRV, Kerberos, OU/groupes/utilisateurs, politique de verrouillage et délégation helpdesk testés ; jointure d'un client Windows pas faite |
| Domaine Windows Server | `dc01` promu en `lab.local` le 5 sept. 2026 (Server 2025 eval, libvirt). Inventaire du 7 sept. : NTDS et DNS tournent, les OU et les comptes helpdesk/SOC/staff sont là, ADUC et GPMC sur le DC. L'invité Windows 11 existe. Je n'ai pas encore rédigé une jointure de domaine ni une session helpdesk dessus |
| Jeu de règles nftables | `nft -c -f` OK ; trafic testé avec trois network namespaces (admin / extérieur / client en liste de blocage), compteurs et journal noyau vérifiés |
| Capture de paquets | capture perso générée dans un network namespace et analysée avec tshark ; exemple public Wireshark `dns.cap` analysé avec un mini-rapport |
| Exemples Sysmon / auditd | toutes les questions ont une réponse, chronologie UTC et liste d'IOC écrites ; `ausearch`/`aureport` sur le journal auditd synthétique |
| Rapport d'incident IR-03 | EVTX public de password spray Kerberos parsé avec python-evtx et analysé de bout en bout |
| Correspondance ATT&CK | 15 ID de techniques vérifiés contre le bundle STIX ATT&CK Enterprise 19.2 ; layer Navigator généré |
| Réponses subnetting | calculées avec Python `ipaddress` |
| Fiches | 99 fiches, lues avec Python `csv` |

Encore ouvert : les scénarios de dépannage Windows, joindre un client Windows
au domaine Samba, Wazuh, un tenant M365, une VM isolée pour les pcaps de
malware, et une machine Splunk. Ces pages le disent. Le domaine Windows
Server est un lab à part (`helpdesk/06`), et il s'arrête à l'inventaire.

## CI

Le workflow est dans `.forgejo/workflows-disabled/ci.yml`, donc Forgejo ne le
prend **pas** (les runners hébergés de Codeberg sont limités, et le job
resterait en file pour toujours). Il lui faut un **runner Forgejo
auto-hébergé avec le label `docker`**. Pour l'activer :

1. Enregistrer un [runner Forgejo](https://forgejo.org/docs/latest/admin/actions/)
   avec le label `docker` pour ce dépôt (Codeberg : dépôt *Settings →
   Actions → Runners*) et activer Actions pour le dépôt.
2. `git mv .forgejo/workflows-disabled/ci.yml .forgejo/workflows/ci.yml`, puis commit et push.

Sur GitHub, copier le fichier vers `.github/workflows/` et mettre `runs-on: ubuntu-latest`.

## Apprentissage en cours

- CompTIA Security+ SY0-701 — en cours
- HTB Academy — modules SOC Analyst / fondamentaux en cours

## Licence

Code : [MIT](LICENSE). Documentation (Markdown, notes, fiches) :
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Voir [LICENSE](LICENSE).
