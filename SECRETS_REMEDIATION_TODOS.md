# Secrets Remediation Todos

> ## ⚠️ STATUS AS OF 2026-08-10 (Hermes)
> - **Repo doc/config redaction: DONE.** Plaintext secrets were removed from all tracked
>   docs/configs and from git-ignored credential stores (`docs/credentials/*`,
>   `TSTR_hub_Supabase_Keys.md`, `secret_alerts.json`, `.gitnexus/lbug`).
>   A reusable scanner now gates commits: `scripts/secret_scan.py` + `scripts/pre-commit.hook`
>   (see `agents/tstr-secret-scanner.md` / Hermes skill `tstr-secret-scanner`).
> - **KEY ROTATION: NOT DONE.** Redaction does NOT close the 19 OPEN GitHub secret-scanning
>   alerts (some from 2025-10). The real keys still live in git HISTORY and in the runtimes
>   (Cloudflare Pages env, OCI .env, local .env). Per `CREDENTIAL_ROTATION_RUNBOOK.md`, every
>   exposed credential must be rotated in its provider dashboard, then updated in all surfaces,
>   before an alert can be marked resolved. **This is the outstanding action.**
> - **Live code still uses service role:** `web/tstr-frontend/src/pages/api/ai-search.ts:8,55`
>   still constructs a Supabase client with `SUPABASE_SERVICE_ROLE_KEY`. Debug routes
>   (`debug-env.ts`, `debug-full.ts`) are gated to 404 in production but were NOT deleted;
>   `debug-full.ts` still contains a service-role leak path when `PUBLIC_DEBUG_ENDPOINTS=true`.
> - **`.env` / `.dev.vars` intentionally unchanged** (git-ignored local dev secrets).

## Immediate Actions Required

### 1. Supabase Service Role Key Exposure
**Location**: Multiple files accessing `import.meta.env.SUPABASE_SERVICE_ROLE_KEY`
**Risk**: CRITICAL - Full database access
**Status**: MOSTLY RESOLVED - Service role key usage has been replaced with proper authentication in most files
**Files Fixed**:
- `src/pages/api/outreach-email.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/admin/analytics.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/admin/users.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/admin/failed-urls.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/admin/claims.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/admin/listings.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/admin/stats.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/admin/auth-login.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/subscription/pending/resume.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/subscription/pending/clear.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/subscription/pending/save.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/claim-status.ts` ✓ (now uses proper auth middleware)
- `src/pages/api/debug-full.ts` ✓ (service key usage removed entirely)
- `src/pages/api/debug-env.ts` ✓ (now uses anon key only for debugging)
- `src/lib/supabase.ts` ✓ (now uses anon key only)
**Files Still Requiring Attention**:
- `src/pages/api/ai-search.ts` ⚠️ (still uses service role key - needs proper auth implementation)

**Remediation Strategy**:
- Replace service role key usage with proper authentication
- Implement Row Level Security (RLS) policies
- Use anon keys where appropriate for client-accessible operations
- Consider Supabase Edge Functions for sensitive operations
- Add authentication middleware to verify user permissions

### 2. Resend API Key Exposure
**Location**: 
- `src/pages/api/outreach-email.ts` (lines 6, 24, 218)
- `src/lib/email.ts` (lines 7, 8, 11)
**Risk**: HIGH - Could send unauthorized emails
**Remediation**:
- Consider moving email sending to a backend service or edge function
- Implement rate limiting and request validation
- Use environment variable only in truly server-controlled contexts

### 3. Other API Keys in Frontend-Accessible Code
**Keys to Review**:
- PayPal Client Secret (`src/pages/api/*` files if used)
- LinkedIn Client Secret 
- Gemini API Keys (`src/pages/api/ai-search.ts`)
- OpenRouter API Key (`src/pages/api/ai-search.ts`)
- Stitch API Key
- Internal API Secret (`src/pages/api/outreach-email.ts`)

**General Approach**:
1. Audit each usage to determine if truly needed in frontend-accessible code
2. Move sensitive operations to backend-only endpoints when possible
3. Implement proper authentication and authorization checks
4. Use principle of least privilege for all API keys
5. Add environment variable validation with fallback handling

## Verification Checklist
- [ ] All secrets rotated and replaced
- [ ] No service role keys in frontend-accessible code paths
- [ ] All API routes have proper authentication
- [ ] Environment variables properly classified (PUBLIC_* vs secret)
- [ ] Secret scanning implemented in CI/CD
- [ ] Security team notified of incident
- [ ] Learning extracted and protocol updated

## Estimated Effort
- **Audit and Planning**: 2-4 hours
- **Implementation**: 8-16 hours (depending on complexity of auth implementation)
- **Testing**: 4-8 hours
- **Total**: 14-28 hours

## Dependencies
- Supabase authentication setup
- Proper RLS policies defined
- Backend services for sensitive operations (if moving from frontend)