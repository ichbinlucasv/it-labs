# How I work

**English** · [Français](how-i-work.fr.md) · [Deutsch](how-i-work.de.md)

This page is for someone who opens the repo and wants to know what I
actually use. The labs are the proof. This page is the context.

## Daily machine

I use CachyOS every day. CachyOS is Arch Linux, with its own kernel and
repositories. I installed it, I update it, and I repair it myself. The
disk is encrypted.

Fedora is the other distro I like. A helpdesk seat often sees the Red
Hat family, so I practise `dnf`, SELinux, and firewalld on purpose.
There is no Fedora lab marked Done here. Debian is the one I already
ran, in the containers for Samba and the Linux break/fix lab. The two
sheets are [templates/linux/arch.md](templates/linux/arch.md) and
[templates/linux/fedora.md](templates/linux/fedora.md).

Rules I follow:

- Arch: one full `pacman -Syu`. I do not partial-upgrade. After that I
  look for `.pacnew` files and I read them. I do not copy one over the
  live file without looking.
- Fedora: I read an SELinux denial before I turn SELinux off. I list
  the firewall zone before I open a port.
- Both: `systemctl --failed` and the error log for this boot, before I
  reinstall a package.

The Windows lab runs on that same PC. libvirt hosts a Windows Server
2025 evaluation domain controller (`dc01`, domain `lab.local`) and a
Windows 11 evaluation client (`win11-soc`). Write-up:
[helpdesk/06-windows-domain](helpdesk/06-windows-domain/).

A second identity lab is Samba AD in a Debian container
(`corp.example.com`). That lab is separate. The Windows guests are not
joined to it. Write-up:
[helpdesk/04-samba-ad-lab](helpdesk/04-samba-ad-lab/).

I also keep Kali and BlackArch guests on this PC. When I have time I do
short exercises there, and on the Windows guests, and I get a little
better. What I publish from that practice is the defender's side: the
log I would read, the check I would run, the control that would have
mattered. Flags and attack steps stay off this repo. The blank note is
[templates/career/practice-note.md](templates/career/practice-note.md).

On the host I also use git, neovim, rustup, Python, Wireshark, and
rootless Podman. The `docker` command on this machine is Podman. Lab
passwords stay in a password manager. They are not in this repository.

## Languages

| Language | How I use it |
|----------|----------------|
| bash | Every day on CachyOS (Arch), and in the Linux troubleshooting lab. Fedora drill in [templates/linux/](templates/linux/fedora.md) |
| PowerShell | On the Windows domain lab, and in the language drills |
| Python | The `seclab` tools in this repo, with pytest |
| Rust | `log-analyzer` and `fim` here. Two other public repos: [Frihart](https://codeberg.org/ichbinlucasv/Frihart) and [HashChat](https://codeberg.org/ichbinlucasv/HashChat) |
| C | Study, and short compile-and-read drills. No C project in this repo yet |
| C++ | Same place as C: drills, not a program I ship |
| C# | A language drill in [templates/](templates/). No C# application here |
| Java | A language drill |
| Kotlin | A language drill |
| Haskell | A language drill. An older HashChat note mentioned Haskell. The code I am writing now is Rust |

The blank forms in [templates/](templates/) are the weekly rhythm: one
helpdesk or SOC sheet, and one language. I copy a form and fill it while
I work. A filled guess does not belong in git.

## AI

I use AI on this work, and I say so.

**Grok** (xAI) is the assistant I use for planning, for a second pass on
writing, and for the harder builds. I work with it in the terminal.

On the same PC I run a local model, so study chat does not need a cloud
key. **Ollama** serves a **Qwen** model. Three local apps share it:

- **Hermes** is the local coding assistant. I ask for one function at a
  time, then I compile or run the result.
- **OpenClaw** is a local agent app on the same model, for smaller tasks.
- **Odysseus** is a local browser workspace (chat and notes) on the same
  model. I use it as a study tutor: one topic at a time, defensive
  material, on virtual machines on this PC.

A lab moves to **Done** when I have run the check myself and kept the
output. A draft written with Grok or Qwen stays **Planned** or **In
progress** until that run exists. The evidence files are command output.

The model stays on defensive study and on code. This repository has no
exploit procedures in it.

## What to open first

For a helpdesk seat or a junior SOC seat, start here:

1. [Windows domain](helpdesk/06-windows-domain/) — a real AD DS lab, still **In progress**. On 4 Oct 2026 `win11-soc` was already in `lab.local`, a helpdesk reset is written up, and the empty workstation GPO is the ticket. Still open: an interactive helpdesk sign-in, and an unlock (lockout threshold is 0).
2. [Linux troubleshooting](helpdesk/03-linux-troubleshooting/) — **Done**, with terminal output in `evidence/`.
3. [Incident write-ups](soc-analyst/03-incident-writeups/) and [Sigma rules](soc-analyst/05-sigma-rules/) — how I read a log, and how I write a detection.
4. [Rust](rust/) — `log-analyzer` and `fim`, with tests and clippy clean. Longer Rust code: [Frihart](https://codeberg.org/ichbinlucasv/Frihart) and [HashChat](https://codeberg.org/ichbinlucasv/HashChat). [Python](python/) is the other small toolkit, with pytest.
5. [Templates](templates/) — the forms I use to practise a work day.

## What I am still learning

Security+ SY0-701 is not passed. HTB Academy is in progress. German is
in progress. Portuguese is my first language. French and English are
both C1. I am looking first in France, for helpdesk or a junior SOC role
(alternance or POEI). Germany is the other option, and I can work there
in English. Once I am working, I start a distance degree at IU
(Internationale Hochschule).

Other practice accounts, same rule (in progress, no rank claimed here):

- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46) — Academy in progress. No rank on this page.
- [TryHackMe](https://tryhackme.com/p/ichbinlucasv)
- [Boot.dev](https://www.boot.dev/u/ichbinlucasv) — the public page stays hidden until level 10, so this repo does not state a level

One SOC alert is already written end to end, with a UTC timeline:
[IR-03](soc-analyst/03-incident-writeups/IR-03-evtx-password-spray.md).
On 4 Oct 2026 I checked `win11-soc` in `lab.local`, reset one staff
password with the helpdesk credential, and wrote the empty
workstation GPO as a ticket. Output is in
[lab 06](helpdesk/06-windows-domain/). The forms in
[templates/career/](templates/career/) stay blank for the next run.

## Contact

Public only. Lab passwords stay off this repo.

- Email: ichbinlucas@pm.me
- [LinkedIn](https://www.linkedin.com/in/lucas-nunes-soares-63148637b/)
- [X](https://x.com/ichbinlucasv)
- [Hack The Box](https://profile.hackthebox.com/profile/019c3e11-0637-723b-b224-545dcf0bbc46)

Public profiles:
[codeberg.org/ichbinlucasv](https://codeberg.org/ichbinlucasv) and
[github.com/ichbinlucasv](https://github.com/ichbinlucasv).
