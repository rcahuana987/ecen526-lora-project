# ECEN 526 LoRa Range Characterization Project

This repository contains the code, experiment data, analysis outputs, and report source for an ECEN 526 course project on point-to-point LoRa link characterization at 915 MHz.

The project evaluates how spreading factor affects reliability and throughput on short line-of-sight links and longer obstructed links. The completed dataset in this repo covers two phases:

- `01_bringup`: short-range validation runs at 2 m and 10 m
- `02_sf_tradeoff`: long-range obstructed runs comparing SF7, SF10, and SF12 at roughly 1 mile and 2 miles

## Repository layout

- `firmware/`: Arduino sketches for TX and RX nodes
- `scripts/`: PowerShell and Python utilities for running experiments and summarizing logs
- `data/`: raw CSV logs from completed experiments
- `results/`: generated summaries and plots for completed experiments
- `test_lists/`: CSV definitions for the completed automated experiment phases
- `notes/`: project notes and experiment workflow
- `report/`: LaTeX source for the final written report

## Main workflow

1. Flash matching TX/RX firmware for the target spreading factor.
2. Run a phase script from `scripts/`.
3. Log receiver output to CSV in `data/`.
4. Generate summary tables and plots in `results/`.

Useful entry points:

- `scripts/run_test_01_bringup.ps1`
- `scripts/run_test_02_sf_tradeoff.ps1`
- `scripts/run_test_all_phases.ps1`

## Analysis outputs

The summary pipeline computes:

- packet reception ratio (PRR)
- estimated missed packets
- goodput
- RSSI and SNR statistics
- PHY bitrate and airtime
- occupancy
- burst-loss statistics
- inter-arrival jitter

## Report

The report source is in `report/final_report.tex`.

Before submission, update:

- the author line if the project has more than one author

## Notes

- The repository was cleaned to keep only completed phases with real logged data.
- Incomplete distance-sweep and obstacle-only planning artifacts were intentionally removed.
