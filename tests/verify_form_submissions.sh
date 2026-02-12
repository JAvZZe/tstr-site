#!/bin/bash
# Automated verification script for form testing
# Run after manual form submissions to verify database state

echo "🔍 Form Submission Verification"
echo "==============================="

# Check for test submissions
echo "1. Checking for recent test submissions:"
psql $DATABASE_URL -c "
SELECT
    id,
    business_name,
    status,
    verified,
    claimed,
    created_at,
    owner_id
FROM listings
WHERE business_name LIKE '%RLS Test%'
   OR business_name LIKE '%Test RLS%'
ORDER BY created_at DESC
LIMIT 5;
" 2>/dev/null || echo "❌ Cannot connect to database"

echo ""
echo "2. Checking RLS policies are active:"
psql $DATABASE_URL -c "
SELECT
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('listings', 'claims', 'listing_ownership')
ORDER BY tablename, policyname;
" 2>/dev/null || echo "❌ Cannot connect to database"

echo ""
echo "3. Testing anonymous access (should fail):"
# This would require setting up a test user session
echo "Manual test required: Try accessing listings without authentication"

echo ""
echo "✅ Verification complete. Check results above."