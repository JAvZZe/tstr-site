-- Fix Intertek URL in pending_research table
-- Update incorrect Intertek URLs to the correct one

UPDATE pending_research
SET website = 'https://www.intertek.com/'
WHERE business_name ILIKE '%intertek%'
  AND (website IS NULL OR website != 'https://www.intertek.com/');

-- Show the updated records
SELECT id, business_name, website, validation_error, created_at
FROM pending_research
WHERE business_name ILIKE '%intertek%'
ORDER BY created_at DESC;