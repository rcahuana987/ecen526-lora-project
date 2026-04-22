param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "02_distance_obstacle_1mile_sf12_bw125_cr45_p14_run1" `
    -PhaseFolder "02_distance_sweep" `
    -Location "longrange" `
    -Distance "1609" `
    -Condition "obstacle" `
    -Duration 60 `
    -Notes "1 mile obstacle path SF12" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
