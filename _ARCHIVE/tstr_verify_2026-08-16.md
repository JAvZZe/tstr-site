# TSTR.directory Overnight Verification — 2026-08-16

Local-only run. No deploy, no git push, no credential writes.
Repo: /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working (present, `web/tstr-frontend/package.json` found).

## 1. Build
- root build: TRAP (0 pages, ignored) — not run, not a gate.
- Real gate: `web/tstr-frontend` → `npx dotenv -- npx astro build`
  - Exit code: **0**
  - Pages emitted: **243** HTML files in `dist/` (server built in 107.98s, "Complete!")
- BUILD CAVEAT (real runtime issue, not cosmetic): `Astro.request.headers` used on **prerendered** routes
  - `src/pages/standards/[slug].astro` (warned on every generated slug, ~40+ pages)
  - `src/pages/submit.astro`
  These silently yield nothing at prerender time. Fix = `export const prerender = false;` on those routes, or drop the header dependency.

## 2. Lint
- JS (`npm run lint:js` = `eslint .`, run from repo ROOT — `lint:js` does not exist in the frontend package.json):
  - **0 errors, 22 warnings** — all `@typescript-eslint/no-unused-vars`
  - Files: instrumentation.node.ts (4), BranchLocator.tsx, Header.astro (2), markdown-for-agents.ts, account/subscription.astro (3), admin/listings.astro, api/search/by-standard.ts, claim.astro, login.astro, pricing.astro (4), signup.astro, supabase/functions/paypal-cancel-subscription/index.ts, tests/search-api.spec.ts
  - The 2 known eslint-astro parser false-positives (terms.astro:193, waitlist.astro:142) **did NOT reproduce this run** — clean.
  - No blocking errors.
- Prettier (`npx prettier --write "src/**/*.{astro,ts,tsx,js,jsx,css}"`):
  - **0 source files reformatted** (all already formatted; `--list-different` = 0 afterwards; 0 files with mtime inside the run window).
  - Note: working tree already carries 110 pre-existing modified files under `web/tstr-frontend/src` from earlier formatting runs — not created by this job.

## 3. Secrets
`python3 scripts/secret_scan.py --all` → 991 files scanned, 3 hits:
- `web/tstr-frontend/.dev.vars:12` — google_api_key `AIzaSy…J7Z4`
- `web/tstr-frontend/.dev.vars:13` — google_api_key `AIzaSy…B2RM`
- `web/tstr-frontend/.dev.vars:9`  — stitch token `AQ.Ab8…mPdg`

All three are in `.dev.vars`, confirmed **gitignored** (`web/tstr-frontend/.gitignore:27`). No secrets in tracked source. Per the job rule (gitignored `.dev.vars` only) → CLEAN.

## VERDICT
- BUILD: **PASS** (frontend only — 243 pages, exit 0)
- LINT: **PASS** (0 blocking errors, 22 warnings)
- SECRETS: **CLEAN** (3 hits, all gitignored `.dev.vars`)
