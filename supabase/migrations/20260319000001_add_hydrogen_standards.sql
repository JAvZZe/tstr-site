-- ============================================
-- Hydrogen Testing Standards Expansion
-- Date: 2026-03-19
-- Purpose: Add top hydrogen testing standards based on industry relevance
-- ============================================

INSERT INTO standards (code, name, description, issuing_body, standard_type, url) VALUES
('ASTM G142', 'Standard Test Method for Determination of Susceptibility of Metals to Embrittlement in Hydrogen-Containing Environments', 'Determines susceptibility of metallic materials to hydrogen embrittlement', 'ASTM', 'test_method', 'https://www.astm.org/g0142-98r22.html'),
('ASTM F1459-06', 'Standard Test Method for Determining the Susceptibility of Metallic Materials to Hydrogen Gas Embrittlement', 'Assessment of metallic materials in hydrogen gas environments', 'ASTM', 'test_method', 'https://www.astm.org/f1459-06.html'),
('CSA ANSI/CSA CHMC 1', 'Test Methods for Evaluating Material Compatibility of Metals in Compressed Hydrogen Applications', 'Material compatibility testing for metals in compressed hydrogen', 'CSA', 'test_method', 'https://www.csagroup.org/'),
('CSA ANSI/CSA CHMC 2', 'Test Methods for Evaluating Material Compatibility of Polymers in Compressed Hydrogen Applications', 'Material compatibility testing for polymers in compressed hydrogen', 'CSA', 'test_method', 'https://www.csagroup.org/'),
('ASME B31.12', 'Hydrogen Piping and Pipelines', 'Design and material requirements for hydrogen piping and pipelines; addresses hydrogen embrittlement', 'ASME', 'test_method', 'https://www.asme.org/codes-standards/b31-12-hydrogen-piping-pipelines'),
('ASME BPVC.VIII.3', 'Alternative Rules for Construction of High-Pressure Vessels', 'Alternative rules for high-pressure vessels including conditions for testing in pressurized hydrogen', 'ASME', 'test_method', 'https://www.asme.org/codes-standards/bpvc-viii-3'),
('IEC 62282-3-100', 'Fuel Cell Technologies - Part 3-100: Stationary Fuel Cell Power Systems - Safety', 'Safety requirements for stationary fuel cell power systems', 'IEC', 'test_method', 'https://www.iec.ch/'),
('ISO 16110-1', 'Hydrogen Generators Using Fuel Processing Technologies - Part 1: Safety', 'Hydrogen generators using fuel processing technologies; focuses on safety requirements', 'ISO', 'test_method', 'https://www.iso.org/standard/41911.html'),
('ISO 22734', 'Hydrogen Generators Using Water Electrolysis - Industrial, Commercial, and Residential Applications', 'Testing, safety requirements, and protocols for electrolytic hydrogen generators', 'ISO', 'test_method', 'https://www.iso.org/standard/71940.html'),
('ISO 17268', 'Gaseous Hydrogen - Land Vehicle Refueling Connection Devices', 'Connection devices for gaseous hydrogen refueling', 'ISO', 'test_method', 'https://www.iso.org/standard/62856.html'),
('ISO 16111', 'Transportable Gas Storage Devices - Hydrogen Absorbed in Reversible Metal Hydride', 'Testing for hydrogen storage in metal hydride systems', 'ISO', 'test_method', 'https://www.iso.org/standard/56559.html'),
('CSA HPIT 1', 'Compressed Hydrogen Powered Industrial Truck - On-Board Fuel Storage and Handling Components', 'Components for compressed hydrogen powered industrial trucks', 'CSA', 'test_method', 'https://www.csagroup.org/'),
('NFPA 2', 'Hydrogen Technologies Code', 'Comprehensive safety requirements for hydrogen production, storage, and handling', 'NFPA', 'test_method', 'https://www.nfpa.org/nfpa-2'),
('ISO/TS 19870:2023', 'Methodology for the Assessment of Lifecycle Greenhouse Gas (GHG) Emissions Associated with the Hydrogen Supply Chain', 'Lifecycle GHG emissions assessment methodology for hydrogen supply chain', 'ISO', 'test_method', 'https://www.iso.org/standard/83288.html'),
('ISO 19880-1', 'Gaseous Hydrogen - Fuelling Stations - Part 1: General Requirements', 'Design, installation, safety, and performance requirements for hydrogen fueling stations', 'ISO', 'test_method', 'https://www.iso.org/standard/75075.html');
