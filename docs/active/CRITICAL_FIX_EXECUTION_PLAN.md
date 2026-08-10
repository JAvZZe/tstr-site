# Critical Fix Execution Plan

Date: 2026-06-01
Project: TSTR.directory (`tstr-site-working`)
Audience: implementation agent

## Executive Decision

The most crucial fix is not another feature pass. The immediate priority is to make the current frontend/backend safe and verifiable in production:

1. Remove unsafe service-role and secret usage from public SSR/API surface.
2. Fix claim/admin authentication paths that currently expose or bypass trust controls.
3. Validate the completed PSEO/trust-architecture tasks against the live code and database.
4. Stabilize scraper/backend automation so it does not rely on hardcoded keys, stale WordPress-era flow, or unverifiable dry-run output.

Do these before Europe PSEO expansion, IAF client work, or further UI polish.

## Current Plan Context

`PROJECT_PLAN.md` says the niche localization/trust architecture tasks are complete, but its validation checklist is still open:

- RLS security: unverified standard users must not update `listing_capabilities.verified`.
- PSEO routes must resolve at the edge.
- Dynamic route responses must include `s-maxage`.
- Group pages must correctly list local physical branches.

`PROJECT_STATUS.md` also records a known frontend secrets remediation effort and still lists a Saudi Energy Hub 404 to fix. Treat these as current operational risk until proven otherwise.

## Critical Findings

### P0: Secret and service-role usage remains in Astro API routes

Evidence:

- `web/tstr-frontend/src/pages/api/submit.ts:14`
- `web/tstr-frontend/src/pages/api/claim_submission.ts:14`
- `web/tstr-frontend/src/pages/api/claim-status.ts:14`
- `web/tstr-frontend/src/pages/api/ai-search.ts:8` and `:55`
- `web/tstr-frontend/src/pages/api/subscription/pending/save.ts:5`
- `web/tstr-frontend/src/pages/api/subscription/pending/clear.ts:5`
- `web/tstr-frontend/src/pages/api/subscription/pending/resume.ts:5`
- admin endpoints under `web/tstr-frontend/src/pages/api/admin/*.ts`
- debug endpoints `web/tstr-frontend/src/pages/api/debug-env.ts` and `web/tstr-frontend/src/pages/api/debug-full.ts`

Impact:

- Service-role key bypasses RLS. Any unauthenticated or weakly authenticated route using it is a database integrity risk.
- Debug routes reveal secret presence and runtime configuration.
- Previous reports already identified exposed credentials. Do not assume rotation is complete.

Required fix:

- Delete public debug endpoints or hard-block them to local/dev only.
- Move all secret access to Cloudflare runtime env (`locals.runtime.env`) and fail closed if missing.
- Use anon/authenticated Supabase clients for public forms where RLS allows inserts.
- Keep service-role usage only behind a shared, audited server-only admin helper that verifies a real Supabase user token and staff role before constructing the admin client.
- Rotate all previously exposed secrets outside this repo before considering the incident closed.

Acceptance checks:

- `rg -n "SUPABASE_SERVICE_ROLE_KEY|RESEND_API_KEY|OPENROUTER_API_KEY|GEMINI_API_KEY|PAYPAL|LINKEDIN" web/tstr-frontend/src`
- The remaining matches must be server-only helper modules or routes with explicit authentication/rate limits.
- `/api/debug-env` and `/api/debug-full` must return 404/410 in production or be removed.
- Public form routes must work without service-role credentials.

### P0: Claim verification leaks tokens and accepts weak verification

Evidence:

- `web/tstr-frontend/src/pages/api/claim.ts:125` forces `domainVerified = false`.
- `web/tstr-frontend/src/pages/api/claim.ts:278` and `:294` send verification email twice.
- `web/tstr-frontend/src/pages/api/claim.ts:321` returns `verificationToken` in the API response.
- `web/tstr-frontend/src/pages/api/claim-listing.ts:176` also returns `verificationToken`.
- `web/tstr-frontend/src/pages/api/verify-claim.ts:57` accepts any six-digit code or `123456`.
- Several claim flows select `name` from `listings`, while the codebase mostly uses `business_name`.

Impact:

- A claimant can receive the verification token in the JSON response.
- Verification can be completed with a trivial code.
- Claim UX and ownership records may fail silently because of field/table drift.

Required fix:

- Never return verification tokens or resume tokens except for an explicitly labeled dev-only path that is impossible in production.
- Replace placeholder OTP logic with actual token matching against stored `verification_token`, expiry, and authenticated user/listing ownership.
- Send one verification email per claim.
- Normalize listing field usage to `business_name`.
- Decide whether `listing_owners` or `listing_ownership` is the canonical ownership table. Update routes, RLS, and docs accordingly.

Acceptance checks:

- No `Remove in production` token-return comments remain in production route responses.
- Claim tests cover anonymous claim, authenticated claim, expired token, bad token, and successful verification.
- Manual QA confirms a user cannot claim another listing without the real verification token.

### P0: Admin export and admin login need hardening

Evidence:

- `web/tstr-frontend/src/pages/admin/analytics/export.ts:5` says authentication is TODO and exports click analytics.
- `web/tstr-frontend/src/pages/api/admin/auth-login.ts:29` signs in through a service-role client.
- Admin routes verify role from `user_metadata`, which is client-influenced unless controlled through trusted admin flows.

Impact:

- Analytics export can leak traffic data.
- Service-role login can bypass protections intended for normal auth flows.
- Role checks may be weaker than intended if metadata is not locked down.

Required fix:

- Protect `admin/analytics/export.ts` with the same admin auth middleware as API admin routes.
- Prefer normal Supabase auth for login. Use service-role only for post-auth admin reads if absolutely needed.
- Move role checks to app metadata or a server-controlled `user_profiles` role table.
- Add rate limiting to admin login and email-sending routes.

