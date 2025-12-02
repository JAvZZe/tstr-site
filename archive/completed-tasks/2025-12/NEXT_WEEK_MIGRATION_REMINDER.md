# 🔔 NEXT WEEK: Migrate Database to Neon or PlanetScale

**Created:** 2025-10-29
**Agent:** Claude Code (Sonnet 4.5) - avztest8@gmail.com
**Action Date:** Week of 2025-11-04 (or when context tokens available)
**Priority:** HIGH

---

## Why This Reminder Exists

**Temporary solution implemented today:**
- ✅ GitHub Actions keep-alive workflow
- ✅ Triggers daily Cloudflare build
- ✅ Keeps Supabase active (prevents pause)

**Problem with temporary solution:**
- Still on Supabase free tier (500MB limit)
- Still subject to 7-day inactivity policy
- Generates unnecessary commits daily
- Wastes build minutes

**Better solution next week:**
- Migrate to Neon or PlanetScale
- Stay free forever
- More generous limits
- No keep-alive hacks needed

---

## Context for Next Session

### Current Supabase Project
- **Account:** tstr.site1@gmail.com
- **Project ID:** haimjeaetrsaauitrhfy
- **URL:** https://haimjeaetrsaauitrhfy.supabase.co
- **Data:** 127 active listings
- **Status:** Protected by keep-alive workflow

### Current Code Locations
- **Database config:** `/home/al/tstr-site-working/web/tstr-frontend/src/lib/supabase.ts`
- **Form submission:** `/home/al/tstr-site-working/web/tstr-frontend/src/pages/submit.astro`
- **Oracle scraper:** External (Oracle Cloud) - connection string needs updating

### Credentials Location
- **Master file:** `/home/al/AI_PROJECTS_SPACE/TSTR_CREDENTIALS_MASTER.md`
- **Current keys:**
  - PUBLIC_SUPABASE_URL: https://haimjeaetrsaauitrhfy.supabase.co
  - PUBLIC_SUPABASE_ANON_KEY: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO

---

## Migration Options Comparison

### Option 1: Neon (RECOMMENDED - Easiest)

**Pros:**
- ✅ PostgreSQL compatible (drop-in replacement)
- ✅ Same SQL syntax as Supabase
- ✅ Auto-resumes if paused (better than Supabase)
- ✅ Free forever
- ✅ 500MB storage (same as Supabase free)
- ✅ Minimal code changes

**Migration Steps:**
1. Create Neon account (5 min)
2. Export Supabase data via pg_dump (10 min)
3. Import to Neon via psql (10 min)
4. Update connection strings in 3 files (5 min)
5. Test locally (10 min)
6. Deploy to Cloudflare (5 min)
7. Update Oracle scraper config (5 min)
8. **Total: ~1 hour**

