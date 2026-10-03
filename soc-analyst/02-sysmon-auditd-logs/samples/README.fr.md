# ⚠️ Journaux d'exemple SYNTHÉTIQUES

[English](README.md) · **Français** · [Deutsch](README.de.md)

Chaque fichier de ce dossier a été **produit à la main ou par script pour
l'entraînement**. Ils ne viennent pas d'un incident réel ni d'une organisation
réelle.

- Noms d'hôtes, utilisateurs, domaines et IP sont fictifs (`example.com`,
  `example.net`, adresses RFC 5737, LAN de lab RFC 1918).
- Les hashes sont des marqueurs (`000…0001`) — ils n'identifient aucun fichier réel.
- Le « PowerShell encodé » se décode en `Write-Output 'SYNTHETIC LAB EVENT - harmless'`.
- Chaque événement JSON porte `"_synthetic": true`.

| Fichier | Format | Contenu |
|---------|--------|---------|
| `sysmon.synthetic.jsonl` | lignes JSON, noms de champs Sysmon | Poste `WS-COMPTA-07` : document macro → PowerShell → téléchargement → persistance par clé Run → beaconing → découverte (+ bruit bénin) |
| `security-4625.synthetic.jsonl` | lignes JSON, noms de champs Windows Security | Ouvertures de session échouées (4625) contre `SRV-FILES-01` depuis une adresse externe, plus des fautes de frappe normales |
| `auditd.synthetic.log` | format brut de journal d'audit Linux | Serveur `web01` : devinette de mots de passe SSH → connexion en tant que `deploy` → téléchargement vers `/tmp` → exécution → crontab → lecture de `/etc/shadow` refusée |
