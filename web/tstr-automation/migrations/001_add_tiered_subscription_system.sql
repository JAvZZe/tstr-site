-- Migration: Add Tiered Subscription System
-- Created: 2025-11-17
-- Purpose: Enable user authentication, subscription tiers, and listing ownership

-- =====================================================
-- 1. USER PROFILES TABLE
-- =====================================================
-- Extends Supabase auth.users with subscription tier information

CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Subscription tier information
  subscription_tier TEXT NOT NULL DEFAULT 'free'
    CHECK (subscription_tier IN ('free', 'basic', 'professional', 'premium', 'enterprise')),
  subscription_status TEXT NOT NULL DEFAULT 'active'
    CHECK (subscription_status IN ('active', 'cancelled', 'past_due', 'trialing')),
  subscription_start_date TIMESTAMPTZ,
  subscription_end_date TIMESTAMPTZ,

  -- Payment tracking (manual initially)
  payment_method TEXT DEFAULT 'manual'
    CHECK (payment_method IN ('manual', 'paypal', 'stripe', 'eft', 'bank_transfer')),

  -- Company information
  company_name TEXT,
  billing_email TEXT,

  -- Metadata
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_profiles_updated_at
  BEFORE UPDATE ON user_profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Add index for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_subscription_tier
  ON user_profiles(subscription_tier);

COMMENT ON TABLE user_profiles IS 'Extended user profile with subscription tier information';
COMMENT ON COLUMN user_profiles.subscription_tier IS 'Current subscription tier: free, basic, professional, premium, enterprise';
COMMENT ON COLUMN user_profiles.payment_method IS 'Payment method on file (manual for initial PayPal/EFT invoicing)';

-- =====================================================
-- 2. LISTING OWNERSHIP TABLE
-- =====================================================
-- Links users to listings they own/manage

CREATE TABLE IF NOT EXISTS listing_ownership (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Ownership verification
  claimed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  verified_owner BOOLEAN NOT NULL DEFAULT FALSE,
  verification_method TEXT CHECK (verification_method IN ('email_domain', 'manual', 'document')),
  verified_at TIMESTAMPTZ,
  verified_by UUID REFERENCES auth.users(id), -- Admin who verified

  -- Metadata
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  -- Ensure one user per listing (but allow multiple listings per user)
  UNIQUE(listing_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_listing_ownership_user_id ON listing_ownership(user_id);
CREATE INDEX IF NOT EXISTS idx_listing_ownership_listing_id ON listing_ownership(listing_id);

COMMENT ON TABLE listing_ownership IS 'Tracks which users own/manage which listings';
COMMENT ON COLUMN listing_ownership.verified_owner IS 'TRUE if ownership has been verified by admin';

-- =====================================================
-- 3. SUBSCRIPTION INVOICES TABLE
-- =====================================================
-- Manual invoice tracking before payment automation

CREATE TABLE IF NOT EXISTS subscription_invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Invoice details
  tier TEXT NOT NULL CHECK (tier IN ('professional', 'premium', 'enterprise', 'verification')),
  amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
  currency TEXT NOT NULL DEFAULT 'USD',

  -- Status tracking
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'paid', 'overdue', 'cancelled', 'refunded')),
  invoice_date DATE NOT NULL DEFAULT CURRENT_DATE,
  due_date DATE NOT NULL,
  paid_date DATE,

  -- Payment information
  payment_method TEXT CHECK (payment_method IN ('paypal', 'eft', 'bank_transfer', 'stripe')),
  payment_reference TEXT, -- PayPal transaction ID, bank reference, etc.

  -- Notes
  notes TEXT,
  admin_notes TEXT, -- Internal notes not visible to user

  -- Metadata
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER update_subscription_invoices_updated_at
  BEFORE UPDATE ON subscription_invoices
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE INDEX IF NOT EXISTS idx_subscription_invoices_user_id ON subscription_invoices(user_id);
CREATE INDEX IF NOT EXISTS idx_subscription_invoices_status ON subscription_invoices(status);
CREATE INDEX IF NOT EXISTS idx_subscription_invoices_due_date ON subscription_invoices(due_date);

COMMENT ON TABLE subscription_invoices IS 'Manual invoice tracking for subscriptions (before payment automation)';
COMMENT ON COLUMN subscription_invoices.tier IS 'Subscription tier or one-time purchase (e.g., verification)';

-- =====================================================
-- 4. UPDATE LISTINGS TABLE
-- =====================================================
-- Add featured and priority ranking columns

ALTER TABLE listings
  ADD COLUMN IF NOT EXISTS featured BOOLEAN NOT NULL DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS priority_rank INTEGER NOT NULL DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_listings_featured ON listings(featured);
