-- Fix Auth RLS Initialization Plan issue on claims table
-- Wrap auth.uid() in subquery to avoid per-row re-evaluation

-- Drop the existing policy
DROP POLICY IF EXISTS "Users can view their own claims" ON public.claims;

-- Recreate with optimized auth call
CREATE POLICY "Users can view their own claims" ON public.claims
  FOR SELECT TO authenticated
  USING (user_id = (SELECT auth.uid()));