# ☁️ CLOUD AUTOMATION SOLUTION FOR TSTR.SITE

**Status**: 🎯 RECOMMENDED ARCHITECTURE  
**Date**: October 16, 2025  
**Goal**: Fully automated scraping, validation, and website updates - NO PC REQUIRED

---

## 🎯 CURRENT SITUATION

### What You Have Now (LOCAL)
```
Your PC → Run scrapers manually
       → Generate CSV files
       → Upload to Supabase manually
       → Astro site reads from Supabase
```

**Problem**: Requires your PC to be on and manual intervention

---

## ✨ RECOMMENDED SOLUTION: Google Cloud Platform

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    GOOGLE CLOUD PLATFORM                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────┐     ┌──────────────────┐              │
│  │ Cloud Scheduler  │────→│  Cloud Function  │              │
│  │  (Cron Jobs)     │     │  (Run Scrapers)  │              │
│  │                  │     │                  │              │
│  │ • Daily at 2am   │     │ • Python 3.11    │              │
│  │ • Weekly         │     │ • URL Validation │              │
│  │ • On-demand      │     │ • Auto-cleanup   │              │
│  └──────────────────┘     └────────┬─────────┘              │
│                                    │                         │
│                                    ▼                         │
│                          ┌──────────────────┐                │
│                          │  Cloud Storage   │                │
│                          │  (CSV Reports)   │                │
│                          └────────┬─────────┘                │
│                                   │                          │
└───────────────────────────────────┼──────────────────────────┘
                                    │
                                    ▼
                          ┌──────────────────┐
                          │    SUPABASE      │
                          │  (Database)      │
                          │                  │
                          │ • listings       │
                          │ • pending_research│
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │   ASTRO SITE     │
                          │ (tstr.site)      │
                          │                  │
                          │ Auto-updates     │
                          │ from Supabase    │
                          └──────────────────┘
```

---

## 🏗️ IMPLEMENTATION PLAN

### Phase 1: Migrate Scrapers to Cloud Functions (Week 1)

#### 1. Create Cloud Function for Primary Scraper
```python
# cloud_function_dual_scraper.py
import functions_framework
from dual_scraper import DualPurposeScraper
import os

@functions_framework.http
def run_scraper(request):
    """HTTP Cloud Function to run dual scraper"""
    try:
        scraper = DualPurposeScraper()
        
        # Run scraping
        scraper.scrape_google_maps_api("testing laboratory", "Singapore")
        
        # Generate CSVs
        scraper.generate_directory_csv()
        scraper.generate_sales_contacts_csv()
        scraper.generate_invalid_urls_report()
        
        # Upload directly to Supabase (already integrated!)
        stats = scraper.url_validator.get_stats()
        
        return {
            'status': 'success',
            'listings': len(scraper.directory_listings),
            'leads': len(scraper.sales_contacts),
            'invalid_urls': len(scraper.invalid_urls),
            'validation_stats': stats
        }, 200
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500
```

#### 2. Deploy to Google Cloud
```bash
# Deploy command
gcloud functions deploy tstr-scraper-primary \
  --runtime python311 \
  --trigger-http \
  --entry-point run_scraper \
  --region us-central1 \
  --timeout 540s \
  --memory 512MB \
  --set-env-vars SUPABASE_URL=$SUPABASE_URL,SUPABASE_KEY=$SUPABASE_KEY,GOOGLE_MAPS_API_KEY=$API_KEY
```

#### 3. Setup Cloud Scheduler
```bash
# Schedule to run daily at 2am
gcloud scheduler jobs create http tstr-daily-scrape \
  --schedule="0 2 * * *" \
  --uri="https://us-central1-YOUR_PROJECT.cloudfunctions.net/tstr-scraper-primary" \
  --http-method=POST \
  --time-zone="Asia/Singapore"
```

---

### Phase 2: Automate Database Sync (Week 1)

#### Option A: Direct Supabase Insert (RECOMMENDED)
**Scrapers write directly to Supabase** - Already integrated!

```python
# In cloud function
from supabase import create_client

client = create_client(SUPABASE_URL, SUPABASE_KEY)

# After validation
for listing in scraper.directory_listings:
    client.table("listings").insert({
        'business_name': listing['name'],
        'website': listing['website'],
        'website_verified': listing['website_verified'],
        # ... other fields
    }).execute()
