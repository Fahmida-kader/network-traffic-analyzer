"""
dashboard.py — Visualization & Dashboard Module
Network Traffic Analyzer
"""

import os
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (works without display)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import pandas as pd
import seaborn as sns

from analyzer import (
    load_data,
    protocol_distribution,
    top_talkers,
    top_destinations,
    bandwidth_by_protocol,
    traffic_over_time,
    port_activity,
    avg_packet_size,
    total_bandwidth_mb,
)

# ── Global style ──────────────────────────────────────────────────────────────
DARK_BG   = "#0d1117"
CARD_BG   = "#161b22"
ACCENT    = "#58a6ff"
GREEN     = "#3fb950"
ORANGE    = "#f0883e"
RED       = "#f85149"
PURPLE    = "#d2a8ff"
TEXT      = "#c9d1d9"
SUBTEXT   = "#8b949e"
GRID      = "#21262d"

PALETTE = [ACCENT, GREEN, ORANGE, RED, PURPLE, "#ffa657", "#79c0ff", "#56d364"]

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    CARD_BG,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   TEXT,
    "axes.titlecolor":   TEXT,
    "xtick.color":       SUBTEXT,
    "ytick.color":       SUBTEXT,
    "text.color":        TEXT,
    "grid.color":        GRID,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "font.family":       "monospace",
})


# ── Individual chart helpers ───────────────────────────────────────────────────

def _bar(ax, series, title, xlabel, ylabel, color=ACCENT, horizontal=False):
    vals  = series.values
    labs  = series.index.astype(str)
    if horizontal:
        bars = ax.barh(labs, vals, color=color, edgecolor=DARK_BG, linewidth=0.5)
        ax.set_xlabel(xlabel)
        ax.invert_yaxis()
        for bar in bars:
            w = bar.get_width()
            ax.text(w + max(vals)*0.01, bar.get_y()+bar.get_height()/2,
                    f"{w:,}", va="center", fontsize=8, color=SUBTEXT)
    else:
        bars = ax.bar(labs, vals, color=color, edgecolor=DARK_BG, linewidth=0.5)
        ax.set_ylabel(ylabel)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x()+bar.get_width()/2, h + max(vals)*0.01,
                    f"{h:,}", ha="center", fontsize=8, color=SUBTEXT)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    ax.grid(axis="x" if horizontal else "y")
    ax.spines[["top","right","left" if not horizontal else "bottom"]].set_visible(False)


def chart_protocol_pie(ax, df):
    dist = protocol_distribution(df)
    colors = PALETTE[:len(dist)]
    wedges, texts, autotexts = ax.pie(
        dist.values, labels=dist.index, colors=colors,
        autopct="%1.1f%%", startangle=140,
        wedgeprops=dict(edgecolor=DARK_BG, linewidth=1.5),
        pctdistance=0.82,
    )
    for t in texts:      t.set_color(TEXT);    t.set_fontsize(9)
    for t in autotexts:  t.set_color(DARK_BG); t.set_fontsize(8); t.set_fontweight("bold")
    ax.set_title("Protocol Distribution", fontsize=11, fontweight="bold", pad=10)


def chart_bandwidth(ax, df):
    bw = bandwidth_by_protocol(df)
    _bar(ax, bw / 1024, "Bandwidth by Protocol (KB)",
         "Protocol", "KB", color=GREEN)


def chart_top_talkers(ax, df):
    t = top_talkers(df, 8)
    series = pd.Series(t.iloc[:,1].values, index=t.iloc[:,0])
    _bar(ax, series, "Top Source IPs", "Packet Count", "", color=ORANGE, horizontal=True)


def chart_top_destinations(ax, df):
    t = top_destinations(df, 8)
    series = pd.Series(t.iloc[:,1].values, index=t.iloc[:,0])
    _bar(ax, series, "Top Destination IPs", "Packet Count", "", color=RED, horizontal=True)


