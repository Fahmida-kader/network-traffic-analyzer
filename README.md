# 🛡 Network Traffic Analyzer

> **CV Line:** Network Traffic Analyzer (Python, Scapy, Pandas, Matplotlib)

A command-line tool that captures network packets, identifies protocols, extracts metadata, stores data in CSV, analyzes traffic patterns, and generates a rich visual dashboard.

---
![Dashboard](screenshots/dashboard.png)
## Pipeline

```
Capture Packets  →  Identify Protocols  →  Extract Information
      ↓
Store Data (CSV)  →  Analyze Traffic  →  Create Charts  →  Dashboard
```

---

## Folder Structure

```
network-traffic-analyzer/
│
├── venv/               ← virtual environment (not committed)
├── capture.py          ← Step 1: Packet capture (Scapy / simulated)
├── analyzer.py         ← Step 2: Traffic analysis with Pandas
├── dashboard.py        ← Step 3: Charts & dashboard with Matplotlib
├── traffic.csv         ← Generated packet data
├── requirements.txt    ← Python dependencies
├── screenshots/        ← Dashboard PNG output
└── README.md
```

---

## Quick Start

```bash
# 1. Clone & enter project
cd network-traffic-analyzer

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Capture packets (generates traffic.csv)
python capture.py

# 5. Analyze traffic (prints report to terminal)
python analyzer.py

# 6. Generate dashboard (saves screenshots/dashboard.png)
python dashboard.py
```

---

## Modules

### `capture.py`
- Simulates realistic network traffic (TCP, UDP, ICMP, DNS, HTTP, HTTPS, ARP)
- Captures src/dst IP, protocol, ports, packet length, timestamp
- Saves 200 records to `traffic.csv`
- **Real capture:** swap simulation with `scapy.sniff()` (requires `sudo`)

### `analyzer.py`
- Loads CSV with Pandas
- Protocol distribution, top talkers, top destinations
- Bandwidth per protocol, traffic over time, port activity
- Rich terminal table output

### `dashboard.py`
- Dark-themed 3×3 grid dashboard
- KPI strip: total packets, bandwidth, avg size, unique IPs
- Charts: protocol pie, bandwidth bar, packet size histogram,
  traffic timeline, top IPs (horizontal bars), port heatmap
- Saves to `screenshots/dashboard.png`

---

## Real Scapy Capture (Linux/macOS, requires sudo)

```python
from scapy.all import sniff, IP, TCP, UDP

def packet_callback(pkt):
    if IP in pkt:
        proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "OTHER"
        # write to CSV ...

sniff(prn=packet_callback, count=200, store=False)
```

---

## Tech Stack

| Tool        | Purpose                        |
|-------------|--------------------------------|
| Python 3.9+ | Core language                  |
| Scapy       | Packet capture & parsing       |
| Pandas      | Data storage & analysis        |
| Matplotlib  | Charts & dashboard             |
| Seaborn     | Statistical visualization      |
| Rich        | Terminal tables & formatting   |

---

## CV Description

**Network Traffic Analyzer** (Python, Scapy, Pandas, Matplotlib)  
Built a CLI tool that captures live network packets using Scapy, identifies protocols (TCP/UDP/ICMP/DNS/HTTP), extracts metadata, stores records in CSV, and generates an interactive dashboard with protocol distribution, bandwidth analysis, top talkers, traffic timeline, and port activity charts using Pandas and Matplotlib.
