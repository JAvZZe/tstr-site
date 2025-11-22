-- ============================================
-- Universal Standards-Based Search System
-- Date: 2025-11-20
-- Purpose: Enable search by certifications/standards across ALL testing categories
-- ============================================

-- ============================================
-- 1. STANDARDS TABLE
-- ============================================
-- Stores testing standards, certifications, and test methods
-- Examples: ISO 19880-3, ASTM D7042, SAE J2601, USP, GMP, API 571

CREATE TABLE standards (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- Core identification
  code TEXT NOT NULL UNIQUE,                    -- "ISO 19880-3", "ASTM D7042", "USP <797>"
  name TEXT NOT NULL,                           -- "Hydrogen Valves Testing", "Jet Fuel Flash Point"
  description TEXT,                             -- Full description of what this standard covers
  
  -- Classification
  issuing_body TEXT,                            -- "ISO", "ASTM", "SAE", "FDA", "EPA", "API"
  category_id UUID REFERENCES categories(id),   -- Link to industry category (optional)
  standard_type TEXT DEFAULT 'test_method' CHECK (
    standard_type IN ('test_method', 'certification', 'accreditation', 'compliance')
  ),
  
  -- Reference
  url TEXT,                                     -- Link to official standard documentation
  revision TEXT,                                -- "2016", "Rev A", "Amendment 2"
  
  -- Metadata
  is_active BOOLEAN DEFAULT TRUE,               -- FALSE if standard is deprecated
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 2. LISTING CAPABILITIES TABLE
-- ============================================
-- Junction table linking listings to standards they can perform
-- Stores technical specifications as flexible JSONB

CREATE TABLE listing_capabilities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  
  -- Relations
  listing_id UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
  standard_id UUID NOT NULL REFERENCES standards(id) ON DELETE CASCADE,
  
  -- Technical specifications (flexible per category)
  -- Examples:
  -- Hydrogen: {"max_pressure_bar": 700, "state": "gaseous", "equipment": ["blast_bunker", "cryostat"]}
  -- Pharma: {"gmp_certified": true, "sterility_class": "Class 100", "fda_registered": true}
  -- Materials: {"temperature_range_c": [-196, 1000], "materials": ["titanium", "inconel"]}
  specifications JSONB DEFAULT '{}',
  
  -- Verification status
  verified BOOLEAN DEFAULT FALSE,               -- Admin verified this capability
  verified_at TIMESTAMPTZ,
  verified_by UUID REFERENCES auth.users(id),
  
  -- Additional info
  notes TEXT,                                   -- Internal notes, evidence of capability
  display_order INTEGER DEFAULT 0,              -- For sorting on listing pages
  
  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Ensure each listing can only claim each standard once
  UNIQUE(listing_id, standard_id)
);

-- ============================================
-- 3. INDEXES FOR SEARCH PERFORMANCE
-- ============================================

-- Fast lookup of all capabilities for a standard
CREATE INDEX idx_capabilities_standard ON listing_capabilities(standard_id);

-- Fast lookup of all capabilities for a listing
CREATE INDEX idx_capabilities_listing ON listing_capabilities(listing_id);

-- Enable JSONB search on specifications
CREATE INDEX idx_capabilities_specs ON listing_capabilities USING GIN(specifications);

-- Standard search by code (exact match)
CREATE INDEX idx_standards_code ON standards(code);

-- Standard search by issuing body
CREATE INDEX idx_standards_issuing_body ON standards(issuing_body);

-- Category-specific standards
CREATE INDEX idx_standards_category ON standards(category_id);

-- Active standards only (for frontend dropdowns)
CREATE INDEX idx_standards_active ON standards(is_active) WHERE is_active = TRUE;

-- ============================================
-- 4. ROW LEVEL SECURITY (RLS)
-- ============================================

-- Enable RLS on new tables
ALTER TABLE standards ENABLE ROW LEVEL SECURITY;
ALTER TABLE listing_capabilities ENABLE ROW LEVEL SECURITY;

-- Standards: Public read, admin write
CREATE POLICY "Standards are publicly readable"
  ON standards FOR SELECT
  USING (TRUE);

CREATE POLICY "Admins can manage standards"
  ON standards FOR ALL
  USING (auth.role() = 'authenticated');

-- Listing capabilities: Public read, owners can manage their own
CREATE POLICY "Capabilities are publicly readable"
  ON listing_capabilities FOR SELECT
  USING (TRUE);

CREATE POLICY "Listing owners can manage their capabilities"
  ON listing_capabilities FOR ALL
  USING (
    listing_id IN (
      SELECT id FROM listings WHERE owner_id = auth.uid()
    )
  );

CREATE POLICY "Admins can manage all capabilities"
  ON listing_capabilities FOR ALL
  USING (auth.role() = 'authenticated');

-- ============================================
-- 5. HELPER FUNCTIONS
-- ============================================

-- Function to search listings by standard with technical filters
CREATE OR REPLACE FUNCTION search_by_standard(
  p_standard_code TEXT,
  p_category_id UUID DEFAULT NULL,
  p_min_specs JSONB DEFAULT '{}'
)
RETURNS TABLE (
  listing_id UUID,
  business_name TEXT,
  website TEXT,
  standard_code TEXT,
  standard_name TEXT,
  specifications JSONB
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    l.id AS listing_id,
    l.business_name,
    l.website,
    s.code AS standard_code,
    s.name AS standard_name,
    lc.specifications
  FROM listings l
  JOIN listing_capabilities lc ON l.id = lc.listing_id
  JOIN standards s ON lc.standard_id = s.id
  WHERE 
    s.code = p_standard_code
    AND (p_category_id IS NULL OR l.category_id = p_category_id)
    AND l.status = 'active'
    AND lc.specifications @> p_min_specs  -- JSONB contains operator
  ORDER BY 
    lc.verified DESC,  -- Verified capabilities first
    l.is_featured DESC,
    l.created_at DESC;
END;
$$ LANGUAGE plpgsql STABLE;

-- ============================================
-- 6. COMMENTS FOR DOCUMENTATION
-- ============================================

COMMENT ON TABLE standards IS 'Testing standards, certifications, and test methods across all industries';
COMMENT ON TABLE listing_capabilities IS 'Links listings to standards they can perform, with technical specifications';
COMMENT ON COLUMN listing_capabilities.specifications IS 'Flexible JSONB field for category-specific technical metadata';
COMMENT ON FUNCTION search_by_standard IS 'Search listings by standard code with optional technical specification filters';

-- ============================================
-- Migration Complete
-- ============================================
-- Next steps:
-- 1. Apply migration: supabase db push --linked
-- 2. Seed initial standards data
-- 3. Build search API endpoint
-- 4. Create frontend search interface
