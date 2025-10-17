# 📁 Project Cleanup Script
# Archives completed/old documentation files

$sourceDir = "C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site"
$archiveDir = "$sourceDir\archive\completed-tasks"

# Create archive directory if needed
if (-not (Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Path $archiveDir -Force
}

# Files to archive (completed tasks)
$filesToArchive = @(
    "WEBSITE_FIXES_SUMMARY.md",
    "FIX_CLOUDFLARE_ENV_VARS_NOW.md",
    "DEPLOYMENT_VERIFICATION.md",
    "FAST_TRACK_DEPLOYMENT.md",
    "WEBSITE_DEPLOYMENT_STATUS.md",
    "URL_VALIDATION_SETUP.md",
    "URL_VALIDATION_INTEGRATION.md",
    "SESSION_SUMMARY_2025-10-15.md",
    "SESSION_SUMMARY_2025-10-16.md",
    "SESSION_SUMMARY_2025-10-16_CLAUDE.md",
    "DEPLOYMENT_ENV.md",
    "GEMINI_CLI_UPGRADE_GUIDE.md"
)

Write-Host "🗂️  Archiving completed task documentation..." -ForegroundColor Cyan

foreach ($file in $filesToArchive) {
    $sourcePath = Join-Path $sourceDir $file
    $destPath = Join-Path $archiveDir $file
    
    if (Test-Path $sourcePath) {
        Move-Item -Path $sourcePath -Destination $destPath -Force
        Write-Host "✅ Archived: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Not found: $file" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host "📁 Archived files are in: $archiveDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Active documentation structure:" -ForegroundColor Cyan
Write-Host "   START_HERE.md            ← Read this first!"
Write-Host "   PROJECT_STATUS.md        ← Current state"
Write-Host "   DEPLOYMENT_READY_SUMMARY.md ← What's next"
Write-Host "   handoff_core.md          ← Session history"
