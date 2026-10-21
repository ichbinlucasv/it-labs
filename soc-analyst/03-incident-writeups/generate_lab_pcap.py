#!/usr/bin/env python3
"""Build a small synthetic incident pcap (DNS, DHCP, periodic HTTP).

Every address is from an RFC 5737 documentation range or a lab subnet.
The file is a training capture, not malware and not a third-party dump.
Output defaults to ./lab-incident.pcap, which git ignores (*.pcap).
"""
from __future__ import annotations

import socket
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = int(datetime(2026, 10, 21, 9, 0, 0, tzinfo=timezone.utc).timestamp())
CLIENT = "192.0.2.50"
DNS = "192.0.2.53"
WEB = "203.0.113.80"
MAC_CLIENT = "020000000032"
MAC_DNS = "020000000035"
MAC_WEB = "020000000050"
MAC_BCAST = "ffffffffffff"


def checksum(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack(f"!{len(data) // 2}H", data))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def ipv4(src: str, dst: str, proto: int, payload: bytes, ident: int) -> bytes:
    total = 20 + len(payload)
    header = struct.pack(
        "!BBHHHBBH4s4s",
        0x45,
        0,
        total,
        ident,
        0x4000,
        64,
        proto,
        0,
        socket.inet_aton(src),
        socket.inet_aton(dst),
    )
    csum = checksum(header)
    header = struct.pack(
        "!BBHHHBBH4s4s",
        0x45,
        0,
        total,
        ident,
        0x4000,
        64,
        proto,
        csum,
        socket.inet_aton(src),
        socket.inet_aton(dst),
    )
    return header + payload


def udp(src: str, dst: str, sport: int, dport: int, payload: bytes, ident: int) -> bytes:
    length = 8 + len(payload)
    header = struct.pack("!HHHH", sport, dport, length, 0)
    pseudo = socket.inet_aton(src) + socket.inet_aton(dst) + struct.pack("!BBH", 0, 17, length)
    csum = checksum(pseudo + header + payload)
    header = struct.pack("!HHHH", sport, dport, length, csum or 0xFFFF)
    return ipv4(src, dst, 17, header + payload, ident)


def tcp(
    src: str,
    dst: str,
    sport: int,
    dport: int,
    seq: int,
    ack: int,
    flags: int,
    payload: bytes,
    ident: int,
) -> bytes:
    offset = 5 << 4
    header = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, offset, flags, 65535, 0, 0)
    length = len(header) + len(payload)
    pseudo = socket.inet_aton(src) + socket.inet_aton(dst) + struct.pack("!BBH", 0, 6, length)
    csum = checksum(pseudo + header + payload)
    header = struct.pack("!HHIIBBHHH", sport, dport, seq, ack, offset, flags, 65535, csum, 0)
    return ipv4(src, dst, 6, header + payload, ident)


def eth(dst_mac: str, src_mac: str, packet: bytes) -> bytes:
    return bytes.fromhex(dst_mac + src_mac) + b"\x08\x00" + packet


def encode_name(name: str) -> bytes:
    out = b""
    for label in name.split("."):
        out += bytes([len(label)]) + label.encode()
    return out + b"\x00"


def dns_query(name: str, ident: int) -> bytes:
    return struct.pack("!HHHHHH", ident, 0x0100, 1, 0, 0, 0) + encode_name(name) + struct.pack("!HH", 1, 1)


def dns_response(name: str, ip: str, ident: int) -> bytes:
    question = encode_name(name) + struct.pack("!HH", 1, 1)
    answer = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 30, 4) + socket.inet_aton(ip)
    header = struct.pack("!HHHHHH", ident, 0x8180, 1, 1, 0, 0)
    return header + question + answer


def dhcp_option(code: int, data: bytes = b"") -> bytes:
    if code == 255:
        return b"\xff"
    return bytes([code, len(data)]) + data


def dhcp(op: int, xid: int, yiaddr: str, mac: str, options: bytes) -> bytes:
    chaddr = bytes.fromhex(mac) + b"\x00" * 10
    packet = struct.pack(
        "!BBBBIHH4s4s4s4s",
        op,
        1,
        6,
        0,
        xid,
        0,
        0x8000,
        b"\x00\x00\x00\x00",
        socket.inet_aton(yiaddr),
        b"\x00\x00\x00\x00",
        b"\x00\x00\x00\x00",
    )
    packet += chaddr + b"\x00" * 64 + b"\x00" * 128 + b"\x63\x82\x53\x63" + options
    return packet


