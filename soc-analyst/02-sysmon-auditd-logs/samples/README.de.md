# ⚠️ SYNTHETISCHE Beispiel-Logs

[English](README.md) · [Français](README.fr.md) · **Deutsch**

Jede Datei in diesem Ordner wurde **von Hand oder per Skript zum Üben
erzeugt**. Sie stammen nicht aus einem echten Incident und nicht aus einer
echten Organisation.

- Hostnamen, Benutzer, Domänen und IPs sind fiktiv (`example.com`,
  `example.net`, RFC-5737-Adressen, RFC-1918-Lab-LAN).
- Hashes sind Platzhalter (`000…0001`) — sie bezeichnen keine echte Datei.
- Das „kodierte PowerShell“ dekodiert zu `Write-Output 'SYNTHETIC LAB EVENT - harmless'`.
- Jedes JSON-Ereignis trägt `"_synthetic": true`.

| Datei | Format | Inhalt |
|-------|--------|--------|
| `sysmon.synthetic.jsonl` | JSON-Zeilen, Sysmon-Feldnamen | Arbeitsstation `WS-COMPTA-07`: Makro-Dokument → PowerShell → Download → Run-Key-Persistenz → Beaconing → Discovery (+ gutartiges Rauschen) |
| `security-4625.synthetic.jsonl` | JSON-Zeilen, Feldnamen von Windows Security | Fehlgeschlagene Anmeldungen (4625) gegen `SRV-FILES-01` von einer externen Adresse, plus normale Tippfehler |
| `auditd.synthetic.log` | rohes Linux-Audit-Logformat | Server `web01`: SSH-Passwörter raten → Anmeldung als `deploy` → Download nach `/tmp` → Ausführung → Crontab → verweigerter Lesezugriff auf `/etc/shadow` |