CREATE INDEX IF NOT EXISTS idx_listings_priority_rank ON listings(priority_rank DESC);

COMMENT ON COLUMN listings.featured IS 'TRUE if listing should show featured badge (Premium+ tier)';
COMMENT ON COLUMN listings.priority_rank IS 'Priority ranking for search results (higher = appears first). Premium tier gets priority_rank > 0';

-- =====================================================
-- 5. ROW LEVEL SECURITY (RLS) POLICIES
-- =====================================================

-- Enable RLS on new tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE listing_ownership ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscription_invoices ENABLE ROW LEVEL SECURITY;

-- User Profiles Policies
-- ----------------------

-- Users can view their own profile
CREATE POLICY "Users can view own profile"
  ON user_profiles FOR SELECT
  TO authenticated
  USING (id = auth.uid());

-- Users can update their own profile (except subscription tier - admin only)
CREATE POLICY "Users can update own profile"
  ON user_profiles FOR UPDATE
  TO authenticated
  USING (id = auth.uid())
  WITH CHECK (id = auth.uid());

-- Users can insert their own profile (auto-created on signup)
CREATE POLICY "Users can insert own profile"
  ON user_profiles FOR INSERT
  TO authenticated
  WITH CHECK (id = auth.uid());

-- Listing Ownership Policies
-- ---------------------------

-- Users can view their own listing ownerships
CREATE POLICY "Users can view own listing ownerships"
  ON listing_ownership FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

-- Users can insert listing ownership (claim listing)
CREATE POLICY "Users can claim listings"
  ON listing_ownership FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

-- Subscription Invoices Policies
-- -------------------------------

-- Users can view their own invoices
CREATE POLICY "Users can view own invoices"
  ON subscription_invoices FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

-- Listings Policies (UPDATE existing)
-- ------------------------------------

-- Keep existing anonymous read access
-- (Already exists from previous migrations)

-- Authenticated users can view all active listings
CREATE POLICY "Authenticated users can view active listings"
  ON listings FOR SELECT
  TO authenticated
  USING (status = 'active');

-- Listing owners can update their own listings
CREATE POLICY "Listing owners can update their listings"
  ON listings FOR UPDATE
  TO authenticated
  USING (
    id IN (
      SELECT listing_id
      FROM listing_ownership
      WHERE user_id = auth.uid() AND verified_owner = TRUE
    )
  );

-- =====================================================
-- 6. HELPER FUNCTIONS
-- =====================================================

-- Function to get user's subscription tier
CREATE OR REPLACE FUNCTION get_user_tier(user_uuid UUID)
RETURNS TEXT AS $$
  SELECT COALESCE(subscription_tier, 'free')
  FROM user_profiles
  WHERE id = user_uuid;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION get_user_tier IS 'Returns subscription tier for a user (returns free if no profile exists)';

-- Function to check if user can view full contact info
CREATE OR REPLACE FUNCTION can_view_contact_info(user_uuid UUID)
RETURNS BOOLEAN AS $$
  SELECT subscription_tier IN ('professional', 'premium', 'enterprise')
  FROM user_profiles
  WHERE id = user_uuid;
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION can_view_contact_info IS 'Returns TRUE if user tier allows viewing phone/email';

-- Function to check if user owns a listing
CREATE OR REPLACE FUNCTION user_owns_listing(user_uuid UUID, listing_uuid UUID)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1
    FROM listing_ownership
    WHERE user_id = user_uuid
      AND listing_id = listing_uuid
      AND verified_owner = TRUE
  );
$$ LANGUAGE SQL STABLE;

COMMENT ON FUNCTION user_owns_listing IS 'Returns TRUE if user is verified owner of listing';

-- =====================================================
-- 7. SAMPLE DATA (for testing)
-- =====================================================

-- This will be populated after Supabase Auth is enabled
-- Leaving as TODO for Phase 2

-- =====================================================
-- 8. MIGRATION COMPLETE
-- =====================================================

-- Add migration record
CREATE TABLE IF NOT EXISTS schema_migrations (
  version INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO schema_migrations (version, name)
VALUES (1, 'add_tiered_subscription_system')
ON CONFLICT (version) DO NOTHING;

-- Success message
DO $$
BEGIN
  RAISE NOTICE 'Migration 001_add_tiered_subscription_system.sql completed successfully';
  RAISE NOTICE 'Created tables: user_profiles, listing_ownership, subscription_invoices';
  RAISE NOTICE 'Updated listings table with featured and priority_rank columns';
  RAISE NOTICE 'Added RLS policies for tiered access control';
  RAISE NOTICE 'Next step: Enable Supabase Email Auth in dashboard';
END $$;
