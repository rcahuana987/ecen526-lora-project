import argparse
import csv
from datetime import datetime
import serial

def main():
    parser = argparse.ArgumentParser(description="Log LoRa RX serial output to CSV.")
    parser.add_argument("--port", required=True, help="Serial port, e.g. COM7")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--out", required=True, help="Output CSV file")
    parser.add_argument("--test", default="", help="Test name")
    parser.add_argument("--location", default="", help="Location name")
    parser.add_argument("--distance", default="", help="Distance in meters")
    parser.add_argument("--condition", default="", help="LOS / wall / corner")
    parser.add_argument("--notes", default="", help="Optional notes")
    args = parser.parse_args()

    print(f"Opening serial port {args.port} at {args.baud} baud...")
    ser = serial.Serial(args.port, args.baud, timeout=1)

    print(f"Logging from {args.port} to {args.out}")
    print("Press Ctrl+C to stop.\n")

    header_written = False

    with open(args.out, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        try:
            while True:
                raw = ser.readline().decode(errors="ignore").strip()
                if not raw:
                    continue

                print(raw)

                if raw.startswith("time_ms,seq,"):
                    if not header_written:
                        base_header = raw.split(",")
                        full_header = base_header + [
                            "pc_timestamp",
                            "test_name",
                            "location",
                            "distance_m",
                            "condition",
                            "notes",
                        ]
                        writer.writerow(full_header)
                        csv_file.flush()
                        header_written = True
                    continue

                if not raw[0].isdigit():
                    continue

                parts = raw.split(",")
                if len(parts) < 11:
                    continue

                row = parts + [
                    datetime.now().isoformat(timespec="seconds"),
                    args.test,
                    args.location,
                    args.distance,
                    args.condition,
                    args.notes,
                ]
                writer.writerow(row)
                csv_file.flush()

        except KeyboardInterrupt:
            print("\nStopped logging.")
        finally:
            ser.close()

if __name__ == "__main__":
    main()