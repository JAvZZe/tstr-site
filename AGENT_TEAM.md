# TSTR Agent Team — Roles, Process & Collaboration

This document defines the **roles** that operate on the TSTR.directory project,
the **process** each follows, and **how they work together**. It is
harness-neutral: an agent can be Claude, Codex, Gemini, Qwen, the Hermes
Agent, or any CLI tool. The role matters, not the name. This file is the
human-readable map; the machine-readable role definitions live in `agents/`
(see "Two layers" below).

> Bootstrap first: `cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./bootstrap_global.sh`
> then `./start-agent.sh` (per `AGENTS.md`). Do not skip — context lives outside
> the repo (OCI, Supabase, Cloudflare, GitHub secrets).

---

## Two layers of role definitions

1. **Harness-native source (Hermes):** `/home/al/.hermes/profiles/tstr-hub_pm/skills/tstr-*/SKILL.md`
   — the authoritative behavior spec when running inside the Hermes harness.
2. **Harness-neutral mirror:** `agents/tstr-*.md` (this repo) — same content,
   Claude/Codex/CLI-readable frontmatter. Use these when operating outside
   Hermes. If the two disagree, the Hermes `SKILL.md` wins.

Keep both in sync. Editing the role behavior = edit the Hermes `SKILL.md`, then
regenerate `agents/tstr-<name>.md`.

---

## The roles (18)

| Role | Files | Owns | Hands off to |
|------|-------|------|--------------|
| **team-lead** (orchestrator) | agents/tstr-team-lead.md | routing, sequencing, report-first gate | all others |
| **agent-creator** (meta) | agents/tstr-agent-creator.md | designs/new TSTR agents from best practice | team-lead |
| **frontend** | agents/tstr-frontend.md | Astro/React build, components, supabase.ts hygiene | perf, ux, db, deploy |
| **perf** | agents/tstr-perf.md | Core Web Vitals (LCP/INP/CLS), bundle, CF edge | frontend, qa |
| **ux** | agents/tstr-ux.md | WCAG 2.1 AA, keyboard, contrast, responsive | frontend, perf |
| **db** | agents/tstr-db.md | Supabase schema, drift, indexes, RLS *presence* | security, frontend |
| **deploy** | agents/tstr-deploy.md | pre-deploy checklist + live verify (Wrangler/curl) | frontend, security |
| **qa** | agents/tstr-qa.md | Playwright + independent LLM critic on diffs | frontend, verification-gate |
| **tdd** | agents/tstr-tdd.md | red-green-refactor, Prove-It bugs | qa, frontend |
| **code-review** | agents/tstr-code-review.md | review discipline | qa |
| **verification-gate** | agents/tstr-verification-gate.md | static CI lint/scan gate (scripts/) | qa, deploy |
| **content** | agents/tstr-content.md | blog/standards/sector copy, anti-AI-slop voice | seo, frontend |
| **seo** | agents/tstr-seo.md | meta/JSON-LD, GEO/AEO, CWV *targets* | content, frontend |
| **growth** | agents/tstr-growth.md | off-page, distribution, brand | content, seo |
| **security** | agents/tstr-security.md | RLS *correctness*, secrets, authz | db, deploy, frontend |
| **security-hardening** | agents/tstr-security-hardening.md | hardening pass | security |
| **data-ops** | agents/tstr-data-ops.md | ingest, dedup, geo | db, scraper-agent |
| **scraper-agent** | agents/tstr-scraper-agent.md | OCI scraper runs/recovery | data-ops, db |

---

## The collaboration model

### 1. Intake → route (team-lead)
Every task enters through **team-lead**, which routes to one role (or a short
sequence). team-lead does NOT do the work; it dispatches. A task that spans
domains becomes a small pipeline (e.g. feature → frontend → qa → deploy).

### 2. Build → gate → verify → deploy (the spine)
```
code change
   └─ frontend (implements)
        └─ tdd (tests first) + qa (Playwright + independent LLM critic)
             └─ verification-gate (CI: lint-changed.sh + verify-changed.sh — BLOCKING)
                  └─ deploy (pre-check lockfile/env/gates, then live verify)
```
No step is skipped. `verification-gate` is fail-closed: a missing/red gate
blocks the push.

### 3. Audit loop (scheduled, not on-demand)
- **perf / ux / db / seo** run on a cadence (cron) and REPORT findings; they
  propose fixes but do not commit without "proceed".
- **verification-gate watchdog** re-scans new commits for secrets/drift.

