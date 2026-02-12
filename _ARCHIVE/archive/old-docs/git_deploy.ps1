# Git deployment script for TSTR.site

Write-Host "Committing code..." -ForegroundColor Yellow

git commit -m "Initial commit - TSTR site with automated scrapers"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Commit successful!" -ForegroundColor Green
} else {
    Write-Host "Commit failed. Error code: $LASTEXITCODE" -ForegroundColor Red
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create GitHub repository at: https://github.com/new"
Write-Host "2. Run these commands:"
Write-Host "   git remote add origin https://github.com/YOUR-USERNAME/tstr-site.git"
Write-Host "   git branch -M main"
Write-Host "   git push -u origin main"
Write-Host ""
Write-Host "3. Then connect to Netlify at: https://app.netlify.com"
