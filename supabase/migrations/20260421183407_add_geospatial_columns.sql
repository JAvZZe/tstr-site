-- Enable PostGIS extension for geospatial operations
CREATE EXTENSION IF NOT EXISTS "postgis" WITH SCHEMA "extensions";

-- Add geospatial and map configuration columns to listings table
ALTER TABLE listings 
ADD COLUMN IF NOT EXISTS coverage_radius_km INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS map_tier TEXT DEFAULT 'basic' CHECK (map_tier IN ('basic', 'premium', 'enterprise'));

-- Ensure latitude and longitude are indexed for geospatial lookups if needed
CREATE INDEX IF NOT EXISTS idx_listings_latitude ON listings(latitude);
CREATE INDEX IF NOT EXISTS idx_listings_longitude ON listings(longitude);

-- Add a comment to describe the new columns
COMMENT ON COLUMN listings.coverage_radius_km IS 'Service coverage radius in kilometers for the provider.';
COMMENT ON COLUMN listings.map_tier IS 'Tier determining map features: basic (static), premium (dynamic + radius), enterprise (full interactive).';
