# TSTR.site - Fast Track to Live Deployment

**Created**: 2025-10-14  
**Goal**: Get TSTR.site live as quickly as possible  
**Time Estimate**: 2-4 hours

---

## Current Status Analysis

✅ **What You Have:**
- Frontend: Astro site with Supabase integration (`web/tstr-frontend/`)
- Backend: Two Python scrapers (PRIMARY & SECONDARY) ready
- Database: Supabase schema defined (SQL files exist)
- GitHub Repo: Connected to `https://github.com/JAvZZe/tstr-site.git`
- Git Branch: `main` with some uncommitted changes

❌ **What's Missing:**
- No `.env` file in frontend (Supabase credentials not configured)
- Database schema not executed in Supabase yet
- No scraped data (no listings in database)
- Frontend not built for production
- Not deployed to hosting platform

---

## FASTEST PATH TO LIVE (Choose One)

### Option A: MVP Launch (2 hours) - RECOMMENDED
Deploy a functional but minimal site with placeholder data

### Option B: Full Data Launch (4 hours)
Deploy with real scraped listings from testing labs

---

## OPTION A: MVP LAUNCH (FASTEST - 2 HOURS)

### Step 1: Set Up Supabase (15 minutes)

```powershell
# 1. Get your Supabase credentials
# Visit: https://app.supabase.com/project/YOUR_PROJECT/settings/api
# Copy: Project URL and anon public key

# 2. Create .env file in frontend
cd web\tstr-frontend
@"
PUBLIC_SUPABASE_URL=https://your-project.supabase.co
PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
"@ | Out-File -FilePath ".env" -Encoding utf8

# 3. Execute database schema in Supabase dashboard
# Visit: https://app.supabase.com/project/YOUR_PROJECT/sql/new
# Copy and run each SQL file in order:
#   - SUPABASE_STEP_1_EXTENSIONS.sql
#   - SUPABASE_STEP_2_TABLES_FIXED.sql
#   - SUPABASE_STEP_3_INDEXES.sql
#   - SUPABASE_STEP_4_SEED_DATA.sql (this adds sample categories/locations)
```

### Step 2: Add Sample Data (10 minutes)

The SEED_DATA.sql file should create sample categories. If not, manually add via Supabase dashboard:

**Categories to add:**
- Oil & Gas Testing
- Pharmaceutical Testing
- Biotech Testing
- Environmental Testing
- Materials Testing
- Genetics Testing
- Satellite Testing

**Locations to add:**
- Houston, Texas (city level)
- Aberdeen, UK (city level)
- Singapore (city level)
- San Francisco, California (city level)
- Basel, Switzerland (city level)

### Step 3: Test Frontend Locally (5 minutes)

```powershell
cd web\tstr-frontend

# Install dependencies (if not done)
npm install

# Start dev server
npm run dev

# Visit: http://localhost:4321
# Should see homepage with categories from Supabase
```

### Step 4: Deploy to Cloudflare Pages (30 minutes)

**Option A: Via GitHub (Recommended)**

```powershell
# 1. Commit current changes
git add web/tstr-frontend
git commit -m "feat: frontend ready for deployment"
git push origin main

# 2. Go to: https://dash.cloudflare.com
# 3. Pages → Create a project → Connect to Git
# 4. Select repository: JAvZZe/tstr-site
# 5. Configure build settings:
#    - Framework preset: Astro
#    - Build command: cd web/tstr-frontend && npm run build
#    - Build output directory: web/tstr-frontend/dist
#    - Root directory: /
# 6. Add Environment Variables:
#    PUBLIC_SUPABASE_URL=your-supabase-url
#    PUBLIC_SUPABASE_ANON_KEY=your-anon-key
# 7. Click "Save and Deploy"
```

**Option B: Direct Upload (Faster, but manual updates)**

