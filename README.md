# Network Traffic Analyzer

A Python-based CLI tool that captures network packets, identifies protocols, analyzes traffic patterns, and generates a visual dashboard.

![Dashboard](screenshots/dashboard.png)

---

## What it does

```
Capture Packets  →  Identify Protocols  →  Extract Metadata
        ↓
Store as CSV  →  Analyze Traffic  →  Generate Dashboard
```

Captures 200+ packets across 7 protocols (TCP, UDP, ICMP, DNS, HTTP, HTTPS, ARP), runs statistical analysis with Pandas, and produces a dark-themed 7-chart dashboard saved as PNG.

---

## Tech Stack

| Tool          | Purpose                       |
|---------------|-------------------------------|
| Python 3.9+   | Core language                 |
| Scapy         | Packet capture & parsing      |
| Pandas        | Data storage & analysis       |
| Matplotlib    | Charts & dashboard            |
| Seaborn       | Statistical visualization     |

---

## Project Structure

```
network-traffic-analyzer/
│
├── capture.py          ← Packet capture (Scapy / simulated mode)
├── analyzer.py         ← Traffic analysis with Pandas
├── dashboard.py        ← 7-chart dashboard with Matplotlib
├── requirements.txt    ← Dependencies
├── screenshots/        ← Dashboard output
└── README.md
```

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/Fahmida-kader/network-traffic-analyzer.git
cd network-traffic-analyzer

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python capture.py       # generates traffic.csv
python analyzer.py      # prints analysis report
python dashboard.py     # saves screenshots/dashboard.png
```

---

## Dashboard

The dashboard includes:

- Protocol distribution (pie chart)
- Bandwidth usage per protocol
- Packet size distribution (histogram)
- Traffic volume over time (timeline)
- Top source & destination IPs
- Most active ports

---

## Real Packet Capture

By default the tool runs in simulation mode (no root required). To capture live traffic with Scapy on Linux/macOS:

```python
from scapy.all import sniff, IP, TCP, UDP

def packet_callback(pkt):
    if IP in pkt:
        proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTHER"
        # write to CSV ...

sniff(prn=packet_callback, count=200, store=False)
```

> Requires `sudo` on Linux/macOS.