**Cons:**
- Still 500MB limit (but won't pause)

**Best for:** Quick migration, minimal changes

---

### Option 2: PlanetScale (Most Storage)

**Pros:**
- ✅ 5GB free storage (10x more than Supabase!)
- ✅ 1 billion row reads/month
- ✅ 10 million row writes/month
- ✅ Never pauses
- ✅ Free forever
- ✅ Great for long-term growth

**Migration Steps:**
1. Create PlanetScale account (5 min)
2. Export Supabase data (10 min)
3. Convert PostgreSQL → MySQL schema (30 min)
4. Import to PlanetScale (15 min)
5. Update code for MySQL syntax (30 min)
6. Test locally (15 min)
7. Deploy to Cloudflare (5 min)
8. Update Oracle scraper (20 min)
9. **Total: ~2.5 hours**

**Cons:**
- MySQL not PostgreSQL (more code changes)
- Schema conversion needed
- Different SQL syntax in some places

**Best for:** Long-term free solution with room to grow

---

## Decision Matrix for Next Week

**Choose Neon if:**
- Want quickest migration (1 hour)
- Don't need more than 500MB soon
- Want minimal code changes
- PostgreSQL experience

**Choose PlanetScale if:**
- Need more storage (5GB)
- Planning to grow beyond 500MB
- Willing to invest 2.5 hours
- MySQL experience or willing to learn

**My recommendation:** Start with Neon (easier), migrate to PlanetScale later if you hit 500MB limit.

---

## Pre-Migration Checklist

Before starting migration next week, ensure:

- [ ] Keep-alive workflow is working (check GitHub Actions tab)
- [ ] Supabase is still active (login to dashboard)
- [ ] 127 listings still displaying on live site
- [ ] Form submissions still work
- [ ] Oracle scraper still running
- [ ] Have credentials from TSTR_CREDENTIALS_MASTER.md
- [ ] Have Supabase database password

---

## Migration Day Workflow

### Phase 1: Preparation (15 min)
1. Read SUPABASE_PAUSE_CRISIS.md (detailed steps)
2. Create new Neon/PlanetScale account
3. Note new connection details
4. Test new database connection

### Phase 2: Data Export (15 min)
1. Login to Supabase dashboard
2. Export schema via pg_dump
3. Export data via pg_dump
4. Verify files created correctly
5. Check file sizes

### Phase 3: Data Import (15 min)
1. Create tables in new database
2. Import schema
3. Import data
4. Verify row counts match (127 listings)
5. Test queries

### Phase 4: Code Updates (15 min)
1. Update supabase.ts with new URL/keys
2. Update submit.astro if needed
3. Update Cloudflare environment variables
4. Test locally
5. Commit changes

### Phase 5: Deployment (10 min)
1. Push to GitHub
2. Wait for Cloudflare build
3. Verify site shows 127 listings
4. Test form submission
5. Check database receives data

### Phase 6: Oracle Scraper (10 min)
1. Update scraper connection string
2. Test scraper locally
3. Deploy to Oracle Cloud
4. Verify scraper can write
5. Monitor next scheduled run

### Phase 7: Cleanup (10 min)
1. Delete GitHub Actions keep-alive workflow
2. Delete .build-trigger file
3. Commit cleanup
4. Mark Supabase project for deletion (optional)
5. Update documentation

**Total estimated time: ~1.5 hours** (Neon) or **~3 hours** (PlanetScale)

---

## What to Do Next Week

**When you start next session:**

1. **Read this file first**
2. **Check current status:**
   - Is Supabase still active?
   - Is keep-alive workflow running?
   - Are listings still showing?

3. **Decide: Neon or PlanetScale?**
   - Neon = faster, easier
   - PlanetScale = more storage

4. **Follow migration steps** from SUPABASE_PAUSE_CRISIS.md

5. **Test thoroughly** before deleting Supabase

6. **Update credentials** in TSTR_CREDENTIALS_MASTER.md

---

## Important Files Reference

**Migration guide:**
- `/home/al/AI_PROJECTS_SPACE/SUPABASE_PAUSE_CRISIS.md` - Full details

**Current credentials:**
- `/home/al/AI_PROJECTS_SPACE/TSTR_CREDENTIALS_MASTER.md`

**Code to update:**
- `/home/al/tstr-site-working/web/tstr-frontend/src/lib/supabase.ts`
- `/home/al/tstr-site-working/web/tstr-frontend/src/pages/submit.astro`
- Oracle scraper config (external)

**Keep-alive (to remove after migration):**
- `/home/al/tstr-site-working/.github/workflows/keep-supabase-active.yml`
- `/home/al/tstr-site-working/.build-trigger`

---

## After Migration

**Update these documents:**
1. TSTR_CREDENTIALS_MASTER.md (new database credentials)
2. SESSION_STATE.json (new database provider)
3. Delete NEXT_WEEK_MIGRATION_REMINDER.md (this file)
4. Delete SUPABASE_PAUSE_CRISIS.md (no longer needed)

**Verify everything works:**
- Site displays 127 listings ✓
- Form submissions save to new database ✓
- Oracle scraper writes to new database ✓
- No Supabase dependencies remain ✓

---

## Estimated Costs

**Neon Free:**
- Cost: $0/month forever
- Storage: 500MB
- Compute: Generous free tier
- Upgrade to paid: $19/month (if needed)

**PlanetScale Free:**
- Cost: $0/month forever
- Storage: 5GB
- Reads: 1 billion rows/month
- Writes: 10 million rows/month
- Upgrade to paid: $29/month (if needed)

**Both are FREE and better than Supabase free tier.**

---

## Questions to Ask at Start of Next Session

1. Is keep-alive workflow still running? (Check GitHub Actions)
2. Is Supabase still active? (Check dashboard)
3. Are we ready to migrate? (1-3 hours available?)
4. Which provider: Neon (easy) or PlanetScale (more storage)?

---

## Success Criteria

Migration is successful when:
- ✅ All 127 listings visible on tstr.site
- ✅ Form submissions save to new database
- ✅ Oracle scraper writes to new database
- ✅ No errors in Cloudflare logs
- ✅ Keep-alive workflow deleted
- ✅ Supabase project marked for deletion
- ✅ Documentation updated

---

**Summary:**
- **Today:** Keep-alive protects Supabase
- **Next week:** Migrate to Neon (1h) or PlanetScale (3h)
- **Result:** Stay free forever, better limits, no pausing

**Don't forget this migration!** Set calendar reminder for next week.

---

**Agent:** Claude Code (Sonnet 4.5) - avztest8@gmail.com
**Created:** 2025-10-29
**Review Date:** 2025-11-04
