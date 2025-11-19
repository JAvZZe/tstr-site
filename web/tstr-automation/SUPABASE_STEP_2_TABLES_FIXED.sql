-- ============================================
-- TSTR.site Database Setup - STEP 2: CREATE TABLES
-- ============================================
-- Run this AFTER Step 1 completes successfully

-- Global → Region → Country → City hierarchy
CREATE TABLE IF NOT EXISTS locations (
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

-- Industry categories
CREATE TABLE IF NOT EXISTS categories (
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

-- Industry-specific custom fields
CREATE TABLE IF NOT EXISTS custom_fields (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
  field_name TEXT NOT NULL,
  field_label TEXT NOT NULL,
  field_type TEXT NOT NULL CHECK (field_type IN ('text', 'number', 'boolean', 'select', 'multi_select', 'date', 'url')),
  options JSONB,
  is_required BOOLEAN DEFAULT FALSE,
  is_searchable BOOLEAN DEFAULT TRUE,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Business listings
CREATE TABLE IF NOT EXISTS listings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  owner_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  category_id UUID REFERENCES categories(id) NOT NULL,
  location_id UUID REFERENCES locations(id) NOT NULL,
  
  business_name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  website TEXT,
  email TEXT,
  phone TEXT,
  address TEXT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  
  plan_type TEXT DEFAULT 'free' CHECK (plan_type IN ('free', 'basic', 'featured', 'premium')),
  is_featured BOOLEAN DEFAULT FALSE,
  featured_until TIMESTAMPTZ,
  
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'expired', 'suspended')),
  verified BOOLEAN DEFAULT FALSE,
  claimed BOOLEAN DEFAULT FALSE,
  
  views INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ
);

-- Custom field values per listing
CREATE TABLE IF NOT EXISTS listing_custom_fields (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  custom_field_id UUID REFERENCES custom_fields(id) ON DELETE CASCADE,
  value JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(listing_id, custom_field_id)
);

-- Listing images
CREATE TABLE IF NOT EXISTS listing_images (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  is_primary BOOLEAN DEFAULT FALSE,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Payment tracking
CREATE TABLE IF NOT EXISTS payments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE SET NULL,
  owner_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  
  amount DECIMAL(10, 2) NOT NULL,
  currency TEXT DEFAULT 'GBP',
  payment_method TEXT CHECK (payment_method IN ('bank_transfer', 'paypal', 'bitcoin', 'stripe')),
  
  reference_number TEXT,
  proof_image_url TEXT,
  
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'rejected', 'refunded')),
  verified_by UUID REFERENCES auth.users(id),
  verified_at TIMESTAMPTZ,
  
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Search analytics
CREATE TABLE IF NOT EXISTS search_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  query TEXT,
  filters JSONB,
  results_count INTEGER,
  ip_hash TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- SUCCESS: Once complete, proceed to STEP_3_INDEXES.sql
