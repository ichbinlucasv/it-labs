# Lab 03 — Host-Firewall mit nftables

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Done — Syntax geprüft, danach Datenverkehr mit drei Network Namespaces getestet, die den Server, einen Admin-Client und einen externen Client darstellen ([`netns-test.sh`](netns-test.sh), Ausgabe in [`evidence/`](evidence/)); noch nicht dauerhaft mit `nftables.service` auf einer echten VM eingerichtet.

## Ziel

Eine Default-Deny-Host-Firewall für einen Linux-Server mit nftables:
zustandsbehaftete Filterung, SSH nur aus dem Admin-Subnetz und mit
Rate-Limit, öffentliche Web-Ports, notwendiges ICMP/ICMPv6, ein Set als
Sperrliste und Logging. (Security+ D3 — sicheres Netzwerkdesign; D2 — Härtung.)

## Aufbau

- VM mit Debian 12 / Ubuntu 24.04 und **Konsolenzugang** (falls man sich per
  SSH aussperrt), `sudo apt install nftables`.
- Das Lab-LAN `10.20.30.0/24` ist das Admin-Subnetz. Die Sperrliste nutzt
  RFC-5737-Adressen als Platzhalter.
- Regelwerk: [`ruleset.nft`](ruleset.nft).

## Schritte

1. Das Regelwerk **lesen** und vorhersagen, was passiert mit: SSH von
   `10.20.30.5`, SSH von `192.0.2.10`, HTTPS von überall, Ping, Verkehr von `198.51.100.66`.
2. **Syntax prüfen, ohne anzuwenden** (parst und validiert gegen den Kernel,
   übernimmt aber nichts):

   ```bash
   sudo nft -c -f ruleset.nft && echo "syntax OK"
   ```

3. **Gefahrlos testen** — entweder in einem Wegwerf-Network-Namespace:

   ```bash
   sudo ip netns add fwtest
   sudo ip netns exec fwtest nft -f ruleset.nft
   sudo ip netns exec fwtest nft list ruleset
   sudo ip netns del fwtest
   ```

   oder auf der VM mit automatischem Rollback, falls man sich aussperrt:

   ```bash
   sudo nft list ruleset > /root/nft-backup.nft
   sudo nft -f ruleset.nft
   # if SSH still works, cancel the rollback (Ctrl-C); otherwise it restores:
   sleep 120 && sudo nft -f /root/nft-backup.nft
   ```

4. **Dauerhaft einrichten**: nach `/etc/nftables.conf` kopieren, `sudo systemctl enable --now nftables`.
5. **Von einer anderen Lab-VM prüfen**: `nc -zv 10.20.30.10 22` / `curl -I http://10.20.30.10`
   und Zähler/Logs beobachten:

   ```bash
   sudo nft list chain inet lab_filter input      # counters
   sudo journalctl -k -g 'nft-in-' -f             # log prefixes
   ```

6. **Sperrliste zur Laufzeit pflegen** (kein Neuladen nötig):

   ```bash
   sudo nft add element inet lab_filter blocklist_v4 '{ 203.0.113.99 }'
   sudo nft list set inet lab_filter blocklist_v4
   ```

### Durchgeführte Validierung

Ich hatte keine zwei VMs und habe daher Network Namespaces verwendet: Jeder
Namespace hat eigene Interfaces, Routen und ein eigenes nftables-Regelwerk —
das reicht, um zu testen, was eine Firewall durchlässt.
[`netns-test.sh`](netns-test.sh) baut diese Umgebung auf, führt die Tests
ohne und mit Regelwerk aus und räumt danach auf:

```text
admin   10.20.30.5      --veth--  fw  10.20.30.10  (server under test, fake services on 22/80/443)
outside 192.0.2.10      --veth--  fw  192.0.2.1 / 198.51.100.1
        198.51.100.66   (in the blocklist)
```

```bash
sudo sysctl -w net.netfilter.nf_log_all_netns=1   # allow log lines from non-host namespaces
sudo ./netns-test.sh
sudo dmesg | grep nft-                              # log prefixes
sudo sysctl -w net.netfilter.nf_log_all_netns=0
```

Ergebnisse ([vollständige Ausgabe](evidence/netns-test.txt), nftables v1.1.3):

| Test | Ohne Regelwerk | Mit Regelwerk | Wie vorhergesagt? |
|------|----------------|---------------|-------------------|
| SSH vom Admin `10.20.30.5` | offen | offen | ja |
| SSH von `192.0.2.10` | offen | **blockiert**, geloggt `nft-in-ssh-denied` | ja |
| HTTP/HTTPS von `192.0.2.10` | offen | offen | ja |
| TCP 3306 von `192.0.2.10` | abgewiesen (kein Dienst) | **blockiert** ohne Antwort, geloggt `nft-in-drop` | ja |
| Alles von `198.51.100.66` | offen | **blockiert**, geloggt `nft-in-blocklist` | ja |
| Ping von `192.0.2.10` | Antwort | Antwort (Accept mit Rate-Limit) | ja |
| 20 SSH-Verbindungen hintereinander vom Admin | — | 8 offen, 12 blockiert | ja (Burst 5 + Nachfüllen) |
| `192.0.2.10` zur Laufzeit auf die Sperrliste | — | 443 blockiert; nach dem Entfernen wieder offen | ja |
| Server → `198.51.100.66:443` | — | von der Output-Chain blockiert | ja |

