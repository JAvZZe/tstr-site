-- ============================================
-- TSTR.site Custom Fields Migration
-- Add niche-specific custom fields for 4 testing categories
-- Created: 2025-11-01
-- Track B: Custom Fields SQL for Testing Niches
-- ============================================

-- ============================================
-- 1. OIL & GAS TESTING CUSTOM FIELDS
-- ============================================
DO $$
DECLARE
  oil_gas_id UUID;
BEGIN
  -- Get category ID
  SELECT id INTO oil_gas_id FROM categories WHERE slug = 'oil-gas-testing';

  IF oil_gas_id IS NULL THEN
    RAISE EXCEPTION 'Category oil-gas-testing not found';
  END IF;

  -- Insert custom fields
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, is_required, is_searchable, display_order) VALUES
    (oil_gas_id, 'testing_types', 'Testing Types', 'multi_select', false, true, 1),
    (oil_gas_id, 'real_time_analytics', 'Real-Time Analytics', 'boolean', false, true, 2),
    (oil_gas_id, 'equipment_brands', 'Equipment Brands/Models', 'text', false, true, 3),
    (oil_gas_id, 'coverage_type', 'Coverage Type', 'multi_select', false, true, 4),
    (oil_gas_id, 'certifications', 'Certifications', 'multi_select', false, true, 5),
    (oil_gas_id, 'rapid_deployment', 'Rapid Deployment Capable', 'boolean', false, true, 6),
    (oil_gas_id, 'recent_projects', 'Recent Projects/Case Studies', 'text', false, false, 7);

  -- Update options for multi_select fields
  UPDATE custom_fields
  SET options = '["Well Logging", "Production Testing", "Flow Assurance", "Pressure Testing", "NDT Inspection"]'::jsonb
  WHERE category_id = oil_gas_id AND field_name = 'testing_types';

  UPDATE custom_fields
  SET options = '["Onshore", "Offshore", "Both"]'::jsonb
  WHERE category_id = oil_gas_id AND field_name = 'coverage_type';

  UPDATE custom_fields
  SET options = '["API", "ISO 17025", "ASME"]'::jsonb
  WHERE category_id = oil_gas_id AND field_name = 'certifications';

  RAISE NOTICE 'Oil & Gas Testing custom fields added successfully';
END $$;

-- ============================================
-- 2. PHARMACEUTICAL TESTING CUSTOM FIELDS
-- ============================================
DO $$
DECLARE
  pharma_id UUID;
BEGIN
  -- Get category ID
  SELECT id INTO pharma_id FROM categories WHERE slug = 'pharmaceutical-testing';

  IF pharma_id IS NULL THEN
    RAISE EXCEPTION 'Category pharmaceutical-testing not found';
  END IF;

  -- Insert custom fields
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, is_required, is_searchable, display_order) VALUES
    (pharma_id, 'analytical_techniques', 'Analytical Techniques', 'multi_select', false, true, 1),
    (pharma_id, 'drug_specializations', 'Drug Type Specializations', 'multi_select', false, true, 2),
    (pharma_id, 'regulatory_compliance', 'Regulatory Compliance', 'multi_select', false, true, 3),
    (pharma_id, 'lab_accreditations', 'Laboratory Accreditations', 'multi_select', false, true, 4),
    (pharma_id, 'turnaround_time', 'Test Turnaround Time', 'select', false, true, 5),
    (pharma_id, 'electronic_reporting', 'Electronic Data Reporting', 'boolean', false, true, 6),
    (pharma_id, 'consultancy_services', 'Consultancy Services Offered', 'text', false, false, 7);

  -- Update options for multi_select and select fields
  UPDATE custom_fields
  SET options = '["HPLC", "Mass Spectrometry", "GC-MS", "Microbial Testing", "ELISA"]'::jsonb
  WHERE category_id = pharma_id AND field_name = 'analytical_techniques';

  UPDATE custom_fields
  SET options = '["Biologics", "Small Molecules", "Gene Therapy", "Vaccines"]'::jsonb
  WHERE category_id = pharma_id AND field_name = 'drug_specializations';

  UPDATE custom_fields
  SET options = '["FDA", "EMA", "GMP", "GLP"]'::jsonb
  WHERE category_id = pharma_id AND field_name = 'regulatory_compliance';

  UPDATE custom_fields
  SET options = '["ISO 17025", "CAP", "CLIA"]'::jsonb
  WHERE category_id = pharma_id AND field_name = 'lab_accreditations';

  UPDATE custom_fields
  SET options = '["Same Day", "24 Hours", "48 Hours", "1 Week", "2+ Weeks"]'::jsonb
  WHERE category_id = pharma_id AND field_name = 'turnaround_time';

  RAISE NOTICE 'Pharmaceutical Testing custom fields added successfully';
END $$;

-- ============================================
-- 3. ENVIRONMENTAL TESTING CUSTOM FIELDS
-- ============================================
DO $$
DECLARE
  env_id UUID;
