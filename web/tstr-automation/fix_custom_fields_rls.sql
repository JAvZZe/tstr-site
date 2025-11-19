-- Fix RLS policy for listing_custom_fields to allow public read access
-- This allows the frontend (using anon key) to read custom field values

-- Enable RLS on listing_custom_fields if not already enabled
ALTER TABLE listing_custom_fields ENABLE ROW LEVEL SECURITY;

-- Drop existing policy if it exists
DROP POLICY IF EXISTS "Allow public read access to custom field values" ON listing_custom_fields;

-- Create policy allowing anyone to read custom field values
-- (They can only see values for active listings anyway)
CREATE POLICY "Allow public read access to custom field values"
ON listing_custom_fields
FOR SELECT
TO public
USING (true);

-- Also ensure custom_fields table allows public read
ALTER TABLE custom_fields ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow public read access to custom field definitions" ON custom_fields;

CREATE POLICY "Allow public read access to custom field definitions"
ON custom_fields
FOR SELECT
TO public
USING (true);

-- Verify policies
SELECT tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename IN ('listing_custom_fields', 'custom_fields')
ORDER BY tablename, policyname;
