<#
Stop and remove the isolated Ollama container and its network.
#>
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Output "Stopping container..."
docker compose down

Write-Output "Stopped and removed container resources. Model data remains in ./data"
