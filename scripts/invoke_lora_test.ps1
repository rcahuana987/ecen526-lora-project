param(
    [Parameter(Mandatory = $true)]
    [string]$TestName,

    [Parameter(Mandatory = $true)]
    [string]$PhaseFolder,

    [Parameter(Mandatory = $true)]
    [string]$Location,

    [Parameter(Mandatory = $true)]
    [string]$Distance,

    [Parameter(Mandatory = $true)]
    [string]$Condition,

    [Parameter(Mandatory = $true)]
    [int]$Duration,

    [string]$Notes = "",
    [string]$RxPort = "COM7",
    [int]$Baud = 115200,
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

function Resolve-PythonExe {
    param([string]$Preferred)

    if ($Preferred) {
        return $Preferred
    }

    $candidates = @(
        "C:\Users\rcahu\AppData\Local\Programs\Python\Python312\python.exe",
        "python",
        "py"
    )

    foreach ($candidate in $candidates) {
        if ($candidate -like "*\*") {
            if (Test-Path -LiteralPath $candidate) {
                return $candidate
            }
        }
        else {
            $command = Get-Command $candidate -ErrorAction SilentlyContinue
            if ($command) {
                return $command.Source
            }
        }
    }

    throw "Could not find a working Python interpreter."
}

$python = Resolve-PythonExe -Preferred $PythonExe
$repoRoot = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $repoRoot "data\$PhaseFolder"
$resultsDir = Join-Path $repoRoot "results\$PhaseFolder"
$baseOutFile = Join-Path $dataDir "$TestName.csv"

New-Item -ItemType Directory -Force -Path $dataDir | Out-Null
New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null

$outFile = $baseOutFile
if (Test-Path -LiteralPath $baseOutFile) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $outFile = Join-Path $dataDir "$TestName`_$timestamp.csv"
}

Write-Host ""
Write-Host "=========================================="
Write-Host "Running test: $TestName"
Write-Host "RX Port:      $RxPort"
Write-Host "Duration:     $Duration seconds"
Write-Host "Output:       $outFile"
if ($outFile -ne $baseOutFile) {
    Write-Host "Note:         Existing file found, saving this run with a timestamp."
}
Write-Host "Python:       $python"
Write-Host "=========================================="
Write-Host ""

$logArgs = @(
    "scripts\log_rx.py",
    "--port", $RxPort,
    "--baud", $Baud,
    "--out", $outFile,
    "--test", $TestName,
    "--location", $Location,
    "--distance", $Distance,
    "--condition", $Condition,
    "--notes", "`"$Notes`""
)

$logProcess = Start-Process -FilePath $python `
    -ArgumentList $logArgs `
    -WorkingDirectory $repoRoot `
    -NoNewWindow `
    -PassThru

Start-Sleep -Seconds $Duration

if (-not $logProcess.HasExited) {
    Stop-Process -Id $logProcess.Id -Force
}

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Single-run analysis:"
& $python (Join-Path $repoRoot "scripts\analyze_lora_csv.py") --file $outFile

Write-Host ""
Write-Host "Updating summary..."
& $python (Join-Path $repoRoot "scripts\summarize_all_runs.py") --input_dir $dataDir --out (Join-Path $resultsDir "summary.csv")

Write-Host ""
Write-Host "Updating plots..."
& $python (Join-Path $repoRoot "scripts\plot_lora_results.py") --summary (Join-Path $resultsDir "summary.csv") --out_dir $resultsDir

Write-Host ""
Write-Host "Completed: $TestName"
Write-Host ""
