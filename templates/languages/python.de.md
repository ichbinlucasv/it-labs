# Python

[English](python.md) · [Français](python.fr.md) · **Deutsch**

Ich nutze es für kleine Arbeiten an Logs. Die Werkzeuge, die schon Tests
haben, liegen in [python/](../../python/). Diese Seite ist die 25 Minuten
drumherum.

Nur die Standardbibliothek, außer ein Lab hat schon eine Bibliothek
gewählt.

## 25 Minuten

```bash
cd python && . .venv/bin/activate 2>/dev/null || true
python -m seclab.authlog samples/auth.log.synthetic --threshold 5
pytest -q
```

Dann ändere ich eine Sache an einer **Kopie** des Beispiels und sage, was
das Werkzeug ausgegeben hat. Die Kopie setze ich zurück. Das Werkzeug
„verbessere“ ich nicht in denselben 25 Minuten, außer ein Test ist schon
rot.

## Das tippe ich, bis es sitzt

Ein Zähler für fehlgeschlagene SSH-Zeilen. Langweilig mit Absicht.

```python
from collections import Counter
from pathlib import Path

def failed_users(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    for line in text.splitlines():
        if "Failed password" not in line:
            continue
        parts = line.split()
        if "for" in parts:
            user = parts[parts.index("for") + 1]
            if user != "invalid":
                counts[user] += 1
    return counts

if __name__ == "__main__":
    sample = Path("samples/auth.log.synthetic").read_text(encoding="utf-8", errors="replace")
    print(failed_users(sample).most_common(5))
```

Dieses Stück ist mit Absicht unvollständig. Im Beispiel macht
`Failed password for invalid user admin` `user` gleich `invalid`, und die
Zeile wird übersprungen. `seclab.authlog` behält diesen Benutzer. Ich lese
eine echte Zeile, bevor ich es „korrigiere“.

## Übung

Nichts hinzufügen. In zwei Sätzen erklären, was `seclab.authlog` zählt und
dieses Stück nicht. Die README in `python/` ist erlaubt, nachdem ich es
versucht habe.

## Das verwechsle ich noch

- `split()`, das die Satzzeichen schluckt, die ich brauchte
- ein ganzes Log in eine Liste lesen, obwohl ich nur einen Zähler brauchte
- jede Exception fangen und „error“ ausgeben
