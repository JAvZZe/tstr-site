-- =====================================================
-- FIX: Allow Anonymous Submissions to Listings Table
-- =====================================================
-- Root Cause: RLS enabled but no INSERT policy for anon role
-- Solution: Create policy allowing anon to INSERT with status='pending'
-- Date: 2025-11-18

-- Drop any existing policies that might conflict
DROP POLICY IF EXISTS "Allow public submissions to pending listings" ON public.listings;
DROP POLICY IF EXISTS "Allow authenticated submissions to pending listings" ON public.listings;

-- Create policy for anonymous users to submit listings
-- Anonymous users can only create listings with:
--   - status = 'pending' (they are unverified)
--   - verified = false (not yet verified)
--   - claimed = false (not yet claimed by owner)
CREATE POLICY "Allow public submissions to pending listings"
  ON public.listings
  FOR INSERT
  TO anon
  WITH CHECK (
    status = 'pending'
    AND verified = false
    AND claimed = false
  );

-- Create policy for authenticated users to submit listings
-- Same constraints as anonymous for consistency
CREATE POLICY "Allow authenticated submissions to pending listings"
  ON public.listings
  FOR INSERT
  TO authenticated
  WITH CHECK (
    status = 'pending'
    AND verified = false
    AND claimed = false
  );

-- Ensure RLS is enabled on listings table
ALTER TABLE public.listings ENABLE ROW LEVEL SECURITY;

-- Ensure status column has correct default
ALTER TABLE public.listings
  ALTER COLUMN status SET DEFAULT 'pending';

-- Verification query (view current state):
-- SELECT policyname, roles, cmd, qual FROM pg_policies
-- WHERE tablename = 'listings' AND cmd = 'INSERT'
-- ORDER BY policyname;
