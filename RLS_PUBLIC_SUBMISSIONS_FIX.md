# RLS Policy Fix: Public Form Submissions

## Problem

Form submissions from `/submit` page were failing with:
```
new row violates row-level security policy for table 'listings'
```

**Root Cause**: RLS (Row-Level Security) was enabled on the `listings` table, but there was no INSERT policy allowing anonymous users to submit listings.

## Solution

Applied RLS policy that allows:
- **Anonymous users** (anon role) to INSERT with constraints
- **Authenticated users** to INSERT with same constraints
- Only listings with: `status='pending'`, `verified=false`, `claimed=false`

## Files Created/Modified

### 1. Migration File
**Location**: `/web/tstr-automation/supabase/migrations/20251118000001_fix_rls_public_submissions.sql`

```sql
-- Create policy for anonymous submissions
CREATE POLICY "Allow public submissions to pending listings"
  ON public.listings
  FOR INSERT
  TO anon
  WITH CHECK (
    status = 'pending'
    AND verified = false
    AND claimed = false
  );

-- Create policy for authenticated submissions
CREATE POLICY "Allow authenticated submissions to pending listings"
  ON public.listings
  FOR INSERT
  TO authenticated
  WITH CHECK (
    status = 'pending'
    AND verified = false
    AND claimed = false
  );
```

### 2. Existing Policy Files

These files existed but may not have been applied:
- `/web/tstr-automation/migrations/allow_public_submissions.sql`
- `/web/tstr-automation/migrations/fix_public_submissions_rls.sql`

The new migration consolidates and properly applies the policy.

## How to Apply the Migration

### Option 1: Via Supabase CLI (Recommended)

```bash
cd /home/al/AI\ PROJECTS\ SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-automation
supabase db push --linked
```

This will:
1. Connect to the linked Supabase project
2. Apply the migration
3. Verify the policy is created

### Option 2: Via Supabase Dashboard

1. Go to https://supabase.io/ → your project → SQL Editor
2. Copy contents of migration file
3. Execute the SQL
4. Verify with:
   ```sql
   SELECT policyname, roles, cmd FROM pg_policies
   WHERE tablename = 'listings' AND cmd = 'INSERT'
   ORDER BY policyname;
   ```

### Option 3: Direct PostgreSQL (if CLI not available)

```sql
-- Copy entire migration file and execute
```

## Verification

### Check Policies Are Applied

```sql
SELECT policyname, roles, cmd, qual FROM pg_policies
WHERE tablename = 'listings'
ORDER BY policyname;
```

Should show:
```
policyname                                    | roles          | cmd    | qual
----------------------------------------------+----------------+--------+------
Allow authenticated submissions to pending... | {authenticated}| INSERT | ...
Allow public submissions to pending listings  | {anon}         | INSERT | ...
```

### Test Form Submission

1. Go to http://tstr.site/submit
2. Fill out the form with test data:
   - Company Name: "Test Company"
   - Category: "Environmental Testing"
   - Website: "https://example.com"
   - Email: "test@example.com"
   - Address: "Test City, Test Country"
   - Description: Optional

3. Click "Submit Listing"
4. Should see: "✓ Thank you! Your listing has been submitted successfully."
5. Listing will appear in database with `status='pending'`

### Automated Test

Browser console on `/submit` page:
```javascript
// Copy contents of test_submit.js and run
```

## Policy Details

### What the Policy Allows
- Anonymous/public users can INSERT new listings
- Only if the INSERT data includes: `status='pending'`, `verified=false`, `claimed=false`
- Prevents bypassing the review workflow

### What the Policy Blocks
- Inserting listings with `status='active'` or other values
- Setting `verified=true` or `claimed=true` on insert
- Anonymous users cannot UPDATE or DELETE
- Anonymous users cannot read listings (controlled by separate SELECT policy)

### Design Rationale
1. **Pending status**: New submissions go to pending queue for review
2. **Unverified flag**: Marks submissions not yet validated
3. **Unclaimed flag**: Marks submissions not yet claimed by owner
4. **No SELECT policy**: Public can't read listings via this role (handled separately)

## Related Policies

The listings table may have additional RLS policies for:
- **Authenticated users**: Claiming and updating their own listings
- **Service role**: Admin operations (via build process)
- **Public READ**: Reading active/verified listings

Verify complete policy set with:
```sql
SELECT policyname, roles, cmd FROM pg_policies
WHERE tablename = 'listings'
ORDER BY policyname, cmd;
```

## Troubleshooting

### Still Getting "violates row-level security"?

1. **Check policy is applied**:
   ```sql
   SELECT * FROM pg_policies WHERE tablename = 'listings';
   ```

2. **If empty**, migration hasn't run yet:
   ```bash
   # Using CLI
   supabase db push --linked

   # Or manually execute migration SQL
   ```

3. **Check form data**:
   - Form must submit: `status='pending'`, `verified=false`, `claimed=false`
   - Check browser console for exact data being sent

4. **Check RLS enabled**:
   ```sql
   SELECT relname, relrowsecurity FROM pg_class WHERE relname = 'listings';
   -- Should show: listings | t (true)
   ```

### Policy has different name?

Multiple policy creation attempts may have left old policies. Clean up:
```sql
DROP POLICY IF EXISTS "Allow public submissions" ON public.listings;
DROP POLICY IF EXISTS "Allow anonymous submissions" ON public.listings;
DROP POLICY IF EXISTS "Allow public insert" ON public.listings;
-- Then reapply the migration
```

## Deployment Status

- Migration created: 2025-11-18
- Files committed: ✓
- Ready to deploy: ✓ (awaiting `supabase db push`)

## Next Steps

1. Apply migration: `supabase db push --linked`
2. Test form submission at http://tstr.site/submit
3. Verify listing appears in database with `status='pending'`
4. Check admin dashboard for pending approvals

---

**Created**: 2025-11-18
**Status**: Ready to deploy
**Risk**: Low (only enables existing functionality)
**Impact**: Public form submissions will now work correctly
