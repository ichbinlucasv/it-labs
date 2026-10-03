# Mes reformulations, l'exercice de priorité et des tickets tirés de mon lab

[English](my-rewrites.md) · **Français** · [Deutsch](my-rewrites.de.md)

Organisation fictive : *Exemple SARL* (40 utilisateurs, domaine `example.com`).
Toutes les personnes, les hôtes et les numéros de tickets sont inventés. La
section 3 s'appuie sur les pannes que j'ai vraiment provoquées dans
[helpdesk lab 03](../03-linux-troubleshooting/) — les commandes et les
messages d'erreur sont copiés des preuves de ce lab, seuls l'« utilisateur »
et le cadre du ticket sont fictifs.

---

## 1. Reformulations des mauvais tickets

### « internet broken »

Ce que je devrais demander d'abord : qui, quel appareil, qu'est-ce qui
échoue exactement (tous les sites ? une appli ?), depuis quand, qu'est-ce qui
a changé, quelqu'un d'autre est-il touché ?

```text
Title:      [Network] One user cannot open any website since this morning — Teams OK
Requester:  <name>, <team>, <phone/Teams>
Asset:      <hostname>, Windows 11
Category:   Network   Impact: Single user   Urgency: Degraded   Priority: P3 (see matrix)
Description:
  User reports "no internet" in the browser since ~08:40. Teams still works,
  so the link and the network are up -> suspect DNS or proxy.
Troubleshooting done:
  - [time] ipconfig /all -> <IP/GW/DNS values>
  - [time] Resolve-DnsName <internal name> -> <result>
Next action: compare DNS server with the standard; check proxy settings.
```

Comparé à la version de référence : la référence note aussi que le portable
venait d'être **mis sur la station d'accueil** (nouvel adaptateur réseau =
réglages différents). « Qu'est-ce qui a changé ? » a sa place dans la
checklist.

### « password / reset done »

```text
Title:      [Account] <user> locked out — unlocked, cause found
Requester:  <name>, <team>, contact used for callback
Category:   Account/Access   Impact: Single user   Urgency: Cannot work   Priority: P3
Identity verification: <how, per procedure>
Troubleshooting done:
  - [time] account status: locked, badPwdCount=<n>, source=<device>
  - [time] unlocked / reset (with forced change at next logon)
Resolution: root cause <...>; verified with user at <time>; KB <link>
```

Comparé à la version de référence : le réflexe est souvent de réinitialiser,
mais la référence montre que ce n'était pas nécessaire — seulement un
déverrouillage, plus le téléphone qui réessayait l'ancien mot de passe.
Déverrouiller sans trouver la source, et le compte se reverrouille 10 minutes
plus tard.

### « weird email / deleted it »

```text
Title:      [Security] Suspected phishing — link clicked? credentials entered?
Category:   Security   Impact: Single user (possibly more)   Urgency: High   Priority: P2
Description: sender, subject, time received, did the user click / type anything
Indicators (defanged): sender, URL, attachment name/hash
Actions: do NOT delete; report as attachment to security; escalate to SOC
```

Comparé à la version de référence : la référence ajoute, au L1, la
vérification des **journaux de connexion** de l'utilisateur — un contrôle
rapide qui change la priorité s'il y a une connexion suspecte.

---

## 2. Exercice de priorité (matrice impact × urgence du README du lab)

