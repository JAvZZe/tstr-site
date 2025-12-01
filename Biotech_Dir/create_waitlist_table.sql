-- Create waitlist table for lead capture
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/sql

CREATE TABLE IF NOT EXISTS waitlist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source TEXT DEFAULT 'website',
    status TEXT DEFAULT 'pending',
    notes TEXT
);

-- Create index on email for fast lookups
CREATE INDEX IF NOT EXISTS idx_waitlist_email ON waitlist(email);

-- Create index on created_at for sorting
CREATE INDEX IF NOT EXISTS idx_waitlist_created_at ON waitlist(created_at DESC);

-- Enable Row Level Security
ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can insert (public form submission)
CREATE POLICY "Anyone can submit to waitlist"
    ON waitlist
    FOR INSERT
    TO public
    WITH CHECK (true);

-- Policy: Only authenticated users can read (for admin dashboard)
CREATE POLICY "Authenticated users can read waitlist"
    ON waitlist
    FOR SELECT
    TO authenticated
    USING (true);

-- Policy: Only service role can update/delete
CREATE POLICY "Service role can manage waitlist"
    ON waitlist
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

-- Add helpful comments
COMMENT ON TABLE waitlist IS 'Email waitlist for TSTR.site lead capture';
COMMENT ON COLUMN waitlist.email IS 'Unique email address of subscriber';
COMMENT ON COLUMN waitlist.source IS 'Where the lead came from (website, github, etc)';
COMMENT ON COLUMN waitlist.status IS 'Status: pending, contacted, converted';

-- Verify table was created
SELECT 
    table_name, 
    column_name, 
    data_type, 
    is_nullable
FROM information_schema.columns
WHERE table_name = 'waitlist'
ORDER BY ordinal_position;
