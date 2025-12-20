# OPENHANDS.md - TSTR.site Project

> **CRITICAL**: This project is part of the AI_PROJECTS_SPACE continuity system.
> **Global System**: `/media/al/AI_PROJECTS_SPACE/`
> **Project Context**: Read `TSTR.md` (this directory) for project-specific details.
> **Global Guidance**: See `/media/al/AI_PROJECTS_SPACE/OPENHANDS.md` for system-wide protocols.

---

## 🚨 CRITICAL: MANDATORY FIRST STEP FOR ALL AGENTS

### ⚠️ ALWAYS RUN GLOBAL BOOTSTRAP BEFORE ANY PROJECT WORK

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

## Mandatory Protocol for ALL Agents

### 1. Global Bootstrap (MANDATORY - See Above)

### 2. Project Session Start (ALWAYS)

**After global bootstrap, use project bootstrap**:
```bash
./bootstrap.sh TSTR.site
```

**Why bootstrap > resume**:
- Loads TSTR.site-specific learnings only (manageable vs. overwhelming)
- Filters by project name in tags AND content
- High confidence learnings only (≥4)
- Project-specific context and pending tasks

**Symlinks available**: In this folder, just run `./bootstrap.sh TSTR.site`

### 2. During Work

**Checkpoint frequently**:
```bash
cd "/media/al/AI_PROJECTS_SPACE" && ./checkpoint.sh "description of work completed"
```

**Extract learnings** after errors/discoveries:
```bash
cd "/media/al/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_learning
add_learning(
    "Your learning here",
    "gotcha",  # or "pattern", "optimization", "security"
    confidence=5,
    tags=["TSTR.site", "relevant-tech", "specific-issue"]
)
PYEOF
```

**Track tasks**:
```bash
cd "/media/al/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_task, update_task
task_id = add_task("TSTR.site", "Task description", assigned_to="openhands")
# ... do work ...
update_task(task_id, "completed", result="Result summary")
PYEOF
```

### 3. Session End or Handoff

```bash
cd "/media/al/AI_PROJECTS_SPACE" && ./handoff.sh <agent> <reason>
```

---

## OpenHands-Specific Guidance

### Strengths & Capabilities
- **Agent Framework**: Direct file editing, terminal execution, web browsing for UI testing
- **Ollama Integration**: Leverages local models (qwen2.5-coder for speed, deepseek-coder for complexity)
- **Development Workflow**: Handles full-stack development tasks autonomously
- **Testing & Validation**: Can run builds, tests, and verify deployments

### Workflow Preferences
1. **Test Before Deploy**: Always validate changes before pushing to production
2. **Free Tier Focus**: Stay within $1.04/month budget (Supabase free tier)
3. **Documentation**: Update PROJECT_STATUS.md after any successful changes
4. **Performance**: Use qwen2.5-coder for fast iteration, deepseek-coder for complex tasks

---

## Project-Specific Instructions

**Read these files IN ORDER**:

1. **START_HERE.md** - Quick orientation checklist
2. **TSTR.md** - PRIMARY agent instructions (architecture, commands, priorities)
3. **.ai-session.md** - Latest session context and active tasks
4. **PROJECT_STATUS.md** - Deployment status and infrastructure details
5. **HANDOFF_TO_CLAUDE.md** - Current handoff (if exists)

---

## TSTR.site Overview

**Business Model**: B2B directory + lead generation for testing laboratories in specialized, high-margin industries.

**Tech Stack**: Custom site (not WordPress) - Astro + React + Google Cloud Functions + Supabase

**Current Status**: Production - 163 listings deployed, scrapers active on OCI, frontend LIVE at https://tstr.site

**Strategic Focus**: Hydrogen Infrastructure Testing + Biotech/Pharma/Life Sciences

**Budget Constraint**: FREE TIERS ONLY - Currently $1.04/month ✅

---

## 📊 PROJECT STATUS PROTOCOL (MANDATORY)

**CRITICAL**: All agents MUST read and update `PROJECT_STATUS.md` before/after any work:

### Before Starting Work:
```bash
cat PROJECT_STATUS.md
```

### After Completing Changes:
1. **Update PROJECT_STATUS.md** with version increment and change details
2. **Commit and push** the updated status document
3. **Document ALL changes** that affect the live website

### Protocol Requirements:
- ✅ **ALWAYS** update PROJECT_STATUS.md after successful changes
- ✅ **NEVER** deploy changes without documenting them
- ✅ **READ FIRST** - Check current state before making changes
- ✅ **VERSION BUMP** - Increment version number for each update
- ✅ **TIMESTAMP** - Include date/time and agent attribution

---

## Architecture Overview

