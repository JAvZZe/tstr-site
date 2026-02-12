# 🧹 TSTR.directory — Folder & File Cleanup Plan

> **Created**: 2026-02-11 by Gemini (Antigravity)
> **Purpose**: Clean up misplaced files across AI_PROJECTS_SPACE and the TSTR project
> **Executor**: Any agent (designed for Gemini Flash / lesser agents)
> **Approach**: Mechanical, step-by-step. No judgment calls required.

---

## ⚠️ CRITICAL RULES FOR THE EXECUTING AGENT

1. **Execute ONE phase at a time.** Do not skip phases.
2. **Checkpoint after each phase** using: `cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./checkpoint.sh "Cleanup Phase X complete"`
3. **Verify after each phase** using the verification command provided.
4. **If any command fails**, STOP and report the error. Do not continue.
5. **Do NOT modify file contents** — this plan only MOVES files.
6. **Do NOT touch**: `.git/`, `node_modules/`, `.venv/`, `web/tstr-frontend/`, `web/tstr-automation/`, `web/backend/`, `supabase/`
7. **Git commit after each phase** from the appropriate repo root.

---

## Pre-Flight Checklist

Before starting, run these checks:

```bash
# 1. Confirm you're on the right machine
hostname
# Expected: al's Linux machine

# 2. Confirm paths exist
ls -d /media/al/AI_DATA/AI_PROJECTS_SPACE/
ls -d /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/

# 3. Check git status in both repos (should be clean)
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && git status
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working && git status

# 4. Bootstrap
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./bootstrap_global.sh
```

If git status shows uncommitted changes, commit or stash them first before proceeding.

---

## PHASE 1: Delete Empty/Stale Directories in ACTIVE_PROJECTS

**Risk**: LOW (these directories contain no meaningful code)
**Location**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/`

### Step 1.1 — Verify they're empty/stale

```bash
# Confirm TSTR.site only has a near-empty bruno folder
find /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR.site/ -type f
# Expected: only bruno.json (126 bytes)

# Confirm TSTR_site only has a context dump
find /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR_site/ -type f
# Expected: possibly empty or just a context dump markdown
```

### Step 1.2 — Remove them

```bash
rm -rf /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR.site/
rm -rf /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR_site/
```

### Step 1.3 — Verify

```bash
ls /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/
# Expected: only TSTR-site/ (and possibly .claude/, .vscode/)
```

### Step 1.4 — Checkpoint

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && git add -A && git commit -m "Cleanup Phase 1: Remove stale TSTR.site and TSTR_site dirs from ACTIVE_PROJECTS"
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./checkpoint.sh "Cleanup Phase 1 complete - removed stale ACTIVE_PROJECTS dirs"
```

---

## PHASE 2: Organize AI_PROJECTS_SPACE Root — Move Docs to ARCHIVE

**Risk**: LOW (moving documentation files only)
**Location**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/`

### Step 2.1 — Create archive subdirectory for this cleanup

```bash
mkdir -p /media/al/AI_DATA/AI_PROJECTS_SPACE/ARCHIVE/2026-02-11_root_cleanup/
```

### Step 2.2 — Move old reports and summaries

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE

mv AGENT_EXECUTION_PLAN.md           ARCHIVE/2026-02-11_root_cleanup/
mv AI_Instruction_Start_In_all_interactions_commit.txt  ARCHIVE/2026-02-11_root_cleanup/
mv BRUNO_INTEGRATION_SUMMARY.md      ARCHIVE/2026-02-11_root_cleanup/
mv CHANGELOG_2025-11-20.md           ARCHIVE/2026-02-11_root_cleanup/
mv CODEBASE_ANALYSIS.md              ARCHIVE/2026-02-11_root_cleanup/
mv DETAILED_FILE_INVENTORY.md        ARCHIVE/2026-02-11_root_cleanup/
mv DROID_VS_CLAUDE_CLI_COMPARISON.md ARCHIVE/2026-02-11_root_cleanup/
mv EXECUTION_SUMMARY.md              ARCHIVE/2026-02-11_root_cleanup/
mv FINAL_SESSION_SUMMARY.md          ARCHIVE/2026-02-11_root_cleanup/
mv FOLDER_OPTIMIZATION_PLAN.md       ARCHIVE/2026-02-11_root_cleanup/
mv Factory_AI_Droid_Code.txt         ARCHIVE/2026-02-11_root_cleanup/
mv GEMINI_HANDOFF_INSTRUCTIONS.md    ARCHIVE/2026-02-11_root_cleanup/
mv MCP_ECOSYSTEM_ANALYSIS.md         ARCHIVE/2026-02-11_root_cleanup/
```

