# Modèles du quotidien

[English](README.md) · **Français** · [Deutsch](README.de.md)

À côté de chaque fichier, les formulaires sont `.fr.md` et `.de.md`.

Je copie un fichier, je remplis les blancs, je garde la copie dans mes notes.
Les blancs restent vides dans git.

Je n'ouvre pas tout ça chaque jour. Un jour utile, c'est une fiche helpdesk
ou SOC, plus **un** bloc de langue. La liste des langues est longue pour que
je n'en laisse pas une de côté pendant six mois. Ce n'est pas une liste à
finir avant le petit-déjeuner.

## Ce matin

1. Copier [career/daily.md](career/daily.md).
2. Prendre la colonne du jour.
3. M'arrêter quand le minuteur finit. Écrire une ligne sur ce que je n'ai pas
   su faire de mémoire.

| Jour | Pratique métier | Langue (25 min) |
| --- | --- | --- |
| Lun | [Ticket helpdesk](helpdesk/ticket.md) | [bash](languages/bash.md) |
| Mar | [Connexion impossible](helpdesk/cant-log-on.md) ou [réinitialisation du mot de passe](helpdesk/password-reset.md) | [PowerShell](languages/powershell.md) |
| Mer | [Triage d'alerte](soc/alert-triage.md) | [Python](languages/python.md) |
| Jeu | [Chronologie](soc/timeline.md) sur une vieille alerte | [Rust](languages/rust.md) ou [C](languages/c.md), une semaine sur deux |
| Ven | [Bilan de la semaine](career/weekly.md) | Une parmi [C++](languages/cpp.md), [C#](languages/csharp.md), [Java](languages/java.md), [Kotlin](languages/kotlin.md), [Haskell](languages/haskell.md). J'alterne. Pas les cinq. |
| Sam | Labo, si les invités sont allumés. [Lab 06](../helpdesk/06-windows-domain/) ou un break/fix Linux. | Seulement si la langue de vendredi est encore floue. |
| Dim | Repos, ou [récit d'entretien](career/story.md) à partir d'une vraie note de labo. | Repos. |

## Helpdesk

La forme longue du ticket est déjà dans
[helpdesk/01-ticket-writing/template.md](../helpdesk/01-ticket-writing/template.md).
Ceux-ci, je les veux en poste.

| Formulaire | Quand je l'utilise |
| --- | --- |
| [ticket.md](helpdesk/ticket.md) | Toute nouvelle demande |
| [ticket.fr.md](helpdesk/ticket.fr.md) | Le même ticket en français, pour un desk en France |
| [shift-start.md](helpdesk/shift-start.md) | Les 15 premières minutes |
| [cant-log-on.md](helpdesk/cant-log-on.md) | « Je n'arrive pas à entrer » |
| [password-reset.md](helpdesk/password-reset.md) | Réinitialisation ou déverrouillage. Vérifier qui demande. |
| [new-user.md](helpdesk/new-user.md) | Arrivant |
| [leaver.md](helpdesk/leaver.md) | Quelqu'un est parti |
| [escalation.md](helpdesk/escalation.md) | Je suis bloqué et je transmets |
| [remote-session.md](helpdesk/remote-session.md) | Je suis sur son écran |
| [kb.md](helpdesk/kb.md) | Le même correctif est arrivé deux fois |

## SOC

| Formulaire | Quand je l'utilise |
| --- | --- |
| [shift-handover.md](soc/shift-handover.md) | Je prends la file, ou je la quitte |
| [alert-triage.md](soc/alert-triage.md) | Une alerte. Pas cinq outils. |
| [timeline.md](soc/timeline.md) | Heures en UTC, la plus ancienne d'abord |
| [ioc-note.md](soc/ioc-note.md) | Quelque chose à chercher, defangé |
| [detection-idea.md](soc/detection-idea.md) | L'alerte que je voudrais, et ce qui serait du bruit |
| [end-of-shift.md](soc/end-of-shift.md) | Ce qui est encore ouvert |

## Carrière

| Formulaire | Quand je l'utilise |
| --- | --- |
| [daily.md](career/daily.md) | Chaque jour d'étude |
| [weekly.md](career/weekly.md) | Vendredi |
| [story.md](career/story.md) | Une vraie histoire pour un entretien. Seulement après avoir fait le travail. |
| [practice-note.fr.md](career/practice-note.fr.md) | Un exercice TryHackMe, HTB, Boot.dev, Kali ou BlackArch. Note du défenseur seulement. |
| [helpdesk-session.fr.md](career/helpdesk-session.fr.md) | Prochaine session helpdesk. La réinitialisation du 4 oct. 2026 est [session-2026-10-04](../helpdesk/06-windows-domain/evidence/session-2026-10-04.fr.md). |
| [domain-join.fr.md](career/domain-join.fr.md) | Prochain contrôle de jonction. Le contrôle du 4 oct. 2026 est [domain-2026-10-04](../helpdesk/06-windows-domain/evidence/domain-2026-10-04.fr.md). |
| [lab-ticket.fr.md](career/lab-ticket.fr.md) | Prochain ticket. La GPO poste vide est [HD-2026-10-04](../helpdesk/06-windows-domain/evidence/HD-2026-10-04.fr.md). |
| [application.fr.md](career/application.fr.md) | Le court texte pour une alternance ou un POEI. C'est moi qui l'envoie. |

## Règles que je continue d'enfreindre

- Pas de mots de passe, de cookies, ni de noms de clients dans une note que
  je pourrais coller dans git.
- Je cite l'erreur. Je n'écris pas « ça a échoué ».
- Un changement, puis je vérifie. Ensuite le changement suivant.
- Si je n'ai fait qu'installer un outil, la note dit installé. Elle ne dit
  pas que je le connais.
- UTC sur les notes SOC. L'heure locale va sur un ticket helpdesk si je dis
  le fuseau.
- Une note de pratique n'a pas de flag et pas d'étapes d'attaque. Elle dit
  ce que je vérifierais.
