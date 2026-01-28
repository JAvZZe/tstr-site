-- ============================================
-- tstr.directory Database Setup - STEP 6: CATEGORY RLS POLICY
-- ============================================
-- This policy allows public, anonymous access to view all categories.

-- 1. Enable Row Level Security (RLS) on the 'categories' table
ALTER TABLE public.categories ENABLE ROW LEVEL SECURITY;

-- 2. Create a policy to allow public read access
-- This policy allows anyone (anon role) to SELECT from the categories table.
CREATE POLICY "Allow public read access to all categories"
ON public.categories
FOR SELECT
TO anon
USING (true);

-- ============================================
-- IMPORTANT: After running this script, your categories
-- should be visible on the public website.
-- ============================================
