# TSTR.SITE - Cloud Scheduler Setup

Write-Host "Setting Up Automated Schedules..." -ForegroundColor Yellow

gcloud config set project business-directory-app-8888888

Write-Host "Creating primary scraper schedule..." -ForegroundColor Cyan
gcloud scheduler jobs create http tstr-primary-scraper --location=us-central1 --schedule="0 2 */3 * *" --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-primary" --http-method=GET --time-zone="Asia/Singapore" --description="Primary scraper every 3 days"

Write-Host "Creating secondary scraper schedule..." -ForegroundColor Cyan
gcloud scheduler jobs create http tstr-secondary-scraper --location=us-central1 --schedule="0 3 * * 0" --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-secondary" --http-method=GET --time-zone="Asia/Singapore" --description="Secondary scraper weekly"

Write-Host "Creating cleanup schedule..." -ForegroundColor Cyan
gcloud scheduler jobs create http tstr-monthly-cleanup --location=us-central1 --schedule="0 4 1 * *" --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-cleanup" --http-method=POST --message-body='{\"mode\":\"2\"}' --headers="Content-Type=application/json" --time-zone="Asia/Singapore" --description="Monthly cleanup"

Write-Host "Done!" -ForegroundColor Green
