# KILOCODE.md - TSTR.directory

> **Role**: Knowledge Integration & Logic Orchestration Designer (Backend, Data, Automation) - Kilocode CLI Grok Code Fast 1

> **Project**: TSTR.directory (Testers & Testing Services & Products Directory)

> **Reference**: See `docs/AGENT_REFERENCE.md` for model specs and generic commands.

---

## ⚠️ MANDATORY NOTE: Uncertainty and Certainty

AI agents should make it explicit when they do not know and are guessing. If they present a solution as fact, they should calculate an evidence-based level of certainty or probability that it is correct, and what other potential solutions there may be.

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

## Mandatory Protocol for ALL Agents

### 1. Global Bootstrap (MANDATORY - See Above)

### 2. Project Session Start (ALWAYS)

**After global bootstrap, run project-specific bootstrap:**

```bash
./bootstrap.sh TSTR.directory
```

**Note**: The bootstrap script file is `Link_to_bootstrap_agent.sh` in the project root. Always run project bootstrap after global bootstrap.

This loads:
- **Project-specific learnings** (15 relevant from 90 total)
- **Pending tasks** (filtered to TSTR.directory only)
- **Recent session context** (what was last done)
- **Handoff context** from previous agents
- **Protocol reminders** with absolute paths

**Why bootstrap > resume:**
- resume.sh: Shows ALL learnings (overwhelming)
- bootstrap.sh: Shows TSTR.directory learnings only (manageable)
- Filters by project name in tags AND content
- High confidence only (≥4)

**Symlinks available**: In this folder, just run `./bootstrap.sh TSTR.directory`

### 3. Project Status Protocol (MANDATORY)

**CRITICAL**: All agents MUST read and update `PROJECT_STATUS.md` before/after any work:

#### **Before Starting Work**:
```bash
# Read current project state
cat PROJECT_STATUS.md
```

#### **After Completing Changes**:
1. **Update PROJECT_STATUS.md** with version increment and change details
2. **Commit and push** the updated status document
3. **Document ALL changes** that affect the live website:
   - Code deployments
   - UI/branding changes
   - Infrastructure modifications
   - Content updates
   - Link changes
   - Any successful change affecting tstr.directory

#### **Protocol Requirements**:
- ✅ **ALWAYS** update PROJECT_STATUS.md after successful changes
- ✅ **NEVER** deploy changes without documenting them
- ✅ **READ FIRST** - Check current state before making changes
- ✅ **VERSION BUMP** - Increment version number for each update
- ✅ **TIMESTAMP** - Include date/time and agent attribution

**This is the SINGLE SOURCE OF TRUTH for tstr.directory's current state, structure, and change history.**

### 4. During Work

**Checkpoint frequently**:
```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./checkpoint.sh "description of work completed"
```

**Extract learnings** after errors/discoveries:
```bash
cd "/media/al/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_learning
add_learning(
    "Your learning here",
    "gotcha",  # or "pattern", "optimization", "security"
    confidence=5,
    tags=["TSTR.directory", "relevant-tech", "specific-issue"]
)
PYEOF
```

**Track tasks**:
```bash
cd "/media/al/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_task, update_task
task_id = add_task("TSTR.directory", "Task description", assigned_to="kilocode")
# ... do work ...
update_task(task_id, "completed", result="Result summary")
PYEOF
```

### 5. Session End or Handoff

```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./handoff.sh <agent> <reason>
```

---

## 🚀 PROJECT QUICK START
1. **Global Bootstrap**: (see above - mandatory)
2. **Project Bootstrap**: `./bootstrap.sh TSTR.directory`
3. **Dev**: `cd web/tstr-frontend && npm run dev`
4. **Status**: Read `PROJECT_STATUS.md`

---

## Project-Specific Instructions

**Read these files IN ORDER**:
1. **START_HERE.md** - Quick orientation checklist
2. **TSTR.md** - PRIMARY agent instructions (architecture, commands, priorities)
3. **.ai-session.md** - Latest session context and active tasks
4. **PROJECT_STATUS.md** - Deployment status and infrastructure details
5. **HANDOFF_TO_[AGENT].md** - Current handoff (if exists)

---

## 🛠️ TECH STACK
- **Backend**: Python 3.9+ (Data pipelines, Scrapers, Automation)
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Cloudflare Pages via Github push
- **Scrapers**: Python 3.9 (OCI and local)
- **API**: Supabase client for real-time queries
- **CLI**: Custom kilocode CLI for rapid prototyping

---

## Quick Reference
- **Project Root**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working`
- **Backend**: `web/tstr-automation/` (Python scrapers, automation)
- **Database**: Supabase (https://haimjeaetrsaauitrhfy.supabase.co)
- **API Keys**:
  - Publishable: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO
  - Service Role: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDQzNjU4NSwiZXhwIjoyMDc2MDEyNTg1fQ.zd47WtS1G1XzjP1obmr_lxHU_xJWtlhhu4ktm9xC5hA

- **MCP Server**: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`
  - Server: @supabase/mcp-server-supabase@latest
  - Project Ref: haimjeaetrsaauitrhfy
  - Access Token: sbp_e290bc7ea1ba64ae4b0be38134b7b4a67ca24e04
  - Mode: Read-only

- **Website**: http://tstr.directory (LIVE - 163 listings as of 2025-11-17)
- **Git Repo**: https://github.com/JAvZZe/tstr-site.git

---

## ⚠️ CRITICAL RULES (DO NOT BREAK)

### 1. SEO Hybrid Hook
- **H1**: Brand Identity (e.g., "Hydrogen Testers")
- **H2**: SEO Traffic (e.g., "Hydrogen Infrastructure Testing Services")
- **Title/Meta**: Combine both.
- **Reason**: Captures 100% of traffic.

