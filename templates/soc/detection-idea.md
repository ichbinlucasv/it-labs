# Detection idea

**English** · [Français](detection-idea.fr.md) · [Deutsch](detection-idea.de.md)

This is a wish for an alert, written after I understood one log line.
It is not a rule I deploy on a network I do not own.

```text
Name:
Log source (Sysmon EID, 4625, auditd key, proxy, ...):
One sentence: what I want to hear about

Fields I need:
-
-

A real example from my notes or a public sample (defanged, cited):

What will be noise:
- patch window
- our own scanner
- service account that does this all day

Who I would ask before turning it on:

Sigma or just a search?  search first / rule later
If a rule exists in this repo, path:
```

Search first. A rule I have not run on a sample is a guess.
