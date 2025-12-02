-- Fix multiple permissive policies on listing_capabilities table
-- Consolidate ALL operations policies for dashboard_user role

-- Drop the overlapping policies
DROP POLICY IF EXISTS "Admins can manage all capabilities" ON public.listing_capabilities;
DROP POLICY IF EXISTS "Listing owners can manage their capabilities" ON public.listing_capabilities;

-- Create consolidated policy for all operations
CREATE POLICY "Admins and owners can manage capabilities"
  ON public.listing_capabilities
  FOR ALL
  USING (
    -- Admins can manage all
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid()
      AND role = 'admin'
    )
    OR
    -- Verified owners can manage their listings' capabilities
    listing_id IN (
      SELECT lo.listing_id FROM listing_owners lo
      WHERE lo.user_id = auth.uid()
      AND lo.status = 'verified'
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid()
      AND role = 'admin'
    )
    OR
    listing_id IN (
      SELECT lo.listing_id FROM listing_owners lo
      WHERE lo.user_id = auth.uid()
      AND lo.status = 'verified'
    )
  );