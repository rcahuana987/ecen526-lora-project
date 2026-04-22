param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "02_sftrade_2mile_obstacle_sf10_bw125_cr45_p14_run1" `
    -PhaseFolder "02_sf_tradeoff" `
    -Location "longrange" `
    -Distance "3219" `
    -Condition "obstacle" `
    -Duration 45 `
    -Notes "2 mile obstacle SF10 tradeoff" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe

