-- Fix multiple permissive policies on standards table
-- Separate SELECT (public) from other operations (authenticated)

-- Drop the problematic admin policy that overlaps with public SELECT
DROP POLICY IF EXISTS "Admins can manage standards" ON public.standards;

-- Recreate admin policy for non-SELECT operations only
CREATE POLICY "Admins can manage standards"
  ON public.standards
  FOR INSERT, UPDATE, DELETE
  TO authenticated
  USING (TRUE)
  WITH CHECK (TRUE);

-- Keep the public SELECT policy (already exists)
-- This ensures only one permissive policy applies to SELECT for any role