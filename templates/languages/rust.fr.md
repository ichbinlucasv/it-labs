# Rust

[English](rust.md) · **Français** · [Deutsch](rust.de.md)

Je m'en sers pour les deux crates dans [rust/](../../rust/), et pour les
projets plus longs hors de ce dépôt. Ici, le but est de garder le langage
en main une fois par semaine.

## 25 minutes

```bash
cd rust
cargo test -q
cargo clippy --all-targets -- -D warnings
```

Si c'est déjà vert, je n'ajoute pas de fonctionnalité. Je lis une fonction
dans `log-analyzer` et je réécris la signature de mémoire.

## Je retape jusqu'à ce que ça tienne

```rust
use std::fs::File;
use std::io::{BufRead, BufReader};

fn count_status(path: &str, code: &str) -> std::io::Result<usize> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut n = 0;
    for line in reader.lines() {
        let line = line?;
        if line.split_whitespace().any(|f| f == code) {
            n += 1;
        }
    }
    Ok(n)
}
```

Je veux que `Result` reste dans la signature. Un `unwrap()` sur un fichier
manquant est l'erreur que j'essaie de ne pas faire.

## Exercice

Je pointe `count_status` sur
[rust/samples/access.log.synthetic](../../rust/samples/access.log.synthetic)
pour `"404"` et je note le nombre. Depuis la racine du dépôt :

```bash
awk '$9 == 404 { c++ } END { print c+0 }' rust/samples/access.log.synthetic
```

Si awk et la fonction ne sont pas d'accord, le bug est le mien. J'écris
quel champ j'ai compté. Le combined log met le statut dans le champ 9. Si
cet échantillon n'a pas cette forme, je dis quel champ j'ai vraiment utilisé.

## Je mélange encore

- `&str` et `String` alors que je voulais seulement regarder
- `unwrap`, parce que l'exemple compilait plus vite
- ajouter une crate avant que la version de la bibliothèque standard soit
  assez laide pour la justifier
