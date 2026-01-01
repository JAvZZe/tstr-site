# TSTR.directory - Global Testing Laboratory Directory

**Project Type**: Live production directory site
**External Path**: `/media/al/AvZ WD White My Passport/PROJECTS/TSTR.directory`
**Status**: 🟢 LIVE - Scrapers Deployed
**Last Updated**: 2025-12-01 12:00 UTC

---

## Current Status

### ✅ Working
- **Site Live**: https://tstr.directory (deployed via GitHub → Cloudflare Pages)
- **Frontend**: Astro + React + Tailwind, functioning
- **Database**: Supabase PostgreSQL with schema deployed
- **19 Listings**: Live and displaying on site (new listings pending upload)
- **CI/CD**: Working after reconnecting GitHub to Cloudflare (Oct 18)
- **Scrapers**: ✅ DEPLOYED on Oracle Cloud (Oct 27)
  - Server: Oracle Linux 9 instance (84.8.139.90)
  - Python 3.9.21 environment with all dependencies
  - Fixed dual_scraper.py structure (orphaned methods issue resolved)
  - Supabase integration working
   - Currently scraping BIVDA (biopharma/biotech testing companies)

### 🔄 In Progress
- **First production scrape**: Running now, targeting BIVDA + BBB sources
- **Cron automation**: Pending (will schedule daily scrapes at 2am UTC)

### 📋 Tech Stack
- **Frontend**: Astro 5.14.4, React 18.3.1, Tailwind CSS
- **Backend**: Python 3.11, dual_scraper.py (listings + leads)
- **Database**: Supabase (PostgreSQL + API)
- **Hosting**: Cloudflare Pages
- **Scraper Deployment**: Google Cloud Functions (currently non-functional)
- **APIs**: Google Maps Places API (for scraping)

---

## Architecture Overview

### Data Flow
```
Google Maps API → dual_scraper.py → Supabase → Cloudflare Pages → User
                    (Python)        (PostgreSQL)  (Astro/React)
```

### Scraper Design
**File**: `web/tstr-automation/dual_scraper.py`
- Dual-purpose: Directory listings + sales lead contacts
- Uses Google Maps Places API as primary source
- Falls back to web scraping if API unavailable
- Includes URL validator to check website validity before adding
- Outputs to CSV and/or directly to Supabase

### Deployment Strategy
**Current**: Oracle Cloud Free Tier (Always Free)
- **Instance**: Oracle Linux 9 VM (84.8.139.90)
- **Access**: SSH via `avz Oracle Linux 9 pvt ssh-key-2025-10-25.key`
- **Location**: `~/tstr-scraper/` on Oracle instance
- **Files deployed**:
  - `dual_scraper.py` (fixed structure)
  - `run_scraper.py` (wrapper with Supabase upload)
  - `url_validator.py`
  - `config.json` (BBB, BIVDA, Biocompare sources)
  - `.env` (configured with real Supabase keys)
- **Scheduler**: Cron (to be configured for daily runs)
- **Cost**: $0/month (Always Free tier)

**Previous Plan** (abandoned due to billing issues):
- Google Cloud Functions - billing in arrears, not pursued

---

## Key Files & Locations

### Documentation (Many docs, sign of context loss issues)
- `README.md` - Overview
- `PROJECT_STATUS.md` - Current state (last updated Oct 18)
- `handoff_core.md` - Agent handoff protocol
- `Agents_Guide_to_Scraper_Best_Practise.txt` - **Universal scraping principles** ⭐
- 40+ other markdown files (agent protocols, deployment guides, session summaries)

### Code
- `web/tstr-frontend/` - Astro site source
- `web/tstr-automation/dual_scraper.py` - Main scraper (32KB, 1000+ lines)
- `web/tstr-automation/cloud_function_main.py` - Cloud Functions entry points
- `web/tstr-automation/deploy.sh` - Deployment script
- `web/tstr-automation/.env` - **BLOCKED: Contains only placeholders** 🚨

### Data
- Database schema: `web/tstr-automation/SUPABASE_*.sql` (7 files)
- 19 listings currently in Supabase and displaying live

---

## Critical Blockers Analysis

### 1. Missing API Keys (.env file)
**Current state**: `.env` exists but has placeholder values
```
SUPABASE_URL="REPLACE_WITH_YOUR_SUPABASE_URL"
SUPABASE_KEY="REPLACE_WITH_YOUR_SUPABASE_SERVICE_ROLE_KEY"
...
```

