"""
capture.py — Packet Capture Module
Network Traffic Analyzer
"""

import csv
import os
import time
import random
from datetime import datetime


# ─────────────────────────────────────────────
#  SIMULATED PACKET CAPTURE
#  (Real capture requires: sudo + scapy installed)
#  For demo/CV purposes, we generate realistic traffic data
# ─────────────────────────────────────────────

PROTOCOLS = ["TCP", "UDP", "ICMP", "DNS", "HTTP", "HTTPS", "ARP"]

SAMPLE_IPS = [
    "192.168.1.1", "192.168.1.10", "192.168.1.25",
    "10.0.0.1",    "10.0.0.55",    "172.16.0.3",
    "8.8.8.8",     "8.8.4.4",      "1.1.1.1",
    "142.250.74.46","151.101.1.140","93.184.216.34",
]

PORTS = {
    "HTTP":  80,
    "HTTPS": 443,
    "DNS":   53,
    "FTP":   21,
    "SSH":   22,
    "SMTP":  25,
}


def simulate_packet():
    """Generate one realistic simulated packet record."""
    proto   = random.choices(PROTOCOLS, weights=[30,20,10,15,10,10,5])[0]
    src_ip  = random.choice(SAMPLE_IPS)
    dst_ip  = random.choice([ip for ip in SAMPLE_IPS if ip != src_ip])
    src_port = random.randint(1024, 65535)
    dst_port = PORTS.get(proto, random.randint(1, 1024))
    length  = random.randint(40, 1500)
    ts      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "timestamp": ts,
        "src_ip":    src_ip,
        "dst_ip":    dst_ip,
        "protocol":  proto,
        "src_port":  src_port,
        "dst_port":  dst_port,
        "length":    length,
    }


def capture_packets(count: int = 200, output_file: str = "traffic.csv"):
    """
    Capture (simulate) `count` packets and save to CSV.

    To use REAL capture with Scapy, replace the body with:
        from scapy.all import sniff
        pkts = sniff(count=count)
        # then parse pkts and write to CSV
    """
    fieldnames = ["timestamp","src_ip","dst_ip","protocol","src_port","dst_port","length"]

    print(f"[*] Starting packet capture — {count} packets → {output_file}")
    print("    (Simulated mode: no root / Scapy required)\n")

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, count + 1):
            pkt = simulate_packet()
            writer.writerow(pkt)
            time.sleep(0.01)          # realistic pacing
            if i % 50 == 0:
                print(f"    Captured {i}/{count} packets …")

    print(f"\n[+] Done. Saved {count} records to '{output_file}'")


# ── Entry point ───────────────────────────────
if __name__ == "__main__":
    capture_packets(count=200, output_file="traffic.csv")
