-- ============================================
-- tstr.directory Database Setup Script
-- Supabase PostgreSQL Schema
-- ============================================
-- Execute this in: Supabase Dashboard → SQL Editor → New Query
-- Run entire script at once (Ctrl/Cmd + Enter)

-- ============================================
-- 1. EXTENSIONS
-- ============================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable PostGIS for location queries (optional, for future radius search)
-- CREATE EXTENSION IF NOT EXISTS "postgis";

-- ============================================
-- 2. CORE TABLES
-- ============================================

-- Global → Region → Country → City hierarchy
CREATE TABLE locations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  parent_id UUID REFERENCES locations(id) ON DELETE CASCADE,
  level TEXT NOT NULL CHECK (level IN ('global', 'region', 'country', 'city')),
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Industry categories (Oil & Gas, Pharma, Biotech, Environmental, Materials)
CREATE TABLE categories (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  parent_id UUID REFERENCES categories(id) ON DELETE SET NULL,
  description TEXT,
  icon TEXT,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Industry-specific custom fields definition
CREATE TABLE custom_fields (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
  field_name TEXT NOT NULL,
  field_label TEXT NOT NULL,
  field_type TEXT NOT NULL CHECK (field_type IN ('text', 'number', 'boolean', 'select', 'multi_select', 'date', 'url', 'email', 'phone')),
  options JSONB,
  placeholder TEXT,
  help_text TEXT,
  is_required BOOLEAN DEFAULT FALSE,
  is_searchable BOOLEAN DEFAULT TRUE,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(category_id, field_name)
);

-- Business listings
CREATE TABLE listings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  owner_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  category_id UUID REFERENCES categories(id) NOT NULL,
  location_id UUID REFERENCES locations(id) NOT NULL,
  
  -- Core details
  business_name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  website TEXT,
  email TEXT,
  phone TEXT,
  address TEXT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  
  -- Monetisation
  plan_type TEXT DEFAULT 'free' CHECK (plan_type IN ('free', 'basic', 'featured', 'premium')),
  is_featured BOOLEAN DEFAULT FALSE,
  featured_until TIMESTAMPTZ,
  featured_at TIMESTAMPTZ,
  
  -- Status
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'expired', 'suspended', 'deleted')),
  verified BOOLEAN DEFAULT FALSE,
  claimed BOOLEAN DEFAULT FALSE,
  
  -- Metadata
  views INTEGER DEFAULT 0,
  clicks INTEGER DEFAULT 0,
  last_viewed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  
  -- Search optimisation
  search_vector tsvector GENERATED ALWAYS AS (
    to_tsvector('english', coalesce(business_name, '') || ' ' || coalesce(description, ''))
  ) STORED
);

-- Custom field values per listing
CREATE TABLE listing_custom_fields (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  custom_field_id UUID REFERENCES custom_fields(id) ON DELETE CASCADE,
  value JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(listing_id, custom_field_id)
);

-- Listing images
CREATE TABLE listing_images (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  thumbnail_url TEXT,
  alt_text TEXT,
  is_primary BOOLEAN DEFAULT FALSE,
  display_order INTEGER DEFAULT 0,
  file_size INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT only_one_primary_per_listing UNIQUE NULLS NOT DISTINCT (listing_id, is_primary)
);

-- Payment tracking
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE SET NULL,
  owner_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  
  amount DECIMAL(10, 2) NOT NULL,
  currency TEXT DEFAULT 'GBP',
  payment_method TEXT CHECK (payment_method IN ('bank_transfer', 'paypal', 'bitcoin', 'stripe')),
  
  -- Bank transfer verification
  reference_number TEXT,
  proof_image_url TEXT,
  transaction_hash TEXT, -- For Bitcoin
  
  -- Plan details
  plan_type TEXT NOT NULL,
  billing_cycle TEXT CHECK (billing_cycle IN ('monthly', 'quarterly', 'annual', 'one_time')),
  start_date TIMESTAMPTZ,
  end_date TIMESTAMPTZ,
  
  -- Status
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'rejected', 'refunded', 'expired')),
  verified_by UUID REFERENCES auth.users(id),
  verified_at TIMESTAMPTZ,
  
  notes TEXT,
  admin_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enquiries/Lead generation
