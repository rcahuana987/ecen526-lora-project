param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "02_distance_hallway_10m_sf7_bw125_cr45_p14_run1" `
    -PhaseFolder "02_distance_sweep" `
    -Location "hallway" `
    -Distance "10" `
    -Condition "LOS" `
    -Duration 60 `
    -Notes "hallway 10m LOS" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
