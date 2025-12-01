# 📊 TSTR.SITE - CENTRALIZED PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - All agents update this document
> **Last Updated**: December 1, 2025 17:00 UTC
> **Updated By**: OpenCode AI Assistant
> **Status**: ✅ PRODUCTION - Live at https://tstr.site with 163 listings + Click Tracking + Admin Dashboard + Updated Branding + Terms of Service + Oil & Gas Scraper Integration + LinkedIn OAuth Redirect URI Configuration

---

## 🎯 PROJECT OVERVIEW

**Name**: TSTR.SITE
**Type**: Testing Laboratory Directory Platform
**Stack**: Astro + React + Supabase + Python Scrapers
**Deployment**: Oracle Cloud Infrastructure (OCI) + Cloudflare Pages
**Status**: ✅ LIVE - https://tstr.site with automated scrapers on OCI

---

## 📈 CURRENT STATUS DASHBOARD

```
┌─────────────────────────────────────────────┐
│  COMPONENT STATUS                           │
├─────────────────────────────────────────────┤
│  ✅ Database (Supabase)        OPERATIONAL  │
│  ✅ URL Validation             LIVE         │
│  ✅ Click Tracking             DEPLOYED ✨  │
│  ✅ OCI Scrapers               DEPLOYED     │
│  ✅ Automated Scheduling       ACTIVE       │
│  ✅ Frontend (Cloudflare)      LIVE         │
│  ✅ Domain (tstr.site)         LIVE         │
└─────────────────────────────────────────────┘

Listings:         163 verified (Pharmaceutical: 108, Materials: 41, Environmental: 14)
Data Quality:     95%+ (URL validation active)
Automation:       100% (cron daily 2 AM GMT)
Cost/Month:       $0.00 (Oracle Always Free Tier)
OCI Uptime:       15 days continuous
Last Scrape:      November 10, 2025 02:31 UTC (on schedule)
```

---

## 🛠️ DEPLOYED INFRASTRUCTURE

### **Oracle Cloud Infrastructure (OCI)**

#### Compute Instance
- **IP Address**: 84.8.139.90
- **OS**: Oracle Linux 9
- **Python**: 3.9.21
- **Location**: `/home/opc/tstr-scraper/`
- **Status**: ✅ OPERATIONAL (15 days uptime)
- **Cost**: FREE (Oracle Always Free Tier)

#### Scraper Deployment
- **Script**: `run_scraper.py`
- **Sources**: Pharmaceutical testing directories (108 listings)
- **Output**:
  - `tstr_directory_import.csv` (108 listings)
  - `sales_contacts.csv` (64 contacts)
  - `invalid_urls.csv` (17 invalid URLs)
- **Status**: ✅ ACTIVE

#### Automated Scheduling (Cron)
- **Schedule**: `0 2 * * *` (Daily at 2:00 AM GMT)
- **Command**: `cd /home/opc/tstr-scraper && /usr/bin/python3 run_scraper.py >> scraper.log 2>&1`
- **Last Run**: November 10, 2025 02:31 UTC
- **Result**: 108 listings scraped, 0 new (all existing in DB)
- **Status**: ✅ RUNNING ON SCHEDULE
- **Purpose**: Keep OCI instance active (prevents Oracle from shelving inactive instances)

### **Database (Supabase)**

- **URL**: https://haimjeaetrsaauitrhfy.supabase.co
- **Region**: US West (Oregon)
- **Plan**: Free Tier
- **Tables**:
  - `listings` (163 verified entries)
  - `custom_fields` (specialized certifications data)
  - `pending_research` (invalid URLs for manual review)
  - `clicks` ✨ NEW - Click tracking analytics (2025-11-22)
- **Status**: ✅ OPERATIONAL

### **Frontend (Cloudflare Pages)**

