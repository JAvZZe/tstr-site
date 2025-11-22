-- Simple waitlist table (alternative to the more complex version)
-- Run this in Supabase SQL Editor if you prefer the simpler schema

CREATE TABLE IF NOT EXISTS waitlist (
    -- Unique Identifier (Primary Key)
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- The Lead Data: Must be unique and non-null (Safety/Integrity Check)
    email TEXT UNIQUE NOT NULL,

    -- The System Data: Essential for tracking sign-up order and age
    signed_up_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Optional: Create an index for faster lookups if the list grows large
CREATE INDEX IF NOT EXISTS idx_waitlist_email ON waitlist (email);
