# Lab 03 — Runbook Fehleranalyse Linux

[English](README.md) · **Deutsch**

**Status:** Done — Szenarien 1–5 und 7 habe ich in einem Debian-13-systemd-Container absichtlich kaputt gemacht und repariert, die Terminalausgaben liegen in [`evidence/`](evidence/); Szenario 6 nur teilweise (der OOM-Kill war hier nicht reproduzierbar, siehe unten).

## Ziel

Ein praxisnahes Runbook für häufige Probleme auf Linux-Servern und -Desktops
unter Debian/Ubuntu, mit Fokus auf Log-Analyse und der Überprüfung jeder
Hypothese — und mit dem Nachweis, dass ich es tatsächlich durchgeführt habe.

## Aufbau

- Geplant: VM mit Debian 12 / Ubuntu 24.04 und Snapshots.
- **Tatsächlich verwendet:** ein Debian-13-(trixie)-Root-Dateisystem, erstellt
  mit `debootstrap` und gestartet mit `systemd-nspawn --boot --private-network`.
  systemd, journald, nginx und sshd laufen also echt, der Container hat aber
  nur ein Loopback-Interface (nichts erreicht mein Netzwerk). Die genauen
  Befehle stehen in [`lab-container.md`](lab-container.md) (Englisch).
- Hostname im Container: `lab1`. Die Benutzer `alice` und `bob` sowie die
  Gruppe `finance` sind Lab-Konten. Die Adressen im DNS-Szenario stammen aus
  Dokumentations- bzw. Lab-Bereichen (`192.0.2.53`, `10.20.30.20`).
- Ablauf pro Szenario: absichtlich kaputt machen → Symptom so beobachten, wie
  es ein Benutzer sieht → mit den Befehlen unten analysieren → beheben → prüfen.

## Schritte

### 0. Die ersten fünf Befehle auf jedem System

```bash
uptime                     # load, how long since reboot
df -h; df -i               # disk space AND inodes
free -h                    # memory / swap
systemctl --failed         # failed units
journalctl -p err -b       # errors since boot
```

In einem Container zeigen `uptime`, `free` und `df /` die Werte des **Hosts**
(gemeinsamer Kernel und Overlay-Dateisystem) — das sollte man wissen, bevor
man Schlüsse daraus zieht. Ausgabe: [`evidence/0-first-five-commands.txt`](evidence/0-first-five-commands.txt).

### 1. Dienst startet nicht

```bash
systemctl status nginx
journalctl -u nginx -n 50 --no-pager
sudo nginx -t              # config syntax test (most daemons have one)
ss -tlnp | grep ':80'      # port already in use?
```

*So habe ich den Fehler erzeugt:* das `;` am Ende von
`listen 80 default_server` in `/etc/nginx/sites-enabled/default` entfernt.

Beobachtung ([Nachweis](evidence/1-service-wont-start.txt)):

```text
$ nginx -t
[emerg] 104#104: invalid parameter "listen" in /etc/nginx/sites-enabled/default:23
nginx: configuration file /etc/nginx/nginx.conf test failed
$ sed -n 22,23p /etc/nginx/sites-enabled/default
	listen 80 default_server
	listen [::]:80 default_server;
```

Die Meldung nennt **Zeile 23**, der Fehler steht aber in **Zeile 22**: Ohne
Semikolon liest nginx beide Zeilen als eine Direktive und beschwert sich erst
beim zweiten `listen`. Lehre: Wenn ein Parser Zeile N meldet, auch Zeile N-1
ansehen. Nach dem Wiederherstellen der Datei: `nginx -t` OK, Dienst `active`,
HTTP 200 auf `127.0.0.1`.

*Zweiter Fehler — Port belegt:* Ich habe einen Python-Webserver als
transiente Unit auf Port 80 gestartet und danach nginx. Im Journal stand
`bind() to 0.0.0.0:80 failed (98: Address already in use)`, und
`ss -tlnp` zeigte `users:(("python3",pid=135,fd=3))` auf `:80` — Prozessname
und PID sagen genau, was zu stoppen ist.

### 2. Festplatte voll

```bash
df -h /
sudo du -xh / --max-depth=1 2>/dev/null | sort -h | tail
sudo journalctl --disk-usage
sudo journalctl --vacuum-size=200M
sudo lsof +L1              # deleted files still held open by a process
```

*So habe ich den Fehler erzeugt:* Statt die echte Platte zu füllen, habe ich
ein 100-MB-tmpfs unter `/srv/data` eingehängt und einen Dienst gestartet, der
ständig in `/srv/data/app.log` schreibt.

