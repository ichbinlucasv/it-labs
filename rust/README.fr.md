# Outils de sécurité en Rust (workspace cargo)

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — deux crates avec 11 tests unitaires qui passent ; clippy et rustfmt propres.

## Objectif

Apprendre Rust en construisant deux petits outils défensifs, sûrs et bien
testés :

| Crate | Ce qu'elle fait |
|-------|-----------------|
| [`log-analyzer`](crates/log-analyzer/) | Résume les journaux d'accès Apache/Nginx au format *combined* : clients les plus vus, codes de statut, clients avec beaucoup d'erreurs (balayage), et requêtes qui matchent des heuristiques transparentes (traversée de chemin y compris encodée en pourcent, fichiers sensibles, sondes de panneaux d'admin, user-agents de scanners, motifs d'injection). Bibliothèque standard seulement. |
| [`fim`](crates/fim/) | **Contrôle d'intégrité** minimal : `baseline` enregistre le SHA-256 et la taille de chaque fichier sous un répertoire ; `check` signale les fichiers **ADDED / REMOVED / MODIFIED**. Ne suit pas les liens symboliques. Utilise la crate `sha2`. |

(Security+ D4 — contrôle d'intégrité des fichiers, analyse de journaux ;
D1 — intégrité, hash.)

## Mise en place

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

Le code `unsafe` est interdit sur tout le workspace (`[workspace.lints]`).

## Étapes

### log-analyzer

```bash
cargo run -q -p log-analyzer -- --min-errors 3 samples/access.log.synthetic
sudo ./target/release/log-analyzer /var/log/nginx/access.log --top 20
```

Sortie sur l'exemple synthétique (extrait) :

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

Démo sur un répertoire jetable (modifier `sshd_config`, supprimer `hosts`,
déposer un nouveau fichier cron) :

```text
$ fim check /tmp/demo /tmp/fim-baseline.tsv
ADDED     etc/cron.d-evil
REMOVED   etc/hosts
MODIFIED  etc/ssh/sshd_config
1 added, 1 removed, 1 modified, 0 unchanged
exit=1
```

Codes de sortie : `0` propre / baseline écrite, `1` changements détectés,
`2` erreur — donc lançable depuis cron ou un timer systemd, avec alerte si
le code n'est pas zéro.

Limites (voulues, c'est un projet d'apprentissage) : pas de suivi des
droits, du propriétaire ni du mtime, pas de baseline signée (un attaquant
root pourrait la réécrire — les vrais outils stockent la baseline hors de
l'hôte ou la signent), les noms de fichiers avec tabulation ou saut de ligne
sont refusés.

### Tests

```text
$ cargo test
fim:          5 passed (SHA-256 test vectors, add/remove/modify detection, exclusions, TSV round-trip & validation, symlink loop)
log-analyzer: 6 passed (parsing, malformed lines, percent-decoding, classification, summary/report)
$ cargo clippy --all-targets -- -D warnings   -> no warnings
```

## Preuves

- Sortie de `cargo test` / `cargo clippy` (ci-dessus ; le workflow CI les
  lancerait aussi une fois activé — il est désactivé pour l'instant).
- Sortie de `fim check` après modification de fichiers dans le `/etc` d'une
  VM de lab, comparée à l'alerte FIM Wazuh pour le même changement.

## Ce que j'ai appris

_À compléter par Lucas._
