# IR-03 — Password spraying Kerberos dans les journaux Windows Security

[English](IR-03-evtx-password-spray.md) · **Français** · [Deutsch](IR-03-evtx-password-spray.de.md)

| Champ | Valeur |
|-------|--------|
| Analyste | Lucas |
| Date d'analyse | 2026-09-27 |
| Jeu de données et URL | EVTX-ATTACK-SAMPLES de Samir Bousseaden — <https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES> — fichier `Credential Access/kerberos_pwd_spray_4771.evtx` (téléchargé le 2026-09-27 depuis l'URL raw GitHub) |
| Licence | Voir le dépôt (GPL) |
| SHA256 du fichier | `4a0a1c7132e216dbc704c806e9429df9ae3ac00485d5238e50c776e3099ae11d` |
| Plage de temps des données (UTC) | 2020-07-22 20:29:27.321 – 20:29:36.437 (12 événements) |
| Gravité | Élevée (un mot de passe de domaine valide a été trouvé) — dans un environnement réel |
| Statut | Terminé |

Les noms d'hôtes, de comptes et les adresses ci-dessous viennent de cet
exemple public d'entraînement (un domaine de lab `threebeesco.com`), pas d'un
incident réel. Sortie complète des commandes :
[`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt).

## 1. Résumé pour la direction

Sur le contrôleur de domaine `01566s-win16-ir.threebeesco.com`, une seule
adresse source, `172.16.66.1`, a demandé des tickets Kerberos pour **10
comptes différents en 11 millisecondes** — seul un outil fait ça. Sept noms
n'existaient pas, deux comptes existants (`Administrator`, `backdoor`) ont
été refusés pour un mauvais mot de passe, et **un compte, `normal`, a reçu
un ticket** : le mot de passe essayé était le bon pour lui. C'est du password
spraying (un mot de passe, beaucoup de comptes), et ça a marché pour un
compte. Actions recommandées : réinitialiser le mot de passe de `normal`,
voir ce que l'hôte source a fait avec le ticket, et enquêter sur le compte
nommé `backdoor`.

## 2. Périmètre et questions — réponses

| Question | Réponse |
|----------|---------|
| Combien de comptes, depuis où ? | 10 noms d'utilisateurs distincts, tous depuis `172.16.66.1` (le dernier événement l'affiche comme `::ffff:172.16.66.1`, la forme IPv6 IPv4-mapped) |
| Fenêtre de temps et rythme ? | 20:29:36.414 → 20:29:36.437 UTC : 11 requêtes en 23 ms, les 10 noms dans les 20 premières ms |
| Codes d'échec Kerberos ? | 4768 `0x6` (KDC_ERR_C_PRINCIPAL_UNKNOWN — l'utilisateur n'existe pas) × 7 ; 4771 `0x18` (KDC_ERR_PREAUTH_FAILED — mauvais mot de passe) × 2 |
| Un compte a-t-il réussi ? | **Oui** — 4768 avec le statut `0x0` pour `normal` (deux fois, ticket AES256 `0x12`), 9 ms après les échecs |
| Spraying ou force brute ? | Spraying : chaque nom essayé une fois, beaucoup de noms |

Contexte : **4768** = un TGT a été demandé (succès ou échec, selon `Status`) ;
**4771** = la pré-authentification Kerberos a échoué. Un utilisateur inconnu
n'arrive jamais à la pré-authentification, c'est pour ça que ça apparaît
comme un échec 4768 et pas comme un 4771.

## 3. Journal d'enquête

| # | Outil | Action | Résultat |
|---|-------|--------|----------|
| 1 | `sha256sum` | Hasher l'EVTX | `4a0a1c71…ae11d` |
| 2 | [`evtx_to_jsonl.py`](evtx_to_jsonl.py) (python-evtx 0.8.1) | Convertir en un objet JSON par événement | 12 événements. J'ai utilisé python-evtx à la place du `evtx_dump` prévu, parce qu'il ne manquait qu'un `pip install` |
| 3 | `jq` | Compter par EventID | 1 × 1102, 9 × 4768, 2 × 4771 |
| 4 | `jq` | Utilisateurs cibles distincts | 10 (`HD01`, `HD02`, `admin`, `admin02`, `svc-01`, `svc-02`, `bob`, `Administrator`, `backdoor`, `normal`) |
| 5 | `jq` | Adresses source | seulement `172.16.66.1` (ports source 55957–55969 en hausse, puis 52559 en IPv6 IPv4-mapped) |
| 6 | `jq` | Codes de statut | `0x6` × 7, `0x18` × 2, `0x0` × 2 |
| 7 | `jq` | Rythme | tout le spray < 25 ms — un graphe par minute ne sert à rien |
| 8 | Sigma | Nouvelle règle [`win_kerberos_password_spray_correlation.yml`](../05-sigma-rules/rules/win_kerberos_password_spray_correlation.yml) : `value_count` de `TargetUserName` distincts ≥ 5 par `IpAddress` en 5 min sur 4771 `0x18` / 4768 `0x6` ; `sigma check` propre ; convertie avec le backend SQLite et lancée sur les événements | 3 alertes pour `172.16.66.1` (5, 7, 9 utilisateurs distincts) |
| 9 | Hayabusa / Chainsaw | Pas exécuté | — |

## 4. Chronologie (UTC, 2020-07-22)

| Heure | Événement | Détail |
|-------|-----------|--------|
| 20:29:27.321 | 1102 | Journal Security effacé par `3B\a-jbrown` |
| 20:29:36.414–.415 | 4768 `0x6` × 7 | Utilisateurs inconnus `HD01`, `admin`, `svc-02`, `HD02`, `svc-01`, `bob`, `admin02` |
| 20:29:36.425 | 4771 `0x18` × 2 | Mauvais mot de passe pour `Administrator`, `backdoor` |
| 20:29:36.434 | 4768 `0x0` | TGT délivré à `normal` |
| 20:29:36.437 | 4768 `0x0` | Second TGT pour `normal` depuis `::ffff:172.16.66.1` |

À propos du 1102 : le journal a été effacé 9 s avant le spray. Dans cet
exemple, c'est très probablement l'auteur du jeu de données qui remet le
journal à zéro avant l'enregistrement (`a-jbrown` ressemble à un compte
admin). Dans un vrai cas, un journal effacé juste avant une attaque serait
en soi un constat sérieux (T1070.001) ; ici je le note, mais je ne
l'attribue pas à l'attaquant.

## 5. IOC (données d'exemple)

| Type | Valeur | Note |
|------|--------|------|
| IP source | `172.16.66.1` | Adresse interne — il faut enquêter sur l'hôte lui-même |
| Compte compromis | `normal` | Mot de passe deviné |
| Comptes existants visés | `Administrator`, `backdoor` | `backdoor` est un nom suspect pour un compte qui existe |
| Noms inexistants essayés | `HD01`, `HD02`, `admin`, `admin02`, `svc-01`, `svc-02`, `bob` | Liste typique de noms devinés |

## 6. Correspondance ATT&CK

- **T1110.003 Brute Force: Password Spraying** (Credential Access) —
  confirmé : une tentative par compte sur 10 comptes.
- **T1078.002 Valid Accounts: Domain Accounts** — suite possible : le ticket
  de `normal` permettrait à l'attaquant d'agir en tant que cet utilisateur.
  L'exemple s'arrête là, donc ce n'est pas confirmé.
- T1070.001 Clear Windows Event Logs — noté, pas attribué (voir la chronologie).

## 7. Impact

Le mot de passe d'un compte de domaine est connu de celui qui contrôle
`172.16.66.1`. L'attaquant a aussi appris lesquels des noms essayés existent
(`0x6` contre `0x18` le lui dit), dont `Administrator` et `backdoor`.

## 8. Recommandations

1. Réinitialiser le mot de passe de `normal`, révoquer ses sessions/tickets,
   et revoir ses ouvertures de session (4624/4769) après 20:29:36 pour un
   déplacement latéral.
2. Enquêter sur l'hôte `172.16.66.1` (quel processus a envoyé les requêtes).
3. Trouver qui a créé `backdoor` et pourquoi (événements 4720, `whenCreated`).
4. Appliquer une politique de mots de passe qui bloque les mots de passe
   courants, et le MFA là où c'est possible.
5. Déployer la règle de corrélation sur les utilisateurs distincts. Deux
   leçons du test : normaliser `::ffff:x.x.x.x` en `x.x.x.x` avant de
   grouper (sinon le même hôte compte comme deux sources), et ajouter une
   règle de suite « succès pour un des comptes du spray, depuis la même
   source » — ma règle alerte sur les échecs, mais le **succès** est
   l'événement qui compte le plus.

## 9. Preuves

- [`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt) — hash, tableau
  des événements, comptes, et le résultat du rejeu Sigma. L'EVTX lui-même
  n'est pas versionné.
