# Lab 03 — Procédure de dépannage Linux

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — j'ai cassé et réparé les scénarios 1 à 5 et 7 dans un conteneur systemd Debian 13, et j'ai gardé la sortie du terminal dans [`evidence/`](evidence/) ; le scénario 6 seulement en partie (le kill OOM n'a pas pu être reproduit ici, voir plus bas).

## Objectif

Une procédure concrète pour les pannes courantes d'un serveur ou d'un poste
Linux sous Debian/Ubuntu. Le point, c'est de lire les journaux et de vérifier
chaque hypothèse. Et de montrer que je l'ai vraiment fait.

## Mise en place

- Prévu : une VM Debian 12 / Ubuntu 24.04 avec des snapshots.
- **Ce que j'ai utilisé :** un système de fichiers racine Debian 13 (trixie)
  construit avec `debootstrap` et démarré avec
  `systemd-nspawn --boot --private-network`. systemd, journald, nginx et sshd
  tournent pour de vrai, mais le conteneur n'a qu'une interface loopback
  (rien n'atteint mon réseau). Les commandes exactes sont dans
  [`lab-container.md`](lab-container.md).
- Nom d'hôte dans le conteneur : `lab1`. Les utilisateurs `alice` et `bob` et
  le groupe `finance` sont des comptes de lab. Les adresses du scénario DNS
  sont des plages de documentation / de lab (`192.0.2.53`, `10.20.30.20`).
- Chaque scénario : casser exprès → voir le symptôme comme un utilisateur →
  diagnostiquer avec les commandes ci-dessous → réparer → vérifier.

## Étapes

### 0. Les cinq premières commandes sur n'importe quelle machine

```bash
uptime                     # load, how long since reboot
df -h; df -i               # disk space AND inodes
free -h                    # memory / swap
systemctl --failed         # failed units
journalctl -p err -b       # errors since boot
```

Dans un conteneur, `uptime`, `free` et `df /` montrent les valeurs de
l'**hôte** (noyau partagé et système de fichiers overlay). À savoir avant
d'en tirer une conclusion. Sortie :
[`evidence/0-first-five-commands.txt`](evidence/0-first-five-commands.txt).

### 1. Un service ne démarre pas

```bash
systemctl status nginx
journalctl -u nginx -n 50 --no-pager
sudo nginx -t              # config syntax test (most daemons have one)
ss -tlnp | grep ':80'      # port already in use?
```

*Comment je l'ai cassé :* j'ai retiré le `;` à la fin de
`listen 80 default_server` dans `/etc/nginx/sites-enabled/default`.

Ce que j'ai vu ([preuves](evidence/1-service-wont-start.txt)) :

```text
$ nginx -t
[emerg] 104#104: invalid parameter "listen" in /etc/nginx/sites-enabled/default:23
nginx: configuration file /etc/nginx/nginx.conf test failed
$ sed -n 22,23p /etc/nginx/sites-enabled/default
	listen 80 default_server
	listen [::]:80 default_server;
```

L'erreur pointe la **ligne 23**, mais la faute est à la **ligne 22**. Sans
le point-virgule, nginx lit les deux lignes comme une seule directive. Il ne
se plaint qu'en arrivant au second `listen`. Leçon : quand un analyseur
annonce la ligne N, je regarde aussi la ligne N-1. Après avoir restauré le
fichier : `nginx -t` OK, service `active`, HTTP 200 sur `127.0.0.1`.

*Deuxième casse — port déjà pris :* j'ai lancé un serveur web Python sur le
port 80 comme unité transitoire, puis j'ai démarré nginx. Le journal disait
`bind() to 0.0.0.0:80 failed (98: Address already in use)` et `ss -tlnp`
montrait `users:(("python3",pid=135,fd=3))` sur `:80`. Le nom du processus
et le PID disent exactement quoi arrêter.

### 2. Disque plein

```bash
df -h /
sudo du -xh / --max-depth=1 2>/dev/null | sort -h | tail
sudo journalctl --disk-usage
sudo journalctl --vacuum-size=200M
sudo lsof +L1              # deleted files still held open by a process
```

*Comment je l'ai cassé :* au lieu de remplir le vrai disque, j'ai monté un
tmpfs de 100 MB sur `/srv/data` et j'ai lancé un service qui écrit en continu
dans `/srv/data/app.log`.

Ce que j'ai vu ([preuves](evidence/2-disk-full.txt)) : `echo: write error: No
space left on device`, `df` à 100 %, `du` qui désigne les 100 MB de
`app.log`. Ensuite j'ai fait exprès l'erreur classique : `rm app.log`. `df`
**est resté à 100 %**, parce que le processus avait encore le fichier ouvert :

```text
$ lsof -nP +L1
COMMAND PID USER FD   TYPE DEVICE  SIZE/OFF NLINK NODE NAME
sh      171 root 3w   REG   0,62 104857600     0    2 /srv/data/app.log (deleted)
```

L'espace n'est revenu qu'après `systemctl stop chatty-app`. Le bon correctif
sur un vrai serveur : trouver celui qui écrit, puis tronquer (`: > app.log`)
ou faire tourner le journal avec logrotate. Pas supprimer le fichier sous un
processus encore lancé.

### 3. DNS / réseau

```bash
ip -br addr; ip route
ping -c3 10.20.30.1
resolvectl status          # or cat /etc/resolv.conf
dig example.com +short
dig @10.20.30.10 example.com
curl -I https://example.com
```

*Comment je l'ai cassé :* j'ai lancé `dnsmasq` sur `127.0.0.1` comme « DNS
de l'entreprise » (il répond `intranet.lab.example → 10.20.30.20`) et j'ai
mis un mauvais résolveur statique, `nameserver 192.0.2.53`, dans
`/etc/resolv.conf`. C'est la version Linux de l'exemple de ticket 1 dans le
[lab 01](../01-ticket-writing/examples.md).

Ce que j'ai vu ([preuves](evidence/3-dns.txt)) :

```text
$ getent hosts intranet.lab.example; echo exit=$?
exit=2
$ dig +time=2 +tries=1 intranet.lab.example
;; UDP setup with 192.0.2.53#53(192.0.2.53) for intranet.lab.example failed: network unreachable.
$ dig @127.0.0.1 intranet.lab.example +short
10.20.30.20
```

Demander directement au bon serveur marche. Demander à celui qui est
configuré échoue. Le problème est donc la config du résolveur, pas le nom.
Après `nameserver 127.0.0.1`, `getent` et `dig` renvoient tous les deux
`10.20.30.20`. (Dans le conteneur il n'y a aucune route, donc dig dit
`network unreachable`. Sur un vrai LAN, la même erreur se voit en général
comme un timeout.) Note : `dig nosuchhost.intranet.lab.example` a renvoyé
`NOERROR`, parce que `address=/domain/` de dnsmasq répond aussi pour chaque
sous-domaine.

### 4. Permission refusée

```bash
ls -l /srv/share/report.txt
namei -l /srv/share/report.txt     # permissions of every path component
id alice                            # groups
getfacl /srv/share                  # ACLs
```

*Comment je l'ai cassé :* `/srv/share/finance` est `root:finance 750`, le
rapport est `640`, et `alice` n'est pas dans `finance`.

Ce que j'ai vu ([preuves](evidence/4-permission-denied.txt)) : `namei -l` a
montré tout de suite le maillon qui bloque
(`drwxr-x--- root finance finance`), et `id alice` ne montrait pas le groupe
`finance`. Deux correctifs de moindre privilège, les deux testés :

- `usermod -aG finance alice` → alice peut lire, mais **toujours pas écrire**
  (le fichier est `640`). C'est bien ce que le groupe doit permettre.
- Pour une seule personne : `setfacl -m u:alice:rx` sur le répertoire et
  `u:alice:r` sur le fichier → lecture sans toucher au groupe.

Jamais `chmod 777`. Note : un nouveau groupe ne s'applique qu'aux
**nouvelles** sessions (`su - alice` en ouvre une ; l'utilisateur doit se
déconnecter et se reconnecter).

### 5. Problèmes de connexion SSH

```bash
sudo journalctl -u ssh -n 50        # "ssh" on Debian/Ubuntu, "sshd" on RHEL
sudo grep 'Failed password' /var/log/auth.log | tail
sudo sshd -t                        # config syntax
ls -ld ~/.ssh; ls -l ~/.ssh/authorized_keys   # 700 / 600 required
```

*Premier essai de casse :* `chmod 664 ~/.ssh/authorized_keys`. La connexion
par clé **marchait encore**. OpenSSH tolère l'écriture par le groupe quand
ce groupe est le groupe privé de l'utilisateur (`alice:alice`). Cette casse
n'a donc pas reproduit le problème. Je l'ai notée, je ne l'ai pas cachée.

*Deuxième casse :* `chmod 777 /home/alice`. Ensuite
([preuves](evidence/5-ssh-login.txt)) :

```text
alice@127.0.0.1: Permission denied (publickey,password).
$ journalctl -u ssh ... | grep -i modes
Authentication refused: bad ownership or modes for directory /home/alice
```

`sshd -t` était OK (la config va bien). `namei -l` sur `authorized_keys`
montrait `drwxrwxrwx alice alice alice`. Après `chmod 755 /home/alice`, la
connexion remarchait. L'utilisateur ne voit que `Permission denied`. La vraie
raison est seulement dans le journal du **serveur**.

### 6. CPU ou mémoire élevés

```bash
top -o %CPU          # or htop
ps aux --sort=-%mem | head
dmesg -T | grep -i 'out of memory'
```

*CPU :* une unité transitoire qui lance `yes > /dev/null` était à 100 % de
CPU dans `top` et `ps --sort=-%cpu`. `systemctl status runaway-job` nommait
l'unité qui le possède. Arrêter l'unité a corrigé le problème
([preuves](evidence/6-cpu-memory.txt)).

*Mémoire — pas reproduit :* j'ai lancé un job Python avec
`systemd-run -p MemoryMax=64M` qui alloue 500 MB. Il **n'a pas été tué**.
`/sys/fs/cgroup/cgroup.controllers` est vide dans ce conteneur, donc le
contrôleur mémoire n'est pas délégué et la limite est ignorée sans message.
La partie kill OOM (`dmesg` / journal `Out of memory: Killed process`)
demande une VM.

### 7. Problèmes de paquets

```bash
sudo apt update
sudo apt --fix-broken install
sudo dpkg --configure -a
```

*Comment je l'ai cassé :* j'ai construit un petit `.deb` (`lab-tool`) qui
dépend d'un paquet qui n'existe pas, et je l'ai installé avec `dpkg -i`.

Ce que j'ai vu ([preuves](evidence/7-packages.txt)) : `dependency problems -
leaving unconfigured`, état `iU` dans `dpkg -l` (installé, dépaqueté, pas
configuré), puis **chaque** `apt-get install` a refusé de tourner
(`Unmet dependencies. Try 'apt --fix-broken install'`).
`apt-get --fix-broken install` a retiré `lab-tool`. `dpkg --audit` est
revenu propre. Leçon : un seul paquet cassé bloque toutes les installations.
Je corrige celui-là d'abord.

## Preuves

- [`evidence/`](evidence/) — sortie terminal de chaque scénario, cassé → réparé
  (ID d'invocation des unités retirés, rien d'autre modifié).
- Cause dans le journal pour le scénario 1 : `invalid parameter "listen" in
  /etc/nginx/sites-enabled/default:23` et `bind() to 0.0.0.0:80 failed (98:
  Address already in use)`.
- Pas capturé : kill OOM (voir le scénario 6).

## Ce que j'ai appris

- Je lis d'abord le journal du service et le test de config (`journalctl -u`,
  `nginx -t`, `sshd -t`), avant de changer quoi que ce soit. L'erreur vue par
  l'utilisateur (`Job failed`, `Permission denied`) contient rarement la raison.
- Le numéro de ligne d'un analyseur peut être la ligne juste après la vraie faute.
- Supprimer un gros journal ne libère pas l'espace tant qu'un processus le
  garde ouvert. `lsof +L1` le trouve.
- `namei -l` répond à « quel répertoire me bloque ? » en une commande.
- Certaines casses ne cassent pas. OpenSSH a accepté un `authorized_keys`
  inscriptible par le groupe, avec un groupe privé. Tester l'hypothèse vaut
  mieux que la répéter.
- Les conteneurs partagent le noyau de l'hôte. Les chiffres de ressources et
  les limites cgroup peuvent se comporter autrement que sur une VM. Je note
  donc où mon environnement diffère.
