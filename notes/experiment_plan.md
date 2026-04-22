# Reduced-Scope LoRa Experiment Plan

## Hardware setup
- RX board stays with laptop
- TX board runs from a power bank
- RX logs CSV over USB serial
- TX only needs power once flashed

## Common defaults
- Frequency: 915 MHz
- Bandwidth: 125 kHz
- Coding rate: 4/5
- TX power: 14 dBm
- Payload: 20 bytes
- Packet rate: 5 packets/sec
- RX port: COM7

## Command format
Run commands from the project root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\<script_name>.ps1
```

Override the RX serial port if needed:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\<script_name>.ps1 -RxPort COM7
```

## Part 1 - Bring-up
- desk, 2 m, LOS, SF7, 30 sec
- hallway, 10 m, LOS, SF7, 30 sec

Status:
- completed

Commands:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_test_01_bringup.ps1
```

## Part 2 - SF tradeoff
Run long-range comparisons with 45-second tests:
- 1 mile obstacle, SF7
- 1 mile obstacle repeat, SF7
- 2 miles obstacle, SF7
- 1 mile obstacle, SF10
- 1 mile obstacle repeat, SF10
- 2 miles obstacle, SF10
- 1 mile obstacle, SF12
- 1 mile obstacle repeat, SF12
- 2 miles obstacle, SF12

What this covers:
- SF tradeoff at the same path difficulty
- repeatability at 1 mile obstacle
- harder-link comparison between 1 mile and 2 miles obstacle

Status:
- completed

Commands for each experiment:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf7_1mile_obstacle.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf7_1mile_obstacle_repeat.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf7_2mile_obstacle.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf10_1mile_obstacle.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf10_1mile_obstacle_repeat.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf10_2mile_obstacle.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf12_1mile_obstacle.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf12_1mile_obstacle_repeat.ps1
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf12_2mile_obstacle.ps1
```

Command for the whole phase:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_test_02_sf_tradeoff.ps1
```

Important:
- flash both boards to SF7 before the SF7 group
- reflash both boards to SF10 before the SF10 group
- reflash both boards to SF12 before the SF12 group

Command for all active phases in sequence:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\run_test_all_phases.ps1
```

## Workflow
1. Flash TX and RX.
2. Close Arduino Serial Monitor.
3. Keep RX on the laptop.
4. Power TX from the power bank.
5. Open PowerShell in the project root.
6. Run the command for the current experiment or phase.
7. Wait for the script to finish.
8. Confirm the CSV was saved under `data/<phase>/`.
9. Confirm the updated summary and plots were saved under `results/<phase>/`.
