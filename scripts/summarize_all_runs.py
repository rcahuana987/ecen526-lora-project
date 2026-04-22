import argparse
import math
from pathlib import Path
import pandas as pd


def cr_value_from_code(cr_code: int) -> int:
    return max(1, int(cr_code) - 4)


def lora_airtime_ms(payload_bytes, sf, bw_hz, cr_code, preamble=8, crc=1, explicit_header=1):
    sf = int(sf)
    bw_hz = float(bw_hz)
    cr = cr_value_from_code(cr_code)
    de = 1 if (sf >= 11 and bw_hz <= 125000) else 0
    ih = 0 if explicit_header else 1
    crc_val = 1 if crc else 0

    t_sym = (2 ** sf) / bw_hz
    t_preamble = (preamble + 4.25) * t_sym

    numerator = 8 * payload_bytes - 4 * sf + 28 + 16 * crc_val - 20 * ih
    denominator = 4 * (sf - 2 * de)
    payload_symb_nb = 8 + max(math.ceil(numerator / denominator) * (cr + 4), 0)

    t_payload = payload_symb_nb * t_sym
    return (t_preamble + t_payload) * 1000.0


def lora_phy_bitrate_bps(sf, bw_hz, cr_code):
    sf = int(sf)
    bw_hz = float(bw_hz)
    cr = cr_value_from_code(cr_code)
    coding_rate_factor = 4.0 / (4.0 + cr)
    symbol_rate = bw_hz / (2 ** sf)
    return sf * symbol_rate * coding_rate_factor


def percentile(series: pd.Series, q: float):
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return float("nan")
    return float(clean.quantile(q))


def summarize_loss_bursts(seq_series: pd.Series):
    seq = pd.to_numeric(seq_series, errors="coerce").dropna().astype(int).sort_values()
    if seq.empty:
        return {
            "loss_burst_count": 0,
            "mean_loss_burst_packets": 0.0,
            "max_loss_burst_packets": 0,
            "total_loss_burst_packets": 0,
        }

    gaps = seq.diff().dropna() - 1
    bursts = gaps[gaps > 0]

    if bursts.empty:
        return {
            "loss_burst_count": 0,
            "mean_loss_burst_packets": 0.0,
            "max_loss_burst_packets": 0,
            "total_loss_burst_packets": 0,
        }

    return {
        "loss_burst_count": int(len(bursts)),
        "mean_loss_burst_packets": float(bursts.mean()),
        "max_loss_burst_packets": int(bursts.max()),
        "total_loss_burst_packets": int(bursts.sum()),
    }


def summarize_interarrival(time_series: pd.Series):
    time_ms = pd.to_numeric(time_series, errors="coerce").dropna().sort_values()
    interarrival_ms = time_ms.diff().dropna()

    if interarrival_ms.empty:
        return {
            "mean_interarrival_ms": float("nan"),
            "std_interarrival_ms": float("nan"),
            "min_interarrival_ms": float("nan"),
            "max_interarrival_ms": float("nan"),
        }

    return {
        "mean_interarrival_ms": float(interarrival_ms.mean()),
        "std_interarrival_ms": float(interarrival_ms.std()),
        "min_interarrival_ms": float(interarrival_ms.min()),
        "max_interarrival_ms": float(interarrival_ms.max()),
    }


def summarize_file(csv_path: Path):
    df = pd.read_csv(csv_path)
    if df.empty:
        return None

    received = len(df)
    first_seq = int(df["seq"].min())
    last_seq = int(df["seq"].max())
    sent_est = last_seq - first_seq + 1
    missed_est = sent_est - received
    prr = received / sent_est if sent_est > 0 else 0.0

    duration_s = (df["time_ms"].max() - df["time_ms"].min()) / 1000.0
    payload_bytes = float(df["payload_len"].mean())
    goodput_Bps = (received * payload_bytes) / duration_s if duration_s > 0 else 0.0
    pkt_rate_hz = sent_est / duration_s if duration_s > 0 else 0.0

    sf = int(round(df["sf"].mean()))
    bw_khz = float(df["bw_khz"].mean())
    bw_hz = bw_khz * 1000.0
    cr = int(round(df["cr"].mean()))
    tx_power_dbm = float(df["tx_power_dbm"].mean())

    airtime_ms = lora_airtime_ms(payload_bytes, sf, bw_hz, cr)
    phy_bitrate_bps = lora_phy_bitrate_bps(sf, bw_hz, cr)
    occupancy = (airtime_ms / 1000.0) * pkt_rate_hz
    efficiency_Bps_per_occ = goodput_Bps / occupancy if occupancy > 0 else float("nan")
    loss_bursts = summarize_loss_bursts(df["seq"])
    interarrival = summarize_interarrival(df["time_ms"])

    row = {
        "file": csv_path.name,
        "test_name": df["test_name"].iloc[0] if "test_name" in df.columns else "",
        "location": df["location"].iloc[0] if "location" in df.columns else "",
        "distance_m": df["distance_m"].iloc[0] if "distance_m" in df.columns else "",
        "condition": df["condition"].iloc[0] if "condition" in df.columns else "",
        "received_packets": received,
        "estimated_sent_packets": sent_est,
        "estimated_missed_packets": missed_est,
        "prr": prr,
        "duration_s": duration_s,
        "payload_bytes": payload_bytes,
        "goodput_Bps": goodput_Bps,
        "packet_rate_hz": pkt_rate_hz,
        "sf": sf,
        "bw_khz": bw_khz,
        "cr": cr,
        "tx_power_dbm": tx_power_dbm,
        "mean_rssi_dbm": df["rssi_dbm"].mean(),
        "median_rssi_dbm": percentile(df["rssi_dbm"], 0.50),
        "p10_rssi_dbm": percentile(df["rssi_dbm"], 0.10),
        "p90_rssi_dbm": percentile(df["rssi_dbm"], 0.90),
        "min_rssi_dbm": pd.to_numeric(df["rssi_dbm"], errors="coerce").min(),
        "max_rssi_dbm": pd.to_numeric(df["rssi_dbm"], errors="coerce").max(),
        "mean_snr_db": df["snr_db"].mean(),
        "median_snr_db": percentile(df["snr_db"], 0.50),
        "p10_snr_db": percentile(df["snr_db"], 0.10),
        "p90_snr_db": percentile(df["snr_db"], 0.90),
        "min_snr_db": pd.to_numeric(df["snr_db"], errors="coerce").min(),
        "max_snr_db": pd.to_numeric(df["snr_db"], errors="coerce").max(),
        "phy_bitrate_bps": phy_bitrate_bps,
        "airtime_ms": airtime_ms,
        "occupancy": occupancy,
        "efficiency_Bps_per_occ": efficiency_Bps_per_occ,
    }
    row.update(loss_bursts)
    row.update(interarrival)
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    rows = []
    for csv_path in sorted(Path(args.input_dir).glob("*.csv")):
        row = summarize_file(csv_path)
        if row is not None:
            rows.append(row)

    if not rows:
        print("No valid CSV files found.")
        return

    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(args.out, index=False)
    print(f"Saved summary to {args.out}")
    print(
        summary_df[
            [
                "file",
                "distance_m",
                "condition",
                "sf",
                "prr",
                "goodput_Bps",
                "mean_rssi_dbm",
                "mean_snr_db",
                "phy_bitrate_bps",
                "airtime_ms",
                "occupancy",
                "loss_burst_count",
                "max_loss_burst_packets",
                "std_interarrival_ms",
            ]
        ]
    )

if __name__ == "__main__":
    main()
