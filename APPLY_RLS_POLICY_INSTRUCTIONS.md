# Apply RLS Policy for Public Form Submissions

## Quick Summary

The `/submit` form is failing with "row-level security policy violation" because the database doesn't have a policy allowing anonymous users to INSERT listings.

## Files Created

1. **Migration File**:
   - `/web/tstr-automation/supabase/migrations/20251118000001_fix_rls_public_submissions.sql`
   - Contains the RLS policy definition

2. **Application Scripts**:
   - `/web/tstr-automation/execute_public_submissions_rls.py` - Executes the migration
   - `/apply_rls_policy.py` - Alternative Python approach
   - `test_submit.js` - Browser test for form submission

3. **Documentation**:
   - `RLS_PUBLIC_SUBMISSIONS_FIX.md` - Full technical details
   - `APPLY_RLS_POLICY_INSTRUCTIONS.md` - This file

## How to Apply (Choose One Method)

### Method 1: Using Supabase CLI (Easiest)

```bash
cd /home/al/AI\ PROJECTS\ SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working

# Link the project to your Supabase account
supabase link

# Push migrations to production
supabase db push --linked
```

### Method 2: Using Python Script

```bash
cd /home/al/AI\ PROJECTS\ SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-automation

python3 execute_public_submissions_rls.py
# When prompted, enter your Supabase database password
```

**Note**: Requires `psql` command-line tool (usually installed with PostgreSQL).

### Method 3: Manual via Supabase Dashboard (Slowest)

1. Go to https://app.supabase.io/
2. Select your TSTR.site project
3. Click "SQL Editor" in the left sidebar
4. Click "New query"
5. Copy the entire SQL from: `/web/tstr-automation/supabase/migrations/20251118000001_fix_rls_public_submissions.sql`
6. Paste it in the editor
7. Click "Run"
8. Verify with this query:
   ```sql
   SELECT policyname, roles, cmd FROM pg_policies
   WHERE tablename = 'listings' AND cmd = 'INSERT'
   ORDER BY policyname;
   ```

## Verification

After applying, verify the policy works:

### 1. Check Database Policy
```sql
-- Run in Supabase SQL Editor
SELECT policyname, roles, cmd FROM pg_policies
WHERE tablename = 'listings' AND cmd = 'INSERT'
ORDER BY policyname;
```

Should show two rows:
- `Allow authenticated submissions to pending listings`
- `Allow public submissions to pending listings`

### 2. Test Form Submission

1. Go to http://tstr.site/submit
2. Fill in the form (any valid data)
3. Click "Submit Listing"
4. Should see success message: "✓ Thank you! Your listing has been submitted successfully."

### 3. Verify in Database

```sql
-- Check that listing was created
SELECT id, business_name, status, verified, claimed, created_at
FROM listings
ORDER BY created_at DESC
LIMIT 5;
```

New listings should have:
- `status = 'pending'`
- `verified = false`
- `claimed = false`

## What the Policy Does

```sql
CREATE POLICY "Allow public submissions to pending listings"
  ON public.listings
  FOR INSERT
  TO anon
  WITH CHECK (
    status = 'pending'
    AND verified = false
    AND claimed = false
  );
```

This policy:
- **Allows**: Anonymous users (unauthenticated visitors) to insert rows
- **Into**: The `listings` table
- **Only if**: The row has `status='pending'`, `verified=false`, `claimed=false`
- **Effect**: Ensures form submissions are always marked as pending review

## Troubleshooting

### Problem: "psql: command not found"

**Solution**: Install PostgreSQL client tools
```bash
sudo apt install postgresql-client
```

Then retry: `python3 execute_public_submissions_rls.py`

### Problem: "password authentication failed"

**Solution**: Verify password
1. Go to https://app.supabase.io/
2. Select your project
3. Click "Settings" → "Database"
4. Copy the password
5. Use it in the script

### Problem: "relation 'listings' does not exist"

**Solution**: Ensure you're using the correct database name
- Check: `SELECT table_name FROM information_schema.tables;`
- Verify the table exists before running the script

### Problem: Still getting RLS violation after applying policy?

1. **Clear browser cache**: Supabase client may be cached
2. **Verify policy applied**: Re-run the verification SQL above
3. **Check form data**: Form must submit all three fields as true:
   - `status = 'pending'`
   - `verified = false`
   - `claimed = false`

## Technical Details

See `RLS_PUBLIC_SUBMISSIONS_FIX.md` for:
- Root cause analysis
- Policy design rationale
- Related RLS policies
- Advanced troubleshooting

## Timeline

- **Issue Found**: 2025-11-18
- **Migration Created**: 2025-11-18
- **Status**: Ready to deploy
- **Risk**: Low (enables existing functionality)
- **Impact**: Public form submissions will work

---

**Questions?** Check `RLS_PUBLIC_SUBMISSIONS_FIX.md` for detailed documentation.
