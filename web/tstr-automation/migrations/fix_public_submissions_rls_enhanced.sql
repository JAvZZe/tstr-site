-- =====================================================
-- ENHANCEMENT: Explicit RLS Conditions for Submissions
-- =====================================================
-- This clarifies the three conditions for public submissions:
-- 1. status = 'pending' - unreviewed
-- 2. verified = false - not verified by admin
-- 3. claimed = false - not claimed by business owner
--
-- The form at /submit always sends all three conditions,
-- so this change is non-breaking and adds clarity.

-- Step 1: Drop the old policy (more permissive version)
DROP POLICY IF EXISTS "Allow public submissions to pending listings" ON listings;

-- Step 2: Create explicit, comprehensive policy for anonymous users
CREATE POLICY "Allow public submissions to pending listings"
  ON listings
  FOR INSERT
  TO anon
  WITH CHECK (
    status = 'pending'
    AND verified = false
    AND claimed = false
  );

-- Step 3: Also allow authenticated users to submit (but not bypass pending status)
CREATE POLICY IF NOT EXISTS "Allow authenticated submissions"
  ON listings
  FOR INSERT
  TO authenticated
  WITH CHECK (status = 'pending');

-- Step 4: Ensure RLS is enabled
ALTER TABLE listings ENABLE ROW LEVEL SECURITY;

-- Step 5: Verify the policies (run separately in Supabase SQL editor)
-- SELECT policyname, roles, cmd, qual, with_check
-- FROM pg_policies
-- WHERE tablename = 'listings' AND cmd = 'INSERT'
-- ORDER BY policyname;
-- Expected output:
--   policyname: "Allow authenticated submissions"
--   roles: {authenticated}
--   cmd: INSERT
--   qual: (empty)
--   with_check: (status = 'pending'::text)
--
--   policyname: "Allow public submissions to pending listings"
--   roles: {anon}
--   cmd: INSERT
--   qual: (empty)
--   with_check: ((status = 'pending'::text) AND (verified = false) AND (claimed = false))

-- Step 6: Test INSERT with anon role (from Supabase SQL editor with role: anon)
-- INSERT INTO listings (
--   business_name, slug, category_id, location_id,
--   status, verified, claimed
-- ) VALUES (
--   'Test Company', 'test-slug', '<valid-uuid>', '<valid-uuid>',
--   'pending', false, false
-- )
-- RETURNING id;

-- Step 7: Verify data was inserted
-- SELECT business_name, status, verified, claimed
-- FROM listings
-- WHERE business_name = 'Test Company';