def http_session(sport: int, when: int, ident: int) -> list[tuple[int, int, bytes]]:
    request = (
        b"GET /status HTTP/1.1\r\n"
        b"Host: beacon.example\r\n"
        b"User-Agent: LabBeacon/1.0\r\n"
        b"Connection: close\r\n\r\n"
    )
    response = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nOK"
    cseq, sseq = 1000, 5000
    steps = [
        (CLIENT, WEB, MAC_WEB, MAC_CLIENT, sport, 80, cseq, 0, 0x02, b""),
        (WEB, CLIENT, MAC_CLIENT, MAC_WEB, 80, sport, sseq, cseq + 1, 0x12, b""),
        (CLIENT, WEB, MAC_WEB, MAC_CLIENT, sport, 80, cseq + 1, sseq + 1, 0x10, b""),
        (CLIENT, WEB, MAC_WEB, MAC_CLIENT, sport, 80, cseq + 1, sseq + 1, 0x18, request),
        (WEB, CLIENT, MAC_CLIENT, MAC_WEB, 80, sport, sseq + 1, cseq + 1 + len(request), 0x18, response),
        (CLIENT, WEB, MAC_WEB, MAC_CLIENT, sport, 80, cseq + 1 + len(request), sseq + 1 + len(response), 0x11, b""),
        (WEB, CLIENT, MAC_CLIENT, MAC_WEB, 80, sport, sseq + 1 + len(response), cseq + 2 + len(request), 0x11, b""),
    ]
    packets = []
    for index, (src, dst, dmac, smac, sp, dp, seq, ack, flags, payload) in enumerate(steps):
        ip = tcp(src, dst, sp, dp, seq, ack, flags, payload, ident + index)
        packets.append((when, index * 1000, eth(dmac, smac, ip)))
    return packets


def build() -> list[tuple[int, int, bytes]]:
    packets: list[tuple[int, int, bytes]] = []
    ident = 1
    hostname = dhcp_option(12, b"ws-04")
    client_id = dhcp_option(61, b"\x01" + bytes.fromhex(MAC_CLIENT))
    discover = dhcp(
        1,
        0x0A11,
        "0.0.0.0",
        MAC_CLIENT,
        dhcp_option(53, b"\x01") + hostname + client_id + dhcp_option(255),
    )
    offer_opts = (
        dhcp_option(53, b"\x02")
        + dhcp_option(54, socket.inet_aton(DNS))
        + dhcp_option(1, socket.inet_aton("255.255.255.0"))
        + dhcp_option(3, socket.inet_aton("192.0.2.1"))
        + dhcp_option(6, socket.inet_aton(DNS))
        + dhcp_option(51, struct.pack("!I", 3600))
        + hostname
        + dhcp_option(255)
    )
    offer = dhcp(2, 0x0A11, CLIENT, MAC_CLIENT, offer_opts)
    packets.append((BASE, 0, eth(MAC_BCAST, MAC_CLIENT, udp("0.0.0.0", "255.255.255.255", 68, 67, discover, ident))))
    ident += 1
    packets.append((BASE, 20000, eth(MAC_CLIENT, MAC_DNS, udp(DNS, CLIENT, 67, 68, offer, ident))))
    ident += 1

    queries = [
        ("intranet.example", "192.0.2.10", 0x1001),
        ("files.example", "192.0.2.20", 0x1002),
        ("beacon.example", WEB, 0x1003),
    ]
    for offset, (name, answer, qid) in enumerate(queries):
        when = BASE + 1 + offset
        q = dns_query(name, qid)
        a = dns_response(name, answer, qid)
        packets.append((when, 0, eth(MAC_DNS, MAC_CLIENT, udp(CLIENT, DNS, 53000 + offset, 53, q, ident))))
        ident += 1
        packets.append((when, 5000, eth(MAC_CLIENT, MAC_DNS, udp(DNS, CLIENT, 53, 53000 + offset, a, ident))))
        ident += 1

    for burst in range(4):
        packets.extend(http_session(46000 + burst, BASE + 10 + burst * 60, ident))
        ident += 10
    return packets


def write_pcap(path: Path, packets: list[tuple[int, int, bytes]]) -> None:
    with path.open("wb") as handle:
        handle.write(struct.pack("<IHHIIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
        for sec, usec, data in packets:
            handle.write(struct.pack("<IIII", sec, usec, len(data), len(data)))
            handle.write(data)


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("lab-incident.pcap")
    packets = build()
    write_pcap(path, packets)
    print(f"wrote {path} ({len(packets)} packets)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
