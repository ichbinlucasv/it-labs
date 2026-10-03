# Arch day — CachyOS

**English** · [Français](arch.fr.md) · [Deutsch](arch.de.md)

This is the machine I use every day. CachyOS is Arch. Twenty-five
minutes. I run the commands. I write one line on what failed, or on
what I could not remember.

```bash
pacman -Qu
sudo pacman -Syu
sudo find /etc \( -name '*.pacnew' -o -name '*.pacsave' \) -print
systemctl --failed
journalctl -p err -b --no-pager | head
```

## Rules

- One full `pacman -Syu`. I do not run `pacman -Sy` and then install a
  single package later. That is a partial upgrade.
- A `.pacnew` file is a question, not a file to copy over the live one.
- If the upgrade breaks the network, I fix the mirror or the package
  that just changed. I do not reinstall the whole system first.
- `systemctl --failed` before I decide a service is "just Arch being Arch".

## After

What I could not do from memory:

What is still failed, and the unit name:
