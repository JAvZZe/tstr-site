-- ============================================
-- tstr.directory Database Setup - STEP 3: CREATE INDEXES
-- ============================================
-- Run this AFTER Step 2 completes successfully
-- Indexes make searches MUCH faster

CREATE INDEX IF NOT EXISTS idx_listings_category ON listings(category_id);
CREATE INDEX IF NOT EXISTS idx_listings_location ON listings(location_id);
CREATE INDEX IF NOT EXISTS idx_listings_status ON listings(status) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_listings_featured ON listings(is_featured, featured_until) WHERE is_featured = TRUE;
CREATE INDEX IF NOT EXISTS idx_listings_slug ON listings(slug);

CREATE INDEX IF NOT EXISTS idx_locations_parent ON locations(parent_id);
CREATE INDEX IF NOT EXISTS idx_locations_slug ON locations(slug);
CREATE INDEX IF NOT EXISTS idx_locations_level ON locations(level);

CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug);

CREATE INDEX IF NOT EXISTS idx_custom_fields_category ON custom_fields(category_id);
CREATE INDEX IF NOT EXISTS idx_listing_custom_fields_listing ON listing_custom_fields(listing_id);
CREATE INDEX IF NOT EXISTS idx_listing_custom_fields_field ON listing_custom_fields(custom_field_id);

CREATE INDEX IF NOT EXISTS idx_listing_images_listing ON listing_images(listing_id);

CREATE INDEX IF NOT EXISTS idx_payments_listing ON payments(listing_id);
CREATE INDEX IF NOT EXISTS idx_payments_owner ON payments(owner_id);
CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status);

-- SUCCESS: Once complete, proceed to STEP_4_SEED_DATA.sql
