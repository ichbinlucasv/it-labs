# Journée Arch — CachyOS

[English](arch.md) · **Français** · [Deutsch](arch.de.md)

C'est la machine que j'utilise tous les jours. CachyOS, c'est Arch.
Vingt-cinq minutes. Je lance les commandes. J'écris une ligne sur ce
qui a échoué, ou sur ce que je n'ai pas su refaire de mémoire.

```bash
pacman -Qu
sudo pacman -Syu
sudo find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) -print
systemctl --failed
journalctl -p err -b --no-pager | head
```

## Règles

- Un `pacman -Syu` complet. Je ne fais pas `pacman -Sy` pour installer
  un seul paquet plus tard. Ça, c'est une mise à jour partielle.
- Un fichier `.pacnew` est une question, pas un fichier à copier sur
  celui qui tourne.
- Si la mise à jour coupe le réseau, je corrige le miroir ou le paquet
  qui vient de changer. Je ne réinstalle pas tout le système d'abord.
- `systemctl --failed` avant de décider qu'un service « c'est juste Arch ».

## Après

Ce que je n'ai pas su faire de mémoire :

Ce qui est encore en échec, et le nom de l'unité :
