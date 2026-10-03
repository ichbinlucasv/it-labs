# Domaine 2 — Menaces, vulnérabilités et mesures d'atténuation (≈22 %)

[English](2-threats-vulnerabilities-mitigations.md) · **Français** · [Deutsch](2-threats-vulnerabilities-mitigations.de.md)

## Acteurs de menace

| Acteur | Motivation | Moyens |
|--------|------------|--------|
| État-nation | Espionnage, perturbation, guerre | Très élevés (APT) |
| Crime organisé | Argent (ransomware, fraude) | Élevés |
| Hacktiviste | Idéologie | Variables |
| Menace interne | Vengeance, argent, négligence | A déjà l'accès |
| Attaquant peu qualifié | Frisson, réputation | Faibles — utilise les outils des autres |
| Shadow IT | Commodité (pas malveillant) | Risque non géré |

Attributs : interne/externe, moyens/financement, sophistication.

## Vecteurs de menace et surface d'attaque

Par message (e-mail, SMS = smishing, messagerie instantanée), images,
fichiers, voix (vishing), supports amovibles, logiciels vulnérables (avec
client ou sans agent), systèmes non pris en charge, réseaux non sécurisés
(sans fil, filaire, Bluetooth), ports ouverts, identifiants par défaut,
chaîne d'approvisionnement (MSP, éditeurs, fournisseurs).

**Vecteurs humains / ingénierie sociale :** phishing, spear phishing,
whaling, BEC (compromission de la messagerie d'entreprise), pretexting,
usurpation, watering hole, usurpation de marque, typosquatting,
mésinformation/désinformation.

## Types de vulnérabilités

- **Application :** injection en mémoire, dépassement de tampon, conditions
  de course (TOC/TOU), mise à jour malveillante.
- **Web :** injection SQL (SQLi), cross-site scripting (XSS), CSRF, SSRF,
  traversée de répertoire.
- **OS / micrologiciel / matériel :** fin de vie, héritage, micrologiciel non
  corrigé.
- **Virtualisation :** évasion de VM, réutilisation de ressources.
- **Cloud :** mauvaise configuration (buckets publics !), IAM faible.
- **Cryptographie :** algorithmes faibles, mauvaise gestion des clés,
  downgrade.
- **Mobile :** sideloading, jailbreak/root.
- **Zero-day :** aucun correctif n'existe encore.

## Indicateurs d'activité malveillante

Verrouillages de comptes, sessions simultanées à des endroits impossibles
(« impossible travel »), contenu bloqué, pics de consommation de ressources,
journalisation hors du cycle habituel, journaux manquants, données de
compromission publiées ou documentées.

**Familles de malwares :** ransomware, trojan, ver (se propage seul),
spyware, bloatware, virus, keylogger, bombe logique, rootkit.
**Attaques réseau :** DDoS (amplifiée/réfléchie), attaques DNS, sans fil
(evil twin, deauth), on-path (MITM), rejeu d'identifiants.
**Attaques sur les mots de passe :** spraying (peu de mots de passe ×
beaucoup d'utilisateurs), force brute (beaucoup de mots de passe × un
utilisateur), credential stuffing (identifiants déjà compromis, réutilisés).
**Autres :** élévation de privilèges, rejeu, falsification, downgrade,
collision (hash), attaque des anniversaires.

## Mesures d'atténuation

Segmentation, contrôle d'accès (ACL, permissions), liste d'autorisation des
applications, isolation, correctifs, chiffrement, surveillance, moindre
privilège, application de la configuration, mise hors service,
**durcissement** (désactiver les ports/services inutilisés, changer les
valeurs par défaut, retirer les logiciels inutiles, pare-feu de l'hôte,
EDR/HIPS).
