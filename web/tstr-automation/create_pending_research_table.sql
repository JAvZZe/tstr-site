-- Create pending_research table for listings with invalid URLs
-- These are potential clients/companies that need URL research before adding to directory

CREATE TABLE IF NOT EXISTS pending_research (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_name TEXT NOT NULL,
    website TEXT,
    validation_error TEXT,
    original_id UUID,
    category TEXT,
    location_id UUID,
    address TEXT,
    phone TEXT,
    email TEXT,
    description TEXT,
    status TEXT DEFAULT 'pending_research',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    researched_at TIMESTAMP WITH TIME ZONE,
    researched_by TEXT
);

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_pending_research_business_name ON pending_research(business_name);
CREATE INDEX IF NOT EXISTS idx_pending_research_status ON pending_research(status);
CREATE INDEX IF NOT EXISTS idx_pending_research_created_at ON pending_research(created_at);

-- Add RLS (Row Level Security) policies
ALTER TABLE pending_research ENABLE ROW LEVEL SECURITY;

-- Allow read access to authenticated users
CREATE POLICY "Enable read access for all users" ON pending_research
    FOR SELECT USING (true);

-- Allow insert for service role
CREATE POLICY "Enable insert for service role" ON pending_research
    FOR INSERT WITH CHECK (true);

-- Allow update for service role
CREATE POLICY "Enable update for service role" ON pending_research
    FOR UPDATE USING (true);

-- Allow delete for service role
CREATE POLICY "Enable delete for service role" ON pending_research
    FOR DELETE USING (true);

-- Add helpful comment
COMMENT ON TABLE pending_research IS 'Stores listings with invalid URLs for future research and validation. These are potential clients/companies that need their URLs fixed before adding to the main directory.';
