# Domaine 3 — Architecture de sécurité (≈18 %)

[English](3-security-architecture.md) · **Français** · [Deutsch](3-security-architecture.de.md)

## Modèles d'architecture

| Modèle | Points de sécurité |
|--------|--------------------|
| Cloud (IaaS/PaaS/SaaS) | **Responsabilité partagée** — le client reste toujours propriétaire des données et des identités |
| Hybride | Politique cohérente entre le site et le cloud |
| Infrastructure as Code | Relire les modèles comme du code ; détection de dérive |
| Serverless / microservices | Beaucoup de petites surfaces d'attaque ; sécurité des API |
| Réseau : sur site, centralisé ou décentralisé | Point unique de défaillance, ou gestion plus difficile |
| Conteneurs et virtualisation | Provenance des images, isolation, correction des images de base |
| IoT, ICS/SCADA, RTOS, embarqué | Difficile à corriger → les segmenter |
| Haute disponibilité | Redondance, répartition de charge, clustering |

À prendre en compte : disponibilité, résilience, coût, réactivité,
passage à l'échelle, facilité de déploiement/de reprise, disponibilité des
correctifs, transfert du risque, énergie, calcul.

## Sécurité réseau

- **Zones / segmentation** : DMZ (sous-réseau filtré), VLAN, air gap.
- **Équipements** : pare-feu (stateful, NGFW, WAF, UTM), IDS/IPS (en ligne ou
  en tap), serveur de rebond, proxy (direct/inverse), répartiteur de charge,
  802.1X/NAC, capteurs.
- **Modes de panne** : fail-open (disponibilité) contre fail-closed (sécurité).
- **Communication sécurisée** : VPN (IPsec, TLS), SD-WAN, SASE (réseau +
  sécurité comme service cloud).
- **Choix des contrôles** selon la surface d'attaque, la connectivité, le
  placement des équipements.

## Protection des données

- **Types de données** : réglementées, secret commercial, propriété
  intellectuelle, juridiques, financières, lisibles ou non par un humain.
- **Classifications** : public, privé, sensible, confidentiel, restreint,
  critique.
- **États** : au repos, en transit, en cours d'utilisation.
- **Souveraineté / géolocalisation** : lois du pays où les données sont
  stockées (GDPR / RGPD en France et dans l'UE).
- **Méthodes** : chiffrement, hachage, masquage, tokenisation,
  obscurcissement, segmentation, restrictions de permissions.

## Résilience et reprise

- **Sites** : chaud (prêt tout de suite), tiède (le matériel est là, il
  manque les données), froid (seulement le local) ; dispersion géographique.
- **Sauvegardes** : sur site/hors site, fréquence, chiffrement, instantanés,
  réplication, journalisation. Tester les restaurations !
- **Énergie** : onduleur (court terme), groupe électrogène (long terme).
- **Continuité des opérations**, planification de capacité (personnes,
  technologie, infrastructure), tests (exercice sur table, bascule,
  simulation, traitement en parallèle).
- **Mesures** : RTO (en combien de temps on restaure), RPO (quelle perte de
  données est acceptable), MTTR (temps moyen de réparation), MTBF (temps
  moyen entre pannes).
