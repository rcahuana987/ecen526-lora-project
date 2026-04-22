param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
    -TestName "03_obstacle_corner_sf7_bw125_cr45_p14_run1" `
    -PhaseFolder "03_obstacle_tests" `
    -Location "hallway" `
    -Distance "10" `
    -Condition "corner" `
    -Duration 60 `
    -Notes "corner obstacle" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