```powershell
# Build the site
cd web\tstr-frontend
npm run build

# Upload dist folder via Cloudflare dashboard
# Pages → Create a project → Direct Upload
# Drag and drop the dist/ folder
```

### Step 5: Configure Custom Domain (20 minutes - OPTIONAL)

```powershell
# In Cloudflare Pages project settings:
# Custom domains → Add domain → tstr.site
# Follow DNS configuration instructions
# Wait for SSL provisioning (automatic)
```

**Your site is LIVE!** 🎉

---

## OPTION B: FULL DATA LAUNCH (4 HOURS)

### Step 1-3: Same as Option A (30 minutes)

### Step 4: Populate Real Data (1.5 hours)

```powershell
# Set up environment for scrapers
cd web\tstr-automation

# Create .env file
@"
GOOGLE_MAPS_API_KEY=your-api-key-here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here
"@ | Out-File -FilePath ".env" -Encoding utf8

# Install Python dependencies
pip install -r requirements.txt

# Run PRIMARY scraper (listings + leads)
python dual_scraper.py

# Run SECONDARY scraper (more listings)
python scraper.py

# You should now have CSV files:
# - tstr_directory_import.csv
# - tstr_sales_leads.csv
# - tstr_listings_import.csv
```

### Step 5: Import Data to Supabase (30 minutes)

**Option A: Via Supabase Dashboard (Easier)**
1. Visit: https://app.supabase.com/project/YOUR_PROJECT/editor
2. Table Editor → listings → Insert → Upload CSV
3. Map CSV columns to database columns
4. Import

**Option B: Via Python Script (Better for large datasets)**
```powershell
# Create import script
cd web\tstr-automation
python import_to_supabase.py  # You'll need to create this
```

### Step 6: Test Frontend with Real Data (10 minutes)

```powershell
cd web\tstr-frontend
npm run dev
# Visit: http://localhost:4321
# Should now show real listings
```

### Step 7: Deploy (Same as Option A Step 4-5)

---

## POST-DEPLOYMENT CHECKLIST

Once live, complete these tasks:

### Immediate (Day 1)
- [ ] Verify site loads correctly
- [ ] Test category browsing
- [ ] Check mobile responsiveness
- [ ] Verify Supabase data displays
- [ ] Test search functionality (if implemented)

### Week 1
- [ ] Set up Google Analytics
- [ ] Submit sitemap to Google Search Console
- [ ] Create XML sitemap
- [ ] Add meta descriptions for SEO
- [ ] Set up error monitoring (Sentry)
- [ ] Configure automated scraper schedule
- [ ] Start outreach using sales leads CSV

### Week 2
- [ ] Add submission form for labs to list themselves
- [ ] Implement payment integration for premium listings
- [ ] Create detailed listing pages
- [ ] Add geographic drill-down (region → country → city)
- [ ] Set up email notifications

---

## CRITICAL FILES TO COMMIT TO GITHUB

**DO commit:**
```
✅ web/tstr-frontend/src/            (all source code)
✅ web/tstr-frontend/public/          (static assets)
✅ web/tstr-frontend/package.json
✅ web/tstr-frontend/package-lock.json
✅ web/tstr-frontend/astro.config.mjs
✅ web/tstr-frontend/tsconfig.json
✅ web/tstr-frontend/.gitignore
✅ web/tstr-automation/*.py           (scraper scripts)
✅ web/tstr-automation/requirements.txt
✅ web/tstr-automation/config.json
✅ web/tstr-automation/*.sql          (database schemas)
✅ GITHUB_COPILOT.md
✅ GEMINI.md
✅ handoff_core.md
```

**DO NOT commit:**
```
❌ web/tstr-frontend/.env             (has Supabase keys)
❌ web/tstr-frontend/dist/            (build output)
❌ web/tstr-frontend/node_modules/    (dependencies)
❌ web/tstr-automation/.env           (has API keys)
❌ web/tstr-automation/*.csv          (scraped data - too large)
❌ .env.github-copilot                (personal config)
```

