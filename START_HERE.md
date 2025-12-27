# START HERE - TSTR.site Project

**Project**: Global testing laboratory directory (Oil & Gas, Environmental, Materials Testing, etc.)
**Status**: Production - scrapers on OCI, frontend LIVE at https://tstr.site
**Location**: `/home/al/tstr-site-working`

---

## 🚨 CRITICAL: MANDATORY FIRST STEP FOR ALL AGENTS

**⚠️ ALWAYS RUN GLOBAL BOOTSTRAP BEFORE ANY PROJECT WORK:**

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh
```

**This provides:**
- Global system context and learnings
- Cross-project task coordination
- Agent handoff information
- Learning system access for optimal decision making

**Failure to bootstrap may result in:**
- Missing critical context
- Duplicating work already done
- Breaking continuity across agents

---

## ⚠️ PROJECT BOOTSTRAP (After Global Bootstrap)

**Run this SECOND** (after global bootstrap):

```bash
./bootstrap.sh TSTR.site
```

**What this does**:
- ✅ Loads project-specific learnings from database (filtered for TSTR.site)
- ✅ Shows pending tasks (for this project only)
- ✅ Displays recent session context
- ✅ Checks for handoffs
- ✅ Reminds you of protocol

**Why this matters**: Last 3 agents forgot critical learnings #45, #67, #88 and repeated mistakes. Bootstrap prevents this.

**If bootstrap.sh doesn't exist**: You're in the wrong directory or symlinks not created. Check you're in `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/`

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

1. **Fix OCI SSH access** - Locate correct SSH key path and verify scraper logs

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

**Remember**: First Principles. OODA Loop. Test before deploy. No theater, working code only. NB: Always test your assumptions and verify the work to see if it was done correctly. Admit when you do not know. Score the certainty levels.

---

## During Work (Protocol Compliance)

### Every ~30 Minutes or After Significant Progress
```bash
./checkpoint.sh "what you accomplished"
```

### After Errors/Discoveries (3+ failed attempts OR new insights)
```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state"
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

## AI Agent Selection Guide

### When to Use Each Agent

- **Claude Sonnet 4.5**: Complex reasoning, architecture, review, decisions ($$$)
- **Gemini 2.5 Pro**: Continuation when Claude depleted, medium complexity (FREE, rate-limited)
- **OpenRouter**: Batch processing, simple tasks, free tier
- **Qwen3-Coder**: Cost-effective bulk processing and repetitive tasks ($0.45/1M input, $1.50/1M output)
  - Ideal for: Generating multiple similar components, repetitive code tasks, bulk operations
  - Use for: Creating multiple category pages, standard API endpoints, consistent UI patterns

---

## Tools Available From This Folder

Because of symlinks, you can run:
- `./bootstrap.sh TSTR.site` - Load project context
- `./checkpoint.sh "msg"` - Save state
- `./resume.sh` - Load last checkpoint
- `./handoff.sh agent reason` - Transfer to another agent

All point to global system at `/media/al/AI_DATA/AI_PROJECTS_SPACE/`

---

**Next step**: Read `TSTR.md` for full context.
