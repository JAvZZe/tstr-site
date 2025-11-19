-- =====================================================
-- FIX: Allow Anonymous Submissions to Listings Table
-- =====================================================
-- Root Cause: RLS enabled but no INSERT policy for anon role
-- Solution: Create policy allowing anon to INSERT with status='pending'

-- Step 1: Check current state (for debugging)
-- View all existing policies on listings table:
-- SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
-- FROM pg_policies WHERE tablename = 'listings';

-- Step 2: Drop any existing policies that might conflict
DROP POLICY IF EXISTS "Allow public submissions to pending listings" ON listings;
DROP POLICY IF EXISTS "Allow anonymous submissions" ON listings;
DROP POLICY IF EXISTS "Allow public insert" ON listings;

-- Step 3: Create the correct policy
-- Allow anonymous users to INSERT listings ONLY with status='pending'
CREATE POLICY "Allow public submissions to pending listings"
  ON listings
  FOR INSERT
  TO anon
  WITH CHECK (status = 'pending');

-- Step 4: Also allow authenticated users to submit
CREATE POLICY IF NOT EXISTS "Allow authenticated submissions to pending listings"
  ON listings
  FOR INSERT
  TO authenticated
  WITH CHECK (status = 'pending');

-- Step 5: Ensure status column has correct default
ALTER TABLE listings
  ALTER COLUMN status SET DEFAULT 'pending';

-- Step 6: Ensure RLS is enabled (should already be)
ALTER TABLE listings ENABLE ROW LEVEL SECURITY;

-- Verification query (run separately to check):
-- SELECT policyname, roles, cmd, qual FROM pg_policies WHERE tablename = 'listings' AND cmd = 'INSERT';

-- Expected output: Should show two INSERT policies for 'anon' and 'authenticated' roles
