# Erkennungsidee

[English](detection-idea.md) · [Français](detection-idea.fr.md) · **Deutsch**

Das ist ein Wunsch für einen Alert, geschrieben nachdem ich eine Logzeile
verstanden habe. Es ist keine Regel, die ich in einem Netz ausrolle, das
mir nicht gehört.

```text
Name:
Logquelle (Sysmon EID, 4625, auditd-Schlüssel, Proxy, ...):
Ein Satz: worüber ich Bescheid wissen will

Felder, die ich brauche:
-
-

Ein echtes Beispiel aus meinen Notizen oder einer öffentlichen Probe (entschärft, zitiert):

Was Rauschen sein wird:
- Patch-Fenster
- unser eigener Scanner
- Dienstkonto, das dies den ganzen Tag macht

Wen ich fragen würde, bevor ich es einschalte:

Sigma oder nur eine Suche?  zuerst Suche / Regel später
Wenn eine Regel in diesem Repo liegt, Pfad:
```

Zuerst suchen. Eine Regel, die ich nicht auf einer Probe ausgeführt habe,
ist eine Vermutung.