- **URL**: https://tstr.site
- **Location**: `web/tstr-frontend/`
- **Framework**: Astro 5.14.4
- **UI**: React 18.3.1
- **Styling**: TailwindCSS 3.4.1
- **Database**: Supabase JS Client 2.45.4
- **Deployment**: Cloudflare Pages (via GitHub Actions)
- **Features**:
  - Category filters, location search, responsive design
  - ✨ Click tracking via internal redirects (2025-11-22)
  - SEO-optimized internal redirect system
  - 🔧 Admin dashboard for scraper monitoring (2025-11-29)
- **Status**: ✅ LIVE

---

## 💰 COST BREAKDOWN

### **Current Monthly Costs**

| Service | Usage | Cost | Status |
|---------|-------|------|--------|
| **Oracle Cloud (OCI)** | 1 compute instance (Always Free) | $0.00 | FREE |
| **Supabase** | Database + API (Free Tier) | $0.00 | FREE (under 500MB) |
| **Cloudflare Pages** | Frontend hosting (Free Tier) | $0.00 | FREE |
| **GitHub** | Version control + CI/CD (Free) | $0.00 | FREE |
| **Domain (tstr.site)** | Domain registration | ~$12/year | ACTIVE |
| **TOTAL** | | **$0.00/mo** | ✅ |

**Annual Cost**: ~$12/year (domain only)

### **Cost Projections**

**If scaled to 1000+ listings**:
- OCI: Still FREE (Always Free Tier covers 2 AMD instances)
- Supabase: May need to upgrade (~$25/month if >500MB)
- Cloudflare Pages: Still FREE (unlimited requests)
- Total: ~$25/month

**Cost optimization**: Maximizing free tiers across all services

---

## 📦 CODE COMPONENTS

### **Python Scrapers** (Production)

#### 1. `url_validator.py`
- **Purpose**: URL validation module
- **Features**: Two-tier validation (HEAD → GET), caching, timeout handling
- **Status**: ✅ PRODUCTION
- **Success Rate**: 95%
- **Used By**: All scrapers, cleanup script

#### 2. `dual_scraper.py`
- **Purpose**: Google Maps API scraper (pharma, biotech, etc.)
- **Features**: Google Maps API, URL validation, duplicate detection
- **Status**: ✅ PRODUCTION (deployed as cloud function)
- **Validates**: Yes (automatic)
- **Rate Limiting**: 0.5s between requests

#### 3. `main_scraper.py` ✨ NEW
- **Purpose**: Main scraper orchestrator
- **Features**: Combines Google Maps + niche-specific scrapers
- **Status**: ✅ CREATED (pending OCI deployment)
- **Includes**: Oil & Gas, Materials, Environmental scrapers

#### 4. `run_scraper.py` ✨ UPDATED
- **Purpose**: OCI cron job entry point
- **Features**: Runs main_scraper.py daily
- **Status**: ✅ UPDATED (pending OCI deployment)
- **Schedule**: Daily 2 AM GMT

#### 5. `scraper.py`
- **Purpose**: Secondary scraper (listings only)
- **Features**: Alternative sources, duplicate detection, URL validation
- **Status**: ✅ PRODUCTION (deployed as cloud function)
- **Validates**: Yes (automatic)
- **Rate Limiting**: 0.5s between requests

#### 6. `cleanup_invalid_urls.py`
- **Purpose**: Database validation & cleanup
- **Features**: Re-validate existing URLs, move invalid to research
- **Status**: ✅ PRODUCTION (deployed as cloud function)
- **Mode**: Auto-move to pending_research

#### 7. `main.py`
- **Purpose**: Cloud Function entry points
- **Features**: Wraps all scrapers for Google Cloud deployment
- **Status**: ✅ DEPLOYED
- **Functions**: run_primary_scraper, run_secondary_scraper, run_cleanup

### **Configuration Files**

#### `config.json`
- **Purpose**: Scraper targets
- **Google Maps Searches**: 15 categories × locations
- **Alternative Sources**: 3 (Energy Pedia, Pharma Tech, Biocompare)
- **Status**: ✅ ACTIVE