### Step 2.3 — Move system docs to SYSTEM/docs (create if needed)

```bash
mkdir -p /media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/docs/

cd /media/al/AI_DATA/AI_PROJECTS_SPACE

mv AI_AGENT_STANDARDS_PROTOCOL.md  SYSTEM/docs/
mv CLI_TOOLS_ORGANIZATION.md       SYSTEM/docs/
mv LIBPOSTAL_SETUP_GUIDE.md        SYSTEM/docs/
mv PLATFORM_SPECIFIC_CONFIGS.md    SYSTEM/docs/
mv SYSTEM_OVERVIEW.md              SYSTEM/docs/
mv SYSTEM_TOOLS_REFERENCE.md       SYSTEM/docs/
```

### Step 2.4 — Move utility scripts to SYSTEM subdirectories

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE

# State/DB utilities → SYSTEM/state/
mv get_learnings.py    SYSTEM/state/
mv update_tasks.py     SYSTEM/state/
mv checkpoint_log.txt  SYSTEM/state/

# Agent launchers → SYSTEM/agents/
mv ollama_deepseek.sh       SYSTEM/agents/
mv openhands-launcher.sh    SYSTEM/agents/
mv run_system_with_claude.sh SYSTEM/agents/
mv start-ai-stack.sh        SYSTEM/agents/

# Setup/install scripts → SYSTEM/setup/
mv get-docker.sh        SYSTEM/setup/
mv install_libpostal.sh SYSTEM/setup/
```

### Step 2.5 — Handle the API key file (SECURITY)

```bash
# Move the plain-text API key file into the config directory (not git-tracked)
mv /media/al/AI_DATA/AI_PROJECTS_SPACE/Openrouter_API_Key_Claude.txt /media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/config/

