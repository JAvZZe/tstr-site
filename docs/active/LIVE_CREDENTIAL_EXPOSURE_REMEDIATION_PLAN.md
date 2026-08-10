# Live Credential Exposure Remediation Plan

> Created: 2026-06-07
> Owner: Next implementation agent
> Priority: Critical
> Scope: Public production exposure on `https://tstr.directory`

## Summary

The live site currently exposes sensitive runtime configuration through public debug API routes.

> ## 🔎 REALITY CHECK — 2026-08-10 (Hermes)
> Verified against live site + source, not assumptions:
> - **Live exposure: CONTAINED.** `https://tstr.directory/api/debug-env` and `/api/debug-full`
>   return `404` (`{"error":"not_found"}`) in production. They are gated behind
>   `PUBLIC_DEBUG_ENDPOINTS=true` (dev-only). So the P0 public exposure described below is
>   **not currently reachable in production**.
> - **But acceptance criteria are NOT met:**
>   - Phase 1 says "delete both route files" — they were NOT deleted; only gated. `debug-full.ts:29-31`
>     still builds a `keyFirstPart`/`keyLooksValid` leak path when the flag is on.
>   - Phase 6 says `ai-search.ts` must not use service role — it STILL does (`ai-search.ts:8,55`).
> - **Repo redaction sweep (2026-08-10):** plaintext secrets removed from tracked docs/configs
>   and git-ignored credential stores. A commit-gating scanner now exists
>   (`scripts/secret_scan.py` + `scripts/pre-commit.hook`).
> - **Key rotation: NOT done.** 19 GitHub secret-scanning alerts remain OPEN (history + runtimes
>   still hold real keys). Redaction alone does not close them — see `CREDENTIAL_ROTATION_RUNBOOK.md`.
> - **Recommended next step:** either delete `debug-env.ts`/`debug-full.ts` (preferred) or keep
>   the gate but strip the service-role metadata from `debug-full.ts`; and move `ai-search.ts`
>   to anon key + RLS or a server-only admin helper.

Confirmed public endpoints:

- `https://tstr.directory/api/debug-env`
- `https://tstr.directory/api/debug-full`

Confirmed exposure:

- `debug-env` publicly lists runtime environment variable names.
- `debug-env` confirms that sensitive production env vars exist, including `SUPABASE_SERVICE_ROLE_KEY` and `LINKEDIN_CLIENT_SECRET`.
- `debug-full` publicly returns a partial Supabase secret key value, its source, and metadata.

Do not copy exposed secret fragments into commits, docs, issue comments, chat, or logs.

## Immediate Objective

Remove all public debug exposure from production, redeploy, verify the endpoints are unreachable, then rotate affected credentials and update every dependent runtime.

## Required Protocol

Before code work:

1. Run global bootstrap:

   ```bash
   cd /media/al/AI_DATA/AI_PROJECTS_SPACE && ./bootstrap_global.sh
   ```

2. Run git/data audit:

   ```bash
   cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working
   git branch -a --sort=-authordate
   ```

3. Read:

   - `PROJECT_STATUS.md`
   - `CODEX.md`
   - this plan

## Phase 1: Remove Public Debug Routes

Target files:

- `web/tstr-frontend/src/pages/api/debug-env.ts`
- `web/tstr-frontend/src/pages/api/debug-full.ts`

Preferred fix:

- Delete both route files entirely.

Acceptable fallback if route deletion creates routing/deployment issues:

- Replace each route with a hard `404` response and no environment inspection.
- Do not return env names, key prefixes, key lengths, boolean secret-presence flags, runtime object keys, or `import.meta.env` keys.

Verification:

```bash
rg -n "debug-env|debug-full|envKeys|keyFirstPart|SUPABASE_SERVICE_ROLE_KEY|LINKEDIN_CLIENT_SECRET" web/tstr-frontend/src/pages/api
```

Expected result:

- No `debug-env` or `debug-full` route implementation remains.
- No debug endpoint returns secret metadata.

## Phase 2: Remove Tracked Hardcoded Resend Secret

Target files:

- `web/tstr-frontend/src/lib/email.ts`
- `web/tstr-frontend/test_email_sending.mjs`

Required changes:

- Remove the hardcoded Resend API key fallback in `src/lib/email.ts`.
- Remove the literal Resend API key assignment in `test_email_sending.mjs`.
- Use only server-side env access for `RESEND_API_KEY`.
- Do not use `PUBLIC_RESEND_API_KEY`.
- Keep email sending code server-only.

Verification:

```bash
rg -n --hidden --glob '!node_modules' --glob '!dist' --glob '!build' "re_[A-Za-z0-9_\\-]{20,}|PUBLIC_RESEND_API_KEY" web/tstr-frontend
```

Expected result:

- No hardcoded Resend key.
- No `PUBLIC_RESEND_API_KEY` usage.

## Phase 3: Build and Local Secret Scan

Run from `web/tstr-frontend`:

```bash
npm run build
```

Then scan the built output and source for high-risk token patterns:

