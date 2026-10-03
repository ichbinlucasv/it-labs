# Rust

[English](rust.md) · [Français](rust.fr.md) · **Deutsch**

Ich nutze es für die zwei Crates in [rust/](../../rust/) und für die
längeren Projekte außerhalb dieses Repos. Hier soll mir die Sprache einmal
pro Woche in der Hand bleiben.

## 25 Minuten

```bash
cd rust
cargo test -q
cargo clippy --all-targets -- -D warnings
```

Wenn das schon grün ist, füge ich kein Feature hinzu. Ich lese eine
Funktion in `log-analyzer` und schreibe die Signatur aus dem Kopf neu.

## Das tippe ich, bis es sitzt

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

Ich will `Result` in der Signatur behalten. Ein `unwrap()` bei einer
fehlenden Datei ist der Fehler, den ich nicht machen will.

## Übung

Ich richte `count_status` auf
[rust/samples/access.log.synthetic](../../rust/samples/access.log.synthetic)
für `"404"` und schreibe die Zahl auf. Von der Wurzel des Repos:

```bash
awk '$9 == 404 { c++ } END { print c+0 }' rust/samples/access.log.synthetic
```

Wenn awk und die Funktion nicht übereinstimmen, ist der Bug meiner. Ich
schreibe auf, welches Feld ich gezählt habe. Das Combined Log legt den
Status in Feld 9. Wenn dieses Beispiel anders aufgebaut ist, sage ich,
welches Feld ich tatsächlich benutzt habe.

## Bevor ich sage, dass es läuft

- `cargo test` und `cargo clippy --all-targets -- -D warnings` sind die
  Latte in diesem Repo. Grün heisst, ich habe sie laufen lassen, nicht
  dass ich sie auswendig kann.
- Eine Funktion, die fehlschlagen kann, gibt `Result` zurück. Das
  verstecke ich nicht mit `unwrap`.
- Ein Compilerfehler, eine Änderung, dann kompiliere ich wieder. Ich
  lese den ersten Fehler.
- Dieser Workspace verbietet `unsafe`. Das lasse ich so.

## Das verwechsle ich noch

- `&str` und `String`, obwohl ich nur schauen wollte
- `unwrap`, weil das Beispiel schneller kompilierte
- eine Crate hinzufügen, bevor die Stdlib-Version hässlich genug war, um
  das zu rechtfertigen
