-- Seed Base Categories
-- Date: 2026-02-03
-- Purpose: Ensure base categories exist with fixed UUIDs for local/remote consistency.

INSERT INTO categories (id, name, slug, description, icon, display_order) VALUES
  ('6f696c26-6761-4c4f-9e7c-88e8f2a1b92c', 'Oil & Gas Testing', 'oil-gas-testing', 'Pipeline testing, corrosion analysis, weld testing, NDT inspection', 'beaker', 1),
  ('70686172-6d61-4e2b-8a8b-1b6e4e5e4e4e', 'Pharmaceutical Testing', 'pharmaceutical-testing', 'GMP compliance, stability testing, analytical testing', 'pills', 2),
  ('62696f74-6563-4287-9078-0f8f1310951f', 'Biotech Testing', 'biotech-testing', 'Bioanalytical testing, cell culture, biocompatibility', 'dna', 3),
  ('a80a47e9-ca57-4712-9b55-d3139b98a6b7', 'Environmental Testing', 'environmental-testing', 'Water quality, soil testing, air quality analysis', 'leaf', 4),
  ('6d617465-7269-41d4-a716-446655440000', 'Materials Testing', 'materials-testing', 'Metallurgical testing, polymer analysis, failure analysis', 'cube', 5),
  ('2817126e-65fa-4ddf-8ec6-dbedb021001a', 'Hydrogen Infrastructure Testing', 'hydrogen-infrastructure-testing', 'Specialized testing for hydrogen infrastructure: valves, hoses, tanks, seals, and fuel systems.', 'fuel', 6)
ON CONFLICT (slug) DO UPDATE SET id = EXCLUDED.id;
