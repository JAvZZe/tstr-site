# AGENTS.md - Development Guidelines for TSTR.directory

## 🚨 CRITICAL: MANDATORY FIRST STEP FOR ALL AGENTS

**1. ALWAYS RUN GLOBAL BOOTSTRAP BEFORE ANY PROJECT WORK:**

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh
```

**2. MANDATORY GIT & DATA AUDIT:**
Before starting architectural or code work, ALWAYS perform a Git audit to identify stale branches or pending data migrations:
```bash
git branch -a --sort=-authordate
```
Check `PROJECT_STATUS.md` for "Data Debt" entries and ensure critical data in stale branches isn't orphaned.

**This provides:**
- Global system context and learnings
- Cross-project task coordination
- Agent handoff information
- Learning system access for optimal decision making
- **Visibility into orphaned feature branches and pending data enrichments**

**Failure to bootstrap may result in:**
- Missing critical context
- Duplicating work already done
- Breaking continuity across agents

---

## 🛑 AUTO-EXECUTION POLICY (MANDATORY)

**CRITICAL: DO NOT AUTOMATICALLY TAKE FURTHER ACTIONS WITHOUT REPORTING FIRST.**
- After completing a specific requested task, **STOP** and report your findings or completion status to the user.
- **NEVER** autonomously decide to start the next task, refactor code, or run further scripts without explicit user approval.
- Present your findings, propose the next steps, and **WAIT** for the user to say "proceed" or give new instructions.

---

## 🚀 PROJECT INITIALIZATION (After Global Bootstrap)

**When starting work in this project:**
```bash
./start-agent.sh    # Recommended: Complete project initialization with status
# OR
muninn-cli bootstrap TSTR   # Load project memories (PRIMARY)
./bootstrap.sh TSTR-site    # Legacy SQLite context (fallback)
```

**Quick Start Commands:**
```bash
tstr-agent          # Alias for ./start-agent.sh (after ~/.bashrc reload)
./start-agent.sh    # Full project agent initialization
./monitoring/daily_check.sh  # System health check
```

**Note**: The bootstrap script file is `Link_to_bootstrap_agent.sh` in the project root. Always run project initialization after global bootstrap.

This loads:
- Project-specific learnings from database
- Pending tasks for TSTR-site
- Recent session context
- Pending handoffs
- Recent checkpoints

## 🔑 SUPABASE CONFIGURATION

**URL**: https://haimjeaetrsaauitrhfy.supabase.co
**Anon Key**: [REDACTED - See TSTR_hub_Supabase_Keys.md]
**Service Role Key**: [stored in .env and Cloudflare dashboard]

**MCP Server**: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`
- Server: @supabase/mcp-server-supabase@latest
- Project Ref: haimjeaetrsaauitrhfy
- Access Token: [REDACTED_PAT]
- Mode: Read-only

## 🔄 DEPLOYMENT NOTES

**Cloudflare Pages Deployment Issues:**
- CSS changes may take 1-2 hours to propagate globally
- Subscription page deployed successfully, account page CSS pending
- Check `ACCOUNT_BUTTON_IMPROVEMENTS_HANDOFF.md` for current status
- Monitor: https://dash.cloudflare.com/pages → tstr-site → Deployments

## 📊 DATA DEBT & STALE BRANCHES

| Branch | Stale Since | Data/Purpose | Conflict Status |
|--------|-------------|--------------|-----------------|
| `hydrogen-standards` | 2026-03-19 | 15 Hydrogen Standards (ASTM G142) | ⚠️ HIGH - Do not merge. Manual extraction required. |
| `feat/astro-6-migration` | 2026-03-24 | Platform Upgrade (Stats Fixes) | ℹ️ LOW - Staged for later phase. |

---

## 📝 PENDING TASKS

## 🧠 SYSTEMS THINKING PROTOCOL (MANDATORY)

**CRITICAL: Infrastructure changes often exceed the boundaries of the Git repository.**

### Why we failed the Supabase-Cloudflare Sync:
During the Supabase credential rotation, agents successfully updated the code and local `.env` files but failed to rotate the keys in the **Cloudflare Pages/Workers Dashboard**. This happened because the agents operated within a "Repository Silo," forgetting that production environment variables are stored on the Edge, not just in the codebase.

### The Protocol:
Before confirming any infrastructure-related task (Keys, URLs, Auth, Database), you MUST perform a **Systemic Audit**:

1.  **Map the Connective Tissue**:
    - **Data**: Supabase (Database, Auth, Storage)
    - **Logic**: OCI (Scrapers, Management Scripts)
    - **Delivery**: Cloudflare (Pages, Workers, KV, DNS)
    - **Bridge**: GitHub (Actions, Secrets)

2.  **Verify Non-Git State**:
    - If you change a secret, check if it's mirrored in **Cloudflare Environment Variables**.
    - If you change a database schema, check if **RLS Policies** or **Views** need updating.
    - If you change a script path, check **systemd timers** or **crontabs** on OCI.

3.  **The "If This, Then That" (ITTT) Analysis**:
    - "If I rotate Supabase keys, I MUST update: Local .env, OCI .env, Cloudflare Dashboard, and GitHub Secrets."

## 📊 PROJECT STATUS PROTOCOL (MANDATORY)

**CRITICAL**: All agents MUST read and update `PROJECT_STATUS.md` before & after any work:

