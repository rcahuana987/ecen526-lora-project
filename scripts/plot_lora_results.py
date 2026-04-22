import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def save_plot(fig, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def plot_prr_vs_distance(df, out_dir):
    plot_df = df.copy()
    plot_df["distance_m"] = pd.to_numeric(plot_df["distance_m"], errors="coerce")
    plot_df = plot_df.dropna(subset=["distance_m", "prr", "sf"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    for sf in sorted(plot_df["sf"].unique()):
        sf_df = plot_df[plot_df["sf"] == sf].sort_values("distance_m")
        ax.plot(sf_df["distance_m"], sf_df["prr"], marker="o", label=f"SF{sf}")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("PRR")
    ax.set_title("PRR vs Distance")
    ax.grid(True)
    ax.legend()
    save_plot(fig, out_dir / "prr_vs_distance.png")

def plot_rssi_vs_distance(df, out_dir):
    plot_df = df.copy()
    plot_df["distance_m"] = pd.to_numeric(plot_df["distance_m"], errors="coerce")
    plot_df = plot_df.dropna(subset=["distance_m", "mean_rssi_dbm", "sf"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    for sf in sorted(plot_df["sf"].unique()):
        sf_df = plot_df[plot_df["sf"] == sf].sort_values("distance_m")
        ax.plot(sf_df["distance_m"], sf_df["mean_rssi_dbm"], marker="o", label=f"SF{sf}")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Mean RSSI (dBm)")
    ax.set_title("RSSI vs Distance")
    ax.grid(True)
    ax.legend()
    save_plot(fig, out_dir / "rssi_vs_distance.png")


def plot_prr_vs_sf(df, out_dir):
    plot_df = df.dropna(subset=["sf", "prr"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    grouped = plot_df.groupby("sf", as_index=False)["prr"].mean()
    ax.plot(grouped["sf"], grouped["prr"], marker="o")
    ax.set_xlabel("Spreading Factor")
    ax.set_ylabel("PRR")
    ax.set_title("PRR vs SF")
    ax.grid(True)
    save_plot(fig, out_dir / "prr_vs_sf.png")


def plot_goodput_vs_airtime(df, out_dir):
    plot_df = df.dropna(subset=["airtime_ms", "goodput_Bps", "sf"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    for sf in sorted(plot_df["sf"].unique()):
        sf_df = plot_df[plot_df["sf"] == sf]
        ax.scatter(sf_df["airtime_ms"], sf_df["goodput_Bps"], label=f"SF{sf}")
    ax.set_xlabel("Airtime per Packet (ms)")
    ax.set_ylabel("Goodput (bytes/s)")
    ax.set_title("Goodput vs Airtime")
    ax.grid(True)
    ax.legend()
    save_plot(fig, out_dir / "goodput_vs_airtime.png")


def plot_prr_vs_occupancy(df, out_dir):
    plot_df = df.dropna(subset=["occupancy", "prr", "sf"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    for sf in sorted(plot_df["sf"].unique()):
        sf_df = plot_df[plot_df["sf"] == sf]
        ax.scatter(sf_df["occupancy"], sf_df["prr"], label=f"SF{sf}")
    ax.set_xlabel("Occupancy")
    ax.set_ylabel("PRR")
    ax.set_title("PRR vs Occupancy")
    ax.grid(True)
    ax.legend()
    save_plot(fig, out_dir / "prr_vs_occupancy.png")


def plot_snr_percentiles_vs_distance(df, out_dir):
    plot_df = df.copy()
    plot_df["distance_m"] = pd.to_numeric(plot_df["distance_m"], errors="coerce")
    plot_df = plot_df.dropna(subset=["distance_m", "p10_snr_db", "median_snr_db", "p90_snr_db", "sf"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    for sf in sorted(plot_df["sf"].unique()):
        sf_df = plot_df[plot_df["sf"] == sf].sort_values("distance_m")
        ax.plot(sf_df["distance_m"], sf_df["median_snr_db"], marker="o", label=f"SF{sf} median")
        ax.fill_between(sf_df["distance_m"], sf_df["p10_snr_db"], sf_df["p90_snr_db"], alpha=0.15)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("SNR (dB)")
    ax.set_title("SNR Percentiles vs Distance")
    ax.grid(True)
    ax.legend()
    save_plot(fig, out_dir / "snr_percentiles_vs_distance.png")


def plot_loss_burst_vs_sf(df, out_dir):
    plot_df = df.dropna(subset=["sf", "max_loss_burst_packets"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    grouped = plot_df.groupby("sf", as_index=False)["max_loss_burst_packets"].mean()
    ax.bar(grouped["sf"].astype(str), grouped["max_loss_burst_packets"])
    ax.set_xlabel("Spreading Factor")
    ax.set_ylabel("Mean Max Loss Burst (packets)")
    ax.set_title("Loss Burst Severity vs SF")
    ax.grid(True, axis="y")
    save_plot(fig, out_dir / "loss_burst_vs_sf.png")


def plot_interarrival_jitter_vs_sf(df, out_dir):
    plot_df = df.dropna(subset=["sf", "std_interarrival_ms"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    grouped = plot_df.groupby("sf", as_index=False)["std_interarrival_ms"].mean()
    ax.bar(grouped["sf"].astype(str), grouped["std_interarrival_ms"])
    ax.set_xlabel("Spreading Factor")
    ax.set_ylabel("Mean Inter-arrival Std (ms)")
    ax.set_title("Timing Jitter vs SF")
    ax.grid(True, axis="y")
    save_plot(fig, out_dir / "interarrival_jitter_vs_sf.png")


def plot_goodput_vs_phy_bitrate(df, out_dir):
    plot_df = df.dropna(subset=["phy_bitrate_bps", "goodput_Bps", "sf"])
    if plot_df.empty:
        return

    fig, ax = plt.subplots(figsize=(7, 4))
    for sf in sorted(plot_df["sf"].unique()):
        sf_df = plot_df[plot_df["sf"] == sf]
        ax.scatter(sf_df["phy_bitrate_bps"], sf_df["goodput_Bps"], label=f"SF{sf}")
    ax.set_xlabel("PHY Data Rate (bps)")
    ax.set_ylabel("Goodput (bytes/s)")
    ax.set_title("Goodput vs PHY Data Rate")
    ax.grid(True)
    ax.legend()
    save_plot(fig, out_dir / "goodput_vs_phy_bitrate.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", required=True)
    parser.add_argument("--out_dir", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.summary)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    plot_prr_vs_distance(df, out_dir)
    plot_rssi_vs_distance(df, out_dir)
    plot_prr_vs_sf(df, out_dir)
    plot_goodput_vs_airtime(df, out_dir)
    plot_prr_vs_occupancy(df, out_dir)
    plot_snr_percentiles_vs_distance(df, out_dir)
    plot_loss_burst_vs_sf(df, out_dir)
    plot_interarrival_jitter_vs_sf(df, out_dir)
    plot_goodput_vs_phy_bitrate(df, out_dir)

    print(f"Saved plots to {out_dir}")

if __name__ == "__main__":
    main()
