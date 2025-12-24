# setup_postgres.ps1
# Automates the setup of PostgreSQL for local development

Write-Host "[SETUP] Starting PostgreSQL Setup for CultivAR..." -ForegroundColor Cyan

# 1. Check if Docker is running
docker ps > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERROR] Docker is not running. Please start Docker Desktop and try again."
    exit 1
}

# 2. Start PostgreSQL service via Docker Compose
Write-Host "[DOCKER] Starting database container..." -ForegroundColor Cyan
docker compose up -d db

# 3. Wait for DB to be healthy
Write-Host "[WAIT] Waiting for PostgreSQL to be ready..." -ForegroundColor Yellow
$retries = 30
while ($retries -gt 0) {
    $status = docker inspect --format='{{json .State.Health.Status}}' cultivar-db 2>$null
    if ($status -eq '"healthy"') {
        Write-Host "[OK] PostgreSQL is healthy!" -ForegroundColor Green
        break
    }
    Write-Host "Still waiting... $retries retries left"
    Start-Sleep -Seconds 2
    $retries = $retries - 1
}

if ($retries -eq 0) {
    Write-Error "[ERROR] PostgreSQL failed to become healthy in time."
    exit 1
}

# 4. Update .env file
Write-Host "[CONFIG] Updating .env file..." -ForegroundColor Cyan
$envPath = ".env"
$pgUri = "postgresql+asyncpg://cultivar:cultivar@localhost:5432/cultivardb"

if (Test-Path $envPath) {
    $content = Get-Content $envPath -Raw
    if ($content -match "DATABASE_URL=") {
        $content = $content -replace "DATABASE_URL=.*", "DATABASE_URL=$pgUri"
    }
    else {
        $content = $content + "`nDATABASE_URL=$pgUri"
    }
    Set-Content $envPath $content -NoNewline
}
else {
    "DATABASE_URL=$pgUri`nENVIRONMENT=development`nDEBUG=true" | Set-Content $envPath
}
Write-Host "[OK] .env updated with PostgreSQL connection string." -ForegroundColor Green

# 5. Run Migrations
Write-Host "[MIGRATE] Running database migrations..." -ForegroundColor Cyan
python -m scripts.migrate
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERROR] Migration failed."
    exit 1
}

# 6. Run Initialization and Ingestion
Write-Host "[SEED] Seeding initial data..." -ForegroundColor Cyan
python -m scripts.init_db_async
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERROR] Initial seeding failed."
    exit 1
}

Write-Host "[INGEST] Ingesting SeedFinder data..." -ForegroundColor Cyan
python -m scripts.ingestion.seedfinder_ingestor
if ($LASTEXITCODE -ne 0) {
    Write-Warning "[WARN] Ingestion failed (possibly due to HyperGraph service being down). This is expected if running without full stack."
}

Write-Host "[DONE] PostgreSQL Setup Complete! You can now run the app with 'python -m cultivar_app'." -ForegroundColor Green