# Verify it's in .gitignore (SYSTEM/config/ should be ignored)
grep -r "config" /media/al/AI_DATA/AI_PROJECTS_SPACE/.gitignore
# If not ignored, add it:
# echo "SYSTEM/config/*.txt" >> /media/al/AI_DATA/AI_PROJECTS_SPACE/.gitignore
```

### Step 2.6 — Verify root is cleaner

```bash
ls /media/al/AI_DATA/AI_PROJECTS_SPACE/*.md
# Expected remaining .md files at root:
#   CLAUDE.md, GEMINI.md, DEEPAGENT.md, DROID.md, KIMI.md,
#   OPENCODE.md, OPENHANDS.md, Qwen3-Coder.md,
#   ARCHITECTURE.md, QUICKSTART.md, README.md, LICENSE

ls /media/al/AI_DATA/AI_PROJECTS_SPACE/*.sh
# Expected remaining .sh files at root:
#   bootstrap_global.sh, checkpoint.sh, handoff.sh, resume.sh

ls /media/al/AI_DATA/AI_PROJECTS_SPACE/*.py /media/al/AI_DATA/AI_PROJECTS_SPACE/*.txt 2>/dev/null
# Expected: NONE (all moved)
```

### Step 2.7 — Commit and checkpoint

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && git add -A && git commit -m "Cleanup Phase 2: Organize root - move docs to ARCHIVE, scripts to SYSTEM"
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./checkpoint.sh "Cleanup Phase 2 complete - root organized"
```

---

## PHASE 3: Clean Up Project Root (tstr-site-working) — Move Handoff Docs

**Risk**: LOW (moving historical markdown files)
**Location**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/`

### Step 3.1 — Create archive subdirectory

```bash
mkdir -p /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/_ARCHIVE/handoffs/
mkdir -p /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/_ARCHIVE/old_guides/
mkdir -p /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/_ARCHIVE/old_plans/
```

### Step 3.2 — Move historical handoff documents

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working

mv HANDOFF_TO_NEXT_AGENT_2025-12-21.md  _ARCHIVE/handoffs/
mv HANDOFF_TO_NEXT_AGENT_2025-12-22.md  _ARCHIVE/handoffs/
mv HANDOFF_TO_NEXT_AGENT_2026-01-03.md  _ARCHIVE/handoffs/
mv HANDOFF_TO_NEXT_AGENT_2026-01-22.md  _ARCHIVE/handoffs/
mv HANDOFF_MIGRATION_RESOLUTION.md      _ARCHIVE/handoffs/
mv HANDOFF_PICKUP.md                    _ARCHIVE/handoffs/
mv HANDOFF_PROJECT_CLEANUP_COMPLETE.md  _ARCHIVE/handoffs/
mv FINAL_HANDOFF_CLEANUP_CORRECTIONS.md _ARCHIVE/handoffs/
```

**NOTE**: Keep `HANDOFF_TO_CLAUDE.md` at root — it's the CURRENT handoff doc referenced by GEMINI.md and CLAUDE.md.

### Step 3.3 — Move old guides and instructions to archive

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working

mv GEMINI_FLASH_CONTACT_PAGE.md    _ARCHIVE/old_guides/
mv GEMINI_FLASH_EMAIL_TEST.md      _ARCHIVE/old_guides/
mv GEMINI_FLASH_INSTRUCTIONS.md    _ARCHIVE/old_guides/
mv GO_LIVE_SEQUENCE.md             _ARCHIVE/old_guides/
mv CLAIM_FORM_EMAIL_ISSUES.md      _ARCHIVE/old_guides/
mv FORM_TESTING_GUIDE.md           _ARCHIVE/old_guides/
mv NOTEBOOKLM_GUIDE.md             _ARCHIVE/old_guides/
mv kilocode.md                     _ARCHIVE/old_guides/
mv security_analysis.md            _ARCHIVE/old_guides/
```

### Step 3.4 — Move old plans/implementations to archive

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working

mv implementation_plan.md  _ARCHIVE/old_plans/
mv task.md                 _ARCHIVE/old_plans/
```

### Step 3.5 — Move reference docs into docs/

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working

mv AGENT_CONTEXT_SETUP_GUIDE.txt   docs/
mv AGENT_PROTOCOL_CONTEXT.md       docs/
mv AGENT_QUICK_REFERENCE.md        docs/
mv AGENT_STATE.md                  docs/
mv INSTRUCTIONS_FOR_AGENTS.txt     docs/
mv PROJECT_CONTEXT_LOAD_EVERY_SESSION.txt  docs/
mv QUICK_REFERENCE_CARD.txt        docs/
mv TOOLS_REFERENCE.md              docs/
mv column_mappings.txt             docs/
```

### Step 3.6 — Move test/debug scripts to tests/

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working

mv check_rls_policies.py       tests/
mv debug_submit_browser.js     tests/
mv debug_submit_form.sh        tests/
mv test_rls_browser.js         tests/
mv test_rls_policies.sh        tests/
mv verify_form_submissions.sh  tests/
```

### Step 3.7 — Move misplaced scraper script

```bash
mv /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/scrape_linkedin_local.py \
   /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-automation/
```

### Step 3.8 — Move schema dump to supabase/

```bash
mv /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/schema_dump.sql \
   /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/supabase/
```

### Step 3.9 — Move Hydrogen session docs to _ARCHIVE

```bash
mv /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/Hydrogen_Infrastructure_Dir_/ \
   /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/_ARCHIVE/
```

### Step 3.10 — Move TSTR_2.0 concept docs to _ARCHIVE

```bash
mv /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/TSTR_2.0/ \
   /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/_ARCHIVE/
```

### Step 3.11 — Fix Media_Logos filenames (remove spaces)

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/Media_Logos/

mv "TSTR Grey Logo.png" "TSTR_Grey_Logo.png"
mv "TSTR Grey Logo.svg" "TSTR_Grey_Logo.svg"
```

### Step 3.12 — Add dev.pid and current_listings.json to .gitignore

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working

# Check if already in .gitignore
grep "dev.pid" .gitignore
grep "current_listings.json" .gitignore

# If NOT found, append them:
echo "" >> .gitignore
echo "# Runtime artifacts" >> .gitignore
echo "dev.pid" >> .gitignore
echo "current_listings.json" >> .gitignore
```

### Step 3.13 — Verify project root is cleaner

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working
ls -1 *.md *.txt *.py *.js *.sh *.json *.ts 2>/dev/null | wc -l
# Expected: significantly fewer than 61 (target: ~20-25 files)

# These files should REMAIN at root (do not move):
# .ai-session.md, .build-trigger, .env.local, .eslintignore, .eslintrc.js,
# .gitignore, .mcp.json, .opencode-init, .prettierrc,
# AGENTS.md, AGENT_PROTOCOL.md, CLAUDE.md, GEMINI.md, HANDOFF_TO_CLAUDE.md,
# OPENCODE.md, OPENHANDS.md, Qwen3-Coder.md,
# PROJECT_STATUS.md, README.md, START_HERE.md, TSTR.md,
# bootstrap.sh, checkpoint.sh, handoff.sh, resume.sh,
# package.json, package-lock.json, playwright.config.ts,
# eslint.config.js, dev.pid, current_listings.json,
# start-agent.sh (and other start-*.sh — consolidation is Phase 5),
# agent-cli, Link_to_bootstrap_agent.sh, test-phases.js
```

### Step 3.14 — Commit and checkpoint

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working && git add -A && git commit -m "Cleanup Phase 3: Organize project root - move handoffs, guides, tests to proper dirs"
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./checkpoint.sh "Cleanup Phase 3 complete - project root organized"
```

---

## PHASE 4: Security — Remove Exposed Keys from Git-Tracked Files

**Risk**: MEDIUM (editing file content, security-sensitive)
**Location**: Project-level CLAUDE.md

### Step 4.1 — Remove the Service Role JWT from CLAUDE.md

Open `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/CLAUDE.md`

Find line 154 (the one containing `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`) and replace the full JWT with:

```
- Service Role: [REDACTED - stored in .env and Cloudflare dashboard]
```

The section (lines 152-154) should look like:

```markdown
**API Keys**:
- Publishable: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO
- Service Role: [REDACTED - stored in .env and Cloudflare dashboard]
```

### Step 4.2 — Verify the key is removed

```bash
grep -r "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/CLAUDE.md
# Expected: NO output (key removed)
```

### Step 4.3 — Check for other exposed secrets (information only — report but don't remove)

```bash
# Search for JWT patterns in git-tracked files (excluding node_modules, .git, .venv)
grep -r "eyJhbGci" /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/ \
  --include="*.md" --include="*.txt" --include="*.json" --include="*.js" --include="*.ts" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.venv \
  -l
# Report any files found but do NOT modify them without approval
```

### Step 4.4 — Commit and checkpoint

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working && git add -A && git commit -m "Security: Redact service role key from CLAUDE.md"
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./checkpoint.sh "Cleanup Phase 4 complete - secrets redacted"
```

---

## PHASE 5: Consolidate Start Scripts (OPTIONAL)

**Risk**: LOW
**Location**: Project root

The project root has 5 nearly identical `start-*.sh` scripts:
- `start-agent.sh`
- `start-claude.sh`
- `start-gemini.sh`
- `start-opencode.sh`
- `start-openhands.sh`

### Step 5.1 — Compare them

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working
md5sum start-*.sh
# If all are identical → keep only start-agent.sh
# If they differ → leave them as-is
```

### Step 5.2 — If all identical, remove duplicates

```bash
# Only execute if md5sums are all the same
rm start-claude.sh start-gemini.sh start-opencode.sh start-openhands.sh
```

### Step 5.3 — Commit

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working && git add -A && git commit -m "Cleanup Phase 5: Consolidate identical start scripts"
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./checkpoint.sh "Cleanup Phase 5 complete"
```

---

## PHASE 6: Update Stale Documentation References

**Risk**: LOW (text-only changes)

### Step 6.1 — Update listing count in GEMINI.md (project-level)

In `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/GEMINI.md`:

Find: `163 listings as of 2025-11-17`
Replace with: `194 listings as of 2026-02-11`

### Step 6.2 — Update listing count in CLAUDE.md (project-level)

In `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/CLAUDE.md`:

Find: `163 listings as of 2025-11-17`
Replace with: `194 listings as of 2026-02-11`

### Step 6.3 — Update "Last Updated" dates

In both project-level `GEMINI.md` and `CLAUDE.md`:

Find: `**Last Updated**: 2025-11-22` or `**Last Updated**: 2025-11-23`
Replace with: `**Last Updated**: 2026-02-11`

### Step 6.4 — Fix stale path references in global CLAUDE.md

In `/media/al/AI_DATA/AI_PROJECTS_SPACE/CLAUDE.md`:

Find ALL occurrences of: `/media/al/AI_SSD/AI_PROJECTS_SPACE`
Replace ALL with: `/media/al/AI_DATA/AI_PROJECTS_SPACE`

Find ALL occurrences of: `/home/al/AI_PROJECTS_SPACE`
Replace ALL with: `/media/al/AI_DATA/AI_PROJECTS_SPACE`

**Verification:**
```bash
grep -n "AI_SSD" /media/al/AI_DATA/AI_PROJECTS_SPACE/CLAUDE.md
# Expected: NO output

grep -n "/home/al/AI_PROJECTS_SPACE" /media/al/AI_DATA/AI_PROJECTS_SPACE/CLAUDE.md
# Expected: NO output
```

### Step 6.5 — Fix stale path references in global GEMINI.md

In `/media/al/AI_DATA/AI_PROJECTS_SPACE/GEMINI.md`:

Find ALL occurrences of: `/home/al/AI_PROJECTS_SPACE`
Replace ALL with: `/media/al/AI_DATA/AI_PROJECTS_SPACE`

### Step 6.6 — Fix stale path references in project-level files

In both project-level `GEMINI.md` and `CLAUDE.md`:

Find ALL occurrences of: `/home/al/AI_PROJECTS_SPACE`
Replace ALL with: `/media/al/AI_DATA/AI_PROJECTS_SPACE`

### Step 6.7 — Commit and checkpoint

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working && git add -A && git commit -m "Cleanup Phase 6: Update stale docs - listing counts, dates, paths"
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && git add -A && git commit -m "Cleanup Phase 6: Fix stale paths in global CLAUDE.md and GEMINI.md"
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./checkpoint.sh "Cleanup Phase 6 complete - docs updated"
```

---

## PHASE 7: Push to GitHub

**Risk**: LOW

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working && git push origin main
cd /media/al/AI_DATA/AI_PROJECTS_SPACE && git push origin main 2>/dev/null || echo "Root repo may not have a remote - that's OK"
```

---

## POST-CLEANUP: Final Verification

Run these commands to confirm everything is clean:

```bash
# 1. Confirm AI_PROJECTS_SPACE root files
echo "=== ROOT FILES ==="
ls -1 /media/al/AI_DATA/AI_PROJECTS_SPACE/*.md /media/al/AI_DATA/AI_PROJECTS_SPACE/*.sh 2>/dev/null

# 2. Confirm ACTIVE_PROJECTS is clean
echo "=== ACTIVE_PROJECTS ==="
ls -1 /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/

# 3. Confirm project root file count
echo "=== PROJECT ROOT FILE COUNT ==="
find /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working -maxdepth 1 -type f | wc -l

# 4. Confirm no secrets in tracked files
echo "=== SECRET SCAN ==="
grep -r "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/ --include="*.md" --exclude-dir=.git --exclude-dir=node_modules -l 2>/dev/null || echo "No secrets found - GOOD"

# 5. Confirm no stale paths
echo "=== STALE PATH SCAN ==="
grep -r "AI_SSD" /media/al/AI_DATA/AI_PROJECTS_SPACE/CLAUDE.md 2>/dev/null || echo "No AI_SSD references - GOOD"
grep -r "/home/al/AI_PROJECTS_SPACE" /media/al/AI_DATA/AI_PROJECTS_SPACE/CLAUDE.md 2>/dev/null || echo "No /home/al refs - GOOD"

# 6. Git status
echo "=== GIT STATUS ==="
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working && git status
```

### Expected Final State

**AI_PROJECTS_SPACE root** (~20 items):
```
├── CLAUDE.md, GEMINI.md, DEEPAGENT.md, DROID.md, KIMI.md   (agent instructions)
├── OPENCODE.md, OPENHANDS.md, Qwen3-Coder.md               (agent instructions)
├── ARCHITECTURE.md, QUICKSTART.md, README.md, LICENSE        (project docs)
├── bootstrap_global.sh, checkpoint.sh, handoff.sh, resume.sh (core scripts)
├── agent-cli, ai-projects-space, project.db                  (system files)
├── ACTIVE_PROJECTS/                                           (projects)
├── ARCHIVE/                                                   (historical)
├── SYSTEM/                                                    (system core)
├── OpenHands/                                                 (consider archiving later)
├── PROJECTS_on_Ubuntu/                                        (consider archiving later)
├── build/, logs/, playground/, tools/                         (consider archiving later)
└── .git, .gitignore, .venv, .claude, .factory, .ruff_cache, .vscode
```

**Project root (tstr-site-working)** (~28 items at root):
```
├── AGENTS.md, AGENT_PROTOCOL.md, CLAUDE.md, GEMINI.md       (agent instructions)
├── OPENCODE.md, OPENHANDS.md, Qwen3-Coder.md                (agent instructions)
├── HANDOFF_TO_CLAUDE.md                                       (current handoff)
├── PROJECT_STATUS.md, README.md, START_HERE.md, TSTR.md      (project docs)
├── .ai-session.md                                             (session state)
├── package.json, package-lock.json, playwright.config.ts      (project config)
├── .gitignore, .eslintrc.js, .eslintignore, .prettierrc       (tool config)
├── .mcp.json, .opencode-init, .build-trigger, .env.local     (tool config)
├── bootstrap.sh, checkpoint.sh, handoff.sh, resume.sh         (symlinks)
├── start-agent.sh, agent-cli, Link_to_bootstrap_agent.sh     (launcher scripts)
├── eslint.config.js, test-phases.js                           (config/test)
├── _ARCHIVE/          (historical docs, handoffs, old plans)
├── bruno/             (API testing collections)
├── docs/              (reference documentation)
├── management/        (data management scripts)
├── Media_Logos/        (brand assets)
├── monitoring/         (monitoring scripts)
├── plans/              (planning docs)
├── src/                (shared types)
├── supabase/           (Supabase config + migrations)
├── tasks/              (task tracking)
├── tests/              (test scripts)
└── web/                (frontend + automation + backend)
```

---

## DEFERRED ITEMS (Require User Decision)

These items were identified but NOT included in the cleanup plan because they require a judgment call:

1. **OpenHands/ clone at AI_PROJECTS_SPACE root** — Is this actively being developed? If not, delete or archive.
2. **PROJECTS_on_Ubuntu/ at root** — Is this for another machine? If not, archive.
3. **tools/ and build/ at root** — Stale? Archive?
4. **Agent .md files (DROID.md, KIMI.md)** — Are Droid and Kimi still in use? If not, archive.
5. **management/ scripts** — Should they move into web/tstr-automation/? They're closely related.
6. **"TSTR Hub" branding** on pricing page and footer — Frontend code change needed (not a file move).
7. **Copyright 2025 → 2026** — Frontend code change needed.
8. **Missing /about page** — New page creation needed.
9. **Migration archive (39 SQL files)** in ACTIVE_PROJECTS/TSTR-site/migration_archive/ — Keep as reference or archive?

---

**End of Plan.**