def chart_traffic_timeline(ax, df):
    ts = traffic_over_time(df, freq="5s")
    ax.fill_between(ts.index, ts.values, color=ACCENT, alpha=0.3)
    ax.plot(ts.index, ts.values, color=ACCENT, linewidth=1.5)
    ax.set_title("Traffic Volume Over Time", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Time")
    ax.set_ylabel("Packets / 5s")
    ax.grid(True)
    ax.spines[["top","right"]].set_visible(False)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right", fontsize=7)


def chart_packet_size_hist(ax, df):
    ax.hist(df["length"], bins=30, color=PURPLE, edgecolor=DARK_BG, linewidth=0.5)
    ax.axvline(df["length"].mean(), color=ORANGE, linestyle="--", linewidth=1.5,
               label=f"Mean: {df['length'].mean():.0f}B")
    ax.set_title("Packet Size Distribution", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Bytes")
    ax.set_ylabel("Frequency")
    ax.legend(fontsize=8)
    ax.grid(axis="y")
    ax.spines[["top","right"]].set_visible(False)


def chart_port_heatmap(ax, df):
    top10 = port_activity(df, 10)
    colors = [ACCENT if p in (80,443,53,22) else SUBTEXT for p in top10.iloc[:,0]]
    bars = ax.bar(top10.iloc[:,0].astype(str), top10.iloc[:,1],
                  color=colors, edgecolor=DARK_BG, linewidth=0.5)
    ax.set_title("Top Destination Ports", fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel("Port")
    ax.set_ylabel("Count")
    ax.grid(axis="y")
    ax.spines[["top","right"]].set_visible(False)
    legend_patches = [
        mpatches.Patch(color=ACCENT,  label="Well-known port"),
        mpatches.Patch(color=SUBTEXT, label="Other port"),
    ]
    ax.legend(handles=legend_patches, fontsize=8)


# ── KPI strip ─────────────────────────────────────────────────────────────────

def draw_kpi_strip(fig, df):
    """Draw a row of KPI boxes at the top of the figure."""
    kpis = [
        ("Total Packets",    f"{len(df):,}",                  ACCENT),
        ("Total Bandwidth",  f"{total_bandwidth_mb(df):.2f} MB", GREEN),
        ("Avg Packet Size",  f"{avg_packet_size(df):.0f} B",  ORANGE),
        ("Protocols Seen",   str(df['protocol'].nunique()),    PURPLE),
        ("Unique Src IPs",   str(df['src_ip'].nunique()),      RED),
        ("Unique Dst IPs",   str(df['dst_ip'].nunique()),      "#ffa657"),
    ]
    strip_ax = fig.add_axes([0.02, 0.91, 0.96, 0.07])
    strip_ax.set_facecolor(DARK_BG)
    strip_ax.axis("off")

    w = 1 / len(kpis)
    for i, (label, value, color) in enumerate(kpis):
        x = i * w + w / 2
        strip_ax.text(x, 0.75, value, ha="center", va="center",
                      fontsize=13, fontweight="bold", color=color,
                      transform=strip_ax.transAxes)
        strip_ax.text(x, 0.18, label, ha="center", va="center",
                      fontsize=8, color=SUBTEXT,
                      transform=strip_ax.transAxes)


# ── Main dashboard ─────────────────────────────────────────────────────────────

def generate_dashboard(df: pd.DataFrame, output_dir: str = "screenshots"):
    os.makedirs(output_dir, exist_ok=True)

    fig = plt.figure(figsize=(20, 14), facecolor=DARK_BG)
    fig.suptitle(
        "🛡  Network Traffic Analyzer — Dashboard",
        fontsize=18, fontweight="bold", color=TEXT, y=0.99,
    )

    # KPI strip
    draw_kpi_strip(fig, df)

    # 3×3 grid (leaving top strip space)
    gs = gridspec.GridSpec(
        3, 3,
        figure=fig,
        top=0.90, bottom=0.05,
        left=0.05, right=0.97,
        hspace=0.45, wspace=0.35,
    )

    chart_protocol_pie(      fig.add_subplot(gs[0, 0]), df)
    chart_bandwidth(         fig.add_subplot(gs[0, 1]), df)
    chart_packet_size_hist(  fig.add_subplot(gs[0, 2]), df)
    chart_traffic_timeline(  fig.add_subplot(gs[1, :]), df)   # full-width row
    chart_top_talkers(       fig.add_subplot(gs[2, 0]), df)
    chart_top_destinations(  fig.add_subplot(gs[2, 1]), df)
    chart_port_heatmap(      fig.add_subplot(gs[2, 2]), df)

    out = os.path.join(output_dir, "dashboard.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=DARK_BG)
    plt.close(fig)
    print(f"[+] Dashboard saved → {out}")
    return out


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = load_data("traffic.csv")
    generate_dashboard(df)
