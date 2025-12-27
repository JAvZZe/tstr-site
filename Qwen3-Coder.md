# Qwen3-Coder.md - TSTR.site Project

> **CRITICAL**: This project is part of the AI_PROJECTS_SPACE continuity system.
> **Global System**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/`
> **Project Context**: Read `TSTR.md` (this directory) for project-specific details.

---

## ⚠️ MANDATORY NOTE: Uncertainty and Certainty

AI agents should make it explicit when they do not know and are guessing. If they present a solution as fact, they should calculate an evidence-based level of certainty or probability that it is correct, and what other potential solutions there may be.

---

## 🚨 CRITICAL: Mandatory First Step

### ⚠️ ALWAYS BOOTSTRAP BEFORE STARTING WORK

**Before using Qwen3-Coder for any task, you MUST run:**

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh
```

**What this provides:**
- **Project-specific learnings** and context from the continuity system
- **Pending tasks** filtered to relevant projects
- **Session history** and handoff information from other agents
- **Learning system access** that may affect model selection and task routing decisions

**Why mandatory:**
- Qwen3-Coder is integrated with the multi-agent continuity system
- Bootstrap ensures you have full context and don't duplicate work
- Provides access to accumulated knowledge and task state
- Required for all agents (Claude, Gemini, OpenHands, OpenCode, etc.)

**Failure to bootstrap may result in:**
- Missing important context and learnings
- Duplicating work already done by other agents
- Inefficient task routing and model selection
- Breaking continuity across the multi-agent system

---

## Mandatory Protocol for ALL Agents

### 1. Global Bootstrap (MANDATORY - See Above)

### 2. Project Session Start (RECOMMENDED)

**After global bootstrap, run project-specific bootstrap:**

```bash
./bootstrap.sh TSTR.site
```

**Note**: The bootstrap script file is `Link_to_bootstrap_agent.sh` in the project root. Always run project bootstrap after global bootstrap.

This loads:
- **Project-specific learnings** (15 relevant from 90 total)
- **Pending tasks** (filtered to TSTR.site only)
- **Recent session context** (what was last done)
- **Handoff context** from previous agents
- **Protocol reminders** with absolute paths

**Why bootstrap > resume**:
- resume.sh: Shows ALL learnings (overwhelming)
- bootstrap.sh: Shows TSTR.site learnings only (manageable)
- Filters by project name in tags AND content
- High confidence only (≥4)

**Symlinks available**: In this folder, just run `./bootstrap.sh TSTR.site`

### 2. Project Status Protocol (MANDATORY)

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
   - Any successful change affecting tstr.site

#### **Protocol Requirements**:
- ✅ **ALWAYS** update PROJECT_STATUS.md after successful changes
- ✅ **NEVER** deploy changes without documenting them
- ✅ **READ FIRST** - Check current state before making changes
- ✅ **VERSION BUMP** - Increment version number for each update
- ✅ **TIMESTAMP** - Include date/time and agent attribution

**This is the SINGLE SOURCE OF TRUTH for tstr.site's current state, structure, and change history.**

### 3. During Work

**Checkpoint frequently**:
```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./checkpoint.sh "description of work completed"
```

**Extract learnings** after errors/discoveries:
```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
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
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_task, update_task
task_id = add_task("TSTR.site", "Task description", assigned_to="qwen3-coder")
# ... do work ...
update_task(task_id, "completed", result="Result summary")
PYEOF
```

### 3. Session End or Handoff

```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./handoff.sh <agent> <reason>
```

---

## Qwen3-Coder / Cost-Effective Development Specifics

### Strengths & Capabilities
- **Bulk Code Generation**: Efficiently create multiple similar components, pages, or API endpoints
- **Repetitive Tasks**: Apply consistent patterns across multiple files with cost-effective processing
- **Pattern Implementation**: Apply standard patterns and best practices across the codebase
- **Cost Optimization**: $0.45/1M input, $1.50/1M output - ideal for large-scale development tasks
- **Multi-file Operations**: Process multiple files simultaneously with consistent transformations

### Best Use Cases for TSTR.site
1. **Component Generation**: Create multiple similar listing components, category pages, or UI elements
2. **API Endpoint Creation**: Generate standardized API endpoints for new features
3. **Documentation**: Create consistent documentation across multiple files or components
4. **Refactoring**: Apply consistent code improvements across multiple files
5. **Testing**: Generate multiple similar test cases or test files
6. **SEO Implementation**: Apply SEO patterns across multiple pages consistently

