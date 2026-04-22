param(
    [Parameter(Mandatory = $true)]
    [string]$TestList,

    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$testListPath = Join-Path $repoRoot $TestList

if (-not (Test-Path -LiteralPath $testListPath)) {
    throw "Test list not found: $testListPath"
}

$rows = Import-Csv -LiteralPath $testListPath
if (-not $rows) {
    throw "No tests found in $testListPath"
}

foreach ($row in $rows) {
    & (Join-Path $PSScriptRoot "invoke_lora_test.ps1") `
        -TestName $row.test_name `
        -PhaseFolder $row.phase_folder `
        -Location $row.location `
        -Distance $row.distance_m `
        -Condition $row.condition `
        -Duration ([int]$row.duration_s) `
        -Notes "$($row.location) $($row.condition) validation" `
        -RxPort $RxPort `
        -Baud $Baud `
        -PythonExe $PythonExe
}
