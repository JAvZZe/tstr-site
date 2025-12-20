-- Fix submit page 500 error by adding RLS policy for anonymous listing inserts
-- Date: 2025-12-04
-- Description: Allow anonymous users to submit pending listings via the submit form

-- Add policy to allow anonymous users to insert pending listings
CREATE POLICY "Allow anonymous insert for pending listings"
  ON public.listings
  FOR INSERT
  TO public
  WITH CHECK (status = 'pending');