-- Add missing columns to listings table
ALTER TABLE listings 
ADD COLUMN IF NOT EXISTS trust_score INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS outreach_sent_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS category_slug TEXT;

-- Index for performance
CREATE INDEX IF NOT EXISTS idx_listings_trust_score ON listings(trust_score);
CREATE INDEX IF NOT EXISTS idx_listings_category_slug ON listings(category_slug);

-- Update category_slug from categories table for existing listings
UPDATE listings l
SET category_slug = c.slug
FROM categories c
WHERE l.category_id = c.id
AND l.category_slug IS NULL;
