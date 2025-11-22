-- Add region column to listings table
-- This allows filtering/grouping listings by geographic region (useful for compliance, language, etc.)

ALTER TABLE listings ADD COLUMN IF NOT EXISTS region TEXT DEFAULT 'global';

-- Create index for efficient region-based queries
CREATE INDEX IF NOT EXISTS idx_listings_region ON listings(region);

-- Add comment for documentation
COMMENT ON COLUMN listings.region IS 'Geographic region of the listing (e.g., usa, eu, apac, global)';