```

**✅ NO CSV FILES NEEDED - Data flows directly to database**

#### Option B: CSV Upload (Alternative)
If you prefer CSV workflow:
```python
# Upload CSV to Cloud Storage
from google.cloud import storage

storage_client = storage.Client()
bucket = storage_client.bucket('tstr-scraper-results')
blob = bucket.blob(f'listings_{timestamp}.csv')
blob.upload_from_string(csv_data)

# Trigger Supabase import via API
```

---

### Phase 3: Astro Site Auto-Updates (Already Working!)

Your Astro site already reads from Supabase, so updates are **automatic**:

```typescript
// In your Astro component
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  import.meta.env.PUBLIC_SUPABASE_URL,
  import.meta.env.PUBLIC_SUPABASE_ANON_KEY
);

// Fetch listings (auto-updates on each page load/rebuild)
const { data: listings } = await supabase
  .from('listings')
  .select('*')
  .eq('website_verified', true)
  .order('created_at', { ascending: false });
```

**✅ Site updates automatically - no manual work needed**

---

## 💰 COST ESTIMATE (Google Cloud)

### Monthly Costs (Small Scale)

| Service | Usage | Cost |
|---------|-------|------|
| Cloud Functions | 30 runs/month @ 2min each | **FREE** (2M invocations free) |
| Cloud Scheduler | 3 jobs | **$0.30** ($0.10/job) |
| Cloud Storage | 10GB reports | **$0.20** ($0.02/GB) |
| Outbound Network | ~1GB/month | **$0.12** |
| **TOTAL** | | **~$0.62/month** |

**Supabase**: Free tier (up to 500MB database, 2GB bandwidth)

**TOTAL MONTHLY COST: ~$1 or less** ✅

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Setup Google Cloud Project
```bash
# 1. Create project
gcloud projects create tstr-automation --name="TSTR Automation"

# 2. Set as active
gcloud config set project tstr-automation

# 3. Enable APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 2: Prepare Code for Cloud
```bash
cd web/tstr-automation

# Create requirements.txt
echo "requests==2.31.0
beautifulsoup4==4.12.2
python-dotenv==1.0.0
supabase==2.0.0
functions-framework==3.5.0" > requirements.txt

# Create cloud function wrapper
# (I'll create this file next)
```

### Step 3: Deploy Functions
```bash
# Deploy primary scraper
gcloud functions deploy tstr-scraper-primary \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=run_primary_scraper \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=512MB

# Deploy secondary scraper
gcloud functions deploy tstr-scraper-secondary \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=run_secondary_scraper \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=540s \
  --memory=512MB
```

### Step 4: Setup Automated Scheduling
```bash
# Daily primary scrape (2am Singapore time)
gcloud scheduler jobs create http tstr-daily-primary \
  --location=us-central1 \
  --schedule="0 2 * * *" \
  --uri="https://us-central1-tstr-automation.cloudfunctions.net/tstr-scraper-primary" \
  --http-method=GET \
  --time-zone="Asia/Singapore"

# Weekly secondary scrape (Sunday 3am)
gcloud scheduler jobs create http tstr-weekly-secondary \
  --location=us-central1 \
  --schedule="0 3 * * 0" \
  --uri="https://us-central1-tstr-automation.cloudfunctions.net/tstr-scraper-secondary" \
  --http-method=GET \
  --time-zone="Asia/Singapore"
```

### Step 5: Configure Environment Variables
```bash
# Set secrets in Cloud Functions
gcloud functions secrets versions add SUPABASE_URL \
  --data-file=- <<< "https://haimjeaetrsaauitrhfy.supabase.co"

gcloud functions secrets versions add SUPABASE_KEY \
  --data-file=- <<< "your-service-role-key"

gcloud functions secrets versions add GOOGLE_MAPS_API_KEY \
  --data-file=- <<< "your-api-key"
```

---

## 🔄 WORKFLOW (FULLY AUTOMATED)

### Daily Automated Flow
```
2:00 AM (Singapore Time)
├─ Cloud Scheduler triggers Cloud Function
├─ Cloud Function runs dual_scraper.py
│  ├─ Scrapes Google Maps API
│  ├─ Validates all URLs automatically
│  ├─ Writes verified listings to Supabase
│  └─ Moves invalid URLs to pending_research
├─ Supabase database updated
├─ Astro site reads from Supabase (automatic)
└─ Users see updated listings on tstr.site

NO PC REQUIRED ✅
NO MANUAL WORK ✅
FULLY AUTOMATED ✅
```

