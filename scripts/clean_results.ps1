param(
    [string]$ResultsDir = "..\results",
    [switch]$DryRun
)

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$resultsPath = Join-Path $scriptRoot $ResultsDir
$resolvedResultsDir = Resolve-Path -LiteralPath $resultsPath -ErrorAction Stop
$targetDir = $resolvedResultsDir.Path

$filesToDelete = Get-ChildItem -LiteralPath $targetDir -Recurse -File |
    Where-Object { $_.Extension -in @(".png", ".csv") }

if (-not $filesToDelete) {
    Write-Host "No .png or .csv files found under $targetDir"
    exit 0
}

Write-Host "Found $($filesToDelete.Count) generated file(s) under $targetDir"

foreach ($file in $filesToDelete) {
    if ($DryRun) {
        Write-Host "[dry-run] Would remove $($file.FullName)"
    }
    else {
        Remove-Item -LiteralPath $file.FullName
        Write-Host "Removed $($file.FullName)"
    }
}

if ($DryRun) {
    Write-Host "Dry run complete. No files were deleted."
}
else {
    Write-Host "Cleanup complete."
}