**Fix**: User must populate with real values from:
- Supabase dashboard (keys documented in `handoff_core.md`)
- Google Maps API key

**Risk**: High. Without this, scrapers cannot connect to database.

### 2. Google Cloud Billing
**Status**: Unknown, possibly in arrears
**Project ID**: `business-directory-app-8888888`
**Region**: `us-central1`

**Options**:
1. **Fix billing**: User pays arrears, scrapers deploy to existing project
2. **Migrate**: Create new Google Cloud account, redeploy to free tier
3. **Alternative**: Use different cloud provider (AWS Lambda, Azure Functions, Cloudflare Workers)

**Recommendation**: Check Google Cloud Console first. If arrears are small (<$50), pay and continue. If large or recurring, migrate to fresh free tier.

---

## Agent Coordination Observations

### Documentation Proliferation
**Issue**: 40+ markdown files created by previous agents
- Sign of memory loss between sessions
- Multiple "handoff" and "status" documents with conflicting info
- Agent protocol files for CASCADE, Gemini, Claude Desktop

**Pattern**: Each agent created new status files instead of updating existing ones
**Lesson**: This is exactly what the new continuity system prevents ✓

### What Worked
- `Agents_Guide_to_Scraper_Best_Practise.txt` contains solid universal principles
- `handoff_core.md` protocol (single handoff doc)
- `PROJECT_STATUS.md` as single source of truth (though not always updated)

### What Didn't Work
- Too many agent-specific protocol files
- Duplicate session summaries
- No persistent task queue (tasks documented in multiple places)
- No learning extraction system

---

## Extracted Universal Principles (Saved to DB)

From `Agents_Guide_to_Scraper_Best_Practise.txt`:

1. **Ethics**: Check robots.txt, respect disallowed paths
2. **Anti-blocking**: Random delays, rotate User-Agents, avoid honeypots
3. **Cost optimization**: Indirect extraction (reusable functions) > direct LLM parsing
4. **JS handling**: Check for internal APIs before using headless browser
5. **Token efficiency**: Clean/compress HTML before LLM parsing, use smaller models
6. **Deployment**: Never commit .env files, always check existence before deploy
7. **Cloudflare CI/CD**: If broken, disconnect and reconnect repo
8. **Cloud Functions**: 540s timeout limit, design for chunked processing

*All saved to learnings table with confidence ratings 4-5.*

---

## Next Actions (Priority Order)

### P1 - USER ACTION REQUIRED
1. Check Google Cloud Console billing status
2. Decide: Pay arrears OR create new account
3. Populate `.env` file with real API keys

### P2 - AGENT TASKS (after P1 complete)
4. Test `dual_scraper.py` locally with real keys
5. Deploy scrapers to cloud (existing or new account)
6. Set up Cloud Scheduler for automatic runs
7. Verify scrapers are adding new listings to database

### P3 - ENHANCEMENTS
8. Implement clickable category links on frontend
9. Add monitoring/alerting for scraper failures
10. Document actual scraper performance (cost per listing, time, success rate)

---

## Recommendations

### Immediate
1. **Consolidate documentation**: Most of those 40+ files can be archived
2. **Use continuity system**: Track tasks in our new database, not scattered markdown
3. **Test locally first**: Before deploying to cloud, verify scraper works with real keys

### Strategic
1. **Cost tracking**: Once scrapers running, measure actual cost per scraping run
2. **Free tier priority**: Google Cloud Functions free tier = 2M invocations/month, 400K GB-seconds
3. **Cloudflare Workers alternative**: Consider Cloudflare Workers (100K requests/day free) if Google Cloud costs escalate

### Learning Application
- Apply new checkpoint system: Don't lose context between sessions
- Use task queue in database: Clear prioritization
- Extract learnings as work progresses: Build institutional knowledge

---

## Project-Specific Context

**User Profile**: Non-tech, AuDHD, prefers terse factual communication
**Approach**: Lean MVP, quick iteration, systematic testing
**Pain Point**: Context loss between agent sessions (hence the 40+ docs)
**Solution**: This continuity system addresses core problem

