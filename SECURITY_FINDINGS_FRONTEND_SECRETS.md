# Security Findings: Frontend Secrets Exposure

## Overview
During a security review of the TSTR.directory frontend codebase, multiple credentials and secrets were discovered that pose varying levels of risk to the application's security.

## Findings Summary

### CRITICAL RISK
1. **Supabase Service Role Key**
   - **Value**: `[REDACTED — ROTATE THIS SUPABASE SERVICE-ROLE KEY; see SECURITY_FINDINGS]`
   - **Location**: `.env` file
   - **Usage Pattern**: Accessed via `import.meta.env.SUPABASE_SERVICE_ROLE_KEY` in multiple API routes
   - **Risk Level**: CRITICAL
   - **Impact**: This key provides FULL database access (bypasses Row Level Security). If compromised, attackers could:
     - Read all data in the database
     - Modify or delete any records
     - Potentially gain administrative access to Supabase project
   - **Files Originally Using This Key**:
     - `src/pages/api/outreach-email.ts` (FIXED - now uses proper auth)
     - `src/pages/api/admin/analytics.ts` (FIXED - now uses proper auth)
     - `src/pages/api/admin/users.ts` (FIXED - now uses proper auth)
     - `src/pages/api/admin/failed-urls.ts` (FIXED - now uses proper auth)
     - `src/pages/api/admin/claims.ts` (FIXED - now uses proper auth)
     - `src/pages/api/admin/listings.ts` (FIXED - now uses proper auth)
     - `src/pages/api/admin/stats.ts` (FIXED - now uses proper auth)
     - `src/pages/api/admin/auth-login.ts` (FIXED - now uses proper auth)
     - `src/pages/api/subscription/pending/*.ts` (resume, clear, save) (FIXED - now uses proper auth)
     - `src/pages/api/claim-status.ts` (FIXED - now uses proper auth)
     - `src/pages/api/debug-full.ts` (REMOVED - service key usage eliminated)
     - `src/pages/api/debug-env.ts` (FIXED - now uses anon key only for debugging)
     - `src/pages/api/ai-search.ts` (REQUIRES ATTENTION - still uses service key)
     - `src/lib/supabase.ts` (FIXED - now uses anon key only)

### HIGH RISK
2. **Resend API Key**
   - **Value**: `[REDACTED — rotate in Resend dashboard]`
   - **Location**: `.env` file
   - **Usage**: `src/pages/api/outreach-email.ts` and `src/lib/email.ts`
   - **Risk Level**: HIGH
   - **Impact**: Could allow sending unauthorized emails, potentially leading to:
     - Spam distribution from trusted domain
     - Email sending quota exhaustion
     - Reputation damage

3. **Internal API Secret**
   - **Usage**: Authentication check in `src/pages/api/outreach-email.ts` (lines 16-22)
   - **Risk Level**: HIGH
   - **Impact**: If bypassed, could allow unauthorized access to email sending functionality

### MEDIUM RISK
4. **PayPal Configuration**
   - **Client ID**: `[REDACTED — rotate in PayPal dashboard]`
   - **Client Secret**: `[REDACTED — rotate in PayPal dashboard]`
   - **Location**: `.env` file
   - **Risk Level**: MEDIUM-HIGH
   - **Impact**: Could allow creation of unauthorized PayPal transactions or refunds

5. **LinkedIn OAuth Secret**
   - **Client Secret**: `[REDACTED — rotate in LinkedIn dashboard]`
   - **Location**: `.env` file
   - **Risk Level**: MEDIUM
   - **Impact**: Could allow unauthorized LinkedIn API access on behalf of the application

6. **AI Service API Keys**
   - **Gemini API Key**: `[REDACTED — rotate Gemini key]`
   - **Gemini API Key Alt**: `[REDACTED — rotate Gemini key]`
   - **OpenRouter API Key**: `[REDACTED — rotate OpenRouter key]`
   - **Location**: `.env` file
   - **Usage**: `src/pages/api/ai-search.ts`
   - **Risk Level**: MEDIUM
   - **Impact**: Could lead to:
     - API quota exhaustion and associated costs
     - Potential for AI service abuse
     - Rate limiting affecting legitimate users

7. **Stitch API Key**
   - **Value**: `[REDACTED — rotate in Stitch dashboard]`
   - **Location**: `.env` file
   - **Risk Level**: MEDIUM
   - **Impact**: Unauthorized access to Stitch services

## Root Cause Analysis

This security issue likely occurred due to:

1. **Misunderstanding of Environment Variable Scope**: Developers may have assumed that `import.meta.env` variables in Astro are only available at build time and not exposed to the client, when in fact they are embedded in the built serverless functions.

