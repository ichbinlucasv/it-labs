#!/usr/bin/env bash
# Generate a small, harmless HTTP capture entirely inside an isolated network
# namespace (loopback only — no traffic leaves the machine, nothing third-party).
# Requires: root (for netns/tcpdump), python3, curl, tcpdump.
# Output: ./lab-http.pcap  (ignored by git via *.pcap in .gitignore)
set -euo pipefail

NS=caplab
OUT="${1:-lab-http.pcap}"

cleanup() {
    [[ -n "${SRV_PID:-}" ]] && kill "$SRV_PID" 2>/dev/null || true
    [[ -n "${CAP_PID:-}" ]] && kill "$CAP_PID" 2>/dev/null || true
    ip netns del "$NS" 2>/dev/null || true
}
trap cleanup EXIT

ip netns add "$NS"
ip netns exec "$NS" ip link set lo up

ip netns exec "$NS" python3 -m http.server 8080 --bind 127.0.0.1 >/dev/null 2>&1 &
SRV_PID=$!
ip netns exec "$NS" tcpdump -i lo -U -w "$OUT" 'tcp port 8080' 2>/dev/null &
CAP_PID=$!
sleep 1

for path in / /admin /robots.txt /index.html; do
    ip netns exec "$NS" curl -s -o /dev/null -A "lab-client/1.0" "http://127.0.0.1:8080${path}" || true
done
sleep 1
kill "$CAP_PID"; wait "$CAP_PID" 2>/dev/null || true
echo "Capture written to $OUT"
