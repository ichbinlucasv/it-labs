# Fedora-Tag

[English](fedora.md) · [Français](fedora.fr.md) · **Deutsch**

Ich mag Fedora. Dieses Blatt ist die Übung für ein Firmen-Linux, das
wie Red Hat aussieht: `dnf`, SELinux, firewalld. Fünfundzwanzig
Minuten, auf einer Fedora-Maschine oder in einem Container.

Eine Zeile zählt erst, nachdem ich sie ausgeführt habe. Wenn heute kein
Fedora-Gast da ist, schreibe ich den Befehl aus dem Gedächtnis und
markiere ihn als nicht gelaufen. Eine Vermutung hake ich nicht ab.

```bash
dnf check-update
sudo dnf upgrade
systemctl --failed
journalctl -p err -b --no-pager | head
sudo ausearch -m avc -ts recent
firewall-cmd --list-all
rpm -V bash
```

`rpm -V bash` ist die Form. Ich tausche ein Paket ein, das ich wirklich benutze.

## Regeln

- Pakete kommen aus den offiziellen Repos. Ein zufälliges RPM aus einem
  Blog ist der Anfang eines Helpdesk-Tickets.
- Eine SELinux-Ablehnung ist eine Logzeile. Ich lese `ausearch`, bevor
  ich überhaupt an `setenforce 0` denke. SELinux abzuschalten ist nicht
  der Fix, den ich aufschreibe.
- Ich nenne die Firewall-Zone, bevor ich einen Port öffne.
  Zuerst `firewall-cmd --list-all`.
- `dnf upgrade` ist die ganze Transaktion. Ich mische keine halb
  fertige Transaktion mit einem Paket von anderswo.

## Danach

Heute gelaufen?  ja / nein. Wo:

Eine SELinux-Ablehnung, die ich in einem Satz erklären kann, oder «keine»:

Port oder Dienst, den ich öffnen wollte, und ob ich es getan habe:
