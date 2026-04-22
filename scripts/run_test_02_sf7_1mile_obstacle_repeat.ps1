param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "02_sftrade_1mile_obstacle_sf7_bw125_cr45_p14_run2" `
    -PhaseFolder "02_sf_tradeoff" `
    -Location "longrange" `
    -Distance "1609" `
    -Condition "obstacle_repeat" `
    -Duration 45 `
    -Notes "1 mile obstacle SF7 repeat" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