**Note**: `.gitignore` already excludes `.env` and `dist/`, but verify before committing!

---

## COMMIT AND PUSH COMMANDS

```powershell
# Check what's changed
git status

# Add frontend changes
git add web/tstr-frontend/package.json web/tstr-frontend/package-lock.json
git add web/tstr-frontend/src/
git add web/tstr-frontend/supabase/

# Add scraper improvements
git add web/tstr-automation/scraper.py
git add web/tstr-automation/config.json

# Add documentation
git add GITHUB_COPILOT.md GEMINI.md handoff_core.md FAST_TRACK_DEPLOYMENT.md

# Verify .env files are NOT staged
git status | Select-String ".env"
# Should return nothing or show as untracked (not staged)

# Commit
git commit -m "feat: improved scrapers, added deployment docs, ready for production"

# Push to GitHub
git push origin main
```

---

## CLOUDFLARE PAGES VS SUPABASE CONFUSION

**Clarification**: These are TWO different services!

### Supabase (Database + Backend)
- **Purpose**: Stores your data (listings, categories, locations)
- **What to do**: Execute SQL schema files in Supabase dashboard
- **No GitHub needed**: Supabase runs independently
- **Access**: Via API keys in `.env` file

### Cloudflare Pages (Frontend Hosting)
- **Purpose**: Hosts your Astro website (HTML/CSS/JS)
- **What to do**: Connect GitHub repo to Cloudflare
- **GitHub integration**: Auto-deploys when you push to `main` branch
- **Access**: Public URL (e.g., tstr-site.pages.dev)

**Flow**:
1. Frontend (Cloudflare) → calls → Backend (Supabase) → returns data
2. GitHub only affects frontend deployment (Cloudflare watches your repo)
3. Database changes happen directly in Supabase dashboard

---

## TROUBLESHOOTING

### "Site shows but no data"
- Check `.env` has correct Supabase credentials
- Verify database schema is executed in Supabase
- Check browser console for API errors

### "Build failed on Cloudflare"
- Verify build command: `cd web/tstr-frontend && npm run build`
- Check environment variables are set in Cloudflare dashboard
- Review build logs for specific errors

### "Can't connect to Supabase"
- Verify Project URL and Anon Key are correct
- Check RLS policies allow anonymous reads
- Test connection with `test_supabase.py`

### "Scrapers not working"
- Check Google Maps API key is valid
- Verify API is enabled in Google Cloud Console
- Check rate limits and quotas
- Test with smaller config.json targets first

---

## RECOMMENDED: OPTION A FIRST

**My recommendation**: Start with Option A (MVP Launch)

**Why?**
1. **Fastest to market** (2 hours vs 4 hours)
2. **Test deployment workflow** without data complications
3. **Verify everything works** before adding real data
4. **Can add data later** without redeploying (Supabase updates live)
5. **Lower risk** of errors during first deployment

**Once live with Option A, you can:**
- Run scrapers and import data without redeployment
- Data appears automatically (frontend fetches from Supabase)
- Iterate on design while gathering real listings

---

## NEXT IMMEDIATE STEPS

```powershell
# 1. Set up Supabase credentials
cd web\tstr-frontend
# Create .env file with your Supabase keys

# 2. Test locally
npm install
npm run dev

# 3. If it works, commit and deploy
git add web/tstr-frontend/
git commit -m "feat: frontend configured and tested"
git push origin main

# 4. Set up Cloudflare Pages deployment
# Visit: https://dash.cloudflare.com
```

**Time to be live: ~2 hours from now!** 🚀

---

**Questions? Issues? Check:**
- Cloudflare Pages docs: https://developers.cloudflare.com/pages/
- Supabase docs: https://supabase.com/docs
- Astro deployment: https://docs.astro.build/en/guides/deploy/

**Last Updated**: 2025-10-14  
**Agent**: GitHub Copilot CLI
