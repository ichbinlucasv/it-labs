# Fedora day

**English** · [Français](fedora.fr.md) · [Deutsch](fedora.de.md)

I like Fedora. This is the drill for a company Linux that looks like
Red Hat: `dnf`, SELinux, firewalld. Twenty-five minutes, on a Fedora
machine or a container.

A line counts only after I ran it. If I have no Fedora guest today, I
write the command from memory and I mark it not run. I do not tick a
guess.

```bash
dnf check-update
sudo dnf upgrade
systemctl --failed
journalctl -p err -b --no-pager | head
sudo ausearch -m avc -ts recent
firewall-cmd --list-all
rpm -V bash
```

`rpm -V bash` is the shape. I swap in one package I actually use.

## Rules

- Packages come from the official repos. A random RPM from a blog post
  is how a helpdesk ticket starts.
- An SELinux denial is a log line. I read `ausearch` before I even
  think about `setenforce 0`. Turning SELinux off is not the fix I write
  down.
- I name the firewall zone before I add a port. `firewall-cmd --list-all`
  first.
- `dnf upgrade` is the whole transaction. I do not mix a half-finished
  one with a single package from somewhere else.

## After

Ran today?  yes / no. Where:

SELinux denial I can explain in one sentence, or "none":

Port or service I was tempted to open, and whether I did:
