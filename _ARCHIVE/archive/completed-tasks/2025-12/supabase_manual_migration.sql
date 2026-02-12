-- MANUAL SQL MIGRATION: LinkedIn OAuth and Rights Management
-- Apply this in Supabase SQL Editor: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/sql
-- Date: 2025-11-30
-- Description: Implements corporate domain verification and listing ownership system

-- Create listing_owners table for rights management
CREATE TABLE IF NOT EXISTS listing_owners (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('owner', 'editor', 'admin')) DEFAULT 'owner',
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'rejected')),
  verification_method TEXT CHECK (verification_method IN ('domain_match', 'email_verification', 'admin_approval')),
  verified_at TIMESTAMPTZ,
  verification_token TEXT,
  token_expires_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Ensure one active ownership per listing per user
  UNIQUE(user_id, listing_id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_listing_owners_user_id ON listing_owners(user_id);
CREATE INDEX IF NOT EXISTS idx_listing_owners_listing_id ON listing_owners(listing_id);
CREATE INDEX IF NOT EXISTS idx_listing_owners_status ON listing_owners(status);

-- Enable Row Level Security
ALTER TABLE listing_owners ENABLE ROW LEVEL SECURITY;

-- RLS Policies for listing_owners table

-- Users can view their own ownership records
CREATE POLICY "Users can view own ownership" ON listing_owners
  FOR SELECT USING (auth.uid() = user_id);

-- Users can insert ownership claims
CREATE POLICY "Users can claim listings" ON listing_owners
  FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Users can update their own pending claims
CREATE POLICY "Users can update own pending claims" ON listing_owners
  FOR UPDATE USING (
    auth.uid() = user_id AND
    status = 'pending'
  );

-- Only admins can update ownership status to verified/rejected
CREATE POLICY "Admins can update ownership status" ON listing_owners
  FOR UPDATE USING (
    EXISTS (
      SELECT 1 FROM user_profiles
      WHERE id = auth.uid()
      AND role = 'admin'
    )
  );

-- Add claim-related columns to listings table
ALTER TABLE listings
  ADD COLUMN IF NOT EXISTS claimed BOOLEAN DEFAULT false,
  ADD COLUMN IF NOT EXISTS claimed_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS website_domain TEXT,
  ADD COLUMN IF NOT EXISTS contact_email TEXT;

-- Create index for domain lookups
CREATE INDEX IF NOT EXISTS idx_listings_website_domain ON listings(website_domain);
CREATE INDEX IF NOT EXISTS idx_listings_claimed ON listings(claimed);

-- Update existing listings to extract domains
UPDATE listings
SET website_domain = CASE
  WHEN website LIKE 'http%' THEN
    REPLACE(REPLACE(REPLACE(website, 'https://', ''), 'http://', ''), 'www.', '')
  ELSE NULL
END
WHERE website_domain IS NULL AND website IS NOT NULL;

-- Add function to extract domain from URL
CREATE OR REPLACE FUNCTION extract_domain(url TEXT)
RETURNS TEXT AS $$
BEGIN
  IF url IS NULL OR url = '' THEN
    RETURN NULL;
  END IF;

  -- Remove protocol
  url := regexp_replace(url, '^https?://', '');

  -- Remove www prefix
  url := regexp_replace(url, '^www\.', '');

  -- Extract domain (everything before first / or ?)
  url := split_part(url, '/', 1);
  url := split_part(url, '?', 1);
  url := split_part(url, '#', 1);

  RETURN lower(trim(url));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Add function to check if user can auto-claim listing
CREATE OR REPLACE FUNCTION can_auto_claim(user_email TEXT, listing_website TEXT)
RETURNS BOOLEAN AS $$
DECLARE
  user_domain TEXT;
  listing_domain TEXT;
BEGIN
  IF user_email IS NULL OR listing_website IS NULL THEN
    RETURN FALSE;
  END IF;

  -- Extract domain from email
  user_domain := split_part(user_email, '@', 2);
  IF user_domain IS NULL THEN
    RETURN FALSE;
  END IF;

  -- Extract domain from website
  listing_domain := extract_domain(listing_website);
  IF listing_domain IS NULL THEN
    RETURN FALSE;
  END IF;

  -- Exact match
  IF lower(user_domain) = lower(listing_domain) THEN
    RETURN TRUE;
  END IF;

  -- Handle common TLD variations (optional enhancement)
  user_domain := regexp_replace(lower(user_domain), '\.(com|org|net|edu|gov)$', '');
  listing_domain := regexp_replace(lower(listing_domain), '\.(com|org|net|edu|gov)$', '');

  RETURN user_domain = listing_domain;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Add trigger to update website_domain when website changes
CREATE OR REPLACE FUNCTION update_website_domain()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.website IS DISTINCT FROM OLD.website THEN
    NEW.website_domain := extract_domain(NEW.website);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_website_domain
  BEFORE INSERT OR UPDATE ON listings
  FOR EACH ROW
  EXECUTE FUNCTION update_website_domain();

-- Add admin role to user_profiles if not exists
ALTER TABLE user_profiles
  ADD COLUMN IF NOT EXISTS role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin'));

-- Create admin user function (for development)
CREATE OR REPLACE FUNCTION make_user_admin(user_email TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  UPDATE user_profiles
  SET role = 'admin'
  WHERE billing_email = user_email;

  RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Verification: Check that everything was created
SELECT 'Migration completed successfully!' as status;