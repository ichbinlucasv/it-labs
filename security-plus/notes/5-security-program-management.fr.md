# Domaine 5 — Gestion et supervision du programme de sécurité (≈20 %)

[English](5-security-program-management.md) · **Français** · [Deutsch](5-security-program-management.de.md)

## Gouvernance

- **Politiques** (haut niveau, obligatoires) : AUP, sécurité de
  l'information, continuité d'activité, reprise après sinistre, réponse à
  incident, SDLC, gestion des changements.
- **Normes** : mots de passe, contrôle d'accès, sécurité physique,
  chiffrement.
- **Procédures** : gestion des changements, arrivée/départ, playbooks.
- **Guides** : recommandations, pas obligatoires.
- Contexte externe : réglementaire, juridique, sectoriel, local/régional,
  national, mondial. Suivi et révision.
- Structures : conseils, comités, organismes publics, centralisé contre
  décentralisé.
- Rôles pour les systèmes et les données : **propriétaire** (rend des
  comptes), **responsable de traitement** (décide pourquoi et comment les
  données personnelles sont traitées), **sous-traitant** (traite pour le
  compte du responsable), **dépositaire/intendant** (le soin au quotidien).

## Gestion des risques

- Identification → évaluation (au cas par cas, récurrente, une fois,
  continue) → analyse → registre → traitement → rapport.
- **Qualitatif** (haut/moyen/bas, carte de chaleur) contre **quantitatif** :
  - SLE = valeur de l'actif × facteur d'exposition
  - ARO = occurrences attendues par an
  - **ALE = SLE × ARO**
- Registre des risques : indicateurs de risque clés, propriétaires du
  risque, seuil de risque.
- Tolérance au risque contre **appétit pour le risque** (expansif,
  conservateur, neutre).
- Stratégies : **transférer** (assurance), **accepter** (dérogation/exception),
  **éviter** (arrêter l'activité), **réduire** (contrôles).
- Analyse d'impact sur l'activité : RTO, RPO, MTTR, MTBF.

## Risque tiers

Évaluation des fournisseurs (test d'intrusion, clause de droit d'audit,
preuves d'audits internes, évaluations indépendantes, analyse de la chaîne
d'approvisionnement), choix du fournisseur (diligence, conflit d'intérêts),
accords : **SLA** (niveaux de service), **MOA/MOU** (intention), **MSA**
(conditions cadres), **WO/SOW** (travail précis), **NDA**, **BPA**
(partenaires commerciaux). Suivi des fournisseurs, questionnaires, règles
d'engagement.

## Conformité

Rapports internes/externes, conséquences du non-respect (amendes, sanctions,
atteinte à la réputation, perte de licence, effets contractuels), suivi de
la conformité (diligence/soin, attestation, automatisation). **Vie privée** :
effets juridiques, personne concernée, responsable de traitement contre
sous-traitant, propriété, inventaire et conservation des données, **droit à
l'oubli** (GDPR). En France : la CNIL est l'autorité de protection des
données ; l'ANSSI est l'agence nationale de cybersécurité ; NIS2 étend les
obligations à davantage de secteurs.

## Audits et évaluations

Attestation, interne (conformité, comité d'audit, auto-évaluation), externe
(réglementaire, examens, tiers indépendant). **Test d'intrusion** : physique,
offensif (red), défensif (blue), intégré (purple) ; environnement connu
(boîte blanche), partiellement connu (grise), inconnu (boîte noire) ;
reconnaissance passive contre active.

## Sensibilisation à la sécurité

Campagnes de phishing et signalement, reconnaître un comportement anormal
(risqué, inattendu, non voulu), guides pour les utilisateurs (manuels de
politique, conscience de la situation, menace interne, gestion des mots de
passe, supports amovibles, ingénierie sociale, sécurité opérationnelle,
travail hybride/à distance), signalement et suivi (au début, puis régulier),
conception et mise en œuvre.
