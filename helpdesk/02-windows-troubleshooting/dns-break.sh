#!/usr/bin/env bash
# Scenario 1 of the Windows runbook, run without Windows:
# DNS is the thing that fails, the "link" (UDP to the resolver) is up,
# then a resolver that actually answers example.com fixes the lookup.
# Nothing listens outside 127.0.0.1. No root required.
set -uo pipefail

PORT=15353
WORKDIR=$(mktemp -d)
cleanup() {
    [[ -n "${DNS_PID:-}" ]] && kill "$DNS_PID" 2>/dev/null || true
    wait "$DNS_PID" 2>/dev/null || true
    rm -rf "$WORKDIR"
}
trap cleanup EXIT

echo "### 1. Symptom: the resolver port is closed"
if dig @127.0.0.1 -p "$PORT" example.com A +time=1 +tries=1 >/dev/null 2>&1; then
    echo "FAIL  expected no answer on 127.0.0.1:$PORT"
    exit 1
fi
echo "PASS  dig @127.0.0.1:$PORT example.com -> no answer (connection refused or timeout)"

echo
echo "### 2. Start a lab resolver that only knows example.com"
python3 - "$PORT" <<'PY' &
import socket, struct, sys
port = int(sys.argv[1])

def name_at(data, offset):
    labels = []
    while True:
        length = data[offset]
        if length == 0:
            return ".".join(labels), offset + 1
        if length & 0xC0:
            raise ValueError("compression in query")
        offset += 1
        labels.append(data[offset:offset + length].decode())
        offset += length

def encode(name):
    out = b""
    for label in name.split("."):
        out += bytes([len(label)]) + label.encode()
    return out + b"\x00"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", port))
while True:
    data, addr = sock.recvfrom(512)
    ident = data[:2]
    qname, end = name_at(data, 12)
    question = data[12:end + 4]
    if qname == "example.com":
        header = ident + struct.pack("!HHHHH", 0x8180, 1, 1, 0, 0)
        answer = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 30, 4) + socket.inet_aton("203.0.113.10")
        sock.sendto(header + question + answer, addr)
    else:
        header = ident + struct.pack("!HHHHH", 0x8183, 1, 0, 0, 0)
        sock.sendto(header + question, addr)
PY
DNS_PID=$!
sleep 0.3

echo
echo "### 3. Same question, resolver up"
dig @127.0.0.1 -p "$PORT" example.com A +time=2 +tries=1 +norecurse
echo
echo "### 4. A name the resolver does not know"
dig @127.0.0.1 -p "$PORT" not-a-host.example A +time=2 +tries=1 +norecurse
echo
echo "### 5. Read it the way the runbook says"
echo "Gateway/path was never the problem: UDP to 127.0.0.1:$PORT failed, then succeeded."
echo "The name example.com resolved to 203.0.113.10 (documentation address)."
echo "not-a-host.example came back NXDOMAIN, so the resolver itself is answering."
