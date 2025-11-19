-- Enable public read access to locations table for frontend
-- This is safe because locations are public reference data

-- Enable RLS if not already enabled
ALTER TABLE locations ENABLE ROW LEVEL SECURITY;

-- Drop policy if it exists (idempotent)
DROP POLICY IF EXISTS "Enable read access for all users" ON locations;

-- Create policy to allow anonymous read access
CREATE POLICY "Enable read access for all users"
ON locations
FOR SELECT
USING (true);
