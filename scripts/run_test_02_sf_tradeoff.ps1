param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

Write-Host "Part 2 compares 1-mile obstacle, repeated 1-mile obstacle, and 2-mile obstacle paths."
Write-Host "Flash both TX and RX to SF7 before starting."
Write-Host ""

Read-Host "Press Enter when the boards are flashed and ready for SF7"

& (Join-Path $PSScriptRoot "run_test_02_sf7_1mile_obstacle.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

& (Join-Path $PSScriptRoot "run_test_02_sf7_1mile_obstacle_repeat.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

& (Join-Path $PSScriptRoot "run_test_02_sf7_2mile_obstacle.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

Write-Host ""
Write-Host "Reflash both TX and RX to SF10 before continuing."
Read-Host "Press Enter when the boards are flashed and ready for SF10"

& (Join-Path $PSScriptRoot "run_test_02_sf10_1mile_obstacle.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

& (Join-Path $PSScriptRoot "run_test_02_sf10_1mile_obstacle_repeat.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

& (Join-Path $PSScriptRoot "run_test_02_sf10_2mile_obstacle.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

Write-Host ""
Write-Host "Reflash both TX and RX to SF12 before continuing."
Read-Host "Press Enter when the boards are flashed and ready for SF12"

& (Join-Path $PSScriptRoot "run_test_02_sf12_1mile_obstacle.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

& (Join-Path $PSScriptRoot "run_test_02_sf12_1mile_obstacle_repeat.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

& (Join-Path $PSScriptRoot "run_test_02_sf12_2mile_obstacle.ps1") `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

