-- ============================================
-- VERIFY CUSTOM FIELDS MIGRATION
-- Confirms that custom fields were added correctly for all 4 testing niches
-- Created: 2025-11-01
-- ============================================

-- ============================================
-- 1. COUNT CUSTOM FIELDS PER CATEGORY
-- ============================================
SELECT
  c.name AS category_name,
  c.slug AS category_slug,
  COUNT(cf.id) AS custom_fields_count
FROM categories c
LEFT JOIN custom_fields cf ON c.id = cf.category_id
WHERE c.slug IN ('oil-gas-testing', 'pharmaceutical-testing', 'environmental-testing', 'materials-testing')
GROUP BY c.id, c.name, c.slug
ORDER BY c.name;

-- Expected results:
-- Environmental Testing: 7 fields
-- Materials Testing: 7 fields
-- Oil & Gas Testing: 7 fields
-- Pharmaceutical Testing: 7 fields

-- ============================================
-- 2. DETAILED VIEW OF OIL & GAS TESTING FIELDS
-- ============================================
SELECT
  cf.field_name,
  cf.field_label,
  cf.field_type,
  cf.is_required,
  cf.is_searchable,
  cf.display_order,
  cf.options
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug = 'oil-gas-testing'
ORDER BY cf.display_order;

-- Expected fields:
-- testing_types (multi_select) - ["Well Logging", "Production Testing", "Flow Assurance", "Pressure Testing", "NDT Inspection"]
-- real_time_analytics (boolean)
-- equipment_brands (text)
-- coverage_type (multi_select) - ["Onshore", "Offshore", "Both"]
-- certifications (multi_select) - ["API", "ISO 17025", "ASME"]
-- rapid_deployment (boolean)
-- recent_projects (text)

-- ============================================
-- 3. DETAILED VIEW OF PHARMACEUTICAL TESTING FIELDS
-- ============================================
SELECT
  cf.field_name,
  cf.field_label,
  cf.field_type,
  cf.is_required,
  cf.is_searchable,
  cf.display_order,
  cf.options
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug = 'pharmaceutical-testing'
ORDER BY cf.display_order;

-- Expected fields:
-- analytical_techniques (multi_select) - ["HPLC", "Mass Spectrometry", "GC-MS", "Microbial Testing", "ELISA"]
-- drug_specializations (multi_select) - ["Biologics", "Small Molecules", "Gene Therapy", "Vaccines"]
-- regulatory_compliance (multi_select) - ["FDA", "EMA", "GMP", "GLP"]
-- lab_accreditations (multi_select) - ["ISO 17025", "CAP", "CLIA"]
-- turnaround_time (select) - ["Same Day", "24 Hours", "48 Hours", "1 Week", "2+ Weeks"]
-- electronic_reporting (boolean)
-- consultancy_services (text)

-- ============================================
-- 4. DETAILED VIEW OF ENVIRONMENTAL TESTING FIELDS
-- ============================================
SELECT
  cf.field_name,
  cf.field_label,
  cf.field_type,
  cf.is_required,
  cf.is_searchable,
  cf.display_order,
  cf.options
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug = 'environmental-testing'
ORDER BY cf.display_order;

-- Expected fields:
-- test_types (multi_select) - ["Water Quality", "Soil Testing", "Air Quality", "Noise", "Asbestos"]
-- field_lab_services (multi_select) - ["Field Only", "Lab Only", "Both"]
-- esg_reporting (boolean)
-- sampling_equipment (text)
-- compliance_standards (multi_select) - ["ISO 14001", "EPA", "NELAC"]
-- monitoring_tech (text)
-- custom_programs (boolean)

-- ============================================
-- 5. DETAILED VIEW OF MATERIALS TESTING FIELDS
-- ============================================
SELECT
  cf.field_name,
  cf.field_label,
  cf.field_type,
  cf.is_required,
  cf.is_searchable,
  cf.display_order,
  cf.options
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug = 'materials-testing'
ORDER BY cf.display_order;

-- Expected fields:
-- material_types (multi_select) - ["Metals", "Polymers", "Composites", "Nanomaterials", "Ceramics"]
-- test_procedures (multi_select) - ["Tensile Testing", "Fatigue Testing", "Corrosion Testing", "Hardness Testing", "Failure Analysis"]
-- instrumentation (text)
-- industry_sectors (multi_select) - ["Aerospace", "Automotive", "Semiconductor", "Medical Device"]
-- custom_test_dev (boolean)
-- rd_capabilities (text)
-- project_lead_time (select) - ["Same Day", "1-3 Days", "1 Week", "2-4 Weeks", "1+ Month"]

-- ============================================
-- 6. VALIDATE JSON OPTIONS FORMAT
-- ============================================
-- Check that all multi_select and select fields have valid JSON options
SELECT
  c.slug AS category_slug,
  cf.field_name,
  cf.field_type,
  cf.options,
  CASE
    WHEN cf.field_type IN ('multi_select', 'select') AND cf.options IS NULL THEN 'MISSING OPTIONS'
    WHEN cf.field_type IN ('multi_select', 'select') AND jsonb_array_length(cf.options) = 0 THEN 'EMPTY OPTIONS'
    WHEN cf.field_type IN ('multi_select', 'select') THEN 'OK'
    ELSE 'N/A'
  END AS validation_status
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug IN ('oil-gas-testing', 'pharmaceutical-testing', 'environmental-testing', 'materials-testing')
  AND cf.field_type IN ('multi_select', 'select')
ORDER BY c.slug, cf.display_order;

-- Expected: All rows should have validation_status = 'OK'

-- ============================================
-- 7. SUMMARY STATISTICS
-- ============================================
SELECT
  'Total Custom Fields' AS metric,
  COUNT(*) AS value
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug IN ('oil-gas-testing', 'pharmaceutical-testing', 'environmental-testing', 'materials-testing')

UNION ALL

SELECT
  'Fields with Options' AS metric,
  COUNT(*) AS value
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug IN ('oil-gas-testing', 'pharmaceutical-testing', 'environmental-testing', 'materials-testing')
  AND cf.options IS NOT NULL

UNION ALL

SELECT
  'Searchable Fields' AS metric,
  COUNT(*) AS value
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug IN ('oil-gas-testing', 'pharmaceutical-testing', 'environmental-testing', 'materials-testing')
  AND cf.is_searchable = TRUE

UNION ALL

SELECT
  'Required Fields' AS metric,
  COUNT(*) AS value
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug IN ('oil-gas-testing', 'pharmaceutical-testing', 'environmental-testing', 'materials-testing')
  AND cf.is_required = TRUE;

-- Expected summary:
-- Total Custom Fields: 28 (7 per category × 4 categories)
-- Fields with Options: 16 (all multi_select and select fields)
-- Searchable Fields: ~24 (most fields except text descriptions)
-- Required Fields: 0 (all optional for now)

-- ============================================
-- 8. CHECK FOR DUPLICATES
-- ============================================
SELECT
  c.slug AS category_slug,
  cf.field_name,
  COUNT(*) AS duplicate_count
FROM custom_fields cf
JOIN categories c ON cf.category_id = c.id
WHERE c.slug IN ('oil-gas-testing', 'pharmaceutical-testing', 'environmental-testing', 'materials-testing')
GROUP BY c.slug, cf.field_name
HAVING COUNT(*) > 1;

-- Expected: No rows (no duplicates)

-- ============================================
-- VERIFICATION COMPLETE
-- ============================================
-- If all queries above return expected results, the migration was successful
