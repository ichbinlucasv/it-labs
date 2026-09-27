# How I built the lab container

Debian 13 host, as root. The container has `--private-network`: only a
loopback interface, so services inside cannot be reached from outside and
cannot reach anything.

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

On a normal systemd host `machinectl shell lab1` replaces the `nsenter` step.

Mistake I made once: `nsenter` into the **systemd-nspawn** process instead of
the container's systemd put me in the host's namespaces, and `hostname lab1`
renamed the host. Check `pstree` first and target the child `systemd` PID.
