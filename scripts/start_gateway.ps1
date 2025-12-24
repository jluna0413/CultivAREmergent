# Start the MCP Gateway Infrastructure
# Usage: ./start_gateway.ps1

Write-Host "Starting MCP Gateway (LibreChat + Algorand SSE)..." -ForegroundColor Cyan

# Check if .env exists, if not warn
if (-not (Test-Path "../../.env")) {
    Write-Host "Warning: Root .env file not found. ensure ALGORAND_SIGNER_PRIVATE_KEY is set." -ForegroundColor Yellow
}

# Run Docker Compose
docker-compose -f infrastructure/gateway/docker-compose.gateway.yml up -d

Write-Host "Gateway Started!" -ForegroundColor Green
Write-Host " - LibreChat Interface: http://localhost:3080"
Write-Host " - Algorand MCP SSE:    http://localhost:8000/sse"
Write-Host ""
Write-Host "To view logs: docker-compose -f infrastructure/gateway/docker-compose.gateway.yml logs -f"
