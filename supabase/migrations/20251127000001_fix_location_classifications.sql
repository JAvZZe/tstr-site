-- ============================================
-- Fix Location Data Classification Issues
-- Date: 2025-11-27
-- Purpose: Correct misclassified locations, fix parent relationships, and clean up duplicates
-- ============================================

-- 1. Fix "New York" city -> should be region (state)
UPDATE locations
SET level = 'region', name = 'New York'
WHERE id = 'ff98c268-a7f6-463f-8c89-a45e29c2d5ef';

-- 2. Delete incorrect "Global" city entry (Global should only be at global level)
DELETE FROM locations
WHERE id = '4e362b36-cecc-4211-8fa4-bf130b845fa9';

-- 3. Delete redundant "Singapore" city entry (Singapore is both country and city, but city is redundant)
DELETE FROM locations
WHERE id = '0b7795f4-9ca1-4630-87d9-b94ce4d2a969';

-- 4. Remove duplicate London entry
-- First, check which London entry has listings associated
-- For now, delete the second London entry (keep the original)
DELETE FROM locations
WHERE id = '8849f79a-45d6-4d05-af28-285704013d33';

-- 5. Fix country parent relationships
-- Move Germany under Europe
UPDATE locations
SET parent_id = 'fca58d48-fd86-4ce5-834d-2af0c9f66331'
WHERE id = '278460d5-e563-4fdb-93c5-530558c2545a';

-- Move Netherlands under Europe
UPDATE locations
SET parent_id = 'fca58d48-fd86-4ce5-834d-2af0c9f66331'
WHERE id = '8aa3f6ff-cd02-4ef6-9e53-caad984fd38e';

-- Move Canada under North America
UPDATE locations
SET parent_id = 'f5dd17ac-34b0-4927-a382-1620e5dee1e3'
WHERE id = '0ad2249c-5410-4770-ad07-2bf50e1f26d1';

-- 6. Fix name issues
-- Fix "Kuwait Kuwait" -> "Kuwait"
UPDATE locations
SET name = 'Kuwait', slug = 'kuwait'
WHERE id = 'cc4b7836-3379-4e5e-a9c8-2c100677d0ba';

-- 7. Standardize city name casing (convert lowercase city names to proper case)
UPDATE locations
SET name = 'North Brunswick', slug = 'north-brunswick'
WHERE id = '505ab576-6390-4220-a7d0-eecb0872958e';

UPDATE locations
SET name = 'Hill AFB', slug = 'hill-afb'
WHERE id = '64c89153-bdfe-4e4e-b2d9-666157b40978';

UPDATE locations
SET name = 'Nederland', slug = 'nederland'
WHERE id = 'b02a198e-a36b-4aa1-a8cf-1adb42cdbba7';

UPDATE locations
SET name = 'Morrisville', slug = 'morrisville'
WHERE id = '6ac44ba7-fdbb-4dd6-a7bc-e7daa628579c';

UPDATE locations
SET name = 'Brainerd', slug = 'brainerd'
WHERE id = 'd67c6ff7-b99e-4931-b972-92862a3c4771';

UPDATE locations
SET name = 'Abilene', slug = 'abilene'
WHERE id = '97bd893c-181e-421d-9e1c-48514405f4c7';

UPDATE locations
SET name = 'Puposky', slug = 'puposky'
WHERE id = '9d9dc3fb-91ee-4dc1-8266-8b8d7dbfdcf7';

UPDATE locations
SET name = 'Independence', slug = 'independence'
WHERE id = 'f0266a27-3651-497c-ab46-e8cd24cb320b';

UPDATE locations
SET name = 'Romulus', slug = 'romulus'
WHERE id = '93803cfb-60f6-423d-8867-286a45d7439c';

UPDATE locations
SET name = 'Stillwater', slug = 'stillwater'
WHERE id = 'f57de571-0c12-49de-b793-0b64a5e9db11';

UPDATE locations
SET name = 'Addison', slug = 'addison'
WHERE id = '46b29f09-3f23-40ce-9046-d3a4c15d02e4';

UPDATE locations
SET name = 'Elmhurst', slug = 'elmhurst'
WHERE id = '8133b34d-65de-483c-ba89-9f88abfdedd4';

UPDATE locations
SET name = 'Minneapolis', slug = 'minneapolis'
WHERE id = '97013aed-47d3-4104-8079-fac294d59627';

UPDATE locations
SET name = 'Warwick', slug = 'warwick'
WHERE id = 'a20af9da-00c6-4d32-aa47-2d9c1465e479';

UPDATE locations
SET name = 'Kokomo', slug = 'kokomo'
WHERE id = 'cdb57e3a-c8db-4336-816c-ada4f1bb6f7b';

UPDATE locations
SET name = 'Westminster', slug = 'westminster'
WHERE id = '0b241618-6328-40e6-b775-4354a6116dc0';

UPDATE locations
SET name = 'Plano', slug = 'plano'
WHERE id = '4520cf54-6195-4e57-a7d2-5dc9d40f9de4';

UPDATE locations
SET name = 'Cleveland', slug = 'cleveland'
WHERE id = 'd6eeb742-68f7-4c21-834e-80a32282d12c';

UPDATE locations
SET name = 'Al Qurain', slug = 'al-qurain'
WHERE id = '040ba3b4-cb18-476f-b428-d6db22079f33';

UPDATE locations
SET name = 'New Berlin', slug = 'new-berlin'
WHERE id = '425cb59b-99ba-4ef0-9bb6-e7b515ad9b4a';

UPDATE locations
SET name = 'Des Moines', slug = 'des-moines'
WHERE id = 'fe02d095-f38f-4692-94a1-260804af2e93';

UPDATE locations
SET name = 'Harrisburg', slug = 'harrisburg'
WHERE id = '2ef25314-322d-448c-b1f1-d4bc8179c30e';

UPDATE locations
SET name = 'Naples', slug = 'naples'
WHERE id = '5b3ae6a0-52c4-455f-9e95-c0cad03ca0af';

UPDATE locations
SET name = 'Milford', slug = 'milford'
WHERE id = '9c1cdcbe-f245-4d95-9799-f07bc4f05355';

UPDATE locations
SET name = 'Livonia', slug = 'livonia'
WHERE id = '837223af-99f5-4a5c-acd4-cdeb74337581';

UPDATE locations
SET name = 'Hudson', slug = 'hudson'
WHERE id = 'fc1a649b-59c4-498a-95ac-539cce9e0949';

UPDATE locations
SET name = 'Upper Marlboro', slug = 'upper-marlboro'
WHERE id = 'c1a2a157-1e65-44dc-9e78-66dc1d89c3ef';

UPDATE locations
SET name = 'Kentwood', slug = 'kentwood'
WHERE id = '1a2092f2-5715-4520-be90-da38140d81dc';

UPDATE locations
SET name = 'Munich', slug = 'munich-germany'
WHERE id = 'c8a8c491-ed8c-428c-ad6e-53130e040748';

UPDATE locations
SET name = 'Apeldoorn', slug = 'apeldoorn-netherlands'
WHERE id = '78d6c1bf-3a87-4f47-8fec-dd79957a613e';

UPDATE locations
SET name = 'Surrey', slug = 'surrey-canada'
WHERE id = '1f00cc78-1b80-4d37-a700-9f5a0047c05b';

UPDATE locations
SET name = 'Bartlesville', slug = 'bartlesville-united-states'
WHERE id = '47a889b4-984c-45e7-864f-8db351d03c2d';

-- Update timestamps for modified records
UPDATE locations
SET updated_at = NOW()
WHERE updated_at < NOW();