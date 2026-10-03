# Rust

What I use it for: the two crates in [rust/](../../rust/), and the longer
projects outside this repo. Here, the point is to keep the language in my
hands once a week.

## 25 minutes

```bash
cd rust
cargo test -q
cargo clippy --all-targets -- -D warnings
```

If that is already green, I do not add a feature. I read one function in
`log-analyzer` and rewrite the signature from memory.

## Type this until it sticks

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

I want `Result` to stay in the signature. A `unwrap()` on a missing file is
the mistake I am trying not to make.

## Exercise

Point `count_status` at
[rust/samples/access.log.synthetic](../../rust/samples/access.log.synthetic)
for `"404"` and write the number down. From the repo root:

```bash
awk '$9 == 404 { c++ } END { print c+0 }' rust/samples/access.log.synthetic
```

If awk and the function disagree, the bug is mine. I write which field I
counted. The combined log puts the status in field 9. If this sample is
shaped differently, I say which field I actually used.

## I still mix up

- `&str` and `String` when I only needed to look
- `unwrap` because the example compiled faster
- adding a crate before the stdlib version was ugly enough to justify it
