#!/usr/bin/env bash
# Traffic test for ruleset.nft without VMs: three network namespaces joined by
# veth pairs stand in for the server and two clients. Nothing leaves the host.
#
#   admin   10.20.30.5      --veth--  fw  10.20.30.10  (server under test)
#   outside 192.0.2.10      --veth--  fw  192.0.2.1 / 198.51.100.1
#           198.51.100.66   (address from the blocklist)
#
# Usage: sudo ./netns-test.sh        Requires: iproute2, nftables, python3, ping.
set -uo pipefail
cd "$(dirname "$0")"
RULESET=ruleset.nft

cleanup() {
    [[ -n "${LST_PID:-}" ]] && kill "$LST_PID" 2>/dev/null
    for n in fw admin outside; do ip netns del "$n" 2>/dev/null; done
}
trap cleanup EXIT

for n in fw admin outside; do ip netns add "$n"; ip -n "$n" link set lo up; done
ip link add veth-adm type veth peer name eth0 netns admin;   ip link set veth-adm netns fw
ip link add veth-out type veth peer name eth0 netns outside; ip link set veth-out netns fw
ip -n fw addr add 10.20.30.10/24 dev veth-adm
ip -n fw addr add 192.0.2.1/24 dev veth-out
ip -n fw addr add 198.51.100.1/24 dev veth-out
ip -n fw link set veth-adm up; ip -n fw link set veth-out up
ip -n admin addr add 10.20.30.5/24 dev eth0;       ip -n admin link set eth0 up
ip -n outside addr add 192.0.2.10/24 dev eth0
ip -n outside addr add 198.51.100.66/24 dev eth0;  ip -n outside link set eth0 up
ip -n outside route add 10.20.30.0/24 via 192.0.2.1

# Fake services on 22/80/443 in the server namespace: accept, send a banner, close.
ip netns exec fw python3 -c '
import socket, threading
def serve(port):
    s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port)); s.listen()
    while True:
        c, _ = s.accept(); c.sendall(b"lab-listener\n"); c.close()
for p in (22, 80, 443):
    threading.Thread(target=serve, args=(p,), daemon=True).start()
threading.Event().wait()
' &
LST_PID=$!
sleep 1

probe() {  # probe NS SRC DST PORT
    ip netns exec "$1" python3 -c '
import socket, sys
src, dst, port = sys.argv[1], sys.argv[2], int(sys.argv[3])
s = socket.socket(); s.settimeout(2); s.bind((src, 0))
try:
    s.connect((dst, port)); s.recv(64); print(f"{src:>14} -> {dst}:{port:<5} OPEN")
except (socket.timeout, TimeoutError):
    print(f"{src:>14} -> {dst}:{port:<5} BLOCKED (no reply)")
except OSError as e:
    print(f"{src:>14} -> {dst}:{port:<5} REFUSED ({e.strerror})")
' "$2" "$3" "$4"
}

matrix() {
    probe admin   10.20.30.5    10.20.30.10 22
    probe admin   10.20.30.5    10.20.30.10 443
    probe outside 192.0.2.10    10.20.30.10 22
    probe outside 192.0.2.10    10.20.30.10 80
    probe outside 192.0.2.10    10.20.30.10 443
    probe outside 192.0.2.10    10.20.30.10 3306
    probe outside 198.51.100.66 10.20.30.10 443
    if ip netns exec outside ping -c1 -W1 -I 192.0.2.10 10.20.30.10 >/dev/null; then
        echo "    192.0.2.10 -> 10.20.30.10 ICMP  echo reply"
    else
        echo "    192.0.2.10 -> 10.20.30.10 ICMP  no reply"
    fi
}

echo "### 1. Without firewall"; matrix
echo; echo "### 2. nft -c -f $RULESET"; nft -c -f "$RULESET" && echo "syntax OK"
ip netns exec fw nft -f "$RULESET"
echo; echo "### 3. With firewall"; matrix

echo; echo "### 4. 20 SSH connections in a row from the admin subnet (limit 10/minute burst 5)"
for _ in $(seq 1 20); do probe admin 10.20.30.5 10.20.30.10 22; done | sort | uniq -c

echo; echo "### 5. Runtime blocklist: add 192.0.2.10, test 443, remove, test again"
ip netns exec fw nft add element inet lab_filter blocklist_v4 '{ 192.0.2.10 }'
probe outside 192.0.2.10 10.20.30.10 443
ip netns exec fw nft delete element inet lab_filter blocklist_v4 '{ 192.0.2.10 }'
probe outside 192.0.2.10 10.20.30.10 443

echo; echo "### 6. Egress to a blocklisted address from the server"
probe fw 198.51.100.1 198.51.100.66 443

echo; echo "### 7. Rules whose counters moved"
ip netns exec fw nft list ruleset | grep -E 'counter packets [1-9]' | sed -E 's/^[[:space:]]+//'
