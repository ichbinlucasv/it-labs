# Outils de sécurité en Python (`seclab`)

[English](README.md) · **Français** · [Deutsch](README.de.md)

**Status:** Done — trois outils avec 35 tests pytest qui passent.

## Objectif

Automatiser trois petites tâches réelles d'analyste avec du Python propre et
testé, uniquement avec la bibliothèque standard :

| Module | Ce qu'il fait |
|--------|---------------|
| `seclab.authlog` | Résume les échecs et réussites SSH de `auth.log` (ou d'une sortie `journalctl`) : IP les plus vues, utilisateurs visés, utilisateurs inexistants, alertes de seuil, et **connexions réussies depuis des IP qui ont aussi échoué** |
| `seclab.ioc` | Extrait IPv4/IPv6, domaines, URL, e-mails, MD5/SHA1/SHA256 de n'importe quel texte ; refang une entrée défangée (`hxxp`, `[.]`, `[@]`…) et peut défanger la sortie pour un partage sans risque |
| `seclab.hashcheck` | Hash des fichiers (MD5/SHA1/SHA256 en une passe, par blocs) et les compare à une liste de connus mauvais ; code de sortie 1 en cas de correspondance |

(Security+ D4 — automatisation et scripts, analyse de journaux ; D2 — indicateurs.)

## Mise en place

```bash
cd python
python3 -m venv .venv && . .venv/bin/activate
pip install -e '.[test]'      # pytest is the only (test) dependency
pytest
```

Python ≥ 3.10. Aucune dépendance tierce à l'exécution.

## Étapes

### authlog

```bash
python -m seclab.authlog samples/auth.log.synthetic --threshold 5
sudo python -m seclab.authlog /var/log/auth.log --json
journalctl -u ssh --no-pager -o short-iso | python -m seclab.authlog -
```

Extrait de la sortie sur l'exemple synthétique :

```text
Failed attempts     : 10
Unique source IPs   : 3
...
IPs at or above threshold (5):
  203.0.113.45 (8)

!! Successful login from an IP that also failed:
  2026-09-14T21:40:09.650033+00:00  deploy@203.0.113.45 via password
  2026-09-14T22:02:21.883120+00:00  alice@10.20.30.5 via publickey
```

(La deuxième ligne est un cas bénin classique — l'utilisateur s'est trompé
une fois, puis a utilisé sa clé. Le contexte compte : c'est une entrée de
triage, pas un verdict.)

### ioc

```bash
python -m seclab.ioc samples/threat-report.synthetic.txt
python -m seclab.ioc samples/threat-report.synthetic.txt --defang --json
python -m seclab.ioc --refang-only < defanged-report.txt
cat ../soc-analyst/02-sysmon-auditd-logs/samples/*.jsonl | python -m seclab.ioc --defang
```

Choix de conception / limites :

- Les domaines dont la dernière étiquette est une extension de fichier
  courante (`.exe`, `.ps1`, `.docm`, `.sh`, `.zip`…) sont ignorés, même si
  quelques-unes sont de vrais TLD.
- Par défaut, seuls les TLD à 2 lettres (codes pays) et une liste de TLD
  génériques courants ou abusés sont acceptés, et les jetons juste après un
  `\` sont sautés, pour que `CORP\c.martin` ou `Content.Word` ne sortent pas
  comme domaines. `--any-tld` relâche ça.
- `--exclude-private` retire les plages RFC 1918, loopback, lien-local **et**
  de documentation (`ipaddress` de Python traite les plages RFC 5737 comme
  non joignables globalement).
- La détection de hash se fait seulement par la longueur — toute chaîne hex
  de 32/40/64 caractères correspond.

### hashcheck

```bash
python -m seclab.hashcheck samples/fake_dropper.txt              # just print hashes
python -m seclab.hashcheck -k samples/known_bad.example.txt samples/ ; echo "exit=$?"
python -m seclab.hashcheck -k my_iocs.txt ~/Downloads -r --json
```

`samples/known_bad.example.txt` contient le SHA256 du fichier inoffensif
`fake_dropper.txt`, donc la démo produit une correspondance et le code de
sortie 1.

### Tests

```text
$ pytest
35 passed
```

Les tests couvrent des cas limites d'analyse (horodatages classiques contre
ISO, « message repeated N times » de rsyslog, IP invalides), les allers-retours
defang/refang, le filtrage des faux positifs, le hash par blocs (> 1 MiB),
l'analyse de la liste de connus mauvais, et les codes de sortie du CLI.

## Preuves

- Sortie de `pytest` (ci-dessus ; la CI est désactivée tant qu'il n'y a pas
  de runner).
- (Prévu) Capture de `authlog` sur le `auth.log` d'une VM de lab après le
  test de force brute Wazuh ([lab 01 soc-analyst](../soc-analyst/01-wazuh-homelab/)).

## Ce que j'ai appris

_À compléter par Lucas._
