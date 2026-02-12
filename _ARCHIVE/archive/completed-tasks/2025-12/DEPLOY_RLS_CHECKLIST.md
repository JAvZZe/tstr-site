# RLS Policy Deployment Checklist

## Pre-Deployment

- [ ] Read `APPLY_RLS_POLICY_INSTRUCTIONS.md` for overview
- [ ] Review `RLS_PUBLIC_SUBMISSIONS_FIX.md` for technical details
- [ ] Backup current database (optional, changes are reversible)
- [ ] Have Supabase database password ready

## Deployment

### Option A: Supabase CLI
- [ ] Navigate to project root: `cd /home/al/.../TSTR-site/tstr-site-working`
- [ ] Link project: `supabase link`
- [ ] Push migrations: `supabase db push --linked`
- [ ] Check output for "✓ Deployment successful" or similar

### Option B: Python Script
- [ ] Navigate to automation directory: `cd web/tstr-automation`
- [ ] Run script: `python3 execute_public_submissions_rls.py`
- [ ] Enter database password when prompted
- [ ] Check for "✓ SUCCESS" in output

### Option C: Dashboard
- [ ] Open https://app.supabase.io/
- [ ] Select TSTR.site project
- [ ] Navigate to SQL Editor
- [ ] Create new query
- [ ] Copy entire SQL from migration file
- [ ] Execute query
- [ ] Wait for "Success" response

## Verification

- [ ] Run verification query in SQL Editor:
  ```sql
  SELECT policyname, roles, cmd FROM pg_policies
  WHERE tablename = 'listings' AND cmd = 'INSERT'
  ORDER BY policyname;
  ```
- [ ] Confirm two policies listed:
  - [ ] "Allow authenticated submissions to pending listings"
  - [ ] "Allow public submissions to pending listings"

## Testing

- [ ] Open http://tstr.site/submit
- [ ] Fill form with test data:
  - [ ] Company Name: "Test Company [date]"
  - [ ] Category: "Environmental Testing"
  - [ ] Website: "https://example.com"
  - [ ] Email: "test@example.com"
  - [ ] Address: "Test City, Test Country"
  - [ ] Description: "Test submission"
- [ ] Click "Submit Listing"
- [ ] Verify: See success message
- [ ] Check database:
  ```sql
  SELECT id, business_name, status, verified, claimed, created_at
  FROM listings
  ORDER BY created_at DESC
  LIMIT 1;
  ```
- [ ] Confirm new listing has:
  - [ ] `status = 'pending'`
  - [ ] `verified = false`
  - [ ] `claimed = false`

## Post-Deployment

- [ ] Clear browser cache (Ctrl+Shift+Del)
- [ ] Test form again with different browser/device
- [ ] Monitor for any error reports
- [ ] Commit files to git:
  ```bash
  git add APPLY_RLS_POLICY_INSTRUCTIONS.md \
          RLS_PUBLIC_SUBMISSIONS_FIX.md \
          apply_rls_policy.py \
          test_submit.js \
          web/tstr-automation/execute_public_submissions_rls.py \
          web/tstr-automation/supabase/migrations/20251118000001_fix_rls_public_submissions.sql
  git commit -m "Fix RLS policy blocking public form submissions"
  ```
- [ ] Push to repository: `git push`

## Rollback (If Needed)

If something goes wrong:

```sql
-- Remove the policy (reverses the change)
DROP POLICY IF EXISTS "Allow public submissions to pending listings" ON public.listings;
DROP POLICY IF EXISTS "Allow authenticated submissions to pending listings" ON public.listings;

-- Verify removal
SELECT * FROM pg_policies WHERE tablename = 'listings';
```

Then troubleshoot and reapply.

## Success Indicators

- [ ] No RLS errors when submitting form
- [ ] Test listings created with status='pending'
- [ ] Both INSERT policies exist in database
- [ ] Form works from multiple browsers/devices
- [ ] Admin dashboard shows pending submissions

## Troubleshooting

If verification fails:

1. **Policies not found?**
   - Rerun the migration/SQL
   - Check database connection
   - Verify Supabase project selected

2. **Form still fails?**
   - Clear browser cache
   - Check browser console for errors
   - Verify form submits all required fields

3. **Can't connect to database?**
   - Check password is correct
   - Verify database is running
   - Check network connectivity

See `RLS_PUBLIC_SUBMISSIONS_FIX.md` for detailed troubleshooting.

## Sign-Off

- [ ] Deployment completed by: ________________
- [ ] Date: ________________
- [ ] Verified working: ________________
- [ ] Files committed: ________________
- [ ] Status: READY FOR PRODUCTION

---

**Duration**: ~5-10 minutes
**Difficulty**: Low
**Risk**: Very Low (reversible)
**Impact**: Public form submissions enabled

