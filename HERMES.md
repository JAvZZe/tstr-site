# HERMES.md — Hermes Agent Operating Guide (TSTR.directory)

> Scoped for **Hermes**. Loaded when Hermes works in `ACTIVE_PROJECTS/tstr-site-working`.
> TSTR is a **nested, independent git repo** (own remote `github.com/JAvZZe/tstr-site.git`).
> See root `HERMES.md` for global rules. Last updated: 2026-08-04.

## Project shape
- B2B testing-services directory. Astro + React + Tailwind frontend; Python scrapers on OCI; Supabase Postgres; Cloudflare Pages deploy.
- Frontend: `web/tstr-frontend/` · Scrapers: `web/tstr-automation/` · Live: `https://tstr.directory`
- **This folder is git-ignored at the AI_PROJECTS_SPACE root** — it has its OWN git history. Commit/push here, not in root.

## Hermes capabilities mapped
| Task | Hermes approach |
|---|---|
| Read status | `cat PROJECT_STATUS.md`, `cat .ai-session.md`, `cat START_HERE.md` (in order) |
| DB query | Supabase MCP tools if configured, else `supabase db remote psql -c "…"` (supabase at `/usr/bin/supabase`) |
| Scraper ops (OCI) | terminal `ssh -i /tmp/oci-key.pem opc@84.8.139.90` — copy key first: `cp "<key>" /tmp/oci-key.pem && chmod 600 /tmp/oci-key.pem` |
| Frontend | `cd web/tstr-frontend && npm run dev` / `npm run build` |
| Deploy | `git push origin main` → Cloudflare auto-deploy. Local commit does NOT update live site. |
| API tests | Bruno (`bru run bruno/... --env production`) if installed |

## Mandatory protocol (from TSTR.md / CLAUDE.md)
- **READ FIRST**: `PROJECT_STATUS.md` before any change. Update + version-bump + timestamp after.
- **Report first**: finish task → STOP → report → WAIT for "proceed".
- **Schema changes**: run `supabase db diff` before committing; use migration files.
- **Secrets**: Supabase service-role key + API keys were previously exposed in frontend code (remediated). NEVER echo secrets; use `[REDACTED]`. Frontend must not contain service-role/supabase secrets.
- **SEO hook**: H1 "Testers" + H2 "Testing Services" dual-targeting is enforced — do not remove H2/title structure.

## Known TSTR facts (verified)
- Strategic focus: Hydrogen Infrastructure Testing + Biotech/Pharma/Life Sciences.
- OCI scraper: `~/tstr-scraper/`, cron `0 2 * * *`, FREE tier, last run ~2026-02 (194 listings). SSH key on external archive drive.
- Google Cloud OVERDUE/unavailable — all cloud = OCI.
- Supabase free tier: 500MB / 50K rows; RLS required for frontend.

## Hermes memory
- Learnings: `db_utils.add_learning(..., tags=["TSTR.directory", …])` (dual-writes project.db + MuninnDB).
- Bridge refreshes MEMORY.md on commit.

## Caveats
- `agent-cli` NOT on PATH here — use root `./agent-cli` if needed.
- Don't confuse `/media/al/AI_SSD/` (empty/stale) with the real root `/media/al/AI_DATA/`.
