-- Migration: Marketplace Phase 1 - Lead Capture & User Profiles
-- Date: 2026-02-25

-- 1. Create leads_rfq table
CREATE TABLE IF NOT EXISTS leads_rfq (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES listings(id),
  
  -- Buyer info (captured from form)
  buyer_name TEXT NOT NULL,
  buyer_email TEXT NOT NULL,
  buyer_company TEXT,
  buyer_industry TEXT,
  buyer_role TEXT,
  
  -- Request info
  message TEXT NOT NULL,
  status TEXT DEFAULT 'new',                 -- 'new'|'contacted'|'qualified'|'closed'
  notified_lab BOOLEAN DEFAULT false,       -- Flag if email was successfully sent
  
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 2. Enhance user_profiles for CRM data
-- Check if columns exist before adding
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='user_profiles' AND column_name='company_name') THEN
        ALTER TABLE user_profiles ADD COLUMN company_name TEXT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='user_profiles' AND column_name='industry') THEN
        ALTER TABLE user_profiles ADD COLUMN industry TEXT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='user_profiles' AND column_name='role') THEN
        ALTER TABLE user_profiles ADD COLUMN role TEXT;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='user_profiles' AND column_name='user_type') THEN
        ALTER TABLE user_profiles ADD COLUMN user_type TEXT DEFAULT 'buyer'; -- 'buyer'|'provider'|'admin'
    END IF;
END $$;

-- 3. Security policies
ALTER TABLE leads_rfq ENABLE ROW LEVEL SECURITY;

-- No public read access for leads - only admin or the specific lab (later)
-- For now, keep it restricted to service role for internal processing

-- Public insert allowed for lead capture
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'leads_rfq' AND policyname = 'Admins can read all leads'
    ) THEN
        CREATE POLICY "Admins can read all leads"
          ON leads_rfq FOR SELECT
          USING (auth.jwt() ->> 'role' = 'service_role');
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'leads_rfq' AND policyname = 'Public can submit leads'
    ) THEN
        CREATE POLICY "Public can submit leads"
          ON leads_rfq FOR INSERT
          WITH CHECK (true);
    END IF;
END $$;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_leads_rfq_listing_id ON leads_rfq(listing_id);
CREATE INDEX IF NOT EXISTS idx_leads_rfq_buyer_email ON leads_rfq(buyer_email);
