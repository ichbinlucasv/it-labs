# bash

[English](bash.md) · **Français** · [Deutsch](bash.de.md)

Je m'en sers pour l'hôte Linux, tous les jours. Paquets, services, disques,
« pourquoi SSH échoue », un coup d'œil sur un log.

## 25 minutes

1. 10 min. Je tape le bloc ci-dessous de mémoire. `man` seulement après.
2. 10 min. Je casse une chose dans le conteneur du lab
   [helpdesk/03](../../helpdesk/03-linux-troubleshooting/) et j'écris la
   commande qui l'a montrée.
3. 5 min. Une ligne sur la fiche du jour : l'option que j'ai oubliée.

## Je les retape jusqu'à ce que ça tienne

```bash
systemctl status ssh --no-pager
journalctl -u ssh -S today --no-pager
ss -lntup
df -hT
ip -br addr
ip route
getent hosts example.com
id
find /var/log -type f -mtime -1 -printf '%TY-%Tm-%Td %p\n'
```

Une ligne de log, pas tout le fichier :

```bash
journalctl -u ssh --since "1 hour ago" --no-pager | tail -n 40
grep -E 'Failed|Accepted' /var/log/auth.log | tail
```

Debian et Fedora n'utilisent pas le même chemin de log. Si le fichier
manque, je le dis. Je n'invente pas de lignes.

## Exercice

Sur papier, j'écris ce que `ss -lntup` me dit sur un port à l'écoute :
programme, utilisateur, adresse, port. Puis je le lance et je marque ce que
j'ai mal lu.

## Je mélange encore

- `ss` et `netstat`
- `--since` sur journalctl, contre `tail -f` quand il me faut l'historique
- lancer un correctif en root avant d'avoir lu l'erreur