BEGIN
  -- Get category ID
  SELECT id INTO env_id FROM categories WHERE slug = 'environmental-testing';

  IF env_id IS NULL THEN
    RAISE EXCEPTION 'Category environmental-testing not found';
  END IF;

  -- Insert custom fields
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, is_required, is_searchable, display_order) VALUES
    (env_id, 'test_types', 'Test Types', 'multi_select', false, true, 1),
    (env_id, 'field_lab_services', 'Service Location', 'multi_select', false, true, 2),
    (env_id, 'esg_reporting', 'ESG Reporting Capabilities', 'boolean', false, true, 3),
    (env_id, 'sampling_equipment', 'Sampling Equipment', 'text', false, true, 4),
    (env_id, 'compliance_standards', 'Compliance Standards', 'multi_select', false, true, 5),
    (env_id, 'monitoring_tech', 'Monitoring Technology', 'text', false, false, 6),
    (env_id, 'custom_programs', 'Customized Test Programs', 'boolean', false, true, 7);

  -- Update options for multi_select fields
  UPDATE custom_fields
  SET options = '["Water Quality", "Soil Testing", "Air Quality", "Noise", "Asbestos"]'::jsonb
  WHERE category_id = env_id AND field_name = 'test_types';

  UPDATE custom_fields
  SET options = '["Field Only", "Lab Only", "Both"]'::jsonb
  WHERE category_id = env_id AND field_name = 'field_lab_services';

  UPDATE custom_fields
  SET options = '["ISO 14001", "EPA", "NELAC"]'::jsonb
  WHERE category_id = env_id AND field_name = 'compliance_standards';

  RAISE NOTICE 'Environmental Testing custom fields added successfully';
END $$;

-- ============================================
-- 4. MATERIALS TESTING CUSTOM FIELDS
-- ============================================
DO $$
DECLARE
  materials_id UUID;
BEGIN
  -- Get category ID
  SELECT id INTO materials_id FROM categories WHERE slug = 'materials-testing';

  IF materials_id IS NULL THEN
    RAISE EXCEPTION 'Category materials-testing not found';
  END IF;

  -- Insert custom fields
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, is_required, is_searchable, display_order) VALUES
    (materials_id, 'material_types', 'Material Types', 'multi_select', false, true, 1),
    (materials_id, 'test_procedures', 'Test Procedures', 'multi_select', false, true, 2),
    (materials_id, 'instrumentation', 'Instrumentation Specifications', 'text', false, true, 3),
    (materials_id, 'industry_sectors', 'Industry Sectors Served', 'multi_select', false, true, 4),
    (materials_id, 'custom_test_dev', 'Custom Test Development', 'boolean', false, true, 5),
    (materials_id, 'rd_capabilities', 'R&D Capabilities', 'text', false, false, 6),
    (materials_id, 'project_lead_time', 'Project Lead Time', 'select', false, true, 7);

  -- Update options for multi_select and select fields
  UPDATE custom_fields
  SET options = '["Metals", "Polymers", "Composites", "Nanomaterials", "Ceramics"]'::jsonb
  WHERE category_id = materials_id AND field_name = 'material_types';

  UPDATE custom_fields
  SET options = '["Tensile Testing", "Fatigue Testing", "Corrosion Testing", "Hardness Testing", "Failure Analysis"]'::jsonb
  WHERE category_id = materials_id AND field_name = 'test_procedures';

  UPDATE custom_fields
  SET options = '["Aerospace", "Automotive", "Semiconductor", "Medical Device"]'::jsonb
  WHERE category_id = materials_id AND field_name = 'industry_sectors';

  UPDATE custom_fields
  SET options = '["Same Day", "1-3 Days", "1 Week", "2-4 Weeks", "1+ Month"]'::jsonb
  WHERE category_id = materials_id AND field_name = 'project_lead_time';

  RAISE NOTICE 'Materials Testing custom fields added successfully';
END $$;

-- ============================================
-- 5. COMPLETION MESSAGE
-- ============================================
DO $$
DECLARE
  oil_gas_count INTEGER;
  pharma_count INTEGER;
  env_count INTEGER;
  materials_count INTEGER;
  total_count INTEGER;
BEGIN
  -- Count custom fields per category
  SELECT COUNT(*) INTO oil_gas_count
  FROM custom_fields cf
  JOIN categories c ON cf.category_id = c.id
  WHERE c.slug = 'oil-gas-testing';

  SELECT COUNT(*) INTO pharma_count
  FROM custom_fields cf
  JOIN categories c ON cf.category_id = c.id
  WHERE c.slug = 'pharmaceutical-testing';

  SELECT COUNT(*) INTO env_count
  FROM custom_fields cf
  JOIN categories c ON cf.category_id = c.id
  WHERE c.slug = 'environmental-testing';

  SELECT COUNT(*) INTO materials_count
  FROM custom_fields cf
  JOIN categories c ON cf.category_id = c.id
  WHERE c.slug = 'materials-testing';

  total_count := oil_gas_count + pharma_count + env_count + materials_count;

  RAISE NOTICE '';
  RAISE NOTICE '✅ Custom fields migration complete!';
  RAISE NOTICE '';
  RAISE NOTICE 'Custom fields added:';
  RAISE NOTICE '  - Oil & Gas Testing: % fields', oil_gas_count;
  RAISE NOTICE '  - Pharmaceutical Testing: % fields', pharma_count;
  RAISE NOTICE '  - Environmental Testing: % fields', env_count;
  RAISE NOTICE '  - Materials Testing: % fields', materials_count;
  RAISE NOTICE '  - TOTAL: % custom fields', total_count;
  RAISE NOTICE '';
  RAISE NOTICE 'Next steps:';
  RAISE NOTICE '  1. Verify custom fields with verify_custom_fields.sql';
  RAISE NOTICE '  2. Update frontend to display these fields';
  RAISE NOTICE '  3. Build niche-specific scrapers to populate data';
END $$;