Wichtig ist der Unterschied zwischen **abgewiesen** (RST: der Port ist zu,
aber der Host antwortet) und **blockiert** (gar keine Antwort: die Firewall
verwirft). Ein Scanner sieht das Erste als „closed“ und das Zweite als „filtered“.

**Gefundenes und behobenes Problem.** Im ersten Durchlauf fielen die 12
rate-limitierten SSH-Versuche aus dem *Admin*-Subnetz auf die allgemeine
Regel durch und wurden als `nft-in-ssh-denied` geloggt — mit demselben Präfix
wie ein externer SSH-Versuch. Bei einer Untersuchung sähe das wie ein Angriff
aus dem Admin-Netz aus. Ich habe zwei Regeln ergänzt, damit Admin-Verbindungen
über dem Limit ein eigenes Präfix `nft-in-ssh-ratelimit` bekommen (Logzeile
mit Rate-Limit, Drop immer). Zweiter Durchlauf, Zusammenfassung des
Kernel-Logs ([Nachweis](evidence/kernel-log-summary.txt), MAC-Adressen geschwärzt):

```text
      8 nft-in-ssh-ratelimit: IN=veth-adm ... SRC=10.20.30.5 DST=10.20.30.10 PROTO=TCP DPT=22
      2 nft-out-blocklist: IN= OUT=veth-out SRC=198.51.100.1 DST=198.51.100.66 PROTO=TCP DPT=443
      2 nft-in-ssh-denied: IN=veth-out ... SRC=192.0.2.10 DST=10.20.30.10 PROTO=TCP DPT=22
      2 nft-in-drop: IN=veth-out ... SRC=192.0.2.10 DST=10.20.30.10 PROTO=TCP DPT=3306
      2 nft-in-blocklist: IN=veth-out ... SRC=198.51.100.66 DST=10.20.30.10 PROTO=TCP DPT=443
```

(Jede blockierte Verbindung erscheint zweimal, weil der Client sein SYN nach
1 s wiederholt. Der Drop-Zähler zeigte 24 Pakete für die 12 Versuche, aber nur
8 Logzeilen — das eigene Rate-Limit der Log-Anweisung hat funktioniert.)

Hier nicht durchgeführt: Schritt 4 (dauerhafte Einrichtung mit
`nftables.service` auf einer VM) und ein echter SSH-Daemon hinter den Regeln;
die Test-Dienste nehmen Verbindungen nur an und schließen sie wieder.

### Designhinweise

- `policy drop` auf input/forward; output erlaubt (eine strengere
  Egress-Policy wäre ein guter nächster Schritt).
- `ct state invalid drop` vor allem anderen; established/related früh für die Performance.
- Logging mit Rate-Limit, damit ein Angreifer die Platte nicht mit Logzeilen füllen kann.
- `flush ruleset` löscht Regeln anderer Tools (Docker, libvirt) — auf solchen
  Hosts eine eigene Tabelle und `destroy table` / `delete table` verwenden.

## Nachweise

- [`evidence/netns-test.txt`](evidence/netns-test.txt): Ergebnis von
  `nft -c -f`, Testmatrix ohne/mit Regelwerk, Rate-Limit- und
  Sperrlisten-Tests sowie die Regeln, deren Zähler gestiegen sind.
- [`evidence/kernel-log-summary.txt`](evidence/kernel-log-summary.txt):
  `dmesg`-Zeilen mit den `nft-*`-Präfixen, gezählt (MAC-Adressen geschwärzt).

## Was ich gelernt habe

- Erst vorhersagen, dann testen: Weil ich für jeden Fall das erwartete
  Ergebnis vorher notiert hatte, fiel die eine Überraschung (das irreführende
  Log-Präfix) sofort auf.
- Die Reihenfolge in einer Chain zählt: Ein Paket, das eine
  `limit ... accept`-Regel nicht erfüllt, läuft einfach zur nächsten Regel
  weiter — hier landete es in der „denied“-Regel.
- „Abgewiesen“ und „blockiert“ sind unterschiedliche Antworten und sagen
  einem Analysten Unterschiedliches.
- Logging braucht ein eigenes Rate-Limit, sonst kann ein Angreifer die Platte füllen.
- Network Namespaces sind ein günstiger Weg, ein Regelwerk zu testen, ohne
  sich auf einem entfernten Server auszusperren; `nft -c` beweist nur die
  Syntax, nicht das Verhalten.
