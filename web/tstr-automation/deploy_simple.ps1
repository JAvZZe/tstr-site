# TSTR.SITE - Simple Cloud Function Deployment

Write-Host "=================================="
Write-Host "TSTR.SITE Cloud Deployment"
Write-Host "=================================="

# Configuration
$PROJECT_ID = "business-directory-app-8888888"
$REGION = "us-central1"

# Load .env
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#=]+)=(.+)$') {
        $name = $matches[1].Trim()
        $value = $matches[2].Trim()
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

Write-Host "Setting project..." -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

Write-Host "`nDeploying primary scraper..." -ForegroundColor Yellow
gcloud functions deploy tstr-scraper-primary --gen2 --runtime=python311 --region=$REGION --source=. --entry-point=run_primary_scraper --trigger-http --allow-unauthenticated --timeout=540s --memory=512MB --quiet

Write-Host "`nDeployment complete!" -ForegroundColor Green
