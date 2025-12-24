<#
Start script for isolated Ollama container serving gemma3:1b.
Runs docker-compose up -d and ensures the model is pulled into the container's data dir.
Requires: Docker Desktop running.
#>

param(
    [string] $Model = 'gemma3:1b'
)

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Output "Bringing up container (background)..."
docker compose up -d

Write-Output "Waiting for the service to become healthy (give it a few seconds)..."
Start-Sleep -Seconds 3

$container = 'ollama-gemma1b'

# Wait until the Ollama HTTP endpoint responds
$deadline = (Get-Date).AddMinutes(3)
while ((Get-Date) -lt $deadline) {
    try {
        $ok = Invoke-RestMethod -Uri 'http://127.0.0.1:11436/v1/models' -Method Get -TimeoutSec 5 -ErrorAction Stop
        break
    } catch {
        Write-Output "Waiting for Ollama HTTP endpoint..."
        Start-Sleep -Seconds 2
    }
}

Write-Output "Checking if model '$Model' is available inside the service..."
$modelsText = ''
try {
    $modelsText = docker exec $container /usr/bin/ollama ls 2>$null
} catch {
    Write-Warning "Could not run 'ollama ls' inside container: $_"
}

if ($modelsText -and $modelsText -match $Model) {
    Write-Output "Model $Model already present; skipping pull."
} else {
    Write-Warning "Model $Model not present in container. Because the host models path is mounted read-only, the container cannot pull new models into the host directory."
    Write-Output "If you want the container to pull models, change the mount in docker-compose.yml to ':rw' or pull the model on the host Ollama installation."
}

# Ensure a small lightweight model is warmed for fast responses if present
Write-Output "Attempting warm-up using any available small model (gemma3:270m preferred)..."
try {
    $body = @{ model = 'gemma3:270m'; prompt = "Warmup: please reply briefly 'warm'"; max_tokens = 8 } | ConvertTo-Json
    $resp = Invoke-RestMethod -Uri 'http://127.0.0.1:11436/v1/completions' -Method POST -ContentType 'application/json' -Body $body -TimeoutSec 60 -ErrorAction Stop
    Write-Output "Warm-up response:"
    $resp | ConvertTo-Json -Depth 3
} catch {
    Write-Warning "Warm-up failed or gemma3:270m not present: $_"
}

Write-Output "Done. The isolated Ollama instance is available at http://127.0.0.1:11436/v1"
