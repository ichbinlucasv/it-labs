# Idée de détection

[English](detection-idea.md) · **Français** · [Deutsch](detection-idea.de.md)

C'est un souhait d'alerte, écrit après avoir compris une ligne de journal.
Ce n'est pas une règle que je déploie sur un réseau qui n'est pas à moi.

```text
Nom :
Source de logs (Sysmon EID, 4625, clé auditd, proxy, ...) :
Une phrase : ce dont je veux être prévenu

Champs dont j'ai besoin :
-
-

Un vrai exemple de mes notes ou d'un échantillon public (defangé, cité) :

Ce qui sera du bruit :
- fenêtre de correctifs
- notre propre scanner
- compte de service qui fait ça toute la journée

À qui je demanderais avant de l'activer :

Sigma ou juste une recherche ?  recherche d'abord / règle ensuite
Si une règle existe dans ce dépôt, chemin :
```

La recherche d'abord. Une règle que je n'ai pas lancée sur un échantillon
est une supposition.