### Workflow Preferences
1. **Bulk Operations**: Group similar tasks together for cost efficiency
2. **Pattern Application**: Identify and apply consistent patterns across the codebase
3. **Iterative Development**: Generate, test, refine patterns for optimal results

---

## Project-Specific Instructions

**Read these files IN ORDER**:

1. **START_HERE.md** - Quick orientation checklist
2. **TSTR.md** - PRIMARY agent instructions (architecture, commands, priorities)
3. **.ai-session.md** - Latest session context and active tasks
4. **PROJECT_STATUS.md** - Deployment status and infrastructure details
5. **HANDOFF_TO_CLAUDE.md** - Current handoff (if exists)

---

## Quick Reference

**Project Root**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working`

**Frontend**: `web/tstr-frontend/` (Astro + React + Tailwind)
**Scrapers**: `web/tstr-automation/` (Python, deployed on OCI)
**Database**: Supabase (https://haimjeaetrsaauitrhfy.supabase.co)
**API Keys**:
- Publishable: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO
- Service Role: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDQzNjU4NSwiZXhwIjoyMDc2MDEyNTg1fQ.zd47WtS1G1XzjP1obmr_lxHU_xJWtlhhu4ktm9xC5hA

**MCP Server**: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`
- Server: @supabase/mcp-server-supabase@latest
- Project Ref: haimjeaetrsaauitrhfy
- Access Token: sbp_e290bc7ea1ba64ae4b0be38134b7b4a67ca24e04
- Mode: Read-only

**Website**: http://tstr.site (LIVE - 163 listings as of 2025-11-17)

**Git Repo**: https://github.com/JAvZZe/tstr-site.git

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

**Cost Optimization**: Qwen3-Coder offers 85% cost savings vs Claude for bulk operations while maintaining quality:
- Claude Sonnet 4.5: $3/1M input, $15/1M output
- Qwen3-Coder: $0.45/1M input, $1.50/1M output

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

## Recent Implementation Notes (2025-12-25)

### Category/Region Dynamic Routes ✅ LIVE
**Routes created:**
- `/[category]` - Category overview showing all regions (e.g., `/hydrogen-infrastructure-testing`)
- `/[category]/[region]` - Filtered listings by category + region (e.g., `/hydrogen-infrastructure-testing/global`)

**Files:**
- `src/pages/[category]/index.astro` - Category overview page
- `src/pages/[category]/[region]/index.astro` - Category+region listings page
- Both use `export const prerender = true` for static generation

**Deployment:** Live on https://tstr.site with Cloudflare Pages edge caching

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

### SEO Hybrid Hook Strategy ✅ LIVE (2025-11-23)

**CRITICAL MARKETING PRINCIPLE - READ BEFORE ANY LANDING PAGE WORK**

See `MARKETING_STRATEGY.md` for full documentation.

**Core Concept:**
- H1 = Brand Identity ("[Category] Testers")
- H2 = SEO Traffic ("[Category] Testing Services")
- Title/Meta = Both keywords combined

**Why:**
- "Testers" only = 20% of search traffic
- "Testing Services" only = 80% of search traffic
- Hybrid Hook = 100% coverage (+300-400% traffic increase)

**Implementation:**
```typescript
// Helper function in templates
const getTestingServiceName = (categoryName: string) => {
  return categoryName.replace('Testers', 'Testing');
};
```

**Applied to:**
- `/src/pages/[category]/index.astro` - All category pages
- `/src/pages/[category]/[region]/index.astro` - All region pages
- Works automatically for all 6 categories

**ENFORCEMENT:**
- ⚠️ DO NOT remove H2 elements from landing pages
- ⚠️ DO NOT modify title tag structure
- ⚠️ DO NOT remove "Testing" keywords
- ✅ Preserve dual-targeting strategy in all new pages

**Verification:**
```bash
# Check both keywords present
grep -o 'Testers.*Testing' dist/[category]/index.html
```

**Traffic Impact:** Deployed 2025-11-23, monitor Search Console for keyword performance.

---

## Qwen3-Coder Specific Tasks for TSTR.site

### Recommended Bulk Operations
1. **Generate multiple category pages** for new testing sectors
2. **Create standardized listing components** with consistent UI/UX
3. **Apply SEO patterns** across multiple pages efficiently
4. **Implement consistent styling** across components
5. **Generate API endpoints** for new features
6. **Create test files** for multiple components simultaneously

### Cost-Effective Development Strategy
- **Batch similar tasks** to maximize efficiency
- **Generate multiple components** in single sessions
- **Apply consistent patterns** across the codebase
- **Create reusable templates** for future development

---

**Last Updated**: 2025-12-25
**System Version**: AI_PROJECTS_SPACE v2.0