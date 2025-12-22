-- Create leads/contact management system for listing owners
-- Tracks when visitors access contact information and allows owners to manage leads

CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Lead identification
  listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  contact_type TEXT NOT NULL CHECK (contact_type IN ('phone', 'email', 'website')),

  -- Lead source information
  visitor_ip TEXT, -- For analytics (anonymized)
  user_agent TEXT, -- Browser/device info
  referrer TEXT, -- Where they came from

  -- Contact details accessed (for owner's reference)
  contact_value TEXT NOT NULL, -- The actual phone/email/website accessed

  -- Lead status tracking
  status TEXT DEFAULT 'new' CHECK (status IN ('new', 'contacted', 'qualified', 'converted', 'lost')),
  owner_notes TEXT, -- Owner's notes about this lead

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  contacted_at TIMESTAMPTZ, -- When owner marked as contacted
  converted_at TIMESTAMPTZ, -- When converted to customer
  status_changed_by UUID REFERENCES auth.users(id) -- Who changed the status
);

-- Indexes for performance
CREATE INDEX idx_leads_listing_id ON leads(listing_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created_at ON leads(created_at DESC);
CREATE INDEX idx_leads_contact_type ON leads(contact_type);

-- Row Level Security
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- Listing owners can view and manage leads for their listings
CREATE POLICY "Listing owners can manage their leads"
  ON leads FOR ALL
  USING (
    listing_id IN (
      SELECT id FROM listings WHERE owner_id = auth.uid()
    )
  );

-- Admins can view all leads
CREATE POLICY "Admins can view all leads"
  ON leads FOR SELECT
  USING (auth.role() = 'authenticated');

-- Function to create a lead when contact info is accessed
CREATE OR REPLACE FUNCTION create_lead(
  p_listing_id UUID,
  p_contact_type TEXT,
  p_contact_value TEXT,
  p_visitor_ip TEXT DEFAULT NULL,
  p_user_agent TEXT DEFAULT NULL,
  p_referrer TEXT DEFAULT NULL
)
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  lead_id UUID;
BEGIN
  -- Only allow creating leads for active, claimed listings
  IF NOT EXISTS (
    SELECT 1 FROM listings
    WHERE id = p_listing_id
    AND status = 'active'
    AND claimed = true
  ) THEN
    RAISE EXCEPTION 'Cannot create lead for inactive or unclaimed listing';
  END IF;

  INSERT INTO leads (
    listing_id,
    contact_type,
    contact_value,
    visitor_ip,
    user_agent,
    referrer
  ) VALUES (
    p_listing_id,
    p_contact_type,
    p_contact_value,
    p_visitor_ip,
    p_user_agent,
    p_referrer
  ) RETURNING id INTO lead_id;

  RETURN lead_id;
END;
$$;

-- Function to update lead status
CREATE OR REPLACE FUNCTION update_lead_status(
  p_lead_id UUID,
  p_status TEXT,
  p_owner_notes TEXT DEFAULT NULL
)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  listing_owner UUID;
BEGIN
  -- Verify the user owns the listing this lead belongs to
  SELECT l.owner_id INTO listing_owner
  FROM leads ld
  JOIN listings l ON ld.listing_id = l.id
  WHERE ld.id = p_lead_id;

  IF listing_owner != auth.uid() THEN
    RAISE EXCEPTION 'You do not have permission to update this lead';
  END IF;

  -- Update the lead
  UPDATE leads SET
    status = p_status,
    owner_notes = COALESCE(p_owner_notes, owner_notes),
    updated_at = NOW(),
    status_changed_by = auth.uid(),
    contacted_at = CASE WHEN p_status IN ('contacted', 'qualified', 'converted') AND contacted_at IS NULL THEN NOW() ELSE contacted_at END,
    converted_at = CASE WHEN p_status = 'converted' AND converted_at IS NULL THEN NOW() ELSE converted_at END
  WHERE id = p_lead_id;

  RETURN TRUE;
END;
$$;

-- Grant permissions
GRANT EXECUTE ON FUNCTION create_lead TO authenticated;
GRANT EXECUTE ON FUNCTION update_lead_status TO authenticated;

-- Comments for documentation
COMMENT ON TABLE leads IS 'Tracks contact attempts and lead management for listing owners';
COMMENT ON COLUMN leads.contact_type IS 'Type of contact accessed: phone, email, or website';
COMMENT ON COLUMN leads.status IS 'Lead status: new, contacted, qualified, converted, lost';
COMMENT ON COLUMN leads.owner_notes IS 'Owner notes and follow-up information';
COMMENT ON FUNCTION create_lead IS 'Creates a new lead when contact information is accessed';
COMMENT ON FUNCTION update_lead_status IS 'Allows listing owners to update lead status and add notes';