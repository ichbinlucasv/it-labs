# Lab 03 — Rapports d'incident sur des jeux de données publics

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** In progress — [IR-03](IR-03-evtx-password-spray.md) (password spraying Kerberos, exemple EVTX public) est analysé et terminé ; IR-01 (pcap malware-traffic, il faut une VM d'analyse isolée) et IR-02 (Splunk BOTS v1, il faut une instance Splunk) sont encore des plans d'enquête.

## Objectif

M'entraîner à la boucle complète d'analyste sur des jeux de formation
**réels et publics** : cadrer la question, enquêter avec le bon outil, noter
les preuves, faire la correspondance ATT&CK, et écrire un rapport qu'un
manager et un analyste L2/L3 peuvent tous les deux utiliser.
(Security+ D4 — processus de réponse à incident ; D2 — indicateurs ; D5 — rapports.)

## Mise en place

| Rapport | Jeu de données | Source | Outils |
|---------|----------------|--------|--------|
| [IR-01](IR-01-malware-traffic-pcap.md) | Un exercice de formation Malware-Traffic-Analysis.net (pcap) | <https://www.malware-traffic-analysis.net/training-exercises.html> | Wireshark, tshark, Zeek (facultatif) |
| [IR-02](IR-02-splunk-bots-v1.md) | Splunk Boss of the SOC v1 | <https://github.com/splunk/botsv1> | Splunk Enterprise (essai gratuit / licence de dev) |
| [IR-03](IR-03-evtx-password-spray.md) | EVTX-ATTACK-SAMPLES — `Credential Access/kerberos_pwd_spray_4771.evtx` | <https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES> | EvtxECmd / `evtx_dump`, Observateur d'événements, Chainsaw ou Hayabusa (facultatif) |

Jeu de données en plus : **OTRF Security-Datasets** (anciennement Mordor) —
<https://github.com/OTRF/Security-Datasets> / <https://securitydatasets.com/> —
exports JSON de techniques ATT&CK simulées, faciles à charger dans Wazuh/ELK/Splunk.

- Travailler dans une VM d'analyse isolée (snapshots, pas de dossiers partagés,
  pas d'identifiants). Les zip malware-traffic sont protégés par mot de passe
  pour une raison.
- Noter le SHA256 de chaque fichier analysé (habitude de chaîne de possession).
- Chaque rapport suit [`TEMPLATE.md`](TEMPLATE.md).

> **Note d'honnêteté :** IR-01 et IR-02 sont encore des *plans d'enquête et
> des squelettes de rapport*. Leurs constats restent `TBD` tant que je n'ai
> pas analysé les données. IR-03 contient ma propre analyse de l'exemple
> public. Je ne copie ici aucune réponse prise dans les rapports d'autres
> personnes.
>
> Pourquoi IR-01 et IR-02 ne sont pas faits : les pcaps malware-traffic
> contiennent du vrai trafic malveillant, et ma règle est de les ouvrir
> seulement dans une VM d'analyse dédiée et isolée. Ma machine de lab actuelle
> n'en est pas une. BOTS v1 a besoin d'une instance Splunk avec le jeu
> d'environ 6 GB chargé.

## Étapes

1. Télécharger un jeu dans la VM d'analyse, vérifier son hash, noter l'URL et la date.
2. Copier les sections de `TEMPLATE.md` dans le rapport et suivre les étapes d'enquête.
3. Remplir les tableaux de preuves avec les requêtes, les filtres et les résultats exacts (captures d'écran dans `evidence/`).
4. Faire correspondre le comportement confirmé à ATT&CK et mettre à jour le
   [tableau de correspondance](../04-attack-mapping/).
5. Écrire le résumé exécutif **en dernier**.

## Preuves

- [IR-03](IR-03-evtx-password-spray.md) avec [`evidence/IR-03/analysis.txt`](evidence/IR-03/analysis.txt)
  (SHA256 de l'EVTX, tableau des événements, rejeu Sigma).
- IR-01, IR-02 : pas commencés (voir la note d'honnêteté).

## Ce que j'ai appris

- Un petit jeu peut quand même raconter toute l'histoire. 12 événements ont
  suffi pour voir l'énumération, le spraying et une devinette qui a marché.
- Les codes d'état Kerberos laissent fuir de l'information. `0x6` et `0x18`
  disent à un attaquant quels comptes existent.
- Ma détection a alerté sur les échecs, mais l'événement le plus important
  était le succès juste après. Un plan de détection a aussi besoin de la
  règle « qu'est-ce qui s'est passé ensuite ».
- La normalisation des données compte. Le même hôte apparaissait comme
  `172.16.66.1` et `::ffff:172.16.66.1`.
- Tout événement suspect n'appartient pas à l'attaquant (l'effacement de
  journal 1102). Écrire « noté, pas attribué » vaut mieux que d'en faire trop.
