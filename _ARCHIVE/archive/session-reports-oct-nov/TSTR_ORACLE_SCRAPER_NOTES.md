# TSTR.site Oracle Cloud Scraper - Session Notes

**Date**: 2025-10-28
**Discovered by**: Claude during deployment investigation

## Oracle Cloud Scraper Status

### Evidence of Oracle Deployment
- **Database verification**: Supabase has 127 listings (up from 19)
- **Last scrape**: 2025-10-27 18:52 UTC (successful)
- **New entries**: 108 pharmaceutical testing labs (UK-based)
- **Scraper code**: `dual_scraper.py` in `/web/tstr-automation/`

### What Was Scraped
- Company: WOUNDCHEK Laboratories BV, Werfen Limited, Vital Signs Solutions, etc.
- Category: Pharmaceutical Testing (category_id: 20c1a274-0393-4dc9-97f1-dbf5f1293bf9)
- Location: UK region
- All entries have working website URLs

### Oracle Cloud Configuration
**Location**: Unknown (user set up via Oracle dashboard)
**Schedule**: Unknown (but ran successfully on Oct 27)
**API Keys**: Uses Google Maps API (configured in Oracle environment)

**NOTE**: No Oracle configuration found in repo files - deployment managed externally

## Critical Discovery: Static Site Problem

### Root Cause
Astro is a **static site generator** - it queries Supabase at **build time**, not runtime.

**Impact**:
- Scraper works ✅
- Data in Supabase ✅
- Live site shows OLD data ❌

### Solution Required
Site must be **rebuilt** after each scraper run to show new data.

**Options**:
1. Fix GitHub → Cloudflare CI/CD (currently broken)
2. Set up Supabase webhook → Cloudflare rebuild trigger
3. Manual rebuild after each scrape

## Files That Need Updating
1. `/DEPLOYMENT_STATUS.md` - Add Oracle scraper success
2. `/SESSION_STATE.json` - Update lab_count to 127
3. Project database - Add learnings about static site limitations

## Next Steps
1. Document Oracle setup (need user confirmation on details)
2. Fix CI/CD pipeline OR set up auto-rebuild webhook
3. Deploy fresh build with all 127 listings
