param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "04_sftrade_1mile_obstacle_sf12_bw125_cr45_p14_run1" `
    -PhaseFolder "04_sf_tradeoff" `
    -Location "longrange" `
    -Distance "1609" `
    -Condition "obstacle" `
    -Duration 45 `
    -Notes "1 mile obstacle SF12 tradeoff" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