CREATE TABLE enquiries (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  
  -- Contact details
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  company TEXT,
  
  -- Enquiry details
  subject TEXT,
  message TEXT NOT NULL,
  
  -- Metadata
  ip_hash TEXT,
  user_agent TEXT,
  referrer TEXT,
  
  -- Status
  status TEXT DEFAULT 'new' CHECK (status IN ('new', 'contacted', 'converted', 'spam')),
  forwarded_at TIMESTAMPTZ,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Search analytics
CREATE TABLE search_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  query TEXT,
  category_id UUID REFERENCES categories(id),
  location_id UUID REFERENCES locations(id),
  filters JSONB,
  results_count INTEGER,
  
  -- Privacy-preserving analytics
  ip_hash TEXT,
  user_agent_hash TEXT,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- User profiles (extends auth.users)
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT,
  company_name TEXT,
  phone TEXT,
  role TEXT DEFAULT 'owner' CHECK (role IN ('owner', 'admin', 'moderator')),
  
  -- Preferences
  email_notifications BOOLEAN DEFAULT TRUE,
  
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 3. INDEXES FOR PERFORMANCE
-- ============================================

-- Listings indexes
CREATE INDEX idx_listings_category ON listings(category_id) WHERE status = 'active';
CREATE INDEX idx_listings_location ON listings(location_id) WHERE status = 'active';
CREATE INDEX idx_listings_status ON listings(status);
CREATE INDEX idx_listings_featured ON listings(is_featured, featured_until) WHERE is_featured = TRUE AND status = 'active';
CREATE INDEX idx_listings_owner ON listings(owner_id);
CREATE INDEX idx_listings_slug ON listings(slug);
CREATE INDEX idx_listings_search ON listings USING GIN(search_vector);
CREATE INDEX idx_listings_created ON listings(created_at DESC);

-- Locations indexes
CREATE INDEX idx_locations_parent ON locations(parent_id);
CREATE INDEX idx_locations_slug ON locations(slug);
CREATE INDEX idx_locations_level ON locations(level);

-- Categories indexes
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_categories_slug ON categories(slug);

-- Custom field values
CREATE INDEX idx_listing_custom_fields_listing ON listing_custom_fields(listing_id);
CREATE INDEX idx_listing_custom_fields_field ON listing_custom_fields(custom_field_id);
CREATE INDEX idx_listing_custom_fields_value ON listing_custom_fields USING GIN(value);

-- Payments indexes
CREATE INDEX idx_payments_listing ON payments(listing_id);
CREATE INDEX idx_payments_owner ON payments(owner_id);
CREATE INDEX idx_payments_status ON payments(status);
CREATE INDEX idx_payments_dates ON payments(start_date, end_date);

-- Enquiries indexes
CREATE INDEX idx_enquiries_listing ON enquiries(listing_id);
CREATE INDEX idx_enquiries_status ON enquiries(status);
CREATE INDEX idx_enquiries_created ON enquiries(created_at DESC);

-- ============================================
-- 4. ROW LEVEL SECURITY (RLS)
-- ============================================

-- Enable RLS on all tables
ALTER TABLE listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE listing_custom_fields ENABLE ROW LEVEL SECURITY;
ALTER TABLE listing_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE enquiries ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Public can read active listings
CREATE POLICY "Public can view active listings"
ON listings FOR SELECT
USING (status = 'active');

-- Owners can view their own listings (any status)
CREATE POLICY "Owners can view own listings"
ON listings FOR SELECT
USING (auth.uid() = owner_id);

-- Owners can insert listings
CREATE POLICY "Authenticated users can create listings"
ON listings FOR INSERT
WITH CHECK (auth.uid() = owner_id);

-- Owners can update their own listings
CREATE POLICY "Owners can update own listings"
ON listings FOR UPDATE
USING (auth.uid() = owner_id)
WITH CHECK (auth.uid() = owner_id);

-- Admins can do everything
CREATE POLICY "Admins can manage all listings"
ON listings FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM user_profiles
    WHERE user_profiles.id = auth.uid()
    AND user_profiles.role IN ('admin', 'moderator')
  )
);

-- Custom fields: Public read for active listings
CREATE POLICY "Public can view custom fields of active listings"
ON listing_custom_fields FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM listings
    WHERE listings.id = listing_custom_fields.listing_id
    AND listings.status = 'active'
  )
);

-- Custom fields: Owners can manage
CREATE POLICY "Owners can manage own listing custom fields"
ON listing_custom_fields FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM listings
    WHERE listings.id = listing_custom_fields.listing_id
    AND listings.owner_id = auth.uid()
  )
);

