param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "01_bringup_hallway_10m_los_sf7_bw125_cr45_p14_run1" `
    -PhaseFolder "01_bringup" `
    -Location "hallway" `
    -Distance "10" `
    -Condition "LOS" `
    -Duration 30 `
    -Notes "hallway validation" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