Acceptance checks:

- Unauthenticated requests to all `/admin/*` API/export endpoints return 401.
- Non-staff authenticated users receive 403.
- Staff users can complete the required workflow.

### P1: PSEO dynamic route has a likely global-region query bug

Evidence:

- `web/tstr-frontend/src/pages/[category]/[standard]/[region]/index.astro:37` applies `.eq('region', region === 'global' ? undefined : region)`.

Impact:

- For `/.../global`, the query likely filters `region = undefined` instead of omitting the filter, causing false 404/empty pages.

Required fix:

- Build the Supabase query incrementally.
- Only add `.eq('region', region)` when `region !== 'global'`.
- Use `maybeSingle`/empty-state handling where appropriate, not only redirects.

Acceptance checks:

- Test at least one known category/standard/global URL and one specific-region URL.
- Confirm `Cache-Control: s-maxage=86400, stale-while-revalidate=3600`.

### P1: Trust/RLS migration needs verification against actual schema

Evidence:

- `supabase/migrations/20260411000000_niche_localization_trust.sql:20` creates owner capability policy using `public.listing_ownership`.
- The frontend primarily uses `listing_owners`.
- Both tables exist in the generated types/schema, which increases drift risk.
- The migration uses `SECURITY DEFINER` for `get_pseo_stats`.

Impact:

- Owners may not get the intended update ability, or the wrong table may enforce trust policy.
- `verified` protection may not match active app flows.
- Security-definer function needs explicit permission and search-path review.

Required fix:

- Run a real RLS verification script against Supabase with anon, authenticated standard user, staff, and service role contexts.
- Confirm `listing_capabilities.verified` cannot be changed by standard users.
- Confirm owners can update only intended non-verified fields.
- Add/adjust policies against the canonical ownership table.
- Add `SET search_path` or equivalent hardening for security-definer RPCs if missing.

Acceptance checks:

- Scripted test output saved under `docs/active/` or `test-results/`.
- `PROJECT_PLAN.md` validation checklist updated only after tests pass.

### P1: Backend automation still contains stale and unsafe paths

Evidence:

- `web/tstr-automation/auto_updater.py:23` contains a hardcoded Google API key.
- `web/tstr-automation/auto_updater.py:15`, `:84`, and `:86` still describe/manualize WordPress upload flow.
- `web/tstr-automation/base_scraper.py:508` writes `"updated_at": "now()"` as a literal string payload.
- `web/tstr-automation/base_scraper.py:653` creates `dry_run_data` but the run path never fills it.
- `PROJECT_STATUS.md` says scraper alerting is still pending.

Impact:

- Automation can leak or burn API keys.
- Operational flow does not match the current Supabase/Astro architecture.
- Dry-run validation is unreliable.
- Scraper failures can go unnoticed.

Required fix:

- Remove hardcoded API keys. Read from env only.
- Retire or rewrite WordPress-era automation docs/code paths.
- Fix timestamp handling to use Python ISO timestamps or database defaults.
- Populate dry-run output or remove the broken CSV promise.
- Add structured run summaries and failure alerting.

Acceptance checks:

- `python -m py_compile` passes for touched automation files.
- A `--dry-run --limit 2` scraper run produces inspectable output without database writes.
- Failure path emits a clear nonzero exit or alert hook.

## Execution Order

1. Security containment
   - Remove/debug-lock debug endpoints.
   - Create shared server auth/admin helper.
   - Refactor service-role routes behind that helper or anon/RLS paths.
   - Remove hardcoded/historical keys from automation.

2. Claim/admin correctness
   - Fix claim token handling and OTP verification.
   - Protect admin export.
   - Normalize role source and listing field names.

3. Database/RLS validation
   - Decide canonical ownership table.
   - Add focused migration(s) if needed.
   - Write and run RLS verification script.

4. PSEO and route validation
   - Fix global-region query.
   - Verify category/standard/region, group, company, Saudi hub, and sitemap routes.
   - Confirm cache headers.

5. Backend automation reliability
   - Fix env-only secrets.
   - Fix dry-run and timestamp handling.
   - Add scraper failure alerting.

6. Documentation closure
   - Update `PROJECT_PLAN.md` validation checklist only with evidence.
   - Update `PROJECT_STATUS.md` with the actual security/PSEO status.
   - Do not mark IAF/global expansion tasks complete unless paid API access and integration tests exist.

## Suggested Verification Commands

Run from repo root unless noted.

```bash
rg -n "SUPABASE_SERVICE_ROLE_KEY|sb_secret_|RESEND_API_KEY|OPENROUTER_API_KEY|GEMINI_API_KEY|PAYPAL|LINKEDIN|Remove in production|TODO: Add authentication" web/tstr-frontend/src web/tstr-automation -g '!**/node_modules/**' -g '!**/.venv/**'
```

```bash
cd web/tstr-frontend && npm run build
```

```bash
cd web/tstr-automation && python -m py_compile base_scraper.py main_scraper.py auto_updater.py
```

```bash
cd web/tstr-frontend && npm run preview
```

Manual route checks:

- `/[category]/[standard]/global`
- `/[category]/[standard]/[known-region]`
- `/group/[known-group-slug]`
- `/company/[known-company-slug]`
- `/saudi-energy-hub/`
- `/admin/analytics/export` unauthenticated and authenticated

## Non-Goals For This Agent Pass

- Do not build Europe PSEO pages before the core route/security validation passes.
- Do not implement IAF API calls until access, quota, and billing are confirmed.
- Do not refactor the full scraper suite beyond the reliability fixes above.
- Do not stage unrelated dirty files already present in the worktree.

