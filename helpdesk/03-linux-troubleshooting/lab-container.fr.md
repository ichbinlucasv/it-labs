# Comment j'ai construit le conteneur du lab

[English](lab-container.md) · **Français** · [Deutsch](lab-container.de.md)

Hôte Debian 13, en root. Le conteneur a `--private-network` : seulement une
interface de loopback, donc les services dedans ne sont pas joignables depuis
l'extérieur et ne peuvent rien joindre.

```bash
sudo apt install debootstrap systemd-container
sudo debootstrap --variant=minbase \
  --include=systemd,systemd-sysv,dbus,nginx-light,procps,iproute2,iputils-ping,bind9-dnsutils,lsof,acl,sudo,openssh-server,less,psmisc,util-linux \
  trixie /var/lib/machines/lab1 http://deb.debian.org/debian

# extra tools, installed from the host into the root filesystem
sudo chroot /var/lib/machines/lab1 apt-get install -y dnsmasq-base python3-minimal openssh-client dpkg-dev

# boot it (my host has no systemd as PID 1, hence --register=no --keep-unit)
sudo systemd-nspawn -D /var/lib/machines/lab1 --boot --private-network --register=no --keep-unit

# open a root shell in the running container from another terminal
# (<PID> = the container's systemd, e.g. from `pstree -p $(pgrep systemd-nspawn)`)
sudo nsenter -t <PID> -a /bin/bash
echo lab1 > /etc/hostname; hostname lab1
```

Sur un hôte systemd normal, `machinectl shell lab1` remplace l'étape `nsenter`.

Erreur que j'ai faite une fois : un `nsenter` dans le processus
**systemd-nspawn** au lieu du systemd du conteneur m'a mis dans les
namespaces de l'hôte, et `hostname lab1` a renommé l'hôte. Je regarde
`pstree` d'abord et je vise le PID du `systemd` enfant.
