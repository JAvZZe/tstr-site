# 🔧 DEPLOYMENT ENVIRONMENT - Quick Reference

**Purpose**: Fast access to all credentials and commands for any agent  
**Updated**: October 16, 2025 17:30 UTC

---

## 🔑 CREDENTIALS (Quick Copy-Paste)

### Supabase
```bash
SUPABASE_URL=https://haimjeaetrsaauitrhfy.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjAxNTksImV4cCI6MjA3NTYzNjE1OX0.1SoHZoMAeap4p2Fy4HxzHJ4IRZWZ78VamGd0JWQ0OqM
SUPABASE_SERVICE_ROLE_KEY=sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2
```

### Google Cloud
```bash
PROJECT_ID=business-directory-app-8888888
REGION=us-central1
FUNCTION_URL=https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-primary
```

### Gemini API
```bash
GEMINI_API_KEY=AIzaSyBKVKWawwm-1zMTU4cWNqcpgKqpJUvlLwA
STATUS=QUOTA_EXHAUSTED (50/50 requests used)
```

---

## 📂 FILE PATHS

```bash
ROOT=C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site
FRONTEND=C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site\web\tstr-frontend
SCRAPERS=C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site\web\tstr-automation
```

---

## ⚡ DEPLOYMENT COMMANDS

### Git Commit & Push
```powershell
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site
git status
git add .
git commit -m "Deploy: Complete automation with scrapers and frontend"
git push origin main
```

### Netlify Deploy
```powershell
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site\web\tstr-frontend

# First time setup
netlify login
netlify init

# Deploy
netlify build
netlify deploy --prod

# Set environment variables
netlify env:set PUBLIC_SUPABASE_URL "https://haimjeaetrsaauitrhfy.supabase.co"
netlify env:set PUBLIC_SUPABASE_ANON_KEY "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjAxNTksImV4cCI6MjA3NTYzNjE1OX0.1SoHZoMAeap4p2Fy4HxzHJ4IRZWZ78VamGd0JWQ0OqM"
```

### Google Cloud Scheduler
```bash
# Daily scraper at 2am SGT
gcloud scheduler jobs create http tstr-daily-scraper \
  --location=us-central1 \
  --schedule="0 2 * * *" \
  --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-primary" \
  --http-method=GET \
  --time-zone="Asia/Singapore"
```

### Deploy Remaining Cloud Functions
```bash
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site\web\tstr-automation

# Secondary scraper
gcloud functions deploy tstr-scraper-secondary \
  --gen2 --runtime=python311 --region=us-central1 \
  --source=. --entry-point=run_secondary_scraper \
  --trigger-http --allow-unauthenticated \
  --timeout=540s --memory=512MB

# Cleanup function
gcloud functions deploy tstr-cleanup \
  --gen2 --runtime=python311 --region=us-central1 \
  --source=. --entry-point=run_cleanup \
  --trigger-http --allow-unauthenticated \
  --timeout=540s --memory=512MB
```

---

## 🔍 STATUS CHECKS

### Check Git Status
```powershell
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site
git status
git log --oneline -5
```

### Check Netlify Status
```powershell
netlify status
netlify env:list
netlify sites:list
```

### Check Google Cloud
```bash
gcloud functions list --region=us-central1
gcloud scheduler jobs list --location=us-central1
```

### Check Supabase Data
```sql
-- In Supabase SQL Editor
SELECT COUNT(*) FROM listings WHERE website_verified = true;
SELECT * FROM pending_research;
```

---

## 🔧 TROUBLESHOOTING

### Git Push Fails
```powershell
# Check remote
git remote -v

# Force if needed (careful!)
git push origin main --force
```

### Netlify Build Fails
```powershell
# Test build locally
npm run build

# Check logs
netlify logs

# Clear cache
netlify build --clear-cache
```

### Cloud Function Errors
```bash
# Check logs
gcloud functions logs read tstr-scraper-primary --region=us-central1 --limit=50

# Test function
curl https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-primary
```

---

## 📊 CURRENT STATUS

```
✅ Scrapers: Deployed & working (primary only)
⚠️  Frontend: Code ready, not deployed
❌ Scheduling: Not configured
❌ Webhooks: Not configured
```

---

## 🎯 SUCCESS CHECKLIST

- [ ] Git changes committed & pushed
- [ ] Frontend deployed to Netlify
- [ ] Environment variables set in Netlify
- [ ] Cloud Scheduler created
- [ ] Secondary scraper deployed
- [ ] Cleanup function deployed
- [ ] Netlify webhook configured in Supabase
- [ ] Website live and showing data

---

**QUICK ACCESS FILE - Keep this updated after each deployment step**