**Frontend**: `web/tstr-frontend/` (Astro + React + Tailwind)
- Static site generation with prerendered routes
- Dynamic category/region filtering
- Supabase integration for listings data

**Backend**: Supabase (https://haimjeaetrsaauitrhfy.supabase.co)
- PostgreSQL database with listings, categories, regions
- Row Level Security (RLS) enabled
- RESTful API for frontend consumption

**Scrapers**: `web/tstr-automation/` (Python, deployed on OCI)
- Automated data collection from testing service providers
- Scheduled execution (daily at 2:00 AM GMT)
- Oracle Cloud Infrastructure (FREE tier)

**Deployment**: Cloudflare Pages (FREE tier)
- Edge network for global performance
- Automatic builds from GitHub commits
- Custom domain: tstr.site

---

## Current Priorities (Q4 2025 - Q1 2026)

### P0 (Critical - Deploy Immediately)
- None currently

### P1 (High Priority - This Sprint)
- Hydrogen Infrastructure Testing category expansion
- Biotech/Pharma directory development
- Performance optimization and SEO improvements

### P2 (Medium Priority - Next Sprint)
- Additional industry categories
- Advanced filtering and search features
- Mobile responsiveness improvements

---

## Quick Reference

**Project Root**: `/media/al/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working`

**Frontend**: `web/tstr-frontend/` (Astro + React + Tailwind)
**Scrapers**: `web/tstr-automation/` (Python, OCI deployment)
**Database**: Supabase (https://haimjeaetrsaauitrhfy.supabase.co)

**Website**: http://tstr.site (LIVE - 163 listings as of 2025-11-17)

**Git Repo**: https://github.com/JAvZZe/tstr-site.git

**OCI Instance**: 84.8.139.90 (Oracle Linux 9, scrapers deployed)
- Access: SSH via key at `/media/al/1TB_AI_ARCH/AI_PROJECTS_ARCHIVE/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key`

---

## Development Workflow

### Code Changes
1. **Read PROJECT_STATUS.md** - Understand current state
2. **Make changes** - Frontend in `web/tstr-frontend/`, scrapers in `web/tstr-automation/`
3. **Test locally** - Use OpenHands' terminal access to run builds/tests
4. **Deploy** - Commit to GitHub triggers Cloudflare Pages deployment
5. **Verify** - Use OpenHands' web browsing to test live site
6. **Document** - Update PROJECT_STATUS.md with changes

### Database Changes
- Use Supabase dashboard for schema changes
- Update MCP configuration if API changes
- Test with Bruno collections before deploying

### Scraper Changes
- Deploy to OCI instance via SSH
- Update cron schedules if needed
- Monitor logs for data collection success

---

## Common Commands

### Frontend Development
```bash
cd web/tstr-frontend
npm install
npm run dev        # Local development
npm run build      # Production build
npm run preview    # Preview build
```

### Database Operations
```bash
# Via Bruno (recommended)
bru run bruno/supabase/health/ --env production
bru run bruno/supabase/listings/ --env production

# Direct Supabase CLI
supabase db reset  # Reset local database
supabase db push   # Push schema changes
```

### Deployment
```bash
git add .
git commit -m "description of changes"
git push origin main  # Triggers Cloudflare Pages deployment
```

---

## Testing Requirements

**MANDATORY**: Test before deploying

### Frontend Testing
- Build succeeds without errors
- All routes load correctly
- Category/region filtering works
- Mobile responsiveness verified

### Database Testing
- API endpoints return expected data
- RLS policies working correctly
- No breaking schema changes

### Integration Testing
- End-to-end workflow: scraper → database → frontend
- Live site verification after deployment

---

## Why This Matters

**Business Impact**: TSTR.site generates leads for testing laboratories. Downtime or bugs = lost revenue.

**Free Tier Constraints**: $1.04/month budget. Exceeding limits = project failure.

**User Experience**: Non-technical users expect reliable, fast directory service.

**Data Quality**: Inaccurate listings damage credibility and reduce conversions.

---

## Recent Implementation Notes (2025-11-22)

### Category/Region Dynamic Routes ✅ LIVE
**Routes created:**
- `/[category]` - Category overview showing all regions
- `/[category]/[region]` - Filtered listings by category + region

**Files:**
- `src/pages/[category]/index.astro` - Category overview page
- `src/pages/[category]/[region]/index.astro` - Category+region listings page
- Both use `export const prerender = true` for static generation

### Sitemap Optimization ✅ LIVE
**Change:** Sitemap filters out categories with 0 active listings

**Result:** Sitemap: 61 URLs (was 63)

### Supabase API Key Migration ✅ COMPLETE
**New format:** Publishable/secret keys (legacy JWT keys disabled 2025-10-17)

---

**Last Updated**: 2025-12-14
**System Version**: AI_PROJECTS_SPACE v2.0