2. **Lack of Environment Separation**: Using the same `.env` file for both truly public variables (like `PUBLIC_SUPABASE_URL`) and highly sensitive secrets.

3. **Insufficient Code Review Process**: The presence of the service role key in multiple files suggests it was not caught during code review.

4. **Convenience Over Security**: Using the service role key was likely easier than implementing proper authentication and Row Level Security (RLS) policies.

5. **Missing Security Checklist**: No automated checks were in place to prevent committing secrets to the repository.

## Immediate Remediation Steps Taken

1. **Documentation**: Created this security findings document
2. **Learning Extraction**: Added this finding to the organizational learning system
3. **Protocol Updates**: Will implement checks to prevent recurrence
4. **Technical Remediation**: 
   - Replaced Supabase service role key usage with proper authentication middleware in most API routes
   - Updated `src/lib/supabase.ts` to use anon key only (secure for frontend)
   - Removed service key usage entirely from debug endpoints
   - Implemented proper auth verification in subscription, claim-status, outreach-email, and admin endpoints
   - **Still Pending**: `src/pages/api/ai-search.ts` requires proper authentication implementation (still uses service role key)

## Required Actions

### SHORT TERM (Immediate)
1. [ ] **Rotate all exposed secrets** immediately:
   - Supabase Service Role Key
   - Resend API Key
   - PayPal Client Secret
   - LinkedIn Client Secret
   - Gemini API Keys
   - OpenRouter API Key
   - Stitch API Key
   - Internal API Secret

2. [ ] **Replace Supabase Service Role Key usage** with:
   - Proper authentication middleware in API routes
   - Use of anon keys where appropriate
   - Implementation of Row Level Security (RLS) policies
   - Consideration of Supabase Edge Functions for sensitive operations

3. [ ] **Implement proper secret management**:
   - Separate `.env` files for different environments
   - Use of secret management services or encrypted storage
   - Ensure `.env` is in `.gitignore`

### MEDIUM TERM (Within 1 week)
1. [ ] **Audit all API routes** for proper authentication and authorization
2. [ ] **Implement input validation** on all API endpoints
3. [ ] **Add rate limiting** to prevent abuse
4. [ ] **Create security checklist** for pull requests

### LONG TERM (Ongoing)
1. [ ] **Automated secret scanning** in CI/CD pipeline
2. [ ] **Regular security audits** of the codebase
3. [ ] **Security training** for development team
4. [ ] **Principle of least privilege** implementation for all API keys

## Lessons Learned & Prevention Protocols

### Why This Could Have Occurred
1. **Assumption of Safety**: Assuming that API routes are inherently secure without implementing proper authentication
2. **Development Convenience**: Using service role key for quick development bypassing proper auth implementation
3. **Lack of Environment Awareness**: Not understanding that `import.meta.env` values are bundled with the code
4. **Insufficient Peer Review**: Missing during code review process
5. **No Automated Checks**: Lack of pre-commit hooks or CI checks for secrets

### Prevention Protocols to Implement
1. **Mandatory Pre-commit Checks**:
   ```bash
   # Add to .husky/pre-commit
   npx git-secrets --scan
   ```

2. **Environment Variable Classification**:
   - Create `.env.public` for truly public variables (prefixed with `PUBLIC_`)
   - Keep `.env.secret` for server-only secrets (never commit)
   - Document which variables are safe for client exposure

3. **Code Review Checklist Additions**:
   - [ ] No service role keys in frontend-accessible code
   - [ ] All API routes have proper authentication
   - [ ] Environment variables are properly classified
   - [ ] Secrets are not logged or exposed in error messages

4. **Learning System Integration**:
   - This finding has been added to the organizational learning database
   - Tagged with: `security`, `secrets-exposure`, `supabase`, `frontend-security`
   - Confidence level: 5 (high confidence in accuracy)

5. **Automated Detection**:
   - Implement regular scans for patterns like:
     - `<redacted-supabase-prefix>`
     - `<redacted-openrouter-prefix>` (OpenRouter)
     - `<redacted-resend-prefix>` (Resend)
     - `<redacted-linkedin-prefix>` (LinkedIn)
     - `<redacted-paypal-prefix>` (PayPal patterns)

## Verification Steps
After implementing fixes, verify:
1. All API routes require proper authentication
2. No secrets are exposed in client-side bundles
3. Supabase usage follows principle of least privilege
4. Environment variables are properly separated
5. Secret rotation has been completed for all exposed values

## References
- Supabase Documentation: [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)
- Astro Documentation: [Environment Variables](https://docs.astro.build/en/guides/environment-variables/)
- OWASP Secrets Management Cheat Sheet