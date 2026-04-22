param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

Write-Host "Part 2 now uses only the long obstacle-path tests."
Write-Host "Flash both TX and RX with SF12 firmware before running this phase."
Write-Host ""
Read-Host "Press Enter after the boards are flashed and ready"

& (Join-Path $PSScriptRoot "run_test_02_distance_1mile_obstacle.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

& (Join-Path $PSScriptRoot "run_test_02_distance_2mile_obstacle.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
