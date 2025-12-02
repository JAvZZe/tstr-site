-- Fix RLS disabled on schema_migrations table
-- Enable RLS and restrict access to prevent security issues

-- Enable Row Level Security
ALTER TABLE public.schema_migrations ENABLE ROW LEVEL SECURITY;

-- Revoke all privileges from PUBLIC to prevent unauthorized access
REVOKE ALL ON public.schema_migrations FROM PUBLIC;

-- Create policy to allow service role access only (for migrations)
-- Note: No policies for authenticated/anon means only service role can access
-- This is appropriate for internal migration tracking table