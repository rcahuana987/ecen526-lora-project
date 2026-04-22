param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "run_test_01_bringup.ps1") -RxPort $RxPort -Baud $Baud -PythonExe $PythonExe
& (Join-Path $PSScriptRoot "run_test_03_obstacles_sf7.ps1") -RxPort $RxPort -Baud $Baud -PythonExe $PythonExe

Write-Host "Pause before phase 4 if you need to reflash TX and RX for SF changes."
Write-Host ""

& (Join-Path $PSScriptRoot "run_test_04_sf_tradeoff.ps1") -RxPort $RxPort -Baud $Baud -PythonExe $PythonExe
