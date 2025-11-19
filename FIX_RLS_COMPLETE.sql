-- =====================================================
-- COMPREHENSIVE RLS FIX FOR PUBLIC SUBMISSIONS
-- =====================================================
-- Root Cause Analysis:
-- When inserting a listing with category_id and location_id foreign keys,
-- Postgres must verify those IDs exist by doing a SELECT on those tables.
-- If RLS blocks anon from reading categories/locations, the INSERT fails.
--
-- Solution: Allow anon to read categories and locations

-- =====================================================
-- PART 1: Enable anon read access to categories
-- =====================================================

-- Ensure RLS is enabled on categories
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;

-- Drop existing policy if it exists
DROP POLICY IF EXISTS "Allow public read access to categories" ON categories;

-- Create policy to allow anyone to read categories
CREATE POLICY "Allow public read access to categories"
  ON categories
  FOR SELECT
  TO anon
  USING (true);

-- =====================================================
-- PART 2: Enable anon read access to locations
-- =====================================================

-- Ensure RLS is enabled on locations
ALTER TABLE locations ENABLE ROW LEVEL SECURITY;

-- Drop existing policy if it exists
DROP POLICY IF EXISTS "Allow public read access to locations" ON locations;
DROP POLICY IF EXISTS "Enable read access for all users" ON locations;

-- Create policy to allow anyone to read locations
CREATE POLICY "Allow public read access to locations"
  ON locations
  FOR SELECT
  TO anon
  USING (true);

-- =====================================================
-- PART 3: Enable anon insert access to listings
-- =====================================================

-- Drop any conflicting INSERT policies
DROP POLICY IF EXISTS "Allow public submissions to pending listings" ON listings;
DROP POLICY IF EXISTS "Allow anonymous submissions" ON listings;

-- Create policy for anonymous submissions
CREATE POLICY "Allow public submissions to pending listings"
  ON listings
  FOR INSERT
  TO anon
  WITH CHECK (status = 'pending');

-- Ensure RLS is enabled
ALTER TABLE listings ENABLE ROW LEVEL SECURITY;

-- Ensure status defaults to pending
ALTER TABLE listings ALTER COLUMN status SET DEFAULT 'pending';

-- =====================================================
-- VERIFICATION QUERIES (run separately to check)
-- =====================================================

-- Check categories policies:
-- SELECT policyname, roles, cmd FROM pg_policies WHERE tablename = 'categories';

-- Check locations policies:
-- SELECT policyname, roles, cmd FROM pg_policies WHERE tablename = 'locations';

-- Check listings INSERT policies:
-- SELECT policyname, roles, cmd, with_check FROM pg_policies WHERE tablename = 'listings' AND cmd = 'INSERT';