Beobachtung ([Nachweis](evidence/2-disk-full.txt)): `echo: write error: No
space left on device`, `df` bei 100 %, `du` zeigt auf das 100 MB große
`app.log`. Dann habe ich absichtlich den klassischen Fehler gemacht:
`rm app.log`. `df` **blieb bei 100 %**, weil der Prozess die Datei noch
geöffnet hatte:

```text
$ lsof -nP +L1
COMMAND PID USER FD   TYPE DEVICE  SIZE/OFF NLINK NODE NAME
sh      171 root 3w   REG   0,62 104857600     0    2 /srv/data/app.log (deleted)
```

Der Platz wurde erst nach `systemctl stop chatty-app` frei. Richtige Lösung
auf einem echten Server: den schreibenden Prozess finden, dann die Datei
leeren (`: > app.log`) oder mit logrotate rotieren, statt sie unter einem
laufenden Prozess zu löschen.

### 3. DNS / Netzwerk

```bash
ip -br addr; ip route
ping -c3 10.20.30.1
resolvectl status          # or cat /etc/resolv.conf
dig example.com +short
dig @10.20.30.10 example.com
curl -I https://example.com
```

*So habe ich den Fehler erzeugt:* `dnsmasq` auf `127.0.0.1` als „Firmen-DNS“
gestartet (antwortet `intranet.lab.example → 10.20.30.20`) und einen falschen
statischen Resolver `nameserver 192.0.2.53` in `/etc/resolv.conf` eingetragen
— die Linux-Variante von Ticket-Beispiel 1 in [Lab 01](../01-ticket-writing/examples.md).

Beobachtung ([Nachweis](evidence/3-dns.txt)):

```text
$ getent hosts intranet.lab.example; echo exit=$?
exit=2
$ dig +time=2 +tries=1 intranet.lab.example
;; UDP setup with 192.0.2.53#53(192.0.2.53) for intranet.lab.example failed: network unreachable.
$ dig @127.0.0.1 intranet.lab.example +short
10.20.30.20
```

Die direkte Anfrage an den richtigen Server funktioniert, die an den
konfigurierten nicht → das Problem ist die Resolver-Konfiguration, nicht der
Name. Nach `nameserver 127.0.0.1` liefern `getent` und `dig` beide
`10.20.30.20`. (Im Container gibt es gar keine Route, daher meldet dig
„network unreachable“; in einem echten LAN zeigt sich derselbe Fehler meist
als Timeout.) Nebenbei: `dig nosuchhost.intranet.lab.example` lieferte
`NOERROR`, weil dnsmasqs `address=/domain/` auch für alle Subdomains antwortet.

### 4. Zugriff verweigert (Permission denied)

```bash
ls -l /srv/share/report.txt
namei -l /srv/share/report.txt     # permissions of every path component
id alice                            # groups
getfacl /srv/share                  # ACLs
```

*So habe ich den Fehler erzeugt:* `/srv/share/finance` ist `root:finance 750`,
der Bericht `640`, und `alice` ist nicht in `finance`.

Beobachtung ([Nachweis](evidence/4-permission-denied.txt)): `namei -l` zeigte
sofort die blockierende Pfadkomponente (`drwxr-x--- root finance finance`),
und `id alice` zeigte keine Gruppe `finance`. Zwei Lösungen nach dem Prinzip
der minimalen Rechte, beide getestet:

- `usermod -aG finance alice` → alice kann lesen, aber **weiterhin nicht
  schreiben** (Datei ist `640`) — genau das, was die Gruppe erlauben soll.
- Nur für eine Person: `setfacl -m u:alice:rx` auf das Verzeichnis und
  `u:alice:r` auf die Datei → Lesezugriff, ohne die Gruppe anzufassen.

Niemals `chmod 777`. Hinweis: Eine neue Gruppenmitgliedschaft gilt erst bei
einer **neuen** Anmeldung (`su - alice` startet eine; ein Benutzer muss sich
ab- und wieder anmelden).

### 5. Probleme bei der SSH-Anmeldung

```bash
sudo journalctl -u ssh -n 50        # "ssh" on Debian/Ubuntu, "sshd" on RHEL
sudo grep 'Failed password' /var/log/auth.log | tail
sudo sshd -t                        # config syntax
ls -ld ~/.ssh; ls -l ~/.ssh/authorized_keys   # 700 / 600 required
```

