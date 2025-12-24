Param(
    [switch]$Force
)

# Remove models from the container that are also present in the host models directory
$ErrorActionPreference = 'Stop'

$containerName = 'ollama-gemma1b'
$hostModelsDir = 'A:\models\ollama_models'

Write-Output "Listing models in container '$containerName'..."
$raw = docker exec $containerName /usr/bin/ollama ls 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to run 'ollama ls' in container. Output:`n$raw"
    exit 1
}

$containerModels = $raw -split "`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -and ($_ -notmatch '^(NAME|$)') } | ForEach-Object { ($_ -split '\s+')[0] } | Select-Object -Unique

Write-Output "Found container models: $($containerModels -join ', ')"

if (-not (Test-Path $hostModelsDir)) {
    Write-Warning "Host models directory '$hostModelsDir' not found. Nothing to compare."
    exit 0
}

Write-Output "Listing directories in host models directory '$hostModelsDir'..."
$hostModels = Get-ChildItem -Path $hostModelsDir -Directory -ErrorAction SilentlyContinue | ForEach-Object { $_.Name } | Select-Object -Unique

Write-Output "Found host models: $($hostModels -join ', ')"

$toRemove = @()
foreach ($m in $containerModels) {
    if ($hostModels -contains $m) { $toRemove += $m }
}

if (-not $toRemove -or $toRemove.Count -eq 0) {
    Write-Output "No duplicate models found between host and container. Nothing to remove."
    exit 0
}

Write-Output "Duplicate models detected (will remove from container): $($toRemove -join ', ')"

if (-not $Force) {
    Write-Output "Run this script with -Force to actually remove the listed models."
    exit 0
}

foreach ($m in $toRemove) {
    Write-Output "Removing model '$m' from container..."
    docker exec $containerName /usr/bin/ollama rm $m
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Failed to remove model $m (exit $LASTEXITCODE). Continuing."
    } else {
        Write-Output "Removed $m"
    }
}

Write-Output "Cleanup complete."
