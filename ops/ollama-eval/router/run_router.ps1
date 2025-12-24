param(
    [int] $Port = 8000
)

Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Path -Parent)

Write-Host "Running warm-up against Ollama models..."
python .\warmup.py

Write-Host "Starting router on port $Port"
uvicorn app:app --host 127.0.0.1 --port $Port --log-level info
