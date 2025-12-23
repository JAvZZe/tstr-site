-- Migration: 20251220000001_unify_claim_systems.sql
-- Unify claim systems with save/resume functionality and 100% domain verification

-- Add columns for save/resume functionality to claims table
ALTER TABLE claims ADD COLUMN IF NOT EXISTS draft_data JSONB;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS resume_token TEXT;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS draft_expires_at TIMESTAMPTZ;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS verification_status TEXT DEFAULT 'pending' CHECK (verification_status IN ('pending', 'verified', 'rejected'));
ALTER TABLE claims ADD COLUMN IF NOT EXISTS verification_method TEXT;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS verified_at TIMESTAMPTZ;
ALTER TABLE claims ADD COLUMN IF NOT EXISTS domain_verified BOOLEAN DEFAULT FALSE;

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_claims_resume_token ON claims(resume_token) WHERE resume_token IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_claims_draft_expires_at ON claims(draft_expires_at) WHERE draft_expires_at IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_claims_verification_status ON claims(verification_status);

-- Update existing claims to have verification_status
UPDATE claims SET verification_status = 'pending' WHERE verification_status IS NULL;

-- Add RLS policies for draft access (users can only access their own drafts)
ALTER TABLE claims ENABLE ROW LEVEL SECURITY;

-- Policy for authenticated users to access their own claims/drafts
CREATE POLICY "Users can access their own claims" ON claims
FOR ALL USING (
  auth.uid() IS NOT NULL AND (
    business_email = (SELECT email FROM auth.users WHERE id = auth.uid()) OR
    resume_token IS NOT NULL
  )
);

-- Policy for anonymous draft access via resume token
CREATE POLICY "Anonymous draft access via token" ON claims
FOR SELECT USING (
  auth.uid() IS NULL AND
  resume_token IS NOT NULL AND
  draft_expires_at > NOW()
);

-- Function to clean up expired drafts
CREATE OR REPLACE FUNCTION cleanup_expired_drafts()
RETURNS INTEGER AS $$
DECLARE
  deleted_count INTEGER;
BEGIN
  DELETE FROM claims
  WHERE draft_data IS NOT NULL
    AND draft_expires_at < NOW()
    AND verification_status = 'pending';
  GET DIAGNOSTICS deleted_count = ROW_COUNT;
  RETURN deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create a function to generate secure resume tokens
CREATE OR REPLACE FUNCTION generate_resume_token()
RETURNS TEXT AS $$
BEGIN
  RETURN encode(gen_random_bytes(32), 'base64url');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;