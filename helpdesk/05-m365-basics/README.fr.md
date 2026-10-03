# Lab 05 — Bases d'administration Microsoft 365

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Planned — notes de concept seulement ; pas pratiqué dans un tenant Microsoft 365. Il me faut un essai Microsoft 365 ou un tenant développeur, que je n'ai pas encore ; rien ici n'est simulé.

## Objectif

Comprendre les concepts Microsoft 365 / Entra ID qui reviennent au helpdesk :
cycle de vie des utilisateurs, licences, groupes, MFA, réinitialisation de
mot de passe en libre-service, et quel centre d'administration sert à quoi.
C'est un **lab de concepts documenté** — aucune donnée de vrai tenant ici.

## Mise en place

- Option A : bac à sable du programme développeur Microsoft 365 (les conditions
  d'accès ont changé avec le temps — vérifier les conditions actuelles) ou un
  essai Microsoft 365 Business.
- Option B : modules gratuits et guides interactifs Microsoft Learn (parcours
  MS-900 / SC-900) quand je n'ai pas de tenant.
- Tenant fictif : `exemple-sarl.onmicrosoft.com`, domaine personnalisé `example.com`.

## Étapes

### 1. Carte des centres d'administration

| Tâche | Où |
|-------|----|
| Créer des utilisateurs, attribuer des licences, réinitialiser des mots de passe | Centre d'administration Microsoft 365 (`admin.microsoft.com`) |
| Identité, groupes, MFA, accès conditionnel, journaux de connexion | Centre d'administration Microsoft Entra (`entra.microsoft.com`) |
| Boîtes aux lettres, boîtes partagées, flux de messagerie, suivi des messages | Centre d'administration Exchange |
| Stratégies Teams, paramètres de réunion | Centre d'administration Teams |
| Appareils, stratégies de conformité, déploiement d'applications | Intune (`intune.microsoft.com`) |
| Alertes, hameçonnage, quarantaine, incidents Defender | Portail Microsoft Defender (`security.microsoft.com`) |
| Rétention, DLP, eDiscovery | Portail Microsoft Purview |

### 2. Cycle de vie (arrivée / mobilité / départ)

- **Arrivée :** créer l'utilisateur → emplacement d'utilisation (obligatoire
  avant la licence) → attribuer la licence (idéalement par licence de groupe)
  → ajouter aux groupes → enregistrement MFA à la première connexion.
- **Mobilité :** changer les groupes / le service ; retirer les accès qui ne
  servent plus.
- **Départ :** bloquer la connexion → révoquer les sessions → réinitialiser
  le mot de passe → convertir la boîte en boîte partagée ou poser un
  transfert selon la politique → retirer la licence → supprimer après la
  durée de rétention.

PowerShell Microsoft Graph équivalent (documenté, valeurs fictives) :

```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All","Group.ReadWrite.All"
Get-MgUser -Filter "startswith(displayName,'Julien')" | Select DisplayName,UserPrincipalName
Update-MgUser -UserId j.dupont@example.com -AccountEnabled:$false      # block sign-in
Revoke-MgUserSignInSession -UserId j.dupont@example.com
Get-MgSubscribedSku | Select SkuPartNumber,ConsumedUnits
```

### 3. Notions de licence

- Une licence (SKU, par exemple *Microsoft 365 Business Premium*) contient des
  plans de service (Exchange Online, Teams, Intune, Entra ID P1…).
- La **licence basée sur les groupes** réduit les erreurs : ajouter
  l'utilisateur à `LIC_M365_BP`.
- Panne helpdesk classique : « pas de boîte aux lettres » → licence absente
  ou emplacement d'utilisation non renseigné.

### 4. MFA et authentification

- Préférer **Microsoft Authenticator** (correspondance de nombres) ou
  **FIDO2/clés d'accès** au SMS.
- **Paramètres de sécurité par défaut** (gratuits) contre **accès
  conditionnel** (Entra ID P1) : stratégies du type « MFA pour tous les
  utilisateurs », « bloquer l'authentification héritée », « appareil conforme
  exigé pour les admins ».
- Toujours garder **deux comptes break-glass** exclus de l'accès conditionnel,
  avec des mots de passe longs stockés hors ligne et des connexions surveillées.
- La **réinitialisation en libre-service** permet à l'utilisateur de changer
  son mot de passe après avoir prouvé son identité — moins de tickets, mais
  seulement si les méthodes d'enregistrement sont solides.

### 5. Scénarios helpdesk (à faire dans le bac à sable ou sur papier)

| Scénario | Vérifications |
|----------|---------------|
| L'utilisateur a perdu le téléphone avec Authenticator | Vérifier l'identité hors bande → exiger un réenregistrement MFA → révoquer les sessions |
| « Trop de tentatives de connexion » | Journaux de connexion Entra : motif d'échec, IP, lieu, application cliente |
| Accès à une boîte partagée | Centre d'administration Exchange → délégation de boîte (accès total / Envoyer en tant que) |
| Connexion suspecte depuis l'étranger | Journaux de connexion + utilisateurs à risque → bloquer, réinitialiser, révoquer, escalader au SOC |
| Le nouvel arrivant n'a pas Teams | Licence attribuée ? Plan de service activé ? Attendre le provisionnement |

### 6. Rôles d'admin au moindre privilège

Les agents helpdesk reçoivent **Helpdesk Administrator** ou **User
Administrator**, pas Global Administrator. Utiliser **PIM** (Entra ID P2)
pour une élévation juste à temps.

## Preuves

- Captures d'un bac à sable ou d'un essai (noms de tenant floutés) : création
  d'utilisateur, attribution de licence, stratégie d'accès conditionnel en
  mode rapport uniquement, entrée de journal de connexion.
- Ou : badges de fin de module Microsoft Learn.

## Ce que j'ai appris

_À compléter par Lucas._
