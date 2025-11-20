-- ============================================
-- Initial Standards Seed Data
-- Date: 2025-11-20
-- Purpose: Populate standards table with high-value testing standards across all categories
-- ============================================

-- Get category IDs first (we'll need these)
-- Note: Run this to see your category IDs: SELECT id, name, slug FROM categories;

-- ============================================
-- HYDROGEN TESTING STANDARDS
-- ============================================

INSERT INTO standards (code, name, description, issuing_body, standard_type, url) VALUES
('ISO 19880-3', 'Hydrogen Fuelling Stations - Part 3: Valves', 'Testing requirements for valves used in hydrogen fueling infrastructure, covering pressure ratings up to 1000 bar', 'ISO', 'test_method', 'https://www.iso.org/standard/71940.html'),
('SAE J2601', 'Fueling Protocols for Light Duty Gaseous Hydrogen Surface Vehicles', 'Standardized hydrogen fueling protocol for vehicles, ensuring safe and efficient refueling', 'SAE', 'test_method', 'https://www.sae.org/standards/content/j2601_202005/'),
('ISO 11114-1', 'Transportable Gas Cylinders - Compatibility of Materials - Part 1: Metallic Materials', 'Testing for hydrogen embrittlement and material compatibility with high-pressure hydrogen', 'ISO', 'test_method', 'https://www.iso.org/standard/50510.html'),
('ISO 14687', 'Hydrogen Fuel Quality - Product Specification', 'Purity analysis and quality testing for hydrogen fuel used in vehicles and fuel cells', 'ISO', 'test_method', 'https://www.iso.org/standard/69539.html'),
('ISO 19881', 'Hydrogen Fuel - Land Vehicle Fueling System Interface', 'Testing of fueling connectors and interfaces for hydrogen vehicles', 'ISO', 'test_method', 'https://www.iso.org/standard/66627.html');

-- ============================================
-- OIL & GAS TESTING STANDARDS
-- ============================================

INSERT INTO standards (code, name, description, issuing_body, standard_type, url) VALUES
('API 571', 'Damage Mechanisms Affecting Fixed Equipment in the Refining Industry', 'Assessment and testing for corrosion, erosion, and other damage mechanisms in refinery equipment', 'API', 'test_method', 'https://www.api.org/products-and-services/individual-certification-programs/api-571'),
('API 580', 'Risk-Based Inspection', 'Testing and inspection methodology for pressure vessels and piping systems', 'API', 'test_method', 'https://www.api.org/products-and-services/individual-certification-programs/api-580'),
('ISO 17020', 'Conformity Assessment - Requirements for Bodies Performing Inspection', 'Accreditation standard for inspection bodies in oil & gas industry', 'ISO', 'accreditation', 'https://www.iso.org/standard/52994.html'),
('ASTM D7042', 'Standard Test Method for Dynamic Viscosity and Density of Liquids', 'Viscosity testing for crude oil, fuel oils, and petroleum products', 'ASTM', 'test_method', 'https://www.astm.org/d7042-21.html'),
('NACE MR0175', 'Petroleum and Natural Gas Industries - Materials for Use in H2S-Containing Environments', 'Testing for sour gas service material compatibility', 'NACE', 'test_method', 'https://www.nace.org/standards');

-- ============================================
-- PHARMACEUTICAL TESTING STANDARDS
-- ============================================

INSERT INTO standards (code, name, description, issuing_body, standard_type, url) VALUES
('USP <797>', 'Pharmaceutical Compounding - Sterile Preparations', 'Testing and quality standards for sterile pharmaceutical preparations', 'USP', 'compliance', 'https://www.usp.org/compounding/general-chapter-797'),
('USP <71>', 'Sterility Tests', 'Microbiological testing methods for pharmaceutical products', 'USP', 'test_method', 'https://www.usp.org/'),
('FDA 21 CFR Part 211', 'Current Good Manufacturing Practice for Finished Pharmaceuticals', 'cGMP compliance testing and validation requirements', 'FDA', 'compliance', 'https://www.fda.gov/'),
('ISO 13485', 'Medical Devices - Quality Management Systems', 'Quality management system requirements for medical device testing', 'ISO', 'certification', 'https://www.iso.org/standard/59752.html'),
('ICH Q7', 'Good Manufacturing Practice Guide for Active Pharmaceutical Ingredients', 'GMP testing and validation for API production', 'ICH', 'compliance', 'https://www.ich.org/');

-- ============================================
-- BIOTECH TESTING STANDARDS
-- ============================================

INSERT INTO standards (code, name, description, issuing_body, standard_type, url) VALUES
('ISO 10993', 'Biological Evaluation of Medical Devices', 'Biocompatibility testing for medical devices and biomaterials', 'ISO', 'test_method', 'https://www.iso.org/standard/68936.html'),
('FDA 21 CFR Part 210', 'Current Good Manufacturing Practice in Manufacturing', 'cGMP requirements for biologics and biotech products', 'FDA', 'compliance', 'https://www.fda.gov/'),
('ISO 20387', 'Biotechnology - Biobanking - General Requirements for Biobanking', 'Standards for biological sample storage and testing', 'ISO', 'test_method', 'https://www.iso.org/standard/67888.html'),
('USP <1046>', 'Cellular and Tissue-Based Products', 'Testing requirements for cell and gene therapy products', 'USP', 'test_method', 'https://www.usp.org/'),
('ISO 13408', 'Aseptic Processing of Health Care Products', 'Sterilization and aseptic processing validation', 'ISO', 'test_method', 'https://www.iso.org/standard/63532.html');

-- ============================================
-- ENVIRONMENTAL TESTING STANDARDS
-- ============================================

INSERT INTO standards (code, name, description, issuing_body, standard_type, url) VALUES
('EPA Method 1664', 'N-Hexane Extractable Material and Silica Gel Treated', 'Testing for oil and grease in water samples', 'EPA', 'test_method', 'https://www.epa.gov/'),
('ISO 17025', 'General Requirements for Competence of Testing and Calibration Laboratories', 'Accreditation standard for environmental testing laboratories', 'ISO', 'accreditation', 'https://www.iso.org/standard/66912.html'),
('ISO 14001', 'Environmental Management Systems', 'Environmental management certification for testing facilities', 'ISO', 'certification', 'https://www.iso.org/iso-14001-environmental-management.html'),
('ASTM D5174', 'Standard Test Method for Trace Uranium in Water by Pulsed-Laser Phosphorimetry', 'Heavy metal testing in environmental samples', 'ASTM', 'test_method', 'https://www.astm.org/'),
('EPA Method 8260', 'Volatile Organic Compounds by Gas Chromatography/Mass Spectrometry', 'VOC analysis in soil, water, and air samples', 'EPA', 'test_method', 'https://www.epa.gov/');

-- ============================================
-- MATERIALS TESTING STANDARDS
-- ============================================

INSERT INTO standards (code, name, description, issuing_body, standard_type, url) VALUES
('ASTM E8', 'Standard Test Methods for Tension Testing of Metallic Materials', 'Tensile strength and mechanical properties testing for metals', 'ASTM', 'test_method', 'https://www.astm.org/e0008_e0008m-22.html'),
('ISO 6892-1', 'Metallic Materials - Tensile Testing - Part 1: Method of Test at Room Temperature', 'International standard for tensile testing of metals', 'ISO', 'test_method', 'https://www.iso.org/standard/78322.html'),
('ASTM D638', 'Standard Test Method for Tensile Properties of Plastics', 'Tensile testing for plastic and polymer materials', 'ASTM', 'test_method', 'https://www.astm.org/d0638-14.html'),
('ISO 148-1', 'Metallic Materials - Charpy Pendulum Impact Test', 'Impact testing for material toughness and fracture resistance', 'ISO', 'test_method', 'https://www.iso.org/standard/63802.html'),
('ASTM E3', 'Standard Guide for Preparation of Metallographic Specimens', 'Metallography and microstructure analysis procedures', 'ASTM', 'test_method', 'https://www.astm.org/e0003-11r17.html');

-- ============================================
-- Summary
-- ============================================
-- Total standards inserted: 30
-- Coverage:
--   - Hydrogen: 5 standards
--   - Oil & Gas: 5 standards
--   - Pharmaceutical: 5 standards
--   - Biotech: 5 standards
--   - Environmental: 5 standards
--   - Materials: 5 standards
--
-- Next steps:
-- 1. Verify: SELECT code, name, issuing_body FROM standards ORDER BY issuing_body, code;
-- 2. Link to categories if needed: UPDATE standards SET category_id = '...' WHERE code IN (...);
-- 3. Create listing_capabilities entries to link labs to these standards
