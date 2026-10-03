# Domaine 4 — Opérations de sécurité (≈28 %, le plus gros domaine)

[English](4-security-operations.md) · **Français** · [Deutsch](4-security-operations.de.md)

## Référentiels de base et durcissement

Établir → déployer → maintenir les baselines (CIS Benchmarks). Durcir les
mobiles, les postes, les commutateurs/routeurs, le cloud, les serveurs, l'ICS,
l'embarqué, l'IoT. Sans fil : WPA3, RADIUS/802.1X (entreprise), relevés de
site, cartes de chaleur. Mobile : MDM, BYOD / COPE / CYOD, conteneurisation.
Sécurité applicative : validation des entrées, cookies sécurisés, analyse
statique et dynamique du code, signature du code, bac à sable.

## Gestion des actifs

Acquisition/achat → attribution (responsable, classification) →
suivi (inventaire, énumération) → mise au rebut (assainissement,
destruction, certification, conservation des données).

## Gestion des vulnérabilités

Identifier (scans de vulnérabilités, analyse d'application/de code, flux de
menaces, test d'intrusion, bug bounty) → analyser (score **CVSS**, identifiant
**CVE**, faux positif contre faux négatif, priorisation, facteur
d'exposition, variables d'environnement, tolérance au risque) → répondre
(correctif, assurance, segmentation, contrôles compensatoires, exceptions) →
**valider** (re-scanner, auditer, vérifier) → rapporter.

## Surveillance et alertes

Agrégation des journaux, alertes, scans, rapports, archivage, réponse à
l'alerte (quarantaine, **ajustement des alertes**). Outils : **SIEM**, SCAP,
benchmarks, agents ou sans agent, antivirus, DLP, traps SNMP, NetFlow,
scanners de vulnérabilités.

## Capacités de sécurité d'entreprise

Règles de pare-feu et ports, signatures IDS/IPS, filtrage web (avec agent,
proxy, catégories d'URL, réputation), sécurité de l'OS (GPO, SELinux),
protocoles sécurisés (remplacer Telnet→SSH, HTTP→HTTPS, FTP→SFTP,
LDAP→LDAPS, SNMPv1/2→v3), filtrage DNS, sécurité de l'e-mail (**SPF, DKIM,
DMARC**, passerelle), FIM, DLP, NAC, EDR/XDR, analyse du comportement des
utilisateurs.

## Gestion des identités et des accès

Provisionnement/déprovisionnement, attribution des permissions, preuve
d'identité, fédération, SSO (**LDAP, OAuth, SAML**), interopérabilité,
attestation. Modèles de contrôle d'accès : **obligatoire (MAC)**,
**discrétionnaire (DAC)**, **basé sur les rôles (RBAC)**, basé sur des
règles, basé sur des attributs (ABAC), selon l'heure. Facteurs MFA : quelque
chose que tu sais / que tu as / que tu es / l'endroit où tu es. Sans mot de
passe, passkeys. **PAM** : droits juste à temps, coffre de mots de passe,
identifiants éphémères.

## Automatisation et orchestration

Cas d'usage : provisionnement des utilisateurs, provisionnement des
ressources, garde-fous, groupes de sécurité, création de tickets,
escalade, activation/désactivation de services, tests en CI, intégrations
d'API. Intérêts : efficacité, application des baselines, réaction plus
rapide, effet multiplicateur sur l'équipe. Risques : complexité, coût, point
unique de défaillance, dette technique.

## Réponse à incident

**Processus** : préparation → détection → analyse → confinement →
éradication → reprise → retour d'expérience. Formation, tests (exercice sur
table, simulation), analyse de cause racine, chasse aux menaces,
**investigation numérique** : gel juridique, **chaîne de possession**,
acquisition (ordre de volatilité : CPU/cache → RAM → swap → disque →
journaux distants → sauvegardes), rapport, conservation, e-discovery.

## Sources de données pour les enquêtes

Pare-feu, application, poste, journaux de sécurité propres à l'OS, IPS/IDS,
journaux réseau, métadonnées ; scans de vulnérabilités, rapports
automatiques, tableaux de bord, captures de paquets.
