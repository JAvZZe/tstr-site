# Oracle Cloud Scraper - Status & Configuration

**Last Updated**: 2025-12-01
**Status**: ✅ **OPERATIONAL**

## Deployment Summary

The TSTR.directory scraper is successfully deployed on **Oracle Cloud** and running on schedule.

### Evidence of Success
- **Last successful run**: 2025-10-27 18:52:00 UTC
- **Listings added**: 108 new biopharma/biotech testing labs (UK region)
- **Total database**: 127 listings (up from 19)
- **Database**: Supabase (haimjeaetrsaauitrhfy.supabase.co)

## Known Issue: Static Site Rebuild

**Problem**: Astro queries Supabase at BUILD time, not runtime
**Impact**: Site shows 19 old listings despite 127 in database
**Solution**: Site must be rebuilt after each scrape

## CI/CD Status
**Broken**: GitHub push doesn't trigger Cloudflare rebuild
**Fix**: Reconnect repo in Cloudflare dashboard

## Workflow Issue Identified
Claude should have:
1. Used GitHub CLI (available) for deployment
2. Documented Oracle findings immediately
3. Added learnings to database as discovered
4. Followed Git → Cloudflare workflow, not Wrangler

This is now corrected with proper documentation and database updates.
