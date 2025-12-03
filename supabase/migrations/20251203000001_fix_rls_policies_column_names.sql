-- Fix RLS policies with correct column names
-- Addresses column name issues where user_id was incorrectly assumed to exist on all tables

-- 1) Listing owners can manage their capabilities — on listing_owners
DROP POLICY IF EXISTS "Listing owners can manage their capabilities" ON public.listing_owners;

CREATE POLICY "Listing owners can manage their capabilities"
  ON public.listing_owners
  FOR ALL
  TO public
  USING (
    listing_id IN (
      SELECT listings.id FROM listings
      WHERE (listings.owner_id = (SELECT auth.uid()))
    )
  );

-- 2) Users can view their own claims — on claims
DROP POLICY IF EXISTS "Users can view their own claims" ON public.claims;

CREATE POLICY "Users can view their own claims"
  ON public.claims
  FOR SELECT
  TO authenticated
  USING ( business_email = (SELECT auth.jwt() ->> 'email') );

-- 3) Admins can update ownership status — on listing_owners
DROP POLICY IF EXISTS "Admins can update ownership status" ON public.listing_owners;

CREATE POLICY "Admins can update ownership status"
  ON public.listing_owners
  FOR UPDATE
  TO public
  USING (
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE ((user_profiles.id = (SELECT auth.uid())) AND (listing_owners.role = 'admin'::text))
    )
  );

-- 4) Users can claim listings (anon insert) — on claims
DROP POLICY IF EXISTS "Users can claim listings" ON public.claims;

CREATE POLICY "Users can claim listings"
  ON public.claims
  FOR INSERT
  TO public
  WITH CHECK ( (SELECT auth.uid()) = user_id );

-- 5) Users can update own pending claims — on claims
DROP POLICY IF EXISTS "Users can update own pending claims" ON public.claims;

CREATE POLICY "Users can update own pending claims"
  ON public.claims
  FOR UPDATE
  TO public
  USING ( ((SELECT auth.uid()) = user_id) AND (status = 'pending'::text) );

-- 6) Users can view own ownership — on listing_ownership
DROP POLICY IF EXISTS "Users can view own ownership" ON public.listing_ownership;

CREATE POLICY "Users can view own ownership"
  ON public.listing_ownership
  FOR SELECT
  TO public
  USING ( (SELECT auth.uid()) = user_id );

-- 7) Listing owners can update their listings — on listings
DROP POLICY IF EXISTS "Listing owners can update their listings" ON public.listings;

CREATE POLICY "Listing owners can update their listings"
  ON public.listings
  FOR UPDATE
  TO authenticated
  USING (
    id IN (
      SELECT listing_ownership.listing_id FROM listing_ownership
      WHERE ((listing_ownership.user_id = (SELECT auth.uid())) AND (listing_ownership.verified_owner = true))
    )
  );

-- 8) Users can claim listings (authenticated insert) — on claims
DROP POLICY IF EXISTS "Users can claim listings (authenticated)" ON public.claims;

CREATE POLICY "Users can claim listings (authenticated)"
  ON public.claims
  FOR INSERT
  TO authenticated
  WITH CHECK ( user_id = (SELECT auth.uid()) );

-- 9) Users can view own listing ownerships — on listing_ownership
DROP POLICY IF EXISTS "Users can view own listing ownerships" ON public.listing_ownership;

CREATE POLICY "Users can view own listing ownerships"
  ON public.listing_ownership
  FOR SELECT
  TO authenticated
  USING ( user_id = (SELECT auth.uid()) );

-- 10) Users can view own invoices — on subscription_invoices
DROP POLICY IF EXISTS "Users can view own invoices" ON public.subscription_invoices;

CREATE POLICY "Users can view own invoices"
  ON public.subscription_invoices
  FOR SELECT
  TO authenticated
  USING ( user_id = (SELECT auth.uid()) );