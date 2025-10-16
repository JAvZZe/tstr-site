-- ============================================
-- VERIFICATION SCRIPT
-- ============================================
-- Copy this into SQL Editor to check everything worked

-- Check categories (should show 5 rows)
SELECT * FROM categories ORDER BY display_order;

-- Check locations (should show multiple rows including Houston, London, Singapore)
SELECT name, level FROM locations ORDER BY level, name;

-- Check tables exist (should show 8 rows)
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
