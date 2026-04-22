param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "01_bringup_desk_2m_los_sf7_bw125_cr45_p14_run1" `
    -PhaseFolder "01_bringup" `
    -Location "desk" `
    -Distance "2" `
    -Condition "LOS" `
    -Duration 30 `
    -Notes "baseline desk validation" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
