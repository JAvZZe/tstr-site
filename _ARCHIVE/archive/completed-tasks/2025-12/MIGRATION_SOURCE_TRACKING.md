# Source Tracking Migration

Execute this SQL in the Supabase Dashboard to add source tracking fields to the listings table.

## SQL Migration

```sql
-- Add source tracking fields to listings table
-- Tracks which scraper script and location produced each listing

ALTER TABLE listings
ADD COLUMN IF NOT EXISTS source_script TEXT,
ADD COLUMN IF NOT EXISTS script_location TEXT;

-- Add comments for documentation
COMMENT ON COLUMN listings.source_script IS 'Name of the scraper script that created this listing (e.g., oil_gas_playwright.py)';
COMMENT ON COLUMN listings.script_location IS 'File path or location of the scraper script (e.g., web/tstr-automation/scrapers/)';

-- Create index for performance when filtering by source
CREATE INDEX IF NOT EXISTS idx_listings_source_script ON listings(source_script);
CREATE INDEX IF NOT EXISTS idx_listings_script_location ON listings(script_location);
```

## Execution Steps

1. Go to: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/sql
2. Copy the SQL above
3. Paste into the SQL Editor
4. Click "Run"

## Verification

After execution, check that the columns exist:
```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'listings'
AND column_name IN ('source_script', 'script_location');
```

## Benefits

- Complete data lineage tracking
- Performance monitoring by scraper source
- Easy troubleshooting and maintenance
- Future analytics capabilities