#### `requirements.txt`
- **Purpose**: Python dependencies
- **Packages**: requests, beautifulsoup4, supabase, functions-framework, etc.
- **Status**: ✅ DEPLOYED

#### `.env`
- **Purpose**: Environment variables
- **Variables**: SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY
- **Status**: ✅ CONFIGURED (cloud & local)

### **Deployment Scripts**

- `deploy.ps1` - PowerShell deployment script
- `create_schedules.ps1` - Scheduler setup
- `setup_scheduler.ps1` - Alternative scheduler script
- **Status**: ✅ ALL WORKING

---

## 📊 DATA QUALITY METRICS

### **Current Database State**

```
Total Listings:        175
Valid URLs:           95%+ (active validation)
By Category:
- Biopharma & Life Sciences: 108 listings (includes biotech/pharma)
- Materials Testing:   41 listings
- Environmental:       14 listings
- Oil & Gas Testing:   12 listings

By Geographic Region:
- United States:      Primary focus
- Kuwait:             Active
- Thailand:           Active
- United Kingdom:     Active
- Singapore:          Active
```

### **URL Validation Stats**

```
Total Validated:      163+
Success Rate:        95%+
Invalid URLs:         17 (logged in invalid_urls.csv)
Validation Method:    HEAD → GET fallback
Avg Validation Time:  2-3 seconds
Status:              Active on every scraper run
```

---

## 🔄 AUTOMATION WORKFLOW

### **Daily @ 2:00 AM GMT (OCI Cron)**
```
OCI Cron triggers
     ↓
run_scraper.py executes main_scraper.py
     ↓
Runs Google Maps scraper (pharma, biotech)
     ↓
Runs niche scrapers:
  - Oil & Gas (Contract Laboratory)
  - Materials (A2LA)
  - Environmental (TNI)
     ↓
Validates all URLs (95%+ success)
     ↓
Generates CSVs:
  - tstr_directory_import.csv (listings)
  - sales_contacts.csv (contact data)
  - invalid_urls.csv (failed validations)
     ↓
Checks Supabase for duplicates
     ↓
Inserts only new verified listings
     ↓
Logs to scraper.log
     ↓
Frontend (Cloudflare) reads updated Supabase data
     ↓
CRITICAL: Keeps OCI instance active (prevents Oracle shelving)
```

**Last Successful Run**: November 10, 2025 02:31 UTC
- Scraped: 108 listings
- New listings: 0 (all exist in DB)
- Contacts: 64 sales leads
- Invalid URLs: 17

---

## 🔗 IMPORTANT LINKS

### **Production**
- **Live Site**: https://tstr.site
- **GitHub Repo**: https://github.com/JAvZZe/tstr-site

### **Oracle Cloud Infrastructure**
- **Instance IP**: 84.8.139.90
- **SSH Access**: `ssh -i /tmp/oci-key.pem opc@84.8.139.90`
- **SSH Key**: `/media/al/1TB_AI_ARCH/AI_PROJECTS_ARCHIVE/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key`
- **Scraper Path**: `/home/opc/tstr-scraper/`
- **Logs**: `/home/opc/tstr-scraper/scraper.log`

### **Supabase**
- **Dashboard**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
- **Table Editor**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/editor
- **SQL Editor**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/sql
- **URL**: https://haimjeaetrsaauitrhfy.supabase.co

### **Cloudflare**
- **Pages Dashboard**: https://dash.cloudflare.com/
- **Deployment**: Via GitHub Actions push to main

### **Local Paths (Linux)**
- **Project Root**: `/home/al/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/`
- **Automation**: `web/tstr-automation/`
- **Frontend**: `web/tstr-frontend/`
- **Scrapers**: `web/tstr-automation/scrapers/`