-- Images: Public read for active listings
CREATE POLICY "Public can view images of active listings"
ON listing_images FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM listings
    WHERE listings.id = listing_images.listing_id
    AND listings.status = 'active'
  )
);

-- Images: Owners can manage
CREATE POLICY "Owners can manage own listing images"
ON listing_images FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM listings
    WHERE listings.id = listing_images.listing_id
    AND listings.owner_id = auth.uid()
  )
);

-- Payments: Owners can view their own
CREATE POLICY "Owners can view own payments"
ON payments FOR SELECT
USING (auth.uid() = owner_id);

-- Payments: Owners can create
CREATE POLICY "Owners can create payments"
ON payments FOR INSERT
WITH CHECK (auth.uid() = owner_id);

-- Payments: Admins can manage all
CREATE POLICY "Admins can manage all payments"
ON payments FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM user_profiles
    WHERE user_profiles.id = auth.uid()
    AND user_profiles.role IN ('admin', 'moderator')
  )
);

-- Enquiries: Listing owners can view enquiries for their listings
CREATE POLICY "Owners can view enquiries for their listings"
ON enquiries FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM listings
    WHERE listings.id = enquiries.listing_id
    AND listings.owner_id = auth.uid()
  )
);

-- Enquiries: Public can create
CREATE POLICY "Anyone can create enquiries"
ON enquiries FOR INSERT
WITH CHECK (true);

-- User profiles: Users can view/update own profile
CREATE POLICY "Users can view own profile"
ON user_profiles FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
ON user_profiles FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
ON user_profiles FOR INSERT
WITH CHECK (auth.uid() = id);

