param(
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "invoke_test_list.ps1") `
    -TestList "test_lists\03_obstacles_sf7.csv" `
    -RxPort $RxPort `
    -Baud $Baud `
    -PythonExe $PythonExe
