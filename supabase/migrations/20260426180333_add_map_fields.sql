
-- 🗺️ Add Map Fields to listing_premium_data
ALTER TABLE listing_premium_data
  ADD COLUMN IF NOT EXISTS map_tier TEXT NOT NULL DEFAULT 'static'
    CHECK (map_tier IN ('none', 'static', 'premium')),
  ADD COLUMN IF NOT EXISTS coverage_radius_km INTEGER DEFAULT NULL;

COMMENT ON COLUMN listing_premium_data.map_tier IS
  'none=no map, static=Static Maps API img, premium=interactive JS map';
COMMENT ON COLUMN listing_premium_data.coverage_radius_km IS
  'Service area radius in km for premium map polygon. NULL = no polygon.';
