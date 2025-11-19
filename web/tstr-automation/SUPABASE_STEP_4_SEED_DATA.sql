-- ============================================
-- TSTR.site Database Setup - STEP 4: SEED DATA
-- ============================================
-- This adds your initial categories and locations
-- Run this AFTER Step 3 completes successfully

-- Insert Global location (root of hierarchy)
INSERT INTO locations (name, slug, level, parent_id)
VALUES ('Global', 'global', 'global', NULL)
ON CONFLICT (slug) DO NOTHING;

-- Get the Global location ID for use as parent
DO $$
DECLARE
  global_id UUID;
  north_america_id UUID;
  europe_id UUID;
  asia_id UUID;
  usa_id UUID;
  uk_id UUID;
  singapore_id UUID;
BEGIN
  -- Get Global ID
  SELECT id INTO global_id FROM locations WHERE slug = 'global';
  
  -- Insert Regions
  INSERT INTO locations (name, slug, level, parent_id)
  VALUES ('North America', 'north-america', 'region', global_id)
  ON CONFLICT (slug) DO NOTHING
  RETURNING id INTO north_america_id;
  
  IF north_america_id IS NULL THEN
    SELECT id INTO north_america_id FROM locations WHERE slug = 'north-america';
  END IF;
  
  INSERT INTO locations (name, slug, level, parent_id)
  VALUES ('Europe', 'europe', 'region', global_id)
  ON CONFLICT (slug) DO NOTHING
  RETURNING id INTO europe_id;
  
  IF europe_id IS NULL THEN
    SELECT id INTO europe_id FROM locations WHERE slug = 'europe';
  END IF;
  
  INSERT INTO locations (name, slug, level, parent_id)
  VALUES ('Asia', 'asia', 'region', global_id)
  ON CONFLICT (slug) DO NOTHING
  RETURNING id INTO asia_id;
  
  IF asia_id IS NULL THEN
    SELECT id INTO asia_id FROM locations WHERE slug = 'asia';
  END IF;
  
  -- Insert Countries
  INSERT INTO locations (name, slug, level, parent_id)
  VALUES ('United States', 'united-states', 'country', north_america_id)
  ON CONFLICT (slug) DO NOTHING
  RETURNING id INTO usa_id;
  
  IF usa_id IS NULL THEN
    SELECT id INTO usa_id FROM locations WHERE slug = 'united-states';
  END IF;
  
  INSERT INTO locations (name, slug, level, parent_id)
  VALUES ('United Kingdom', 'united-kingdom', 'country', europe_id)
  ON CONFLICT (slug) DO NOTHING
  RETURNING id INTO uk_id;
  
  IF uk_id IS NULL THEN
    SELECT id INTO uk_id FROM locations WHERE slug = 'united-kingdom';
  END IF;
  
  INSERT INTO locations (name, slug, level, parent_id)
  VALUES ('Singapore', 'singapore', 'country', asia_id)
  ON CONFLICT (slug) DO NOTHING
  RETURNING id INTO singapore_id;
  
  IF singapore_id IS NULL THEN
    SELECT id INTO singapore_id FROM locations WHERE slug = 'singapore';
  END IF;
  
  -- Insert Cities
  INSERT INTO locations (name, slug, level, parent_id, latitude, longitude)
  VALUES 
    ('Houston', 'united-states-houston', 'city', usa_id, 29.7604, -95.3698),
    ('San Francisco', 'united-states-san-francisco', 'city', usa_id, 37.7749, -122.4194),
    ('New York', 'united-states-new-york', 'city', usa_id, 40.7128, -74.0060),
    ('London', 'united-kingdom-london', 'city', uk_id, 51.5074, -0.1278),
    ('Singapore', 'singapore-singapore', 'city', singapore_id, 1.3521, 103.8198)
  ON CONFLICT (slug) DO NOTHING;
  
END $$;

-- Insert Categories
INSERT INTO categories (name, slug, description, display_order)
VALUES
  ('Oil & Gas Testing', 'oil-gas-testing', 'Pipeline integrity, corrosion analysis, NDT inspection, petroleum testing', 1),
  ('Pharmaceutical Testing', 'pharmaceutical-testing', 'GMP compliance, stability testing, method validation, impurity analysis', 2),
  ('Biotech Testing', 'biotech-testing', 'Bioanalytical services, cell culture testing, biologics characterization', 3),
  ('Environmental Testing', 'environmental-testing', 'Water quality, soil contamination, air quality, hazardous waste analysis', 4),
  ('Materials Testing', 'materials-testing', 'Metals, polymers, composites, failure analysis, mechanical testing', 5)
ON CONFLICT (slug) DO NOTHING;

-- SUCCESS: Database is now ready!
-- Next step: Test by running a simple query in a new SQL window:
-- SELECT * FROM categories;