**Domain Knowledge Required**:
- Testing laboratories industry
- Directory site business model
- Web scraping ethics and techniques
- Supabase PostgreSQL
- Astro framework
- Google Cloud Functions

**Critical Success Factors**:
1. Scrapers must be cost-effective (<$10/month ideal)
2. Data must be accurate and up-to-date
3. Site must load fast (Cloudflare CDN helps)
4. Must avoid IP blocks (ethical scraping)

---

## Files to Reference

**When working on TSTR.directory**:
1. This file - Project overview
2. `/media/al/.../TSTR.directory/README.md` - Quick start
3. `/media/al/.../TSTR.directory/PROJECT_STATUS.md` - Latest status
4. `/media/al/.../web/tstr-automation/dual_scraper.py` - Scraper code
5. Database learnings with tags: `scraping`, `cloudflare`, `google-cloud`

**Universal principles**: Query learnings table for `scraping`, `deployment`, `cost` tags

---

## Industry Research Methodology (Next Phase)

### Goal
Identify high-value info that testing service buyers want per industry niche, then find sources and adapt scrapers.

### Research Process (OODA + Pareto)

**1. Identify Buyer Personas & Pain Points** (Observe)
- **Who buys?** Procurement managers, QA directors, R&D leads, compliance officers
- **What do they need?** Accreditations, turnaround time, sample types, price ranges, case studies
- **Pain point**: "I need ISO 17025 accredited lab for soil testing in Texas with 48hr turnaround"

**2. Map Industry-Specific Data** (Orient)
For each niche (Oil & Gas, Biopharma & Life Sciences, etc.):
- **Must-have data**: Accreditations (ISO, CLIA, CAP), certifications, test methods
- **Nice-to-have**: Equipment lists, sample volume capacity, client logos, case studies
- **Deal-breakers**: Price transparency, turnaround times, geographic coverage

Example: Biopharma & Life Sciences Testing
- Critical: FDA registration, GMP compliance, stability testing capabilities
- Valuable: API testing experience, CMC support, regulatory filing support
- Sources: BIVDA member directory, Pharmtech lists, FDA registered facilities, Biocompare

**3. Source Discovery** (Orient)
- **Industry associations**: Member directories (like BIVDA for pharma)
- **Regulatory databases**: FDA, EPA, state health departments
- **Trade publications**: Labs mentioned in industry press
- **Competitor analysis**: Who do established players list as partners?

**4. Source Structure Analysis** (Decide)
For each potential source:
- Inspect HTML structure (browser DevTools → Elements)
- Check for pagination, infinite scroll, JS-rendered content
- Test if data is in static HTML or requires JS execution
- Look for APIs (Network tab while browsing)
- Check robots.txt for allowed scraping

**5. Scraper Adaptation** (Act)
- **Static HTML**: BeautifulSoup (current approach for BIVDA)
- **JS-rendered**: Selenium/Playwright (heavier, slower, more detectable)
- **API available**: Direct API calls (fastest, most reliable)
- **Anti-bot protection**: Respect rate limits, rotate user agents, use delays

### Best Practices (from Agents_Guide)
- ✅ Check robots.txt, respect disallowed paths
- ✅ Random delays (1-3s between requests)
- ✅ Rotate User-Agents
- ✅ URL validation before adding to database
- ❌ Never commit .env files
- ❌ Avoid honeypot links (hidden in CSS)

### Current Sources Configured
1. **BBB** - Environmental Testing (US-focused, general)
2. **BIVDA** - Biopharma & Life Sciences Testing (UK-focused, IVD manufacturers)
3. **Biocompare** - Biopharma & Life Sciences Testing (lab services marketplace)

### Next Sources to Research
- **Oil & Gas**: API certifications, NDT testing labs
- **Semiconductor**: SEMI standards, failure analysis labs
- **Food Safety**: AOAC, FDA LACF, allergen testing
- **Clinical**: CLIA certified, CAP accredited labs

---

## Success Metrics

- [x] Scrapers deployed and running automatically
- [ ] New listings added weekly (target: 10-20/week) - **First run in progress**
- [x] Cost <$10/month for scraping infrastructure ($0 on Oracle Free Tier)
- [x] Site uptime >99.5%
- [ ] No IP blocks or scraping bans - **Monitoring**
- [ ] Category links functional on frontend

---

*This project demonstrates the need for the continuity system we just built. Use it as reference for agent coordination patterns.*