### **After Completing Changes**:
1. **Update PROJECT_STATUS.md** with version increment and change details
2. **Commit and push** the updated status document
3. **Document ALL changes** that affect the live website:
   - Code deployments
   - UI/branding changes
   - Infrastructure modifications
   - Content updates
   - Link changes
   - Any successful change affecting tstr.directory

### **Cleanup & Archiving Protocol (MANDATORY)**

To maintain a clean environment and reduce token clutter:
1. **Delete Interim Files**: Once work is merged/completed, delete redundant files like `HANDOFF_*.md`, `implementation_plan.md`, or temporary reports.
2. **Archive Historical Context**: If a document (e.g., an old project plan or complex analysis) has historical value but is no longer "active," move it to the `_ARCHIVE/` directory instead of leaving it in the root.
3. **Reference Archives**: Before starting a task that feels like a "retry" or "resumption," proactively search the `_ARCHIVE/` folder for previous context or "forgotten" history.

---

### **Protocol Requirements**:
- ✅ **ALWAYS** update PROJECT_STATUS.md after successful changes
- ✅ **NEVER** deploy changes without documenting them
- ✅ **READ FIRST** - Check current state before making changes
- ✅ **VERSION BUMP** - Increment version number for each update
- ✅ **TIMESTAMP** - Include date/time and agent attribution

**This is the SINGLE SOURCE OF TRUTH for tstr.directory's current state, structure, and change history.**

**Failure to perform this audit is a breach of the Systems Thinking Protocol.**

## AI Agent CLI Functions (v2.0 Integration)

**Available in all bash sessions** (added to ~/.bashrc):

```bash
# Complex reasoning, architecture, review, decisions
ask-arch "your complex query here"

# Continuation when Claude expensive, medium complexity
ask-gemini "continue this task"

# Code generation, batch processing, simple tasks
ask-code "write a Python function for..."

# Cost-effective bulk processing and repetitive tasks
qwen "generate multiple components for all categories"
```

**Context Dumping for Agent Handoffs:**
```bash
# Dump current system state to markdown (for external agents)
python3 ../../../SYSTEM/state/db_utils.py --dump > .context_dump/current_state.md

# Add new learnings to the system
python3 ../../../SYSTEM/state/db_utils.py --learn "your learning here"
```

## Commands

### Frontend (Astro + React)
```bash
cd web/tstr-frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Testing
```bash
npm run test          # Run all Playwright tests
npx playwright test tests/example.spec.ts    # Run single test
npx playwright test --grep "test name"      # Run tests by name
```

### Python Scrapers
```bash
cd web/tstr-automation
pip install -r requirements.txt
python scrapers/a2la_materials.py    # Run specific scraper
```

**Scraper Deployment Strategy:**
- **Heavy-duty scrapers** (requiring browser automation like Playwright/Selenium): Run locally due to OCI RAM limitations
- **Lightweight scrapers** (simple HTTP/HTML parsing): Deploy to OCI when resources allow
- **Local Automation**: Available with 40GB PC RAM - can run automated local scrapers
- **Current OCI instance**: 84.8.139.90 (Oracle Linux 9) - active for lightweight operations
- **Resource decision**: Local execution for any scraper needing >1GB RAM or JavaScript rendering

### Environment Files (.env)
**IMPORTANT**: .env files contain sensitive secrets and are blocked from read/edit tools. Use bash commands instead:
```bash
# Create .env from example
cp web/tstr-frontend/.env.example web/tstr-frontend/.env
cp web/tstr-automation/.env.example web/tstr-automation/.env

# Read .env file
cat web/tstr-frontend/.env

# Edit .env file
nano web/tstr-frontend/.env  # or vim, code, etc.
```

## Code Style

### TypeScript/JavaScript
- Use strict TypeScript config (`extends: "astro/tsconfigs/strict"`)
- Import order: 1) External libs, 2) Internal components, 3) Relative imports
- Use React functional components with hooks
- Error handling with try/catch and proper logging

### Python
- Use type hints (`from typing import Dict, List, Optional`)
- Import order: 1) stdlib, 2) third-party, 3) local imports
- Inherit from `BaseNicheScraper` for all scrapers
- Use logging, not print statements

### Astro
- Use `export const prerender = true` for static pages
- Fetch data in frontmatter with Supabase client
- Use Tailwind CSS classes, avoid inline styles

### Naming
- Files: kebab-case (`my-component.astro`, `scraper_name.py`)
- Components: PascalCase (`MyComponent`)
- Variables/functions: camelCase (JS) or snake_case (Python)
- Constants: UPPER_SNAKE_CASE

### Git Commits
- Format: `[AGENTNAME] Brief description`
- Include context in body for complex changes

---

## 🔍 Code Review Protocol (Mandatory)

**ALL code changes MUST be reviewed before merge/completion.**

### For Every Agent (Automatic & Proactive)

1. **After writing code**: Proactively offer/use code review
2. **After task completion**: Use `requesting-code-review` skill
3. **Before handoff**: Ensure code reviewed or noted issues documented

### Review Process

```bash
# Get SHAs for review
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)

# Use requesting-code-review skill from Superpowers
```

### Issue Handling

| Severity | Action |
|----------|--------|
| **Critical** | Fix immediately, do not proceed |
| **Important** | Fix before next task |
| **Minor** | Document, fix later |

### Proactive Review Policy

**I will automatically:**
- Offer code review after writing code
- Flag potential issues when I see them
- Suggest improvements proactively
- Not wait to be asked
