-- Run this in Supabase SQL Editor
-- URL: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/sql

CREATE TABLE IF NOT EXISTS pending_research (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
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

CREATE INDEX IF NOT EXISTS idx_pending_research_business_name ON pending_research(business_name);
CREATE INDEX IF NOT EXISTS idx_pending_research_status ON pending_research(status);
CREATE INDEX IF NOT EXISTS idx_pending_research_created_at ON pending_research(created_at);

-- Enable Row Level Security
ALTER TABLE pending_research ENABLE ROW LEVEL SECURITY;

-- Create policies
DROP POLICY IF EXISTS "Enable all for authenticated users" ON pending_research;
CREATE POLICY "Enable all for authenticated users" ON pending_research
    FOR ALL USING (true);
