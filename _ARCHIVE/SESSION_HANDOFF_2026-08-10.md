# TSTR Session Handoff — 2026-08-10

> Resume point after context compaction. Read this FIRST, then `AGENT_TEAM.md`
> for roles/process, then `PROJECT_STATUS.md` for live state.

## What is DONE (committed + pushed to main, CI green, live 200)
- **Verification gate (Part A+B):** `web/tstr-frontend/scripts/lint-changed.sh`
  (prettier, changed-files only), `verify-changed.sh` (static secret/injection
  scan), `verify-watchdog.sh` (cron), `install-hooks.sh` (pre-push). Wired into
  `package.json` (lint/verify/watchdog/prebuild) + `ci.yml` as BLOCKING gates.
  Dead `cloudflare/pages-action` step removed (missing CF_API_TOKEN).
- **Agent team (18 roles), built via tstr-agent-creator loop:**
  team-lead, agent-creator, frontend, perf, ux, db, deploy, qa, tdd,
  code-review, verification-gate, content, seo, growth, security,
  security-hardening, data-ops, scraper-agent. Each: Hermes `SKILL.md` (source)
  + `agents/tstr-*.md` (harness-neutral mirror).
- **Cross-harness mirrors moved OUT of vendor `.claude/`:** now at repo-root
  `agents/tstr-*.md`. `.claude/agents/` deleted (incl. `_ARCHIVE/` of stale
  micro-agents + invented `CLAUDE.md`). `.claude/settings.local.json` +
  `.claude/commands/` left untouched (not ours).
- **`AGENT_TEAM.md` created** (repo root): 18-role map, two-layer defs,
  collaboration model, verified secrets/credentials/tools reality, deploy
  reality, folder discipline. `AGENTS.md` points to it.
- **CI red → fixed:** `secrets.SUPABASE_ANON_KEY` value was empty (name
  existed). Set PUBLIC values only via `gh secret set` (stdin, never echoed):
  `SUPABASE_URL` + `SUPABASE_ANON_KEY`. Deliberately did NOT set
  `SUPABASE_SERVICE_ROLE_KEY` (frontend PUBLIC_ leak = remediated smell;
  build falls back to anon). Fresh `gh workflow run` resolved secrets → run
  31332582527 = success.

## Location of things (folder discipline — TSTR-scoped only)
- Agent role sources: `/home/al/.hermes/profiles/tstr-hub_pm/skills/tstr-*/SKILL.md`
- Agent role mirrors: `<repo>/agents/tstr-*.md`
- Team map: `<repo>/AGENT_TEAM.md` (+ `AGENTS.md` pointer)
- Creds (gitignored, NEVER commit): `<repo>/TSTR_hub_Supabase_Keys.md`
- Global writing/SEO skills: `SYSTEM/skills/` (shared sources, not TSTR-scoped)

## Secrets / credentials reality (verified)
- `TSTR_hub_Supabase_Keys.md` gitignored. Holds URL, anon, service-role, PAT,
  postgres pw.
- GitHub secrets: `SUPABASE_URL` + `SUPABASE_ANON_KEY` (PUBLIC, safe).
  `SUPABASE_SERVICE_ROLE_KEY` intentionally NOT set anywhere frontend-readable.
- Cloudflare dashboard env vars hold anon + service-role (native deploy).
- Supabase MCP read-only in `web/tstr-automation/TSTR1.mcp.json`.
- OCI scrapers: `84.8.139.90` (Oracle Linux 9); SSH key on external archive drive.
- Tools: `supabase` CLI @ `/usr/bin/supabase` (v2.95.4); `wrangler` in
  `web/tstr-frontend/node_modules/.bin/` (local auth often expired → use curl
  verify, state UNVERIFIED); Playwright/Lighthouse/axe via `npx` (not
  pre-installed).

## Deploy reality (VERIFIED)
- Cloudflare native GitHub integration = deploy path (project `tstr-hub`,
  account `93bc6b66…`). Push main → CF builds `web/tstr-frontend` → deploys.
- GitHub "Cloudflare Pages" check = BUILD status only, NOT live proof. Verify
  via Wrangler or curl (title/JSON-LD matches current source).
- Lockfile gotcha: any `package.json` dep change MUST `npm install` to regen
  `package-lock.json` or CF `npm ci` fails silently.

## Open items / decisions
- `tstr-deploy` Wrangler live-verify can't run here (CF token expired) — uses
  HTTP probe; documented as UNVERIFIED-by-Wrangler.
- Verification gate + agent team are the user's requested deliverables — DONE.
- No in-flight task at compaction. Next work is user-directed.

## Resume checklist
1. Read this file + `AGENT_TEAM.md` + `PROJECT_STATUS.md`.
2. `cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./bootstrap_global.sh` then
   `./start-agent.sh` (per AGENTS.md) before project work.
3. If continuing agent work: edit Hermes `SKILL.md`, regenerate
   `agents/tstr-<name>.md`, keep both in sync.
4. Report-first before irreversible actions (tstr-team-lead protocol).
