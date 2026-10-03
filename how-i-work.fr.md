# Comment je travaille

[English](how-i-work.md) · **Français** · [Deutsch](how-i-work.de.md)

Cette page est pour quelqu'un qui ouvre le dépôt et veut savoir ce que
j'utilise vraiment. Les labs sont la preuve. Cette page est le contexte.

## Machine du quotidien

J'utilise CachyOS tous les jours. CachyOS, c'est Arch Linux, avec son
propre noyau et ses propres dépôts. Je l'ai installé, je le mets à jour,
et je le répare moi-même. Le disque est chiffré.

Le lab Windows tourne sur le même PC. libvirt héberge un contrôleur de
domaine Windows Server 2025 évaluation (`dc01`, domaine `lab.local`) et
un client Windows 11 évaluation (`win11-soc`). Compte rendu :
[helpdesk/06-windows-domain](helpdesk/06-windows-domain/).

Un second lab d'identité est un AD Samba dans un conteneur Debian
(`corp.example.com`). Ce lab est à part. Les invités Windows n'y sont
pas joints. Compte rendu :
[helpdesk/04-samba-ad-lab](helpdesk/04-samba-ad-lab/).

Je garde aussi des invités Kali et BlackArch sur ce PC. Quand j'ai le
temps, je fais de courts exercices là, et sur les invités Windows, et
j'avance un peu. Ce que je publie de cette pratique, c'est le côté
défense : le journal que je lirais, le contrôle que je lancerais, la
mesure qui aurait compté. Les flags et les étapes d'attaque restent
hors de ce dépôt. La fiche vide est
[templates/career/practice-note.fr.md](templates/career/practice-note.fr.md).

Sur l'hôte j'utilise aussi git, neovim, rustup, Python, Wireshark, et
Podman sans root. La commande `docker` sur cette machine, c'est Podman.
Les mots de passe du lab restent dans un gestionnaire de mots de passe.
Ils ne sont pas dans ce dépôt.

## Langages

| Langage | Comment je l'utilise |
|---------|----------------------|
| bash | Tous les jours sur CachyOS, et dans le lab de dépannage Linux |
| PowerShell | Sur le lab de domaine Windows, et dans les exercices |
| Python | Les outils `seclab` de ce dépôt, avec pytest |
| Rust | `log-analyzer` et `fim` ici. Deux autres dépôts publics : [Frihart](https://codeberg.org/ichbinlucasv/Frihart) et [HashChat](https://codeberg.org/ichbinlucasv/HashChat) |
| C | Étude, et de courts exercices à compiler et à lire. Pas encore de projet C dans ce dépôt |
| C++ | Au même endroit que le C : des exercices, pas un programme que je livre |
| C# | Un exercice dans [templates/](templates/). Pas d'application C# ici |
| Java | Un exercice de langage |
| Kotlin | Un exercice de langage |
| Haskell | Un exercice de langage. Une ancienne note de HashChat parlait de Haskell. Le code que j'écris maintenant est en Rust |

Les formulaires vides dans [templates/](templates/) sont le rythme de la
semaine : une fiche helpdesk ou SOC, et un langage. Je copie une fiche
et je la remplis en travaillant. Une réponse devinée n'a pas sa place
dans git.

## IA

J'utilise l'IA sur ce travail, et je le dis.

**Grok** (xAI) est l'assistant que j'utilise pour planifier, pour une
relecture, et pour les constructions plus difficiles. Je travaille avec
lui dans le terminal.

Sur le même PC je fais tourner un modèle local, pour que le travail
d'étude n'ait pas besoin d'une clé cloud. **Ollama** sert un modèle
**Qwen**. Trois applications locales le partagent :

- **Hermes** est l'assistant de code local. Je demande une fonction à
  la fois, puis je compile ou je lance le résultat.
- **OpenClaw** est une application d'agents locaux sur le même modèle,
  pour les tâches plus petites.
- **Odysseus** est un espace de travail local dans le navigateur
  (discussion et notes) sur le même modèle. Je l'utilise comme tuteur :
  un sujet à la fois, du défensif, sur des machines virtuelles de ce PC.

Un lab passe à **Done** quand j'ai lancé la vérification moi-même et
gardé la sortie. Un brouillon écrit avec Grok ou Qwen reste **Planned**
ou **In progress** tant que cette exécution n'existe pas. Les fichiers
de preuve sont la sortie des commandes.

Le modèle reste sur l'étude défensive et sur le code. Ce dépôt ne
contient pas de mode d'emploi pour attaquer un système.

## Par où commencer

Pour un poste helpdesk ou un poste SOC junior, commencer ici :

1. [Domaine Windows](helpdesk/06-windows-domain/) — un vrai lab AD DS, encore **In progress**. Le 4 oct. 2026 `win11-soc` était déjà dans `lab.local`, une réinitialisation helpdesk est écrite, et la GPO poste vide est le ticket. Encore ouvert : une session interactive en helpdesk, et un déverrouillage (le seuil est 0).
2. [Dépannage Linux](helpdesk/03-linux-troubleshooting/) — **Done**, avec la sortie du terminal dans `evidence/`.
3. [Rapports d'incident](soc-analyst/03-incident-writeups/) et [règles Sigma](soc-analyst/05-sigma-rules/) — comment je lis un journal, et comment j'écris une détection.
4. [Python](python/) et [Rust](rust/) — de petits outils avec des tests.
5. [Modèles](templates/) — les fiches que j'utilise pour m'entraîner sur une journée de travail.

## Ce que j'apprends encore

Security+ SY0-701 n'est pas obtenu. HTB Academy est en cours. L'allemand
est en cours. Le portugais est ma langue maternelle. Le français et
l'anglais sont tous les deux C1. Je cherche d'abord en France, au
helpdesk ou comme analyste SOC junior (alternance ou POEI). L'Allemagne
est l'autre option, et je peux y travailler en anglais. Une fois au
travail, je commence un diplôme à distance à l'IU (Internationale
Hochschule).

Autres comptes de pratique, même règle (en cours, pas de rang affiché ici) :

- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46) — Academy en cours. Pas de rang sur cette page.
- [TryHackMe](https://tryhackme.com/p/ichbinlucasv)
- [Boot.dev](https://www.boot.dev/u/ichbinlucasv) — la page publique reste cachée avant le niveau 10, donc ce dépôt n'annonce pas de niveau

Une alerte SOC est déjà écrite jusqu'au bout, avec une chronologie UTC :
[IR-03](soc-analyst/03-incident-writeups/IR-03-evtx-password-spray.md).
Le 4 oct. 2026 j'ai vérifié `win11-soc` dans `lab.local`, réinitialisé
un mot de passe staff avec le credential helpdesk, et écrit la GPO
poste vide comme ticket. La sortie est dans le
[lab 06](helpdesk/06-windows-domain/). Les formulaires dans
[templates/career/](templates/career/) restent vides pour la prochaine fois.

## Contact

Seulement ce qui est public. Les mots de passe du lab restent hors de ce dépôt.

- E-mail : ichbinlucas@pm.me
- [LinkedIn](https://www.linkedin.com/in/lucas-nunes-soares-63148637b/)
- [X](https://x.com/ichbinlucasv)
- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46)

Profils publics :
[codeberg.org/ichbinlucasv](https://codeberg.org/ichbinlucasv) et
[github.com/ichbinlucasv](https://github.com/ichbinlucasv).
