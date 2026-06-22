"""
analyzer.py — Traffic Analysis Module
Network Traffic Analyzer
"""

import pandas as pd


def load_data(filepath: str = "traffic.csv") -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["timestamp"])
    print(f"[+] Loaded {len(df)} packet records from '{filepath}'")
    return df


def protocol_distribution(df): return df["protocol"].value_counts()
def top_talkers(df, n=5):     return df["src_ip"].value_counts().head(n).reset_index()
def top_destinations(df, n=5): return df["dst_ip"].value_counts().head(n).reset_index()
def bandwidth_by_protocol(df): return df.groupby("protocol")["length"].sum().sort_values(ascending=False)
def traffic_over_time(df, freq="10s"):
    return df.set_index("timestamp").resample(freq)["length"].count()
def port_activity(df, n=10):  return df["dst_port"].value_counts().head(n).reset_index()
def avg_packet_size(df):      return df["length"].mean()
def total_bandwidth_mb(df):   return df["length"].sum() / (1024 * 1024)


def print_summary(df):
    print("\n" + "="*55)
    print("     NETWORK TRAFFIC ANALYSIS REPORT")
    print("="*55)
    print(f"  Total Packets   : {len(df):,}")
    print(f"  Total Bandwidth : {total_bandwidth_mb(df):.2f} MB")
    print(f"  Avg Packet Size : {avg_packet_size(df):.1f} bytes")
    print(f"  Time Range      : {df['timestamp'].min()}  →  {df['timestamp'].max()}")
    print()
    print("  Protocol Distribution:")
    for proto, cnt in protocol_distribution(df).items():
        print(f"    {proto:<8} {cnt:>5} packets")
    print()
    print("  Top Source IPs:")
    for _, row in top_talkers(df).iterrows():
        print(f"    {row.iloc[0]:<20} {row.iloc[1]:>4} packets")
    print("="*55 + "\n")


if __name__ == "__main__":
    df = load_data("traffic.csv")
    print_summary(df)