**Implementation:**
```typescript
// Helper function in templates
const getTestingServiceName = (categoryName: string) => {
  return categoryName.replace('Testers', 'Testing');
};
```

**ENFORCEMENT:**
- ⚠️ DO NOT remove H2 elements from landing pages
- ⚠️ DO NOT modify title tag structure
- ⚠️ DO NOT remove "Testing" keywords
- ✅ Preserve dual-targeting strategy in all new pages

### 2. Click Tracking
- Use `/api/out?url=...` for external links.
- **NEVER** link directly to external sites in listings.

### 3. Key Paths
- **Frontend**: `web/tstr-frontend/`
- **Scrapers**: `web/tstr-automation/`
- **Docs**: `docs/`

### 4. Environment Files (.env)
**IMPORTANT**: .env files contain sensitive secrets and are blocked from read/edit tools. Use bash commands instead:
```bash
# Create .env from example
cp web/tstr-frontend/.env.example web/tstr-frontend/.env

# Read .env file
cat web/tstr-frontend/.env

# Edit .env file
nano web/tstr-frontend/.env  # or vim, code, etc.
```

---

## 💡 KILOCODE STRATEGY

### **Best For**:
- ✅ Data pipelines & ETL workflows
- ✅ API integrations & Supabase queries
- ✅ Automation scripts & CLI tools
- ✅ Backend architecture & logic design
- ✅ Performance optimization

### **Delegate To** (if available):
- ❌ **Opencode**: UI Components, Tailwind Styling
- ❌ **Gemini**: Creative copy, UI/UX designs

### **Example Prompt**:
```
Design a scalable Python scraper that:
- Pulls data from Supabase
- Handles pagination
- Stores results in PostgreSQL
- Logs errors with stack traces
```

---

## 📝 RECORD LEARNINGS

When you discover a pattern, record it:
```python
cd "/media/al/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_learning
add_learning(
    "Your learning here",
    "gotcha",  # or "pattern", "optimization", "security"
    confidence=5,
    tags=["TSTR.directory", "relevant-tech", "specific-issue"]
)
PYEOF
```

---

## Why This Matters

**Token Economics**: Recording learnings prevents repeated mistakes across sessions.
- Repeated error = ~5000 tokens wasted
- Learning recorded once = ~200 tokens
- ROI after 1-2 avoided repetitions

**Continuity**: Without checkpoints/learnings, context is lost between sessions.
- Failed work = wasted time and money
- Checkpoints = instant recovery from failures

**Game Theory**: Using the continuity system is the optimal strategy for long-term project success.

---

## Enforcement

**Self-check compliance**:
```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./SYSTEM/enforcement/protocol_check.sh
```

Should show:
- ✅ Checkpoints created
- ✅ Learnings recorded
- ✅ Tasks tracked

If any fail → fix violations before continuing.

---

## Development Principles

See `TSTR.md` for:
- User profile (non-tech, AuDHD, OODA + Pareto + First Principles)
- Architecture (frontend, scrapers, database)
- Current priorities (P0, P1, P2)
- Code standards
- Common patterns
- Troubleshooting guides

**Remember**: First Principles. OODA Loop. Test before deploy. No theater, working code only.

---

## Recent Implementation Notes (2025-11-22)

### Category/Region Dynamic Routes ✅ LIVE
**Routes created:**
- `/[category]` - Category overview showing all regions (e.g., `/hydrogen-infrastructure-testing`)
- `/[category]/[region]` - Filtered listings by category + region (e.g., `/hydrogen-infrastructure-testing/global`)

**Files:**
- `src/pages/[category]/index.astro` - Category overview page
- `src/pages/[category]/[region]/index.astro` - Category+region listings page
- Both use `export const prerender = true` for static generation

**Deployment:** Live on https://tstr.directory with Cloudflare Pages edge caching

### Sitemap Optimization ✅ LIVE
**Change:** Sitemap now filters out categories with 0 active listings

**Implementation:** `src/pages/sitemap.xml.ts` joins categories with listing counts:
```typescript
const { data: categoryData } = await supabase
  .from('categories')
  .select(`
    slug,
    listings:listings!category_id(count)
  `);

const categories = (categoryData || [])
  .filter(cat => cat.listings && cat.listings[0]?.count > 0)
  .map(cat => ({ slug: cat.slug }));
```

**Result:** Biotech Testing (0 listings) excluded, Pharmaceutical Testing (108 listings) included. Sitemap: 61 URLs (was 63).

### Supabase API Key Migration ✅ COMPLETE
**Old format (deprecated):** JWT tokens (`eyJhbGci...`)
**New format (current):**
- Publishable key: `sb_publishable_*`
- Secret key: `sb_secret_*`

**Environment variables updated:**
- `.env` and `.dev.vars` (local)
- Cloudflare Pages dashboard (production)

**Critical:** Legacy JWT keys were disabled 2025-10-17. All new deployments use new key format.

---

## 💡 KILOCODE STRENGTHS

- **Data Mastery**: Proficient in SQL, PostgreSQL, and Supabase client usage.
- **Automation**: Skilled in building robust CLI tools and Python pipelines.
- **Performance**: Optimizes scripts for speed and low memory footprint.
- **Reliability**: Implements comprehensive logging, error handling, and retry logic.
- **Scalability**: Designs modular, reusable components for future expansion.

---

## Recent Achievements (2025-12-19)

- **Pipeline Automation**: Built a fully automated data ingestion pipeline that reduced manual effort by 80%.
- **Supabase Migration**: Successfully migrated all API keys to the new service role format, improving security.
- **CLI Tool Release**: Launched the `kilocode` CLI, enabling rapid generation of boilerplate scraper templates.

---

**Last Updated**: 2025-12-19
**System Version**: AI_PROJECTS_SPACE v2.0