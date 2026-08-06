# PI.md — TSTR.directory (Pi Agent Guide)

> **Purpose**: Entry point for Pi agents on this repo. Full continuity and project detail live in **`CLAUDE.md`** and **`TSTR.md`**. Workspace routing and git boundaries live in **`AGENTS.md`** (project) and **`../../AGENTS.md`** (AI_PROJECTS_SPACE root).

---

## Scope

| Doc | Role |
|-----|------|
| **This file** | Pi session start, model routing, non-negotiables |
| **`CLAUDE.md`** | Full agent protocol (bootstrap, checkpoints, SEO, infra) |
| **`AGENTS.md`** | TSTR overlay on root agent registry |
| **`../../AGENTS.md`** | Capability-first routing, GitNexus, git boundaries |
| **`TSTR.md`** | Architecture, commands, P0/P1/P2 priorities |
| **`PROJECT_STATUS.md`** | Live deployment truth — read before work, update after |
| **`PROJECT_PLAN.md`** | Project plan — read before work, update after |

---

## Model Routing Policy

**Pi accesses agents via the OpenRouter API.**

| Role | Primary Model | Fallback | Rationale |
|------|--------------|----------|-----------|
| **Strategy / Architecture** | `deepseek/deepseek-chat-v3-0324` (top Deepseek) | `deepseek/deepseek-r1` | Deep reasoning, root cause analysis, planning |
| **Coding / Implementation** | `anthropic/claude-sonnet-4-20250514` ([PERSON_NAME]) | `anthropic/claude-3-5-sonnet-20241022` | Code generation, debugging, refactoring |
| **Bulk / Simple tasks** | `openrouter/quen3-coder` or free tier | Local Ollama | Cost-effective for repetitive work |

**Policy**: Use top Deepseek for strategy and [PERSON_NAME] for coding until other models improve. Re-evaluate model performance monthly against `AGENTS.md` registry.

---

## Mandatory session start (required)

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working"
./bootstrap.sh TSTR.directory   # or: muninn-cli bootstrap TSTR
cat PROJECT_STATUS.md
```

Optional: `agent-cli bootstrap TSTR-site`

---

## Report first (do not auto-continue)

After the assigned task or when you find a blocking issue:

1. Summarize what was done or found.
2. Propose next steps.
3. **Wait for explicit user approval** before further implementation, deploys, or scope expansion.

Do **not** commit, push, or deploy unless the user asks.

---

## Git boundaries

- **Nested repo only**: All TSTR git operations run in this directory (`tstr-site-working`).
- **Remote**: `https://github.com/JAvZZe/tstr-site.git`
- **Do not** stage TSTR files from the root `AI_PROJECTS_SPACE` repo.
- Tag learnings and tasks with `TSTR-site` or `TSTR.directory`.

---

## Project layout

| Area | Path |
|------|------|
| **Project root** | `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working` |
| **Frontend** | `web/tstr-frontend/` (Astro + React + Tailwind, Cloudflare Pages) |
| **Scrapers** | `web/tstr-automation/` (Python on OCI `[IP_ADDRESS]`) |
| **Database** | [PERSON_NAME] — project ref `haimjeaetrsaauitrhfy` |
| **Live site** | https://tstr.directory |

Secrets: use env / Cloudflare / Supabase dashboards — never commit `.env`, service role keys, or PATs.

---

## Read order (first visit or cold start)

1. `START_HERE.md`
2. `TSTR.md`
3. `.ai-session.md`
4. `PROJECT_STATUS.md`
5. `HANDOFF_TO_CLAUDE.md` (if present)
6. `CLAUDE.md` for protocol depth

---

## During work

- **Checkpoint** (global): `cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && agent-cli checkpoint "description"`
- **Learnings**: `muninn-cli store "..." "concept" "TSTR-site,tags"` or `SYSTEM/state` `add_learning` with `TSTR.directory` tags
- **Tasks**: `agent-cli task` / `db_utils` scoped to TSTR
- **Archive** completed interim docs to `_ARCHIVE/`; delete redundant `HANDOFF_*.md` after merge

---

## Code change discipline

- **GitNexus** (when MCP/index available): run impact analysis before editing symbols; `detect_changes` before commit; warn on HIGH/CRITICAL risk. If degraded, use search/read and note it.
- **Minimize diff**; match existing conventions; no drive-by refactors.
- **Test before deploy**; document live-impacting changes in `PROJECT_STATUS.md` (version bump + timestamp).
- **Uncertainty**: State guesses explicitly; give evidence-based confidence when asserting fixes.

---

## TSTR-specific guardrails

### SEO hybrid hook (landing pages)

Do not remove dual targeting on category/region pages:

- H1: `[Category] Testers`
- H2: `[Category] Testing Services`
- Title/meta: both keyword families

See `MARKETING_STRATEGY.md` and `CLAUDE.md` → SEO Hybrid Hook.

### Supabase keys

Use `sb_publishable_*` / `sb_secret_*` (not legacy JWT). Admin/server routes: service role via server env only, never client bundles.

### Human-facing complex artifacts

Per bifurcated HTML protocol: use `docs/agent_artifacts/` self-contained HTML with export when interactivity helps; use Markdown for machine-facing logs and status.

---

## Pi / workspace notes

- **User rules**: Commits and PRs only when requested; no force-push to main; no `--no-verify` unless asked.
- **Vibe Flow**: Optional workflow shortcuts in `CLAUDE.md` (`/vibe-help`, `CB`, `QD`, etc.) under `salesmark/.cursor/rules/` when using that subtree.
- **OpenRouter**: All agent calls route through OpenRouter. Monitor cost via `ai-stats` alias. Prefer free tier for bulk; pay for strategy/coding quality.

---

## Enforcement self-check

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./SYSTEM/enforcement/protocol_check.sh
```

---

## Handoff

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && agent-cli handoff <agent-id> "<reason>"
```

---

**Last updated**: 2026-06-07
**Canonical detail**: `CLAUDE.md` (protocol), `AGENTS.md` (boundaries), `TSTR.md` (product/engineering)