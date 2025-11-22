-- Create claims table for provider ownership verification
-- This allows providers to claim their listings and verify ownership

CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_name TEXT NOT NULL,
    contact_name TEXT NOT NULL,
    business_email TEXT NOT NULL,
    phone TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'rejected')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for efficient status queries
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status);

-- Create index for email lookups
CREATE INDEX IF NOT EXISTS idx_claims_email ON claims(business_email);

-- Add RLS policies
ALTER TABLE claims ENABLE ROW LEVEL SECURITY;

-- Allow anonymous users to submit claims
CREATE POLICY "Allow anonymous claim submissions"
  ON claims
  FOR INSERT
  TO anon
  WITH CHECK (true);

-- Allow authenticated users to view their own claims (by email)
CREATE POLICY "Users can view their own claims"
  ON claims
  FOR SELECT
  TO authenticated
  USING (business_email = auth.jwt() ->> 'email');

-- Add comments for documentation
COMMENT ON TABLE claims IS 'Stores provider ownership claim requests for listing verification';
COMMENT ON COLUMN claims.business_email IS 'Business email used for domain verification';
COMMENT ON COLUMN claims.status IS 'Claim status: pending (awaiting verification), verified (approved), rejected (denied)';
