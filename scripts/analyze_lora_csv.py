import argparse
import pandas as pd


def cr_value_from_code(cr_code: int) -> int:
    return max(1, int(cr_code) - 4)


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
    gaps = seq.diff().dropna() - 1
    bursts = gaps[gaps > 0]
    if bursts.empty:
        return 0, 0, 0.0
    return int(len(bursts)), int(bursts.max()), float(bursts.mean())


def summarize_interarrival(time_series: pd.Series):
    time_ms = pd.to_numeric(time_series, errors="coerce").dropna().sort_values()
    interarrival_ms = time_ms.diff().dropna()
    if interarrival_ms.empty:
        return float("nan"), float("nan")
    return float(interarrival_ms.mean()), float(interarrival_ms.std())


def main():
    parser = argparse.ArgumentParser(description="Analyze LoRa CSV log.")
    parser.add_argument("--file", required=True, help="CSV file to analyze")
    args = parser.parse_args()

    df = pd.read_csv(args.file)

    if df.empty:
        print("CSV file is empty.")
        return

    received = len(df)
    first_seq = int(df["seq"].min())
    last_seq = int(df["seq"].max())
    sent_est = last_seq - first_seq + 1
    missed_est = sent_est - received
    prr = received / sent_est if sent_est > 0 else 0.0

    duration_s = (df["time_ms"].max() - df["time_ms"].min()) / 1000.0
    payload_bytes = df["payload_len"].mean()
    goodput_bps = (received * payload_bytes) / duration_s if duration_s > 0 else 0.0
    sf = int(round(df["sf"].mean()))
    bw_hz = float(df["bw_khz"].mean()) * 1000.0
    cr = int(round(df["cr"].mean()))
    phy_bitrate_bps = lora_phy_bitrate_bps(sf, bw_hz, cr)
    loss_burst_count, max_loss_burst_packets, mean_loss_burst_packets = summarize_loss_bursts(df["seq"])
    mean_interarrival_ms, std_interarrival_ms = summarize_interarrival(df["time_ms"])

    print(f"File: {args.file}")
    print(f"Received packets: {received}")
    print(f"Estimated sent packets: {sent_est}")
    print(f"Estimated missed packets: {missed_est}")
    print(f"PRR: {prr:.3f}")
    print(f"Duration (s): {duration_s:.2f}")
    print(f"Average payload bytes: {payload_bytes:.2f}")
    print(f"Goodput (bytes/s): {goodput_bps:.2f}")
    print(f"PHY data rate (bps): {phy_bitrate_bps:.2f}")
    print(f"Mean RSSI (dBm): {df['rssi_dbm'].mean():.2f}")
    print(f"Median RSSI (dBm): {percentile(df['rssi_dbm'], 0.50):.2f}")
    print(f"RSSI p10/p90 (dBm): {percentile(df['rssi_dbm'], 0.10):.2f} / {percentile(df['rssi_dbm'], 0.90):.2f}")
    print(f"Mean SNR (dB): {df['snr_db'].mean():.2f}")
    print(f"Median SNR (dB): {percentile(df['snr_db'], 0.50):.2f}")
    print(f"SNR p10/p90 (dB): {percentile(df['snr_db'], 0.10):.2f} / {percentile(df['snr_db'], 0.90):.2f}")
    print(f"Loss burst count: {loss_burst_count}")
    print(f"Max loss burst (packets): {max_loss_burst_packets}")
    print(f"Mean loss burst (packets): {mean_loss_burst_packets:.2f}")
    print(f"Mean inter-arrival (ms): {mean_interarrival_ms:.2f}")
    print(f"Inter-arrival std (ms): {std_interarrival_ms:.2f}")

if __name__ == "__main__":
    main()
