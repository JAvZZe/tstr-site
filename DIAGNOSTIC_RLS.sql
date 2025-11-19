-- =====================================================
-- RLS DIAGNOSTIC & FIX
-- =====================================================

-- STEP 1: Check what policies exist on listings
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE tablename = 'listings'
ORDER BY cmd, roles;

-- STEP 2: Check if categories/locations have RLS blocking reads
SELECT
  schemaname,
  tablename,
  policyname,
  roles,
  cmd
FROM pg_policies
WHERE tablename IN ('categories', 'locations')
ORDER BY tablename, cmd;

-- STEP 3: Check RLS status on all three tables
SELECT
  schemaname,
  tablename,
  rowsecurity
FROM pg_tables
WHERE tablename IN ('listings', 'categories', 'locations');
