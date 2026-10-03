# Arch-Tag — CachyOS

[English](arch.md) · [Français](arch.fr.md) · **Deutsch**

Das ist der Rechner, den ich jeden Tag benutze. CachyOS ist Arch.
Fünfundzwanzig Minuten. Ich führe die Befehle aus. Ich schreibe eine
Zeile dazu, was fehlgeschlagen ist, oder was ich aus dem Gedächtnis
nicht konnte.

```bash
pacman -Qu
sudo pacman -Syu
sudo find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) -print
systemctl --failed
journalctl -p err -b --no-pager | head
```

## Regeln

- Ein volles `pacman -Syu`. Ich mache nicht `pacman -Sy` und installiere
  später ein einzelnes Paket. Das ist ein teilweises Upgrade.
- Eine `.pacnew`-Datei ist eine Frage, keine Datei, die ich über die
  laufende kopiere.
- Wenn das Upgrade das Netz kaputt macht, repariere ich den Mirror oder
  das Paket, das sich gerade geändert hat. Ich installiere nicht zuerst
  das ganze System neu.
- `systemctl --failed`, bevor ich entscheide, ein Dienst sei «einfach Arch».

## Danach

Was ich aus dem Gedächtnis nicht konnte:

Was noch fehlgeschlagen ist, und der Unit-Name:
