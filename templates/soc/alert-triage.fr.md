# Une alerte

[English](alert-triage.md) · **Français** · [Deutsch](alert-triage.de.md)

Une alerte par fiche. UTC. Je réponds à partir du journal avant d'ouvrir un
deuxième outil.

```text
Nom de l'alerte / règle :
ID :
Arrivée (UTC) :
Équipement :
Utilisateur :
Gravité dans l'outil :

Ce que la règle croit qu'il s'est passé (une phrase) :

Premier événement que j'ai ouvert (ID, heure UTC) :
Processus parent, si c'est un endpoint :
Type d'ouverture de session, si c'est une ouverture :

Déjà vu sur cet équipement ?  inconnu / oui, ticket / non

Raison bénigne que je peux nommer :
    [ ] outil d'admin qu'on utilise
    [ ] fenêtre de correctifs / sauvegarde
    [ ] l'utilisateur l'a fait
    [ ] je ne peux pas en nommer

Décision :
    [ ] clôturer, raison :
    [ ] surveiller, ce qui me ferait changer d'avis :
    [ ] escalader, avec la fiche chronologie

Ce que je n'ai pas fait : exécuter le fichier, cliquer le lien, ou essayer le mot de passe.
```

Je m'entraîne sur les journaux synthétiques dans
[soc-analyst/02](../../soc-analyst/02-sysmon-auditd-logs/) ou sur IR-03.
Une fiche sans ID d'événement ne compte pas.