-- ============================================
-- 5. FUNCTIONS & TRIGGERS
-- ============================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to relevant tables
CREATE TRIGGER update_listings_updated_at
  BEFORE UPDATE ON listings
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_categories_updated_at
  BEFORE UPDATE ON categories
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_locations_updated_at
  BEFORE UPDATE ON locations
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_custom_fields_updated_at
  BEFORE UPDATE ON custom_fields
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_listing_custom_fields_updated_at
  BEFORE UPDATE ON listing_custom_fields
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_payments_updated_at
  BEFORE UPDATE ON payments
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER update_user_profiles_updated_at
  BEFORE UPDATE ON user_profiles
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- Auto-create user profile on signup
CREATE OR REPLACE FUNCTION create_user_profile()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO user_profiles (id)
  VALUES (NEW.id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER create_profile_on_signup
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION create_user_profile();

-- Increment view count
CREATE OR REPLACE FUNCTION increment_listing_views(listing_uuid UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE listings
  SET views = views + 1,
      last_viewed_at = NOW()
  WHERE id = listing_uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Expire featured listings
CREATE OR REPLACE FUNCTION expire_featured_listings()
RETURNS VOID AS $$
BEGIN
  UPDATE listings
  SET is_featured = FALSE,
      plan_type = 'free'
  WHERE is_featured = TRUE
    AND featured_until < NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================
-- 6. SEED DATA
-- ============================================

-- Insert root "Global" location
INSERT INTO locations (name, slug, level) VALUES
('Global', 'global', 'global');

-- Get the Global ID for parent references
DO $$
DECLARE
  global_id UUID;
  north_america_id UUID;
  europe_id UUID;
  asia_id UUID;
  usa_id UUID;
  uk_id UUID;
  singapore_id UUID;
  texas_id UUID;
  california_id UUID;
  england_id UUID;
BEGIN
  -- Get Global ID
  SELECT id INTO global_id FROM locations WHERE slug = 'global';
  
  -- Insert Regions
  INSERT INTO locations (name, slug, level, parent_id) VALUES
    ('North America', 'north-america', 'region', global_id),
    ('Europe', 'europe', 'region', global_id),
    ('Asia', 'asia', 'region', global_id)
  RETURNING id INTO north_america_id, europe_id, asia_id;
  
  -- Get region IDs
  SELECT id INTO north_america_id FROM locations WHERE slug = 'north-america';
  SELECT id INTO europe_id FROM locations WHERE slug = 'europe';
  SELECT id INTO asia_id FROM locations WHERE slug = 'asia';
  
  -- Insert Countries
  INSERT INTO locations (name, slug, level, parent_id) VALUES
    ('United States', 'united-states', 'country', north_america_id),
    ('United Kingdom', 'united-kingdom', 'country', europe_id),
    ('Singapore', 'singapore', 'country', asia_id);
  
  -- Get country IDs
  SELECT id INTO usa_id FROM locations WHERE slug = 'united-states';
  SELECT id INTO uk_id FROM locations WHERE slug = 'united-kingdom';
  SELECT id INTO singapore_id FROM locations WHERE slug = 'singapore';
  
  -- Insert States/Regions
  INSERT INTO locations (name, slug, level, parent_id) VALUES
    ('Texas', 'texas', 'region', usa_id),
    ('California', 'california', 'region', usa_id),
    ('England', 'england', 'region', uk_id);
  
  -- Get state IDs
  SELECT id INTO texas_id FROM locations WHERE slug = 'texas';
  SELECT id INTO california_id FROM locations WHERE slug = 'california';
  SELECT id INTO england_id FROM locations WHERE slug = 'england';
  
  -- Insert Cities
  INSERT INTO locations (name, slug, level, parent_id, latitude, longitude) VALUES
    ('Houston', 'houston', 'city', texas_id, 29.7604, -95.3698),
    ('San Francisco', 'san-francisco', 'city', california_id, 37.7749, -122.4194),
    ('London', 'london', 'city', england_id, 51.5074, -0.1278),
    ('Singapore', 'singapore-city', 'city', singapore_id, 1.3521, 103.8198);
END $$;

-- Insert Categories
INSERT INTO categories (name, slug, description, icon, display_order) VALUES
  ('Oil & Gas Testing', 'oil-gas-testing', 'Pipeline testing, corrosion analysis, weld testing, NDT inspection', 'beaker', 1),
  ('Pharmaceutical Testing', 'pharmaceutical-testing', 'GMP compliance, stability testing, analytical testing', 'pills', 2),
  ('Biotech Testing', 'biotech-testing', 'Bioanalytical testing, cell culture, biocompatibility', 'dna', 3),
  ('Environmental Testing', 'environmental-testing', 'Water quality, soil testing, air quality analysis', 'leaf', 4),
  ('Materials Testing', 'materials-testing', 'Metallurgical testing, polymer analysis, failure analysis', 'cube', 5);

-- Insert Custom Fields for Oil & Gas Testing
DO $$
DECLARE
  oil_gas_id UUID;
BEGIN
  SELECT id INTO oil_gas_id FROM categories WHERE slug = 'oil-gas-testing';
  
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, is_required, is_searchable, display_order) VALUES
    (oil_gas_id, 'iso_17025', 'ISO 17025 Accredited', 'boolean', false, true, 1),
    (oil_gas_id, 'asme_certified', 'ASME Certified', 'boolean', false, true, 2),
    (oil_gas_id, 'turnaround_time', 'Standard Turnaround Time', 'select', false, true, 3),
    (oil_gas_id, 'testing_capabilities', 'Testing Capabilities', 'multi_select', false, true, 4),
    (oil_gas_id, 'onsite_testing', 'On-site Testing Available', 'boolean', false, true, 5);
  
  -- Update turnaround_time options
  UPDATE custom_fields
  SET options = '["Same Day", "24 Hours", "48 Hours", "1 Week", "2+ Weeks"]'::jsonb
  WHERE field_name = 'turnaround_time';
  
  -- Update testing_capabilities options
  UPDATE custom_fields
  SET options = '["Pipeline Integrity", "Corrosion Testing", "Weld Testing", "NDT Inspection", "Material Analysis", "Pressure Testing", "Chemical Analysis"]'::jsonb
  WHERE field_name = 'testing_capabilities';
END $$;

-- ============================================
-- 7. COMPLETION MESSAGE
-- ============================================

DO $$
BEGIN
  RAISE NOTICE '✅ tstr.directory database setup complete!';
  RAISE NOTICE '';
  RAISE NOTICE 'Created:';
  RAISE NOTICE '  - 12 tables with RLS policies';
  RAISE NOTICE '  - 5 categories (Oil & Gas, Pharma, Biotech, Environmental, Materials)';
  RAISE NOTICE '  - Global → Region → Country → City location hierarchy';
  RAISE NOTICE '  - Custom fields for Oil & Gas Testing';
  RAISE NOTICE '';
  RAISE NOTICE 'Next steps:';
  RAISE NOTICE '  1. Create your admin user in Supabase Auth';
  RAISE NOTICE '  2. Update your profile role to "admin" in user_profiles table';
  RAISE NOTICE '  3. Get your anon key and service key from Project Settings';
  RAISE NOTICE '  4. Initialize the Astro frontend';
END $$;
