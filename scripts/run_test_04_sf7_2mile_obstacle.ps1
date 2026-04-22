param(
    [string]$RxPort = "COM5",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "04_sftrade_2mile_obstacle_sf7_bw125_cr45_p14_run1" `
    -PhaseFolder "04_sf_tradeoff" `
    -Location "longrange" `
    -Distance "3219" `
    -Condition "obstacle" `
    -Duration 45 `
    -Notes "2 mile obstacle SF7 tradeoff" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
