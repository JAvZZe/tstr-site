# TSTR.SITE - Cloud Function Deployment Script (PowerShell)
# Deploys scrapers to Google Cloud Functions

$ErrorActionPreference = "Stop"

Write-Host "=================================="
Write-Host "TSTR.SITE Cloud Deployment"
Write-Host "=================================="

# Configuration
$PROJECT_ID = "business-directory-app-8888888"
$REGION = "us-central1"
$RUNTIME = "python311"
$TIMEOUT = "540s"
$MEMORY = "512MB"

# Load environment variables from .env
if (Test-Path ".env") {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.*?)\s*$') {
            $name = $matches[1]
            $value = $matches[2]
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
    Write-Host "✓ Loaded .env file" -ForegroundColor Green
} else {
    Write-Host "✗ .env file not found" -ForegroundColor Red
    exit 1
}

# Check if gcloud is available
try {
    gcloud --version | Out-Null
    Write-Host "✓ gcloud CLI found" -ForegroundColor Green
} catch {
    Write-Host "✗ gcloud CLI not installed" -ForegroundColor Red
    exit 1
}

# Set project
Write-Host "`nSetting project: $PROJECT_ID" -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

# Deploy Primary Scraper
Write-Host "`nDeploying primary scraper..." -ForegroundColor Yellow
gcloud functions deploy tstr-scraper-primary `
  --gen2 `
  --runtime=$RUNTIME `
  --region=$REGION `
  --source=. `
  --entry-point=run_primary_scraper `
  --trigger-http `
  --allow-unauthenticated `
  --timeout=$TIMEOUT `
  --memory=$MEMORY `
  --set-env-vars="SUPABASE_URL=$env:SUPABASE_URL,SUPABASE_KEY=$env:SUPABASE_KEY,SUPABASE_SERVICE_ROLE_KEY=$env:SUPABASE_SERVICE_ROLE_KEY" `
  --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Primary scraper deployed" -ForegroundColor Green
} else {
    Write-Host "✗ Primary scraper deployment failed" -ForegroundColor Red
    exit 1
}

# Deploy Secondary Scraper
Write-Host "`nDeploying secondary scraper..." -ForegroundColor Yellow
gcloud functions deploy tstr-scraper-secondary `
  --gen2 `
  --runtime=$RUNTIME `
  --region=$REGION `
  --source=. `
  --entry-point=run_secondary_scraper `
  --trigger-http `
  --allow-unauthenticated `
  --timeout=$TIMEOUT `
  --memory=$MEMORY `
  --set-env-vars="SUPABASE_URL=$env:SUPABASE_URL,SUPABASE_KEY=$env:SUPABASE_KEY,SUPABASE_SERVICE_ROLE_KEY=$env:SUPABASE_SERVICE_ROLE_KEY" `
  --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Secondary scraper deployed" -ForegroundColor Green
} else {
    Write-Host "✗ Secondary scraper deployment failed" -ForegroundColor Red
}

# Deploy Cleanup Function
Write-Host "`nDeploying cleanup function..." -ForegroundColor Yellow
gcloud functions deploy tstr-cleanup `
  --gen2 `
  --runtime=$RUNTIME `
  --region=$REGION `
  --source=. `
  --entry-point=run_cleanup `
  --trigger-http `
  --allow-unauthenticated `
  --timeout=$TIMEOUT `
  --memory=$MEMORY `
  --set-env-vars="SUPABASE_URL=$env:SUPABASE_URL,SUPABASE_KEY=$env:SUPABASE_KEY,SUPABASE_SERVICE_ROLE_KEY=$env:SUPABASE_SERVICE_ROLE_KEY" `
  --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Cleanup function deployed" -ForegroundColor Green
} else {
    Write-Host "✗ Cleanup deployment failed" -ForegroundColor Red
}

# Get function URLs
Write-Host "`n=================================="
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "==================================`n"

Write-Host "Function URLs:"
$primaryUrl = gcloud functions describe tstr-scraper-primary --region=$REGION --gen2 --format="value(serviceConfig.uri)"
Write-Host "Primary Scraper:   $primaryUrl"

$secondaryUrl = gcloud functions describe tstr-scraper-secondary --region=$REGION --gen2 --format="value(serviceConfig.uri)"
Write-Host "Secondary Scraper: $secondaryUrl"

$cleanupUrl = gcloud functions describe tstr-cleanup --region=$REGION --gen2 --format="value(serviceConfig.uri)"
Write-Host "Cleanup:           $cleanupUrl"

Write-Host "`nNext steps:"
Write-Host "1. Test functions: Invoke-WebRequest -Uri " $primaryUrl
Write-Host "2. Setup scheduler: .\setup_scheduler.ps1"
Write-Host "3. Monitor logs: gcloud functions logs read tstr-scraper-primary --region=$REGION"
