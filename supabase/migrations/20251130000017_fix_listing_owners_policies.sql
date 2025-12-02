-- Fix multiple permissive policies on listing_owners table
-- Consolidate UPDATE policies for dashboard_user role

-- Drop the overlapping policies
DROP POLICY IF EXISTS "Users can update own pending claims" ON public.listing_owners;
DROP POLICY IF EXISTS "Admins can update ownership status" ON public.listing_owners;

-- Create consolidated UPDATE policy
CREATE POLICY "Users and admins can update ownership"
  ON public.listing_owners
  FOR UPDATE
  USING (
    -- Users can update own pending claims
    (auth.uid() = user_id AND status = 'pending')
    OR
    -- Admins can update any ownership status
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid()
      AND role = 'admin'
    )
  )
  WITH CHECK (
    (auth.uid() = user_id AND status = 'pending')
    OR
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid()
      AND role = 'admin'
    )
  );