# Wie ich den Lab-Container gebaut habe

[English](lab-container.md) · [Français](lab-container.fr.md) · **Deutsch**

Debian-13-Host, als root. Der Container hat `--private-network`: nur ein
Loopback-Interface, deshalb sind Dienste darin von außen nicht erreichbar
und kommen selbst nirgends hin.

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

Auf einem normalen systemd-Host ersetzt `machinectl shell lab1` den
`nsenter`-Schritt.

Fehler, den ich einmal gemacht habe: `nsenter` in den Prozess
**systemd-nspawn** statt in das systemd des Containers hat mich in die
Namespaces des Hosts gesetzt, und `hostname lab1` hat den Host umbenannt.
Zuerst `pstree` prüfen und die PID des Kind-`systemd` nehmen.
