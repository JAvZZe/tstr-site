-- MIGRATION 0: Environmental sub-categories
INSERT INTO categories (id, name, slug, parent_id, description) VALUES
  (gen_random_uuid(), 'Air Quality Testing', 'environmental-testing/air-quality', 'a80a47e9-ca57-4712-9b55-d3139b98a6b7', 'Emissions testing, particulate matter analysis, and air monitoring services'),
  (gen_random_uuid(), 'Water Quality Testing', 'environmental-testing/water-quality', 'a80a47e9-ca57-4712-9b55-d3139b98a6b7', 'Drinking water testing, wastewater analysis, and groundwater monitoring'),
  (gen_random_uuid(), 'Soil Testing & Contamination', 'environmental-testing/soil-testing', 'a80a47e9-ca57-4712-9b55-d3139b98a6b7', 'Heavy metals testing, contamination analysis, and remediation assessment'),
  (gen_random_uuid(), 'Noise & Vibration Testing', 'environmental-testing/noise-vibration', 'a80a47e9-ca57-4712-9b55-d3139b98a6b7', 'Acoustic testing, noise monitoring, and vibration analysis services'),
  (gen_random_uuid(), 'ESG & Sustainability Testing', 'environmental-testing/esg-sustainability', 'a80a47e9-ca57-4712-9b55-d3139b98a6b7', 'Carbon footprint measurement, GHG emissions verification, and sustainability reporting')
ON CONFLICT (slug) DO NOTHING;

-- MIGRATION 1: Fix Standards Category Linkage
UPDATE standards
SET category_id = '2817126e-65fa-4ddf-8ec6-dbedb021001a'
WHERE code IN (
  'ISO 19880-3', 'ISO 19880-5', 'ISO 11114-4',
  'ISO 14687', 'ISO 19881', 'SAE J2601',
  'SAE J2579', 'CSA HGV 4.3', 'UN ECE R134'
);

-- MIGRATION 2: Add Hydrogen Category Description
UPDATE categories
SET description = 'Specialized testing for hydrogen infrastructure: valves, hoses, tanks, seals, and fuel systems. Search by ISO 19880 series, SAE J2601, UN ECE R134, and H2 embrittlement standards at 350–1000+ bar.'
WHERE id = '2817126e-65fa-4ddf-8ec6-dbedb021001a';

-- MIGRATION 3: Add H2 Browse Nodes
INSERT INTO categories (id, name, slug, parent_id, description) VALUES
  ('0076db0e-1d4e-4003-8060-eb978b5d94e4', 'Valve & Fitting Testing', 'hydrogen-infrastructure-testing/valve-fitting', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'ISO 19880-3 valve qualification at 700 bar. Pressure cycling, material compatibility, and leak testing.'),
  ('cdfaa06e-7c2e-4312-83fb-8143ad9024c9', 'Hose & Seal Testing', 'hydrogen-infrastructure-testing/hose-seal', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'ISO 19880-5 hose and permeation testing. Cryogenic-capable seal qualification at -253°C.'),
  ('5eccabc9-6e74-4584-a259-013b7fdcd646', 'Tank & Pressure Vessel Testing', 'hydrogen-infrastructure-testing/tank-pressure', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'Type III/IV composite tank testing per UN ECE R134. Burst and cycling tests up to 1000 bar.'),
  ('f29966a2-4753-451b-b354-d756c78a8d38', 'Hydrogen Embrittlement Testing', 'hydrogen-infrastructure-testing/embrittlement', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'ISO 11114-4 materials qualification. Metallurgical analysis of metals and elastomers under gaseous H2.'),
  ('508b108a-5563-4287-9078-0f8f1310951f', 'Hydrogen Purity Testing', 'hydrogen-infrastructure-testing/purity', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'ISO 14687 fuel quality specification. Impurity analysis for fuel-cell grade hydrogen.')
ON CONFLICT (slug) DO UPDATE SET id = EXCLUDED.id;

-- MIGRATION 4: Add 5 New Certification Standards
INSERT INTO standards (id, code, name, category_id, description, is_active) VALUES
  (gen_random_uuid(), 'ISO/TS 15916:2026', 'Basic Considerations for the Safety of Hydrogen Systems', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'Fundamental safety requirements for H2 system design, operation, and maintenance. Applicable across all hydrogen infrastructure sectors.', true),
  (gen_random_uuid(), 'TÜV H2-Ready', 'TÜV H2-Ready System Certification', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'European industry certification confirming equipment compatibility with hydrogen service. Issued by TÜV SÜD and TÜV Rheinland.', true),
  (gen_random_uuid(), 'RFNBO', 'Renewable Fuels of Non-Biological Origin', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'EU delegated regulation defining green hydrogen production requirements under Renewable Energy Directive (RED III). Required for EU subsidy and compliance.', true),
  (gen_random_uuid(), 'KGS AC113', 'KGS Compressed Hydrogen Fuel System Code', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'Korean Gas Safety approval code for compressed hydrogen systems in vehicles and fueling stations. Mandatory for Korean market access.', true),
  (gen_random_uuid(), 'CEN ISO 15156', 'Materials for Use in H2S-Containing Environments', '2817126e-65fa-4ddf-8ec6-dbedb021001a', 'Material selection standard for sour service environments. Frequently co-tested in hydrogen infrastructure projects involving pipeline repurposing.', true)
ON CONFLICT (code) DO NOTHING;
