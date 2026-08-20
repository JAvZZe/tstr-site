# TSTR.directory Overnight Verification — 2026-08-15

Local-only run. No deploy, no git push, no credential writes. Prettier `--write` (formatting-only) applied intentionally.

## Build
- **Frontend build (web/tstr-frontend, `astro build`): PASS** — exit 0, completed in ~84.6s (server built ~99.6s).
- Pages generated: **243 HTML files** in `dist/`.
- Root `npm run build`: TRAP (0 pages, no src/pages) — ignored as a gate.
- **Runtime caveat (real):** `Astro.request.headers` is used on prerendered routes and silently yields nothing at prerender time. Build emitted WARN for:
  - `src/pages/standards/[slug].astro` (fires on every /standards/* page)
  - `src/pages/submit.astro`
  - Related header usage also present in `src/pages/testing/standards/[code].astro`, `src/middleware.ts`, and many `src/pages/api/*` routes (API routes are server-rendered, so those are fine — only prerendered routes are the concern).

## Lint
- **JS (eslint . over whole tree): 0 errors, 18 warnings → PASS (no blocking errors).**
- All 18 warnings are `@typescript-eslint/no-unused-vars` across components/pages/tests (BranchLocator.tsx, Header.astro, markdown-for-agents.ts, subscription.astro, listings.astro, by-standard.ts, claim.astro, login.astro, pricing.astro, signup.astro, paypal-cancel-subscription/index.ts, search-api.spec.ts). Non-blocking cleanup, not failures.
- Note: the 2 known eslint-astro parser false-positives (terms.astro:193, waitlist.astro:142) did **not** surface in this full run — no blocking parser errors observed.
- Note: `npm run lint` / `lint:js` scripts only check *changed* files (lint-changed.sh); the full-tree `npx eslint .` above is the meaningful gate.
- **Prettier: 110 source files reformatted** (`src/**/*.{astro,ts,tsx,js,jsx,css}`). Formatting-only, no logic change. Working-tree files modified (intended). No deploy/push.

## Secrets
- `python3 scripts/secret_scan.py --all` scanned 991 files. 3 hits, all in **`web/tstr-frontend/.dev.vars`** (gitignored + untracked — confirmed via `git check-ignore`):
  - `google_api_key` .dev.vars:12 (AIzaSy…J7Z4)
  - `google_api_key` .dev.vars:13 (AIzaSy…B2RM)
  - `stitch` .dev.vars:9 (AQ.Ab8…mPdg)
- These live only in the gitignored local dev-vars file → **CLEAN** per rule (no secrets in tracked source).

## VERDICT
- **BUILD: PASS** (frontend, 243 pages, exit 0)
- **LINT: PASS** (0 blocking eslint errors; 18 unused-var warnings; prettier reformatted 110 source files)
- **SECRETS: CLEAN** (3 hits, all in gitignored/untracked .dev.vars)
