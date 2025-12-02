-- Fix Auth RLS Initialization Plan issue on user_profiles table
-- Wrap auth.uid() in subquery to avoid per-row re-evaluation

-- Drop the existing policy
DROP POLICY IF EXISTS "Users can insert own profile" ON public.user_profiles;

-- Recreate with optimized auth call
CREATE POLICY "Users can insert own profile" ON public.user_profiles
  FOR INSERT TO authenticated
  WITH CHECK (id = (SELECT auth.uid()));