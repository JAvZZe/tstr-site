# tstr.directory - Cloud Scheduler Setup (Option A: Conservative)

Write-Host "=================================="
Write-Host "Setting Up Automated Schedules"
Write-Host "=================================="

$PROJECT_ID = "business-directory-app-8888888"
$REGION = "us-central1"

# Set project
gcloud config set project $PROJECT_ID

# Job 1: Primary Scraper - Every 3 days at 2am
Write-Host "`nCreating primary scraper schedule (every 3 days)..." -ForegroundColor Yellow
gcloud scheduler jobs create http tstr-primary-scraper `
  --location=$REGION `
  --schedule="0 2 */3 * *" `
  --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-primary" `
  --http-method=GET `
  --time-zone="Asia/Singapore" `
  --description="Primary scraper - every 3 days at 2am"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Primary scraper scheduled" -ForegroundColor Green
}

# Job 2: Secondary Scraper - Weekly (Sunday 3am)
Write-Host "`nCreating secondary scraper schedule (weekly)..." -ForegroundColor Yellow
gcloud scheduler jobs create http tstr-secondary-scraper `
  --location=$REGION `
  --schedule="0 3 * * 0" `
  --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-secondary" `
  --http-method=GET `
  --time-zone="Asia/Singapore" `
  --description="Secondary scraper - weekly Sunday 3am"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Secondary scraper scheduled" -ForegroundColor Green
}

# Job 3: Cleanup - Monthly (1st at 4am)
Write-Host "`nCreating cleanup schedule (monthly)..." -ForegroundColor Yellow
gcloud scheduler jobs create http tstr-monthly-cleanup `
  --location=$REGION `
  --schedule="0 4 1 * *" `
  --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-cleanup" `
  --http-method=POST `
  --message-body='{\"mode\":\"2\"}' `
  --headers="Content-Type=application/json" `
  --time-zone="Asia/Singapore" `
  --description="Monthly URL validation and cleanup"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Cleanup scheduled" -ForegroundColor Green
}

Write-Host "`n=================================="
Write-Host "Scheduling Complete!" -ForegroundColor Green
Write-Host "==================================`n"

Write-Host "Schedules:"
Write-Host "1. Primary Scraper:   Every 3 days at 2:00 AM (Singapore)"
Write-Host "2. Secondary Scraper: Every Sunday at 3:00 AM (Singapore)"
Write-Host "3. Cleanup:           1st of month at 4:00 AM (Singapore)"

Write-Host "`nManage schedules:"
Write-Host "List:   gcloud scheduler jobs list --location=$REGION"
Write-Host "Run:    gcloud scheduler jobs run tstr-primary-scraper --location=$REGION"
Write-Host "Pause:  gcloud scheduler jobs pause tstr-primary-scraper --location=$REGION"
Write-Host "Delete: gcloud scheduler jobs delete tstr-primary-scraper --location=$REGION"

Write-Host "`nView in Console:"
$consoleUrl = "https://console.cloud.google.com/cloudscheduler?project=$PROJECT_ID"
Write-Host $consoleUrl
