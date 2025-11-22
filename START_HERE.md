# START HERE - TSTR.site Project

**Project**: Global testing laboratory directory (Oil & Gas, Environmental, Materials Testing, etc.)
**Status**: Production scrapers on OCI, frontend needs deployment
**Location**: `/home/al/tstr-site-working`

---

## ⚠️ MANDATORY: Bootstrap Before ANY Work

**Run this FIRST** (before reading anything else):

```bash
./bootstrap.sh TSTR.site
```

**What this does**:
- ✅ Loads 90 learnings from database (filtered for TSTR.site)
- ✅ Shows pending tasks (for this project only)
- ✅ Displays recent session context
- ✅ Checks for handoffs
- ✅ Reminds you of protocol

**Why this matters**: Last 3 agents forgot critical learnings #45, #67, #88 and repeated mistakes. Bootstrap prevents this.

**If bootstrap.sh doesn't exist**: You're in the wrong directory or symlinks not created. Check you're in `/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/`

---

## New Agent Checklist (Read in Order)

1. ✅ **This file** (you're here - quick orientation)
2. 📋 **`TSTR.md`** - PRIMARY agent instructions (architecture, commands, priorities, troubleshooting)
3. 🎯 **`ORGANIZATION_UPDATE_2025-11-22.md`** - Niche directory structure and strategic focus
4. 📝 **`.ai-session.md`** - Latest session context, learnings, active tasks
5. 🔄 **`HANDOFF_TO_CLAUDE.md`** - Current handoff from previous agent (if exists)
6. 📊 **`PROJECT_STATUS.md`** - Deployment status, infrastructure details, costs

**Niche-Specific Docs**:
- 🔋 **`/Hydrogen Infrastructure Testing/`** - Hydrogen testing standards and implementations
- 🧬 **`/Biotech Directory/`** - Biotech/Pharma/Life Sciences resources and workflows

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

---

## During Work (Protocol Compliance)

### Every ~30 Minutes or After Significant Progress
```bash
./checkpoint.sh "what you accomplished"
```

### After Errors/Discoveries (3+ failed attempts OR new insights)
```bash
cd "/home/al/AI PROJECTS SPACE/SYSTEM/state"
python3 db_utils.py learning-add \
  "What you learned" \
  "gotcha" \
  5 \
  "TSTR.site,relevant-tags"
```

### End of Session
```bash
./checkpoint.sh "final state description"
# OR if handing off to another agent
./handoff.sh <agent-name> <reason>
```

---

## Tools Available From This Folder

Because of symlinks, you can run:
- `./bootstrap.sh TSTR.site` - Load project context
- `./checkpoint.sh "msg"` - Save state
- `./resume.sh` - Load last checkpoint
- `./handoff.sh agent reason` - Transfer to another agent

All point to global system at `/home/al/AI PROJECTS SPACE/`

---

**Next step**: Read `TSTR.md` for full context.