| Ticket | Impact | Urgence | Priorité | Pourquoi |
|--------|--------|---------|----------|----------|
| Ex. 1 — un PC ne navigue pas, Teams marche | Bas (un seul utilisateur, contournement existant) | Moyen (dégradé) | **P4** selon la matrice → je monterais à **P3** | Le DNS statique peut venir d'un logiciel indésirable, ce qui est une question de sécurité |
| Ex. 2 — compte verrouillé | Bas (un seul utilisateur) | Haut (ne peut pas travailler) | **P3** | Correspond à la référence |
| Ex. 3 — lien de phishing cliqué | Moyen (peut-être plus d'utilisateurs) | Haut | **P2** | D'autres boîtes ont peut-être le même message |
| Escalade — 6 utilisateurs à l'étage 2 perdent le réseau toutes les 20 min | Moyen (équipe dégradée) | Haut | **P2** | Tout l'étage est touché, contournement Wi-Fi seulement |
| 3.1 ci-dessous — serveur web intranet tombé | Haut (tout le site) | Haut | **P1** | L'activité est arrêtée pour tout le monde |
| 3.2 ci-dessous — partage du serveur de fichiers plein | Moyen (équipe) | Haut | **P2** | La comptabilité ne peut pas enregistrer de fichiers |
| 3.3 ci-dessous — un utilisateur refusé sur un partage | Bas | Moyen | **P4** | Demande d'accès, pas une panne |

Point à retenir : la matrice est un point de départ ; un aspect sécurité peut
justifier de monter la priorité, et il faut l'écrire dans le ticket.

---

## 3. Tickets écrits à partir de mes propres scénarios de lab

### 3.1 Service tombé après un changement de config (P1 — résolu)

```text
Title:      [Server] Intranet web server returns nothing — nginx fails to start after config edit
Requester:  Monitoring alert + 3 user calls (Accounting, Sales)
Asset:      lab1 (Debian 13, nginx)
Category:   Software   Impact: Whole site   Urgency: Cannot work   Priority: P1

Description:
  Intranet unreachable since 16:43. A config change was deployed a few minutes before.

Troubleshooting done:
  - 16:43 systemctl status nginx -> failed (Result: exit-code), ExecStartPre nginx -t failed
  - 16:43 journalctl -u nginx -> [emerg] invalid parameter "listen" in
          /etc/nginx/sites-enabled/default:23
  - 16:43 nginx -t -> same error; line 22 "listen 80 default_server" is missing its ";"
          (nginx reports the NEXT line)

Resolution:
  Restored previous version of sites-enabled/default, nginx -t OK,
  systemctl restart nginx -> active, HTTP 200 confirmed. Users confirmed at 16:50.
  Root cause: syntax error in change. Follow-up: run "nginx -t" before every
  reload (add to change checklist).
```

### 3.2 Disque plein sur un partage de fichiers (P2 — résolu, avec une erreur documentée)

```text
Title:      [Server] /srv/data full — users get "No space left on device"
Asset:      lab1, filesystem /srv/data (100 MB)
Category:   Hardware/Storage   Impact: Team   Urgency: Cannot work   Priority: P2

Troubleshooting done:
  - df -h /srv/data -> 100 %
  - du -xh /srv/data --max-depth=1 -> app.log = 100 MB
  - rm app.log -> df still 100 % (file deleted but still open)
  - lsof -nP +L1 -> sh (PID 171) holds /srv/data/app.log (deleted)
  - systemctl stop chatty-app -> df 0 %

Resolution:
  Space recovered after stopping the writing service. Root cause: application
  log without rotation. Next action / owner: L2 to add logrotate
  (copytruncate) and a disk-usage alert at 80 %.
Note for the team: deleting a log under a running process does not free space;
truncate it (": > file") or stop the writer first.
```

### 3.3 Accès refusé à un partage (P4 — escaladé pour approbation)

```text
Title:      [Access] alice cannot read /srv/share/finance/report.txt
Requester:  alice (Sales)
Category:   Account/Access   Impact: Single user   Urgency: Degraded   Priority: P4

Troubleshooting done:
  - namei -l -> blocked at "drwxr-x--- root finance finance"
  - id alice -> not in group "finance"

Next action / owner:
  Access to Finance data needs approval from the data owner (Finance manager).
  Request sent. Options once approved: add alice to "finance" (read only,
  file is 640) or a per-user read ACL. No chmod 777.
```

### 3.4 Note d'escalade (L1 → L2) pour un problème que je n'ai pas pu corriger moi-même

Écrit à partir du scénario 6 du lab 03, où je n'ai pas pu tester la limite
mémoire dans mon environnement :

```text
Escalating to L2 Linux.
Summary: A batch job on lab1 was supposed to be limited to 64 MB
         (systemd-run -p MemoryMax=64M) but allocated 500 MB without being stopped.
Done:    Reproduced twice; journal shows the job finished normally (no OOM kill).
         /sys/fs/cgroup/cgroup.controllers is empty -> the memory controller
         is not available to systemd on this host.
Hypothesis: cgroup v2 memory controller not delegated (container / kernel setup),
         so MemoryMax is silently ignored.
Impact:  No outage now; risk that a runaway job exhausts host memory.
Ask:     Confirm cgroup delegation on the host, or move the job to a VM.
```

### 3.5 Note de clôture

```text
Closing ticket 3.2.
Root cause: app.log in /srv/data grew without rotation until the 100 MB
filesystem was full.
Fix: writing service stopped and file removed; space back to 0 % used.
Verified: user saved a file successfully at 16:50.
Prevention: logrotate + 80 % disk alert handed to L2 (linked change request).
KB: "Disk full but du shows nothing — deleted files held open (lsof +L1)".
```
