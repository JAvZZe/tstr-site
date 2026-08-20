# TSTR.directory Overnight Verification — 2026-08-14 03:00 SAST

Local-only run. No deploy, no git push, no credential writes. Repo: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working` (drive mounted, dir present). Node v24.15.0 / npm 12.0.2.

## 1. Build — PASS (with a caveat)

| Target | Command | Exit | Result |
|---|---|---|---|
| Repo root | `npm run build` | 0 | PASS but **0 pages built** |
| Real site `web/tstr-frontend` | `npm run build` | 0 | PASS — **243 pages**, server built in 96.7s |

Caveat: the root-level Astro build is effectively a no-op shell. Its log shows:

```
[WARN] Missing pages directory: src/pages
[build] 0 page(s) built in 1.50s
```

The deployable site lives in `web/tstr-frontend`, which compiles cleanly (Astro/TS, 243 routes). Verification of the root alone would have been a false green — the frontend build is the meaningful gate and it passes.

Non-blocking build warnings (repeated per `/standards/*` route + `/submit`):
`Astro.request.headers` used on a prerendered route (`src/pages/standards/[slug].astro`, `src/pages/submit.astro`). Headers are unavailable at prerender time, so those reads silently yield nothing. Fix by setting `export const prerender = false` on those routes or removing the header dependency.

## 2. Lint — 2 blocking errors

`npm run lint:js` (eslint .) → exit 1: **24 problems (2 errors, 22 warnings)**

Errors (both parse failures, i.e. eslint cannot read the file at all):
- `web/tstr-frontend/src/pages/terms.astro:193:4` — Parsing error: Declaration or statement expected
- `web/tstr-frontend/src/pages/waitlist.astro:142:17` — Parsing error: Declaration or statement expected

Note: the Astro build still succeeds on these files, so this is an eslint-parser/Astro-syntax mismatch rather than proven broken output — but it means those two pages are currently unlinted.

22 warnings, all `@typescript-eslint/no-unused-vars` (pricing.astro ×4, signup.astro, terms/other pages, `supabase/functions/paypal-cancel-subscription/index.ts`, `tests/search-api.spec.ts`). Cosmetic.

`npm run lint:css` (prettier --check .) → exit 2: **565 files unformatted**. Mostly `web/tstr-frontend/test_*.mjs|cjs|js`, `test-results/.last-run.json`, `tests/*.spec.ts`, `workflows/*.md`. Style-only; no auto-fix applied as instructed.

## 3. Secret scan — CLEAN for commit purposes

- `python3 scripts/secret_scan.py` (default `--staged`) → exit 0, "0 file(s), clean". **Vacuous** — nothing is staged, so this scanned nothing.
- `python3 scripts/secret_scan.py --all` → exit 1, **FOUND 1529 secret(s)**.

Triage of the 1529: **1526 are vendored-dependency false positives** inside `web/tstr-automation/_crawl4ai_venv/.../site-packages/` — the `paypal`/`resend` regexes matching base64 blobs and substrings in `playwright/driver/node`, `utilsBundle.js`, `PIL/ImageFont.py`, `cacert.pem`, `tiktoken/*.so`, `.pyc` files. Not credentials.

**3 genuine credential-shaped hits**, all in one file:
```
web/tstr-frontend/.dev.vars:9   SECRET[stitch]          AQ.Ab8…mPdg
web/tstr-frontend/.dev.vars:12  SECRET[google_api_key]  AIzaSy…J7Z4
web/tstr-frontend/.dev.vars:13  SECRET[google_api_key]  AIzaSy…B2RM
```
Exposure check (evidence):
- `git ls-files --error-unmatch web/tstr-frontend/.dev.vars` → not tracked ("Did you forget to 'git add'?")
- `git check-ignore -v` → ignored by `web/tstr-frontend/.gitignore:27:.dev.vars`

So these are local dev-only values, untracked and gitignored — **no new secret leak**. No rotation required on this evidence.

## Verdict

Build green (frontend, 243 pages). No blocking runtime/compile failure. Two eslint parse errors and a large prettier backlog are the only real cleanliness debt. Secret posture unchanged/clean.

## Suggested follow-ups (not actioned)
1. Add an ignore glob for `**/_crawl4ai_venv/**` and `**/site-packages/**` in `secret_scan.py` — a 1529-hit `--all` run is unusable signal and will train people to ignore the scanner.
2. Fix the two `.astro` eslint parse errors so `terms`/`waitlist` are actually linted.
3. Resolve `Astro.request.headers` on the prerendered `standards/[slug]` and `submit` routes.
4. Either format the 565 prettier files once or scope `lint:css` to source dirs (exclude `test_*`, `test-results/`, `workflows/`).
