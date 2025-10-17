-- ============================================
-- TSTR.site Database Setup - STEP 5: RLS POLICIES
-- ============================================
-- This policy allows public, anonymous access to view active listings.

-- 1. Enable Row Level Security (RLS) on the 'listings' table
-- This is usually enabled by default, but we make it explicit here.
ALTER TABLE public.listings ENABLE ROW LEVEL SECURITY;

-- 2. Create a policy to allow public read access
-- This policy allows anyone (anon role) to SELECT listings
-- that have a status of 'active'.
CREATE POLICY "Allow public read access to active listings"
ON public.listings
FOR SELECT
TO anon
USING (status = 'active');

-- ============================================
-- IMPORTANT: After running this script, your active listings
-- should be visible on the public website.
-- ============================================
