# Journée Fedora

[English](fedora.md) · **Français** · [Deutsch](fedora.de.md)

J'aime Fedora. Cette fiche, c'est l'entraînement pour un Linux
d'entreprise qui ressemble à Red Hat : `dnf`, SELinux, firewalld.
Vingt-cinq minutes, sur une machine Fedora ou un conteneur.

Une ligne compte seulement après que je l'ai lancée. Si je n'ai pas
d'invité Fedora aujourd'hui, j'écris la commande de mémoire et je marque
qu'elle n'a pas tourné. Je ne coche pas une supposition.

```bash
dnf check-update
sudo dnf upgrade
systemctl --failed
journalctl -p err -b --no-pager | head
sudo ausearch -m avc -ts recent
firewall-cmd --list-all
rpm -V bash
```

`rpm -V bash` est la forme. Je remplace par un paquet que j'utilise vraiment.

## Règles

- Les paquets viennent des dépôts officiels. Un RPM au hasard, pris
  dans un billet de blog, c'est comme ça qu'un ticket helpdesk commence.
- Un refus SELinux est une ligne de journal. Je lis `ausearch` avant
  même de penser à `setenforce 0`. Couper SELinux n'est pas le correctif
  que j'écris.
- Je nomme la zone du pare-feu avant d'ajouter un port.
  `firewall-cmd --list-all` d'abord.
- `dnf upgrade` est toute la transaction. Je ne mélange pas une
  transaction à moitié finie avec un paquet venu d'ailleurs.

## Après

Lancé aujourd'hui ?  oui / non. Où :

Un refus SELinux que je peux expliquer en une phrase, ou « aucun » :

Port ou service que j'étais tenté d'ouvrir, et si je l'ai fait :
