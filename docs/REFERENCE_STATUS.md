# 📚 TSTR.SITE - REFERENCE STATUS & HISTORY

> **NOTE**: This is a static reference document. For active status, see `PROJECT_STATUS.md`.
> **Last Archived**: December 3, 2025

---

## 📜 VERSION HISTORY ARCHIVE

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

## 📦 COMPONENT DETAILS (REFERENCE)

### **Python Scrapers** (Production)

#### 1. `url_validator.py`
- **Purpose**: URL validation module
- **Features**: Two-tier validation (HEAD → GET), caching, timeout handling
- **Status**: ✅ PRODUCTION
- **Success Rate**: 95%

#### 2. `dual_scraper.py`
- **Purpose**: Google Maps API scraper (pharma, biotech, etc.)
- **Features**: Google Maps API, URL validation, duplicate detection
- **Status**: ✅ PRODUCTION (deployed as cloud function)
- **Rate Limiting**: 0.5s between requests

#### 3. `main_scraper.py`
- **Purpose**: Main scraper orchestrator
- **Features**: Combines Google Maps + niche-specific scrapers
- **Status**: ✅ CREATED (pending OCI deployment)

#### 4. `run_scraper.py`
- **Purpose**: OCI cron job entry point
- **Features**: Runs main_scraper.py daily
- **Status**: ✅ UPDATED (pending OCI deployment)
- **Schedule**: Daily 2 AM GMT

#### 5. `scraper.py`
- **Purpose**: Secondary scraper (listings only)
- **Features**: Alternative sources, duplicate detection, URL validation
- **Status**: ✅ PRODUCTION (deployed as cloud function)

#### 6. `cleanup_invalid_urls.py`
- **Purpose**: Database validation & cleanup
- **Features**: Re-validate existing URLs, move invalid to research
- **Status**: ✅ PRODUCTION (deployed as cloud function)

#### 7. `main.py`
- **Purpose**: Cloud Function entry points
- **Features**: Wraps all scrapers for Google Cloud deployment
- **Status**: ✅ DEPLOYED

### **Configuration Files**

#### `config.json`
- **Purpose**: Scraper targets
- **Google Maps Searches**: 15 categories × locations
- **Alternative Sources**: 3 (Energy Pedia, Pharma Tech, Biocompare)

#### `requirements.txt`
- **Purpose**: Python dependencies
- **Packages**: requests, beautifulsoup4, supabase, functions-framework, etc.

#### `.env`
- **Purpose**: Environment variables
- **Variables**: SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_ROLE_KEY

---

## 🤝 MULTI-AGENT PROTOCOL (REFERENCE)

### **When to Update PROJECT_STATUS.md**
✅ **Always update after**:
- Deploying new code
- Changing infrastructure
- Modifying costs
- Completing major tasks
- Changing schedules
- Database schema changes
- **UI/Branding changes**
- **Content updates**

### **Conflict Resolution**
- Most recent timestamp wins
- Check `handoff_core.md` for context
- Ask user if unclear

---

## 💰 COST PROJECTIONS (REFERENCE)

**If scaled to 1000+ listings**:
- OCI: Still FREE (Always Free Tier covers 2 AMD instances)
- Supabase: May need to upgrade (~$25/month if >500MB)
- Cloudflare Pages: Still FREE (unlimited requests)
- Total: ~$25/month

**Cost optimization**: Maximizing free tiers across all services
