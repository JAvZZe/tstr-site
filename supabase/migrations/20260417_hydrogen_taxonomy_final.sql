-- 20260417_hydrogen_taxonomy_final.sql
-- Goal: Link 15 orphaned hydrogen standards to sub-categories and laboratories.

BEGIN;

-- 1. Standard to Category Linkage
-- Categories:
-- Valve & Fitting: 0076db0e-1d4e-4003-8060-eb978b5d94e4
-- Hose & Seal: cdfaa06e-7c2e-4312-83fb-8143ad9024c9
-- Tank & Pressure Vessel: 5eccabc9-6e74-4584-a259-013b7fdcd646
-- Hydrogen Embrittlement: f29966a2-4753-451b-b354-d756c78a8d38
-- Hydrogen Purity: 508b108a-5563-4287-9078-0f8f1310951f
-- Infrastructure General: 2817126e-65fa-4ddf-8ec6-dbedb021001a

-- Cleanup existing links for these standards to avoid duplicates
DELETE FROM categories_standards 
WHERE standard_id IN (
    '56cdacca-6e20-4062-b0ec-7122ab42ff26', -- ASME B31.12
    'f9228593-c984-4693-a212-5ceb9e2122e6', -- ASME BPVC.VIII.3
    'eb620887-9fba-4e8d-8df2-fb2bdef3d244', -- ISO 19881
    '27ca1599-b414-45f9-8bdc-f02865862100', -- ASTM G142
    '4e470799-f253-4ead-b1c0-2197bdfce63c', -- ASTM F1459-06
    'd949ff63-f8ec-435d-b302-d5bd55d346f6', -- CSA ANSI/CSA CHMC 1
    'cc9858bd-2bd5-48b6-9f38-1795bbc8d04c', -- CSA ANSI/CSA CHMC 2
    'e1429cc8-d1f9-458d-8258-1d4396814ab1', -- ISO 19880-5
    '0bb39d7c-ef8e-48a6-aa8d-5612a368fcaf', -- ISO 19880-3
    'e7994d17-9155-456b-89c9-09f969fb1705', -- ISO 14687
    '15480454-c0c6-4a2e-93b9-7a8c673ab26b', -- ISO 22734
    '11848870-850b-4932-84f3-d9bc2d7df4a9', -- ISO 17268
    '5f91dd63-3d06-4900-9022-6d165a820bfc', -- ISO 16111
    '35ddef39-5462-4001-8e0c-6ea4c4d83e75', -- NFPA 2
    'be1acb95-8e6a-4bd1-a9ac-9a68311c1c83', -- ISO/TS 19870:2023
    'ade4209a-4962-4552-8c28-5c9f7cc556da'  -- ISO 19880-1
);

INSERT INTO categories_standards (category_id, standard_id) VALUES
-- Embrittlement
('f29966a2-4753-451b-b354-d756c78a8d38', '27ca1599-b414-45f9-8bdc-f02865862100'), -- ASTM G142
('f29966a2-4753-451b-b354-d756c78a8d38', '4e470799-f253-4ead-b1c0-2197bdfce63c'), -- ASTM F1459-06
('f29966a2-4753-451b-b354-d756c78a8d38', 'd949ff63-f8ec-435d-b302-d5bd55d346f6'), -- CSA CHMC 1
('f29966a2-4753-451b-b354-d756c78a8d38', 'cc9858bd-2bd5-48b6-9f38-1795bbc8d04c'), -- CSA CHMC 2
-- Valve & Fitting
('0076db0e-1d4e-4003-8060-eb978b5d94e4', '0bb39d7c-ef8e-48a6-aa8d-5612a368fcaf'), -- ISO 19880-3
('0076db0e-1d4e-4003-8060-eb978b5d94e4', '11848870-850b-4932-84f3-d9bc2d7df4a9'), -- ISO 17268
-- Hose & Seal
('cdfaa06e-7c2e-4312-83fb-8143ad9024c9', 'e1429cc8-d1f9-458d-8258-1d4396814ab1'), -- ISO 19880-5
-- Tank & Pressure Vessel
('5eccabc9-6e74-4584-a259-013b7fdcd646', 'f9228593-c984-4693-a212-5ceb9e2122e6'), -- ASME BPVC.VIII.3
('5eccabc9-6e74-4584-a259-013b7fdcd646', '5f91dd63-3d06-4900-9022-6d165a820bfc'), -- ISO 16111
('5eccabc9-6e74-4584-a259-013b7fdcd646', 'eb620887-9fba-4e8d-8df2-fb2bdef3d244'), -- ISO 19881
-- Purity
('508b108a-5563-4287-9078-0f8f1310951f', 'e7994d17-9155-456b-89c9-09f969fb1705'), -- ISO 14687
('508b108a-5563-4287-9078-0f8f1310951f', 'be1acb95-8e6a-4bd1-a9ac-9a68311c1c83'), -- ISO/TS 19870:2023
-- General Infrastructure
('2817126e-65fa-4ddf-8ec6-dbedb021001a', '56cdacca-6e20-4062-b0ec-7122ab42ff26'), -- ASME B31.12
('2817126e-65fa-4ddf-8ec6-dbedb021001a', '35ddef39-5462-4001-8e0c-6ea4c4d83e75'), -- NFPA 2
('2817126e-65fa-4ddf-8ec6-dbedb021001a', '15480454-c0c6-4a2e-93b9-7a8c673ab26b'), -- ISO 22734
('2817126e-65fa-4ddf-8ec6-dbedb021001a', 'ade4209a-4962-4552-8c28-5c9f7cc556da'); -- ISO 19880-1