```bash
rg -n --hidden --glob '!node_modules' --glob '!package-lock.json' "(re_[A-Za-z0-9_\\-]{20,}|sk-[A-Za-z0-9_\\-]{20,}|AIza[0-9A-Za-z_\\-]{20,}|sb_secret_[A-Za-z0-9_\\-]+|eyJ[A-Za-z0-9_\\-]+\\.[A-Za-z0-9_\\-]+\\.[A-Za-z0-9_\\-]+|SERVICE_ROLE|SUPABASE_SERVICE|PAYPAL_CLIENT_SECRET|LINKEDIN_CLIENT_SECRET|OPENROUTER_API_KEY|GEMINI_API_KEY|INTERNAL_API_SECRET)" web/tstr-frontend/src web/tstr-frontend/dist
```

Expected result:

- No hardcoded secrets in browser assets.
- Server-side source may reference secret env var names only where routes are properly authenticated.

## Phase 4: Deploy

Deploy the frontend to Cloudflare Pages using the project’s existing deployment flow.

After deployment, verify the live routes:

```bash
curl -L -i https://tstr.directory/api/debug-env
curl -L -i https://tstr.directory/api/debug-full
```

Expected result:

- Both routes return `404`, `410`, or another non-sensitive response.
- They must not return JSON containing env keys, key prefixes, key lengths, or secret presence booleans.

Scan live public pages and bundles:

```bash
mkdir -p /tmp/tstr-live-audit
curl -L --fail --silent --show-error https://tstr.directory -o /tmp/tstr-live-audit/home.html
curl -L --fail --silent --show-error https://tstr.directory/pricing -o /tmp/tstr-live-audit/pricing.html
curl -L --fail --silent --show-error https://tstr.directory/submit -o /tmp/tstr-live-audit/submit.html
rg -n "(re_[A-Za-z0-9_\\-]{20,}|sk-[A-Za-z0-9_\\-]{20,}|AIza[0-9A-Za-z_\\-]{20,}|sb_secret_[A-Za-z0-9_\\-]+|eyJ[A-Za-z0-9_\\-]+\\.[A-Za-z0-9_\\-]+\\.[A-Za-z0-9_\\-]+|SERVICE_ROLE|SUPABASE_SERVICE|RESEND_API|PAYPAL_CLIENT_SECRET|LINKEDIN_CLIENT_SECRET|OPENROUTER_API_KEY|GEMINI_API_KEY|INTERNAL_API_SECRET)" /tmp/tstr-live-audit
```

Expected result:

- No high-risk secret patterns in public HTML.
- Supabase publishable/anon keys may still appear and are not service-role secrets.

## Phase 5: Rotate Credentials

Because a partial Supabase secret value was publicly disclosed, rotate affected credentials.

Minimum rotations:

- Supabase service-role key.
- Resend API key that is hardcoded in tracked source.

Recommended review/rotation:

- LinkedIn client secret, because production confirms its presence through a public debug endpoint.
- Any Cloudflare Pages runtime secret that appeared in `debug-env`.

Systems Thinking checklist:

- Supabase dashboard: rotate service-role key.
- Cloudflare Pages env vars: update `SUPABASE_SERVICE_ROLE_KEY` and any rotated secrets.
- Local `.env` files: update only if required for local development.
- GitHub Actions secrets: update if deployment or CI uses the same secrets.
- OCI/runtime scraper env vars: update if any service-role key is mirrored there.
- Supabase Edge Functions secrets: update if they use the same key.

Do not commit `.env` files or secret values.

## Phase 6: Auth Review for Service-Role Routes

Audit all routes using `SUPABASE_SERVICE_ROLE_KEY`:

```bash
rg -n "SUPABASE_SERVICE_ROLE_KEY|SERVICE_KEY|supabaseServiceKey" web/tstr-frontend/src/pages/api
```

Each matching route must have one of:

- Strong user authentication and authorization.
- Internal-only bearer secret verification.
- Migration to anon key plus RLS where possible.
- Removal if obsolete.

Special attention:

- `web/tstr-frontend/src/pages/api/ai-search.ts`
- `web/tstr-frontend/src/pages/api/admin/*.ts`
- `web/tstr-frontend/src/pages/api/outreach-email.ts`
- `web/tstr-frontend/src/pages/api/submit.ts`
- `web/tstr-frontend/src/pages/api/claim_submission.ts`
- `web/tstr-frontend/src/pages/api/claim-status.ts`
- `web/tstr-frontend/src/pages/api/subscription/pending/*.ts`

## Phase 7: Documentation and Commit

After successful remediation:

1. Update `PROJECT_STATUS.md` with:
   - Date/time.
   - Agent attribution.
   - Summary of removed debug routes.
   - Credential rotations completed or still pending.
   - Live verification results.

2. Commit using project format:

   ```bash
   git add web/tstr-frontend PROJECT_STATUS.md docs/active/LIVE_CREDENTIAL_EXPOSURE_REMEDIATION_PLAN.md
   git commit -m "[AGENTNAME] Remove live debug credential exposure"
   ```

3. Push only after verification passes.

## Acceptance Criteria

- `https://tstr.directory/api/debug-env` no longer exposes runtime env metadata.
- `https://tstr.directory/api/debug-full` no longer exposes any key prefix or secret metadata.
- No hardcoded Resend key remains in tracked frontend files.
- Public HTML and downloaded Astro bundles contain no high-risk secret patterns.
- Supabase service-role key has been rotated and updated in all required runtimes.
- Resend API key has been rotated and updated in the correct server-side runtime only.
- `PROJECT_STATUS.md` reflects the final production truth.
