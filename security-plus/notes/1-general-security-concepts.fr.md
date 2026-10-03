# Domaine 1 — Concepts généraux de sécurité (≈12 %)

[English](1-general-security-concepts.md) · **Français** · [Deutsch](1-general-security-concepts.de.md)

## Catégories et types de contrôles de sécurité

| Catégorie | Exemples |
|-----------|----------|
| Technique | Règles de pare-feu, MFA, chiffrement, EDR |
| De gestion | Politiques, analyses de risques, programme de sensibilisation |
| Opérationnelle | Gardiens, gestion des changements, sauvegardes faites par le personnel |
| Physique | Serrures, clôtures, lecteurs de badges, CCTV |

| Type | Rôle | Exemple |
|------|------|---------|
| Préventif | Empêcher que ça arrive | Verrouillage de compte, refus du pare-feu |
| Dissuasif | Décourager | Bandeau d'avertissement, caméra visible |
| Détectif | Voir que c'est arrivé | IDS, revue des journaux, alerte SIEM |
| Correctif | Réparer après coup | Restaurer une sauvegarde, corriger |
| Compensatoire | Autre solution quand le contrôle idéal n'est pas possible | Isolation réseau d'une machine qu'on ne peut pas corriger |
| Directif | Dire aux gens quoi faire | Politique, panneau « personnel autorisé uniquement » |

## Principes de base

- **Triade CIA** : confidentialité (chiffrement, contrôle d'accès), intégrité
  (hachage, signatures), disponibilité (redondance, sauvegardes, protection
  contre le DDoS).
- **Non-répudiation** : l'émetteur ne peut pas nier — signatures numériques.
- **AAA** : authentification (qui es-tu), autorisation (que peux-tu faire),
  accounting (qu'as-tu fait — journaux).
- **Zero Trust** : ne jamais faire confiance selon l'emplacement ; vérifier
  explicitement chaque requête. Le *plan de contrôle* (moteur de politique,
  administrateur de politique) décide ; le *plan de données* (point
  d'application de la politique) applique. Identité adaptative, réduction du
  périmètre de menace, zones de confiance implicite.
- **Analyse d'écart** : état actuel contre état voulu (p. ex. contre un
  référentiel).
- **Physique** : bornes, sas de contrôle d'accès (mantrap), éclairage,
  capteurs (infrarouge, pression, micro-ondes, ultrasons).
- **Leurre** : honeypot (un hôte), honeynet (un réseau), honeyfile, honeytoken
  (identifiant ou donnée fictifs qui alertent quand on s'en sert).

## Gestion des changements

Processus d'approbation, responsable, parties prenantes, analyse d'impact,
résultats de tests, **plan de retour arrière**, fenêtre de maintenance, SOP.
Implications techniques : listes d'autorisation/de refus, activités
restreintes, interruption, redémarrages de services/applications,
applications héritées, dépendances. Mettre à jour la documentation et les
schémas ; gestion de versions.

## Notions de cryptographie

| Notion | À retenir |
|--------|-----------|
| Symétrique | Une clé partagée, rapide (AES). Problème : la distribution de la clé |
| Asymétrique | Paire clé publique/privée (RSA, ECC). Sert à l'échange de clés et aux signatures |
| Hachage | À sens unique, longueur fixe (SHA-256). Intégrité, stockage des mots de passe (+ sel) |
| Sel | Valeur aléatoire par mot de passe → met en échec les rainbow tables |
| Étirement de clé | PBKDF2, bcrypt, Argon2 — lents exprès |
| Signature numérique | Empreinte signée avec la clé **privée** de l'émetteur, vérifiée avec sa clé **publique** |
| Chiffrer pour quelqu'un | Utiliser **sa clé publique** ; il déchiffre avec sa clé privée |
| PKI | La CA émet les certificats ; CRL / OCSP (stapling) pour la révocation ; certificats wildcard et SAN |
| Séquestre de clés | Un tiers détient les clés pour la récupération |
| TPM / HSM / enclave sécurisée | Protection matérielle des clés (TPM = sur la carte, HSM = appliance dédiée) |
| Obscurcissement | Stéganographie, tokenisation (remplacer la valeur par un jeton), masquage des données |
| Blockchain | Registre distribué, dont l'altération se voit |
| Niveaux de chiffrement | Disque entier, partition, volume, fichier, base de données, enregistrement ; transport (TLS, IPsec) |