---

## 📊 MONITORING & ALERTS

### Setup Cloud Monitoring
```python
# In cloud function
from google.cloud import logging

client = logging.Client()
logger = client.logger('tstr-scraper')

# Log results
logger.log_struct({
    'timestamp': datetime.now().isoformat(),
    'listings_added': len(scraper.directory_listings),
    'invalid_urls': len(scraper.invalid_urls),
    'success_rate': stats['success_rate']
})
```

### Email Alerts (Optional)
```bash
# Alert if scraper fails
gcloud functions deploy scraper-alert \
  --trigger-event-filters="type=cloudfunctions.googleapis.com/function.error" \
  --trigger-event-filters-path-pattern="function=tstr-scraper-primary"
```

---

## 🆚 ALTERNATIVE: Vercel Cron (If hosting on Vercel)

If you deploy Astro site to Vercel:

```typescript
// api/scrape.ts (Vercel Serverless Function)
export default async function handler(req, res) {
  // Run scraper
  // Update Supabase
  // Return results
}

// vercel.json
{
  "crons": [{
    "path": "/api/scrape",
    "schedule": "0 2 * * *"
  }]
}
```

**Pros**: One platform for everything  
**Cons**: 10-second timeout limit (may need to split scraping)

---

## ✅ RECOMMENDED APPROACH

### **Option 1: Google Cloud Functions (BEST)**
**Why:**
- ✅ Longer execution time (9 minutes)
- ✅ Very cheap (~$1/month)
- ✅ Reliable scheduling
- ✅ Easy Python deployment
- ✅ Can handle large scraping jobs
- ✅ Separate from website hosting

**Use for:**
- Running scrapers
- URL validation
- Database updates
- Report generation

**Astro Site Deployment:** Netlify or Vercel (free tier)

---

### **Option 2: Cloud Run + Cloud Scheduler**
**Why:**
- ✅ More control
- ✅ Can run Docker containers
- ✅ Better for complex workflows
- ✅ Similar pricing

**Use for:**
- More complex scraping needs
- Custom Python environment
- Advanced scheduling

---

## 🎯 NEXT STEPS

### Immediate (This Week)
1. [ ] Create Google Cloud account (or use existing)
2. [ ] Create Cloud project: `tstr-automation`
3. [ ] Deploy test Cloud Function
4. [ ] Test scraper in cloud
5. [ ] Setup Cloud Scheduler

### Short Term (Next Week)
1. [ ] Migrate all scrapers to cloud
2. [ ] Setup automated scheduling
3. [ ] Configure monitoring
4. [ ] Test end-to-end flow

### Long Term (Ongoing)
1. [ ] Monitor scraper performance
2. [ ] Adjust schedules as needed
3. [ ] Add more data sources
4. [ ] Expand to other regions

---

## 📝 SUMMARY

### What Changes
**Before (NOW):**
```
Your PC → Manual scraping → CSV files → Manual upload → Database
```

**After (AUTOMATED):**
```
Cloud Function → Auto-scraping → Direct to Supabase → Astro site updates
(Scheduled)      (URL validated)   (No CSV needed)     (Automatic)
```

### Key Benefits
✅ **No PC Required** - Runs in cloud  
✅ **Fully Automated** - Scheduled scraping  
✅ **Direct Database Updates** - No CSV files needed  
✅ **Auto URL Validation** - Built-in  
✅ **Cost Effective** - ~$1/month  
✅ **Reliable** - Google infrastructure  
✅ **Scalable** - Add more scrapers easily  
✅ **Monitoring** - Track success/failures  

---

## 🚀 READY TO DEPLOY?

**I can create:**
1. Cloud Function wrappers for your scrapers
2. Deployment scripts
3. GitHub Actions for CI/CD
4. Monitoring dashboard
5. Documentation

**Would you like me to:**
- ✅ Create the Cloud Function code NOW
- ✅ Write deployment scripts
- ✅ Setup the infrastructure

**Estimated Time to Full Automation: 1-2 hours** 🎯

---

**Last Updated**: October 16, 2025  
**Status**: Ready to implement  
**Recommendation**: Google Cloud Functions + Cloud Scheduler
