# GitHub Actions Workflows

## Disabled Workflows

### keep-supabase-active.yml.disabled
**Date Disabled:** November 8, 2025
**Reason:** No longer needed - Oracle Cloud scraper now runs daily (2AM GMT)

**Original Purpose:**
- Prevented Supabase free tier from pausing due to 7-day inactivity
- Triggered daily builds to generate database activity
- Was failing with permissions errors

**Why Disabled:**
- Oracle Cloud scraper configured with cron (daily at 2AM GMT)
- Scraper writes to Supabase database daily
- Generates sufficient activity to prevent pausing
- GitHub Actions workflow became redundant
- Stopped failing notification emails

**Alternative Solutions Considered:**
- Fix GitHub Actions permissions → Not worth effort (scraper handles it)
- Migrate to Neon/PlanetScale → Not needed (daily scraper solves issue)
- Upgrade Supabase paid tier → Not needed (free tier sufficient)

**Database Activity:**
- Source: Oracle Cloud Instance (84.8.139.90)
- Schedule: Daily at 2:00 AM GMT via cron
- Script: ~/tstr-scraper/run_scraper.py
- Activity: Read/write listings, check duplicates, upload data
- Risk of pausing: <1% (virtually eliminated)

**Decision:** Disabled workflow on Nov 8, 2025. Daily OCI scraper provides sufficient database activity.

---

**See Also:**
- `/media/al/AI_DATA/AI_PROJECTS_SPACE/SUPABASE_STATUS_ANALYSIS_NOV8.md` - Full analysis
- `/media/al/AI_DATA/AI_PROJECTS_SPACE/SUPABASE_PAUSE_CRISIS.md` - Original crisis document
