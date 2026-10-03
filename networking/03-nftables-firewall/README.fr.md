# Lab 03 — Pare-feu hôte avec nftables

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — syntaxe contrôlée, puis trafic testé avec trois network namespaces qui tiennent lieu du serveur, d'un client admin et d'un client extérieur ([`netns-test.sh`](netns-test.sh), sortie dans [`evidence/`](evidence/)) ; pas encore rendu persistant sur une vraie VM avec `nftables.service`.

## Objectif

Écrire un pare-feu hôte en refus par défaut pour un serveur Linux avec
nftables : filtrage à état, SSH limité à un sous-réseau admin avec limitation
de débit, ports web publics, ICMP et ICMPv6 indispensables, un ensemble de
liste de blocage, et de la journalisation.
(Security+ D3 — conception réseau sûre ; D2 — atténuation / durcissement.)

## Mise en place

- VM Debian 12 / Ubuntu 24.04 avec **accès console** (au cas où je me coupe
  l'accès SSH), `sudo apt install nftables`.
- Le LAN du lab `10.20.30.0/24` est le sous-réseau admin. La liste de blocage
  utilise des adresses RFC 5737 comme exemples.
- Jeu de règles : [`ruleset.nft`](ruleset.nft).

## Étapes

1. **Lire** le jeu de règles et prédire ce qui arrive à : SSH depuis
   `10.20.30.5`, SSH depuis `192.0.2.10`, HTTPS de n'importe où, ping, trafic
   depuis `198.51.100.66`.
2. **Contrôler la syntaxe sans appliquer** (le fichier est lu et validé
   contre le noyau, mais aucune règle n'est installée) :

   ```bash
   sudo nft -c -f ruleset.nft && echo "syntax OK"
   ```

3. **Tester sans risque** — soit dans un network namespace jetable :

   ```bash
   sudo ip netns add fwtest
   sudo ip netns exec fwtest nft -f ruleset.nft
   sudo ip netns exec fwtest nft list ruleset
   sudo ip netns del fwtest
   ```

   soit sur la VM, avec un retour arrière automatique si je me bloque :

   ```bash
   sudo nft list ruleset > /root/nft-backup.nft
   sudo nft -f ruleset.nft
   # if SSH still works, cancel the rollback (Ctrl-C); otherwise it restores:
   sleep 120 && sudo nft -f /root/nft-backup.nft
   ```

4. **Rendre persistant** : copier vers `/etc/nftables.conf`,
   `sudo systemctl enable --now nftables`.
5. **Vérifier** depuis une autre VM du lab : `nc -zv 10.20.30.10 22` /
   `curl -I http://10.20.30.10` et regarder les compteurs et les journaux :

   ```bash
   sudo nft list chain inet lab_filter input      # counters
   sudo journalctl -k -g 'nft-in-' -f             # log prefixes
   ```

6. **Gérer la liste de blocage à chaud** (pas besoin de recharger) :

   ```bash
   sudo nft add element inet lab_filter blocklist_v4 '{ 203.0.113.99 }'
   sudo nft list set inet lab_filter blocklist_v4
   ```

### Vérification faite

Je n'avais pas deux VM, donc j'ai utilisé des network namespaces. Chaque
namespace a ses propres interfaces, ses routes et son jeu de règles nftables.
Ça suffit pour tester ce qu'un pare-feu laisse passer.
[`netns-test.sh`](netns-test.sh) construit ça, lance les tests sans le jeu de
règles puis avec, et nettoie :

```text
admin   10.20.30.5      --veth--  fw  10.20.30.10  (server under test, fake services on 22/80/443)
outside 192.0.2.10      --veth--  fw  192.0.2.1 / 198.51.100.1
        198.51.100.66   (in the blocklist)
```

```bash
sudo sysctl -w net.netfilter.nf_log_all_netns=1   # allow log lines from non-host namespaces
sudo ./netns-test.sh
sudo dmesg | grep nft-                              # log prefixes
sudo sysctl -w net.netfilter.nf_log_all_netns=0
```

Résultats ([sortie complète](evidence/netns-test.txt), nftables v1.1.3) :

| Test | Sans jeu de règles | Avec jeu de règles | Conforme à la prédiction ? |
|------|--------------------|--------------------|----------------------------|
| SSH depuis l'admin `10.20.30.5` | ouvert | ouvert | oui |
| SSH depuis `192.0.2.10` | ouvert | **bloqué**, journalisé `nft-in-ssh-denied` | oui |
| HTTP/HTTPS depuis `192.0.2.10` | ouvert | ouvert | oui |
| TCP 3306 depuis `192.0.2.10` | refusé (pas de service) | **bloqué** en silence, journalisé `nft-in-drop` | oui |
| N'importe quoi depuis `198.51.100.66` | ouvert | **bloqué**, journalisé `nft-in-blocklist` | oui |
| Ping depuis `192.0.2.10` | réponse | réponse (acceptation limitée en débit) | oui |
| 20 connexions SSH d'affilée depuis l'admin | — | 8 ouvertes, 12 bloquées | oui (burst 5 + refill) |
| Ajouter `192.0.2.10` à la liste de blocage à chaud | — | 443 bloqué ; de nouveau ouvert après l'avoir retiré | oui |
| Serveur → `198.51.100.66:443` | — | bloqué par la chaîne output | oui |

À noter, la différence entre **refusé** (RST : le port est fermé mais l'hôte
répond) et **bloqué** (aucune réponse : le pare-feu jette le paquet). Un
scanner voit le premier comme `closed` et le second comme `filtered`.

**Problème trouvé et corrigé.** Au premier passage, les 12 tentatives SSH
limitées en débit depuis le sous-réseau *admin* tombaient dans la règle
générique et étaient journalisées `nft-in-ssh-denied`. Le même préfixe qu'un
extérieur qui tente le SSH. Pendant une enquête, ça ressemblerait à une
attaque depuis l'intérieur du réseau admin. J'ai ajouté deux règles pour que
les connexions admin au-dessus de la limite aient leur propre préfixe
`nft-in-ssh-ratelimit` (la ligne de journal est limitée en débit, le drop
s'applique toujours). Deuxième passage, résumé du journal noyau
([preuves](evidence/kernel-log-summary.txt), adresses MAC masquées) :

```text
      8 nft-in-ssh-ratelimit: IN=veth-adm ... SRC=10.20.30.5 DST=10.20.30.10 PROTO=TCP DPT=22
      2 nft-out-blocklist: IN= OUT=veth-out SRC=198.51.100.1 DST=198.51.100.66 PROTO=TCP DPT=443
      2 nft-in-ssh-denied: IN=veth-out ... SRC=192.0.2.10 DST=10.20.30.10 PROTO=TCP DPT=22
      2 nft-in-drop: IN=veth-out ... SRC=192.0.2.10 DST=10.20.30.10 PROTO=TCP DPT=3306
      2 nft-in-blocklist: IN=veth-out ... SRC=198.51.100.66 DST=10.20.30.10 PROTO=TCP DPT=443
```

(Chaque connexion bloquée apparaît deux fois, parce que le client
retransmet son SYN après 1 s. Le compteur de drop montrait 24 paquets pour
les 12 tentatives, mais seulement 8 lignes de journal. La limitation de débit
propre à l'instruction de log a marché.)

Pas fait ici : l'étape 4 (rendre persistant avec `nftables.service` sur une
VM) et un vrai démon SSH derrière les règles. Les faux services ne font
qu'accepter et fermer.

### Notes de conception

- `policy drop` sur input et forward ; output autorisé (une politique de
  sortie plus stricte est une bonne suite).
- `ct state invalid drop` avant tout le reste ; established/related tôt, pour
  la performance.
- La journalisation est limitée en débit, pour qu'un attaquant ne puisse pas
  remplir le disque avec des lignes de journal.
- `flush ruleset` efface les règles des autres outils (Docker, libvirt). Sur
  ces hôtes, utiliser une table dédiée et `destroy table` / `delete table`
  à la place.

## Preuves

- [`evidence/netns-test.txt`](evidence/netns-test.txt) : résultat de
  `nft -c -f`, matrice de tests sans le jeu de règles et avec, tests de
  limitation de débit et de liste de blocage à chaud, et les règles dont les
  compteurs ont augmenté.
- [`evidence/kernel-log-summary.txt`](evidence/kernel-log-summary.txt) : lignes
  `dmesg` avec les préfixes `nft-*`, comptées (adresses MAC masquées).

## Ce que j'ai appris

- Je prédis d'abord, je teste ensuite. Écrire le résultat attendu pour chaque
  cas avant de lancer le script a rendu la seule surprise évidente (le préfixe
  de journal trompeur).
- L'ordre compte dans une chaîne. Un paquet qui ne matche pas une règle
  `limit ... accept` continue simplement à la règle suivante. Ici il tombait
  dans la règle « denied ».
- « Refusé » et « bloqué » sont deux réponses différentes. Elles ne disent
  pas la même chose à un analyste.
- La journalisation a besoin de sa propre limitation de débit. Sinon un
  attaquant peut remplir le disque.
- Les network namespaces sont un moyen pas cher de tester un jeu de règles
  sans risquer de se couper l'accès à un serveur distant. `nft -c` ne prouve
  que la syntaxe, pas le comportement.