### 4. New capability → agent-creator
When a gap appears, **agent-creator** researches best practice + available
tools, reuses existing roles, verifies external claims, and authors a new
`agents/tstr-<name>.md` (mirrored to the Hermes `SKILL.md`). It does not
free-hand an agent.

### 5. Report-first (mandatory)
Per `AGENTS.md`: after a task, STOP and report. WAIT for "proceed" before the
next action, a refactor, or a push. Autonomy (decide/execute/commit/test) applies
to single-agent granted-authority work; multi-agent routing still reports first.

---

## Secrets, credentials & tools (the reality — read before touching infra)

**Credentials file (gitignored, NEVER commit):** `TSTR_hub_Supabase_Keys.md`
at repo root. Holds: Supabase URL, **anon/public key**, **service-role key**,
Management PAT, Postgres password. Treat all as secret.

**Where each secret lives (Systems-Thinking: infra exceeds the repo):**
- **Supabase URL + anon key** → GitHub Actions secret (`SUPABASE_URL`,
  `SUPABASE_ANON_KEY`) AND Cloudflare Pages dashboard env vars. Used by CI
  build + native CF deploy. These are PUBLIC by design — safe to expose to the
  browser/build.
- **Service-role key** → Cloudflare dashboard + local `.env` ONLY. **NEVER** in
  a `PUBLIC_` frontend env var, GitHub secret fed to a `PUBLIC_` var, or
  committed. `supabase.ts` falls back to anon when service-role is absent, so
  the build works without it. Injecting service-role into the client is the leak
  that was previously remediated — do not reintroduce it.
- **Supabase MCP** (read-only) → `web/tstr-automation/TSTR1.mcp.json`, PAT
  scoped, used for DB queries by agents, not for writes.
- **OCI scrapers** → `84.8.139.90` (Oracle Linux 9); SSH key on external
  archive drive. Heavy scrapers run locally (40GB RAM); lightweight on OCI.

**Tools actually available (verify, don't assume):**
- `supabase` CLI at `/usr/bin/supabase` (v2.95.4): `db lint`, `db diff`,
  `db remote psql`.
- `wrangler` in `web/tstr-frontend/node_modules/.bin/` — for live deploy
  verify (`wrangler pages deployment list/get`). **Local auth is often expired**
  → needs `wrangler login` or a fresh `CLOUDFLARE_API_TOKEN`. When unavailable,
  verify live via `curl` (title/JSON-LD matches current source), and state
  UNVERIFIED rather than claiming live.
- Playwright / Lighthouse / axe-core: **NOT pre-installed** — run on demand via
  `npx` (e.g. `npx playwright`, `npx @axe-core/cli`, `npx lighthouse`).
- Hermes tools (when in-harness): read_file, write_file, patch, search_files,
  terminal, skill_manage, delegate_task, browser_*, cronjob, memory.

---

## Deploy reality (VERIFIED)
- **Cloudflare native GitHub integration** is the deploy path (project
  `tstr-hub`, account `93bc6b66…`). Push to `main` → CF builds `web/tstr-frontend`
  and deploys. No manual deploy step.
- The GitHub "Cloudflare Pages" check = **build status only, NOT live proof**.
  Always confirm the served bundle via Wrangler or curl.
- **Lockfile gotcha:** any `package.json` dep change MUST regenerate
  `package-lock.json` (`cd web/tstr-frontend && npm install`) or CF's `npm ci`
  fails silently.
- The old `cloudflare/pages-action` CI step was removed (it needed a
  non-existent `CF_API_TOKEN`).

---

## Folder discipline (TSTR-scoped only)
- Agent role defs: repo `agents/tstr-*.md` (mirror) + Hermes profile `SKILL.md`
  (source). **No** vendor-named folders (no `.claude/agents/` for TSTR roles).
- Global writing/SEO skills stay in `SYSTEM/skills/` as shared sources.
- Secrets: gitignored file + external dashboards/secrets; never in repo.
- Interim/handoff docs: delete when done, or move to `_ARCHIVE/`.

---

## How a new agent gets created (agent-creator loop)
1. **Research** the role's real surface (repo + verified external source).
2. **Reuse** — patch an existing role if ≥70% overlaps; else create new.
3. **Verify** external claims (GitHub API / live fetch) before adopting.
4. **Author** `agents/tstr-<name>.md` (Claude/CLI frontmatter) + mirror to
   Hermes `SKILL.md`.
5. **Validate** — skill loads, frontmatter within limits, no duplicate peer.
6. **Report**; commit only on "proceed".