### **External Archive**
- **Archive Path**: `/media/al/1TB_AI_ARCH/AI_PROJECTS_ARCHIVE/TSTR-site Archive/`
- **Purpose**: Long-term storage of completed work, reports, and historical data
- **Access**: Mount external drive before accessing archived files

---

## 📝 PENDING TASKS

### **High Priority**
- [x] Deploy Astro website (✅ Live at https://tstr.site)
- [x] Connect custom domain (✅ tstr.site active)
- [x] Automated scraping (✅ Daily cron on OCI)
- [x] Add Oil & Gas Testing category scrapers (✅ Code integrated, pending deployment)
- [ ] Expand Environmental Testing (currently 14 listings)

### **Medium Priority**
- [ ] Add more geographic regions (Asia, Europe, Middle East)
- [ ] Create admin dashboard for monitoring scraper health
- [ ] Setup error alerting (email/Slack for scraper failures)
- [ ] Implement A2LA Materials Testing scraper enhancements
- [ ] Add TNI Environmental scraper improvements

### **Low Priority**
- [ ] Research and fix 17 invalid URLs in invalid_urls.csv
- [ ] Add Google Analytics or privacy-friendly analytics
- [ ] Implement caching layer for faster page loads
- [ ] Optimize OCI scraper for multiple sources simultaneously

### **Authentication & Rights Management** ✅ FULLY OPERATIONAL
- [x] **LinkedIn OAuth UI** - Buttons added to login/signup pages
- [x] **Database Schema** - listing_owners table and functions created ✅
- [x] **Domain Verification Logic** - Auto-claim functions implemented & tested ✅
- [x] **Claim API Endpoints** - Backend logic for listing ownership
- [x] **Setup Scripts** - Configuration guides and test scripts created
- [x] **LinkedIn App Created** - App created and credentials documented ✅
- [x] **Database Migration** - Applied to production ✅
- [x] **Supabase Provider Setup** - LinkedIn provider configured with correct Client ID ✅
- [x] **Environment Variables** - Update production env vars in Cloudflare Pages
- [x] **Provider Name Fix** - Updated frontend to use 'linkedin_oidc' ✅
- [x] **LinkedIn Redirect URI** - Update LinkedIn app OAuth redirect URLs ✅
- [x] **User Profile Creation** - Automatic profile creation trigger ✅
- [x] **Account Dashboard** - User profile display and management ✅
- [x] **End-to-End Testing** - LinkedIn OAuth + automatic profile creation ✅
- [x] **Redirect Loop Fix** - Fixed auth state handling for OAuth callbacks ✅
- [ ] **Owner Dashboard** - User interface for managing claims
- [ ] **Listing Claim UI** - Frontend integration on listing pages
- [ ] **Account Dashboard UX** - Improve styling and user experience (IN PROGRESS)

**Implementation Plan:** See `docs/active/LINKEDIN_OAUTH_IMPLEMENTATION_PLAN.md`
**Setup Guide:** See `LINKEDIN_OAUTH_SETUP_GUIDE.md`
**Strategy:** Corporate Domain Verification Model (80% automation)
**Timeline:** Account dashboard UX improvements in progress
**Progress:** 100% complete - Authentication system fully operational, starting UI enhancements

---

## 🎯 SUCCESS CRITERIA

### **Phase 1: MVP** ✅ COMPLETE
- [x] Build Astro frontend
- [x] Setup Supabase database
- [x] Create Python scrapers
- [x] Implement URL validation
- [x] Deploy to Oracle Cloud (OCI)
- [x] Setup automated scheduling (cron)

### **Phase 2: Production** ✅ COMPLETE
- [x] Deploy website publicly (https://tstr.site)
- [x] Configure custom domain
- [x] Monitor automated runs (daily cron working)
- [x] Gather 100+ verified listings (163 achieved)

### **Phase 3: Growth** 🔄 IN PROGRESS
- [ ] 500+ listings (currently 163)
- [x] Multiple regions (US, Kuwait, Thailand, UK, Singapore)
- [ ] Multiple categories (3 of 5 complete)
- [ ] Lead generation active
- [ ] Revenue generation (AdSense, affiliate, premium listings)
- [ ] **User authentication & rights management** (LinkedIn OAuth + domain verification)

### **Phase 4: Monetization** 📋 PLANNED
- [ ] Professional subscription tier ($295/month)
- [ ] Premium subscription tier ($795/month)
- [ ] Enterprise tier ($2,500/month)
- [ ] Stripe payment integration
- [ ] Owner dashboard for claimed listings

---

## 🔧 MAINTENANCE TASKS

### **Daily**
- Check Cloud Scheduler logs for errors
- Monitor database growth

### **Weekly**
- Review invalid URLs in pending_research
- Check validation success rate

### **Monthly**
- Review cloud costs
- Optimize queries if needed
- Update scraper targets

---

## 📚 DOCUMENTATION INDEX

### **For Developers**
- `PROJECT_REFERENCE.md` - Technical reference
- `CLOUD_AUTOMATION_SOLUTION.md` - Cloud architecture
- `URL_VALIDATION_LIVE.md` - Production validation docs
- `SCHEDULING_STRATEGY.md` - Automation strategy
- `LINKEDIN_OAUTH_IMPLEMENTATION_PLAN.md` - Auth & rights management implementation

### **For Non-Technical**
- `EXECUTIVE_SUMMARY.md` - Business overview
- `QUICK_START.md` - Getting started
- `STATUS.txt` - Quick status check

### **For Operations**
- `DEPLOYMENT_STATUS.md` - Deployment details
- `handoff_core.md` - Session history
- `SESSION_SUMMARY_*.md` - Individual sessions

### **This Document**
- **Purpose**: Single source of truth for all agents
- **Update Frequency**: Every deployment or major change
- **Owners**: All agents (CASCADE, CURSOR, etc.)

---

## 🤝 MULTI-AGENT PROTOCOL

### **When to Update This Document**

✅ **Always update after**:
- Deploying new code
- Changing infrastructure
- Modifying costs
- Completing major tasks
- Changing schedules
- Database schema changes
- **UI/Branding changes** (logos, favicons, links, styling)
- **Content updates** (text, links, footer information)
- **Any successful change that affects the live website**

✅ **Update format**:
```markdown
**Last Updated**: [Date Time UTC]
**Updated By**: [Agent Name]
**Changes**: Brief description
```

### **What Each Agent Should Do**

#### **CASCADE (Windsurf)**
- Update deployment status
- Record infrastructure changes
- Update costs
- Maintain technical accuracy

#### **Future Agents**
- Read this document FIRST before making changes
- Update status after any modifications
- Keep costs current
- Flag conflicts or inconsistencies

### **Conflict Resolution**
- Most recent timestamp wins
- Check `handoff_core.md` for context
- Ask user if unclear

---

## 🚨 KNOWN ISSUES

### **Current Issues**
1. **Biotech & Oil/Gas Categories**: Not yet deployed (0 listings)
   - Impact: Only 3 of 5 categories active
   - Plan: Deploy scrapers in next phase
2. **Invalid URLs**: 17 URLs failed validation
   - Impact: Minor - logged in invalid_urls.csv
   - Action: Manual research needed for pending_research table
3. **Custom Fields**: Some listings missing specialized certification data
   - Impact: Reduced data richness for niche categories
   - Fix: Enhance scraper extraction logic

### **Resolved Issues**
1. ✅ Google Cloud migration to OCI - Successfully migrated to Oracle Always Free
2. ✅ Frontend deployment - Live on Cloudflare Pages
3. ✅ Automated scheduling - Cron running daily on OCI
4. ✅ URL validation - 95%+ success rate achieved
5. ✅ Duplicate listings - Resolved with Supabase checking

---

## 📊 VERSION HISTORY

### **v2.2.7** - December 1, 2025 (CURRENT)
- ✅ LinkedIn OAuth redirect URI configuration identified
- ✅ Supabase provider Client ID corrected
- 🔄 Need to update LinkedIn app redirect URIs
- 🚧 Pending: Oil & Gas scraper deployment to OCI (requires SSH key access)

### **v2.2.2** - December 1, 2025
- ✅ Corrected biotech/pharma categorization: merged into "Biopharma & Life Sciences Testers"
- ✅ Updated submit form to use merged category
- ✅ Removed separate biotech searches from scraper config
- ✅ Updated Biocompare source to use Pharmaceutical Testing category

### **v2.2.1** - November 30, 2025
- ✅ Terms of Service page created at `/terms` with comprehensive legal coverage
- ✅ Terms of Service link added to footer (positioned first in footer links)
- ✅ Footer configuration updated in `src/lib/contacts.ts`

### **v2.2.0** - November 29, 2025
- ✨ Homepage logo updated to "TSTR" on top and "hub" below (lowercase 'h')
- ✅ Favicon redesigned with text-based "TSTR/hub" design (16x16 SVG)
- ✅ LinkedIn icon added to footer across all pages (links to https://linkedin.com/company/tstr-hub)
- ✅ Footer centralized configuration updated in `src/lib/contacts.ts`

### **v2.1.0** - November 22, 2025
- ✨ Click tracking system deployed
- ✅ Internal redirect endpoint (`/api/out`) for analytics
- ✅ 6 listing pages updated with redirect links
- ✅ Security: Open redirect prevention via database validation
- ✅ Performance: Async non-blocking click logging
- ✅ SEO: Internal links preserve PageRank flow

### **v2.0.0** - November 10, 2025
- ✅ Live production at https://tstr.site
- ✅ 163 verified listings (Pharmaceutical: 108, Materials: 41, Environmental: 14)
- ✅ OCI scrapers running daily (2 AM GMT cron)
- ✅ Cloudflare Pages deployment via GitHub Actions
- ✅ $0/month operational cost (Oracle Always Free Tier)
- ✅ Multi-region coverage (US, Kuwait, Thailand, UK, Singapore)

### **v1.0.0** - October 2025
- Initial development and testing
- Google Cloud prototype (migrated to OCI)
- Core scraper development
- URL validation implementation

---

## 🎉 ACHIEVEMENTS

✅ **Production deployment complete** - https://tstr.site live
✅ **163 verified listings** across 3 testing categories
✅ **Fully automated scraping** - Daily OCI cron (15+ days uptime)
✅ **95%+ URL validation success** - Reliable data quality
✅ **$0/month operating cost** - Oracle Always Free + Cloudflare Free
✅ **No PC dependency** - Cloud-native infrastructure
✅ **Multi-region coverage** - 5 countries active
✅ **Professional UI** - Responsive Astro + React + Tailwind
✅ **Click analytics** - Internal redirect tracking system (2025-11-22)

---

## 📚 DOCUMENTATION INDEX

### **Current Context Files (Read These)**
- `TSTR.md` - Primary agent instructions & architecture
- `START_HERE.md` - Quick orientation for new agents
- `PROJECT_STATUS.md` - This file (infrastructure & status)
- `README.md` - Project overview & user-facing docs
- `.ai-session.md` - Session tracking & learnings
- `HANDOFF_TO_CLAUDE.md` - Latest agent handoff

### **Technical Documentation**
- `docs/` - Technical references & guides
- `web/tstr-automation/` - Scraper documentation & reports

### **Archived Documentation**
- `archive/old-docs/` - Historical context files (pre-consolidation)

---

**📌 REMEMBER**: This is the SINGLE SOURCE OF TRUTH. All agents must read and update this document. Keep it current!

---

**Status**: 🟢 ALL SYSTEMS OPERATIONAL
**Next Review**: When new scrapers deployed or major infrastructure changes
**OCI Status**: Active - Daily cron prevents instance shelving