*Erster Versuch:* `chmod 664 ~/.ssh/authorized_keys`. Die Anmeldung per
Schlüssel **funktionierte trotzdem**. OpenSSH toleriert Gruppen-Schreibrechte,
wenn die Gruppe die private Gruppe des Benutzers ist (`alice:alice`) — dieser
Versuch hat das Problem also nicht nachgestellt, und ich habe das notiert,
statt es zu verschweigen.

*Zweiter Versuch:* `chmod 777 /home/alice`. Jetzt ([Nachweis](evidence/5-ssh-login.txt)):

```text
alice@127.0.0.1: Permission denied (publickey,password).
$ journalctl -u ssh ... | grep -i modes
Authentication refused: bad ownership or modes for directory /home/alice
```

`sshd -t` war OK (Konfiguration in Ordnung), `namei -l` auf
`authorized_keys` zeigte `drwxrwxrwx alice alice alice`. Nach
`chmod 755 /home/alice` funktionierte die Anmeldung wieder. Der Benutzer
sieht nur „Permission denied“; der eigentliche Grund steht nur im Log des **Servers**.

### 6. Hohe CPU- / Speicherlast

```bash
top -o %CPU          # or htop
ps aux --sort=-%mem | head
dmesg -T | grep -i 'out of memory'
```

*CPU:* Eine transiente Unit mit `yes > /dev/null` erschien mit 100 % CPU in
`top` und `ps --sort=-%cpu`; `systemctl status runaway-job` nannte die
zugehörige Unit, und das Stoppen der Unit behob das Problem ([Nachweis](evidence/6-cpu-memory.txt)).

*Speicher — nicht reproduziert:* Ich habe einen Python-Job mit
`systemd-run -p MemoryMax=64M` gestartet, der 500 MB belegt. Er wurde
**nicht beendet**; `/sys/fs/cgroup/cgroup.controllers` ist in diesem
Container leer, der Memory-Controller ist also nicht delegiert und das Limit
wird stillschweigend ignoriert. Der OOM-Kill-Teil (`dmesg`/Journal „Out of
memory: Killed process“) braucht eine VM.

### 7. Paketprobleme

```bash
sudo apt update
sudo apt --fix-broken install
sudo dpkg --configure -a
```

*So habe ich den Fehler erzeugt:* ein kleines `.deb` (`lab-tool`) gebaut, das
von einem nicht existierenden Paket abhängt, und es mit `dpkg -i` installiert.

Beobachtung ([Nachweis](evidence/7-packages.txt)): `dependency problems -
leaving unconfigured`, `dpkg -l`-Status `iU` (installiert, entpackt, nicht
konfiguriert), und danach verweigerte **jedes** `apt-get install` den Dienst
(`Unmet dependencies. Try 'apt --fix-broken install'`). `apt-get
--fix-broken install` entfernte `lab-tool`; `dpkg --audit` war danach sauber.
Lehre: Ein kaputtes Paket blockiert alle Installationen, also zuerst das beheben.

## Nachweise

- [`evidence/`](evidence/) — Terminalausgaben aller Szenarien, kaputt → repariert
  (Invocation-IDs der Units entfernt, sonst nichts bearbeitet).
- Ursache im Journal für Szenario 1: `invalid parameter "listen" in
  /etc/nginx/sites-enabled/default:23` und `bind() to 0.0.0.0:80 failed (98:
  Address already in use)`.
- Nicht erfasst: OOM-Kill (siehe Szenario 6).

## Was ich gelernt habe

- Immer zuerst das eigene Log und den Konfigurationstest des Dienstes lesen
  (`journalctl -u`, `nginx -t`, `sshd -t`), bevor man etwas ändert; die
  Fehlermeldung für den Benutzer („Job failed“, „Permission denied“) enthält
  selten den Grund.
- Die Zeilennummer eines Parsers kann eine Zeile hinter dem eigentlichen Fehler liegen.
- Ein großes Log zu löschen gibt keinen Platz frei, solange ein Prozess es
  geöffnet hält — `lsof +L1` findet es.
- `namei -l` beantwortet „welches Verzeichnis blockiert mich?“ mit einem Befehl.
- Manche „Fehler“ sind keine: OpenSSH akzeptierte ein gruppenbeschreibbares
  `authorized_keys` bei privater Gruppe. Testen schlägt Nachsprechen.
- Container teilen sich den Kernel des Hosts: Ressourcenwerte und
  cgroup-Limits können sich anders verhalten als in einer VM, daher notiere
  ich, wo meine Umgebung abweicht.