-- 2. Laboratory Capability Mapping
-- Ensure labs have the capabilities for these standards.
-- Avoiding inserts if they already exist (ON CONFLICT DO NOTHING require PK setup, so using subquery)

-- Wrapper to insert if not exists
INSERT INTO listing_capabilities (listing_id, standard_id)
SELECT l.id, s.id
FROM (VALUES 
    -- Element Materials Technology
    ('a302f6e3-4222-4dce-adcd-746dbb5dc4a2', '27ca1599-b414-45f9-8bdc-f02865862100'), -- ASTM G142
    ('a302f6e3-4222-4dce-adcd-746dbb5dc4a2', '56cdacca-6e20-4062-b0ec-7122ab42ff26'), -- ASME B31.12
    ('a302f6e3-4222-4dce-adcd-746dbb5dc4a2', 'd949ff63-f8ec-435d-b302-d5bd55d346f6'), -- CSA CHMC 1
    -- SGS
    ('460b3d8a-efa3-49b7-a667-5f1ff6f601af', '15480454-c0c6-4a2e-93b9-7a8c673ab26b'), -- ISO 22734
    ('460b3d8a-efa3-49b7-a667-5f1ff6f601af', 'e7994d17-9155-456b-89c9-09f969fb1705'), -- ISO 14687
    ('460b3d8a-efa3-49b7-a667-5f1ff6f601af', 'ade4209a-4962-4552-8c28-5c9f7cc556da'), -- ISO 19880-1
    -- TUV SUD
    ('a837f837-5b02-4c04-a0e8-546316067587', '56cdacca-6e20-4062-b0ec-7122ab42ff26'), -- ASME B31.12
    ('a837f837-5b02-4c04-a0e8-546316067587', '0bb39d7c-ef8e-48a6-aa8d-5612a368fcaf'), -- ISO 19880-3
    -- Intertek
    ('59a9e7a2-64ad-407f-9d63-679e242646b1', '15480454-c0c6-4a2e-93b9-7a8c673ab26b'), -- ISO 22734
    ('59a9e7a2-64ad-407f-9d63-679e242646b1', '11848870-850b-4932-84f3-d9bc2d7df4a9'), -- ISO 17268
    -- DNV
    ('33eba0ec-f866-4475-bf5e-919912b485f7', '56cdacca-6e20-4062-b0ec-7122ab42ff26'), -- ASME B31.12
    -- UL Solutions
    ('3450b7ce-2633-45fb-b6ef-1bfde4d04f41', '15480454-c0c6-4a2e-93b9-7a8c673ab26b'), -- ISO 22734
    -- Resato
    ('6f69c644-55c0-4443-b23b-ce1ebbb4294b', '11848870-850b-4932-84f3-d9bc2d7df4a9'), -- ISO 17268
    -- CSA Group
    ('84bf1fda-235d-4d02-9228-c248d5ff6243', 'd949ff63-f8ec-435d-b302-d5bd55d346f6'), -- CSA CHMC 1
    -- SwRI
    ('9b844234-d075-4653-8ed0-1351ddf7bbbe', '27ca1599-b414-45f9-8bdc-f02865862100')  -- ASTM G142
) AS t(listing_id, standard_id)
JOIN listings l ON l.id = CAST(t.listing_id AS uuid)
JOIN standards s ON s.id = CAST(t.standard_id AS uuid)
WHERE NOT EXISTS (
    SELECT 1 FROM listing_capabilities lc 
    WHERE lc.listing_id = l.id AND lc.standard_id = s.id
);

COMMIT;
