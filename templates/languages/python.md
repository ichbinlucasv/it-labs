# Python

What I use it for: small log chores. The tools that already have tests are
in [python/](../../python/). This page is the 25 minutes around them.

Stdlib only, unless a lab already chose a library.

## 25 minutes

```bash
cd python && . .venv/bin/activate 2>/dev/null || true
python -m seclab.authlog samples/auth.log.synthetic --threshold 5
pytest -q
```

Then change one thing on a **copy** of the sample and say what the tool
printed. Revert the copy. Do not "improve" the tool in the same 25 minutes
unless a test is already red.

## Type this until it sticks

A counter of failed SSH lines. Boring on purpose.

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

If the sample wording does not match `Failed password`, I fix the condition
after I have read one real line. I do not guess a regex first.

## Exercise

Add nothing. Explain, in two sentences, what `seclab.authlog` counts that
this snippet does not. The README in `python/` is allowed after I try.

## I still mix up

- `split()` eating the punctuation I needed
- reading a whole log into a list when I only needed a counter
- catching every exception and printing "error"
