# START HERE - TSTR.site Project

**Project**: Global testing laboratory directory (Oil & Gas, Environmental, Materials Testing, etc.)
**Status**: Production scrapers on OCI, frontend needs deployment
**Location**: `/home/al/tstr-site-working`

---

## New Agent Checklist (Read in Order)

1. ✅ **This file** (you're here - quick orientation)
2. 📋 **`TSTR.md`** - PRIMARY agent instructions (architecture, commands, priorities, troubleshooting)
3. 📝 **`.ai-session.md`** - Latest session context, learnings, active tasks
4. 🔄 **`HANDOFF_TO_CLAUDE.md`** - Current handoff from previous agent (if exists)
5. 📊 **`PROJECT_STATUS.md`** - Deployment status, infrastructure details, costs

---

## Current Priorities (P0)

1. **Fix GitHub workflow failure** - Uncommitted changes blocking "Keep Supabase Active" workflow
2. **Deploy frontend** - Build and deploy Astro site to Cloudflare Pages

**Full priority list**: See `TSTR.md` → "Current Priorities"

---

## Quick Reference

**Scrapers** (Active on OCI):
- Location: OCI instance 84.8.139.90 at `~/tstr-scraper/`
- Scheduler: Cron daily at 2 AM GMT
- Status: ✅ Working (127 listings deployed)

**Frontend** (Not deployed):
- Location: `web/tstr-frontend/`
- Target: Cloudflare Pages
- Status: Built but needs deployment

**Database**:
- Supabase: https://haimjeaetrsaauitrhfy.supabase.co
- Status: ✅ Operational

**For all commands, troubleshooting, and details**: See `TSTR.md`

---

## File Organization

**Root-level docs** (read these):
- `TSTR.md` - Agent instructions
- `.ai-session.md` - Session tracking
- `PROJECT_STATUS.md` - Deployment status
- `README.md` - Project overview

**Technical docs**: `docs/` folder
**Historical docs**: `archive/old-docs/` folder

---

**Remember**: First Principles. OODA Loop. Test before deploy. No theater, working code only.

**Next step**: Read `TSTR.md` for full context.
