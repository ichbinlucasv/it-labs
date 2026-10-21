#!/usr/bin/env bash
# Re-run the Linux break/fix ideas on this machine without touching system services.
# Needs root for the tmpfs and for the unprivileged read test. Cleans up on exit.
set -uo pipefail

if [[ ${EUID} -ne 0 ]]; then
    echo "Run as root: sudo $0"
    exit 1
fi

# nginx -t and cat write the interesting lines on stderr.
exec 2>&1

WORKDIR=$(mktemp -d /tmp/linux-lab.XXXXXX)
DISK="$WORKDIR/disk"
cleanup() {
    if mountpoint -q "$DISK" 2>/dev/null; then
        umount "$DISK" || true
    fi
    rm -rf "$WORKDIR"
}
trap cleanup EXIT

echo "### 0. First look (this host, not the old lab container)"
uptime
df -h / | head -2
free -h | head -2

echo
echo "### 1. nginx -t reports the line after a missing semicolon"
cat > "$WORKDIR/broken.conf" <<'EOF'
events {}
http {
    server {
        listen 127.0.0.1:8088
        listen 127.0.0.1:8089;
        location / { return 200 "ok\n"; }
    }
}
EOF
cat > "$WORKDIR/fixed.conf" <<'EOF'
events {}
http {
    server {
        listen 127.0.0.1:8088;
        listen 127.0.0.1:8089;
        location / { return 200 "ok\n"; }
    }
}
EOF
echo "-- broken --"
nginx -t -c "$WORKDIR/broken.conf" 2>&1 || true
echo "-- fixed --"
nginx -t -c "$WORKDIR/fixed.conf"

echo
echo "### 2. Deleting an open file does not free a full filesystem"
mkdir -p "$DISK"
mount -t tmpfs -o size=8M tmpfs "$DISK"
python3 - "$DISK/app.log" <<'PY'
import sys
path = sys.argv[1]
handle = open(path, "w", buffering=1024 * 1024)
try:
    while True:
        handle.write("x" * 65536)
except OSError as exc:
    print(f"write stopped: {exc.strerror}")
try:
    handle.close()
except OSError as exc:
    print(f"close stopped: {exc.strerror}")
PY
echo "df before delete:"
df -h "$DISK" | tail -1
exec 9<>"$DISK/app.log"
rm -f "$DISK/app.log"
echo "df after rm, fd still open:"
df -h "$DISK" | tail -1
if command -v lsof >/dev/null; then
    echo "deleted-but-open:"
    lsof -nP +L1 9>&- 2>/dev/null | awk -v d="$DISK" 'NR == 1 || index($0, d)' 9>&-
fi
exec 9>&-
echo "df after the holder closed the fd:"
df -h "$DISK" | tail -1

echo
echo "### 3. Permission denied, then a mode that lets another user read"
echo "lab-only" > "$WORKDIR/report.txt"
chmod 755 "$WORKDIR"
chmod 600 "$WORKDIR/report.txt"
echo "-- mode 600, user nobody --"
if su -s /bin/cat nobody "$WORKDIR/report.txt"; then
    echo "FAIL  nobody could read a mode 600 file"
    exit 1
else
    echo "PASS  nobody was denied"
fi
chmod 644 "$WORKDIR/report.txt"
echo "-- mode 644, user nobody --"
su -s /bin/cat nobody "$WORKDIR/report.txt"

echo
echo "### 4. Package query (no install)"
dpkg -s nginx 2>/dev/null | awk -F': ' '/^(Package|Status|Version):/ {print}'
echo
echo "result: OK"
