# Security Checklist for TSTR.site

## Environment Variables Protection

### ✅ Completed
- [x] `.env` is in `.gitignore`
- [x] `.env.production` is in `.gitignore`
- [x] Created `.env.example` for documentation
- [x] Service keys only accessed via `import.meta.env` or `process.env`
- [x] Verified no hardcoded secrets in source code

### Critical Keys to Protect

**Never commit these:**
1. `SUPABASE_SERVICE_ROLE_KEY` - Full database access (in `.env` only)
2. Database passwords
3. API keys with write access
4. OAuth client secrets

**Safe to commit:**
1. `PUBLIC_SUPABASE_URL` - Public API endpoint
2. `PUBLIC_SUPABASE_ANON_KEY` - Client-side access (RLS protected)
3. Public configuration values

## Pre-Commit Checklist

Before every `git commit`:

```bash
# 1. Check for exposed secrets
git diff --cached | grep -i "service_role\|password\|secret\|_key" 

# 2. Verify .env is ignored
git status | grep ".env" 
# Should show: nothing (no .env files)

# 3. Check .gitignore is working
git check-ignore .env
# Should show: .env
```

## API Endpoint Security

### Server-side Only (✅ Correct)
- `/api/submit.ts` uses `SUPABASE_SERVICE_ROLE_KEY`
- Runs server-side only (Astro API routes)
- Not accessible to browser JavaScript

### Client-side (✅ Correct)
- `LeadCapture.astro` only sends POST to `/api/submit`
- No direct Supabase access from client
- Anon key used for read-only operations (listings)

## Row Level Security (RLS)

### Waitlist Table Policies

✅ **INSERT**: Public (anyone can submit email)
```sql
CREATE POLICY "Anyone can submit to waitlist"
    ON waitlist FOR INSERT TO public
    WITH CHECK (true);
```

✅ **SELECT**: Authenticated users only (admins)
```sql
CREATE POLICY "Authenticated users can read waitlist"
    ON waitlist FOR SELECT TO authenticated
    USING (true);
```

✅ **UPDATE/DELETE**: Service role only
```sql
CREATE POLICY "Service role can manage waitlist"
    ON waitlist FOR ALL TO service_role
    USING (true) WITH CHECK (true);
```

## Deployment Security

### Netlify/Cloudflare Environment Variables

When deploying, set these via dashboard (NOT in code):

1. Go to: Site Settings → Environment Variables
2. Add:
   - `PUBLIC_SUPABASE_URL` (safe)
   - `PUBLIC_SUPABASE_ANON_KEY` (safe)
   - `SUPABASE_SERVICE_ROLE_KEY` (CRITICAL - keep secret)

### GitHub Actions

If using CI/CD:

```yaml
# ❌ NEVER DO THIS
env:
  SUPABASE_SERVICE_ROLE_KEY: eyJhbGci... # EXPOSED!

# ✅ CORRECT
env:
  SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
```

Add secrets at: Repository → Settings → Secrets and variables → Actions

## Incident Response

If service key is exposed:

1. **Immediately revoke** at Supabase dashboard
2. Generate new service role key
3. Update `.env` locally
4. Update deployment environment variables
5. Review git history for exposure
6. Force push cleaned history if needed (use `git filter-branch` or BFG Repo-Cleaner)

## Monitoring

Regular checks:

- [ ] Weekly: Review Supabase logs for suspicious activity
- [ ] Monthly: Rotate service role key
- [ ] Before each release: Run security checklist

## Additional Resources

- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth/row-level-security)
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Last Security Audit**: 2025-11-21
**Next Audit Due**: 2025-12-21
