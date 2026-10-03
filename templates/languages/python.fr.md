# Python

[English](python.md) · **Français** · [Deutsch](python.de.md)

Je m'en sers pour de petites corvées sur des logs. Les outils qui ont déjà
des tests sont dans [python/](../../python/). Cette page, c'est les
25 minutes autour.

Bibliothèque standard seulement, sauf si un lab a déjà choisi une
bibliothèque.

## 25 minutes

```bash
cd python && . .venv/bin/activate 2>/dev/null || true
python -m seclab.authlog samples/auth.log.synthetic --threshold 5
pytest -q
```

Ensuite, je change une chose sur une **copie** de l'échantillon, et je dis
ce que l'outil a affiché. Je remets la copie comme avant. Je ne
« l'améliore » pas dans les mêmes 25 minutes, sauf si un test est déjà
rouge.

## Je retape jusqu'à ce que ça tienne

Un compteur de lignes SSH en échec. Ennuyeux exprès.

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

Ce fragment est incomplet exprès. Sur l'échantillon, `Failed password for
invalid user admin` fait que `user` est égal à `invalid`, et la ligne est
sautée. `seclab.authlog` garde cet utilisateur. Je lis une vraie ligne
avant de « corriger ».

## Exercice

Je n'ajoute rien. J'explique, en deux phrases, ce que `seclab.authlog`
compte et que ce fragment ne compte pas. Le README dans `python/` est
permis après que j'ai essayé.

## Je mélange encore

- `split()` qui mange la ponctuation dont j'avais besoin
- lire un log entier dans une liste alors qu'il me fallait seulement un
  compteur
- attraper toutes les exceptions et afficher « error »
