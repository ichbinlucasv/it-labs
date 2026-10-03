# Lab 01 — Wazuh-Homelab (SIEM / XDR)

[English](README.md) · [Français](README.fr.md) · **Deutsch**

**Status:** Planned — Deployment und Triage aufgeschrieben. Noch kein Wazuh-Server aufgesetzt.

## Ziel

Ein kleines selbst gehostetes SIEM mit Wazuh aufsetzen, einen Windows- und
einen Linux-Endpunkt aufnehmen, harmlose „angriffsähnliche“ Aktivität
erzeugen und Alert-Triage üben, so wie ein Junior-SOC-Analyst. (Security+
D4 — SIEM, Log-Zusammenführung, Alarmierung, FIM, Schwachstellenerkennung.)

## Aufbau

| VM | Rolle | Ressourcen (Lab) | IP |
|----|------|------------------|----|
| `wazuh01` | Wazuh-Server + Indexer + Dashboard (All-in-one) | 4 vCPU, 8 GB RAM, 50 GB Platte (Wazuh-Quickstart-Minimum für ~1–25 Agenten) | 10.20.30.30 |
| `ws01` | Windows 11 + Sysmon + Wazuh-Agent | 2 vCPU, 4 GB | 10.20.30.50 |
| `web01` | Ubuntu 24.04 + auditd + Wazuh-Agent | 1 vCPU, 2 GB | 10.20.30.40 |

- Isoliertes Host-only- / internes Netz; NAT nur für Paketdownloads.
- Offizielle Doku: <https://documentation.wazuh.com/current/quickstart.html>
  (beim Schreiben installiert der Quickstart Wazuh **4.14** — immer die
  Version aus der aktuellen Doku nehmen).

## Schritte

### 1. Den All-in-one-Server installieren

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
less wazuh-install.sh                 # read scripts before piping them to bash
sudo bash ./wazuh-install.sh -a
# The admin password is printed at the end; store it in a password manager,
# never in this repo. Dashboard: https://10.20.30.30
```

### 2. Agenten aufnehmen

Im Dashboard: **Agents → Deploy new agent**, OS wählen, Serveradresse
`10.20.30.30` setzen, den erzeugten Befehl kopieren. Auf dem Server prüfen:

```bash
sudo /var/ossec/bin/agent_control -l
```

### 3. Telemetrie verbessern

- **Windows:** Sysmon mit einer Community-Konfiguration installieren
  ([SwiftOnSecurity/sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config)
  oder [olafhartong/sysmon-modular](https://github.com/olafhartong/sysmon-modular)),
  dann in der `ossec.conf` des Agenten ergänzen:

  ```xml
  <localfile>
    <location>Microsoft-Windows-Sysmon/Operational</location>
    <log_format>eventchannel</log_format>
  </localfile>
  ```

  PowerShell Script Block Logging (Ereignis 4104) per GPO oder lokaler
  Richtlinie einschalten.
- **Linux:** `auditd` installieren, Regeln ergänzen (Beispiele in
  [Lab 02](../02-sysmon-auditd-logs/)), und sicherstellen, dass der Agent
  `/var/log/audit/audit.log` liest.
- **FIM:** `<directories check_all="yes" realtime="yes">/etc</directories>`
  in den `syscheck`-Block auf `web01` aufnehmen.

### 4. Harmlose Testaktivität erzeugen (nur das eigene Lab)

| Aktivität | Erwartete Alert-Familie |
|-----------|-------------------------|
| 10 falsche SSH-Passwörter gegen `web01` von einer anderen Lab-VM | sshd-Authentifizierungsfehler / Brute Force |
| `sudo` mit falschem Passwort | PAM- / sudo-Fehler |
| Lokalen Benutzer auf `web01` anlegen und löschen | Benutzer hinzugefügt/entfernt |
| `/etc/hosts` ändern | FIM-Integritätsprüfsumme geändert |
| Auf `ws01`: `powershell -EncodedCommand`, das `Write-Output test` ausführt | Sysmon-/PowerShell-Regeln |
| Einen `HKCU\...\Run`-Wert auf `notepad.exe` setzen | Registry-Persistenz (Sysmon 13) |

Optional **Atomic Red Team**-Tests *nur* in der Lab-VM, nachdem ich jeden
Test gelesen habe.

### 5. Triage für jeden Alert

1. Welche Regel hat ausgelöst, welches Level, welcher Agent?
2. Wer (Benutzer), was (Prozess/Befehl), wo (Host/IP), wann (Zeitstempel, UTC)?
3. Erwartet? (Change-Ticket, Admin-Aktivität, bekannte Software)
4. Weitergehen: andere Ereignisse desselben Hosts/Benutzers/derselben IP ±15 min.
5. Urteil: True Positive / benignes True Positive / False Positive → dokumentieren.
6. Nachschärfen: Ausnahmen für bestätigte False Positives (mit Begründung).

### 6. Optional — Vergleich mit ELK

Der Elastic Stack (Elasticsearch + Kibana + Elastic Agent/Fleet) kann
dieselben Logs sammeln. Wazuh bringt eigenen Indexer und eigenes Dashboard
mit (Forks von OpenSearch), beide auf einer kleinen VM laufen zu lassen ist
nicht empfohlen; ELK auf einer eigenen VM versuchen und vergleichen:
Regelsprache, Dashboards, Ressourcenverbrauch.

## Nachweise

- Dashboard-Screenshot mit beiden Agenten **Active**.
- Screenshots der Alerts zu jeder Aktivität in der Tabelle oben, mit meinen
  Triage-Notizen.
- FIM-Ereignis für `/etc/hosts` mit alter und neuer Prüfsumme.

## Was ich gelernt habe

_Noch von Lucas auszufüllen._
