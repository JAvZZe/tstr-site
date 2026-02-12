#!/bin/bash
# Test script to verify RLS policy fixes
# Run after applying the migration to ensure policies are working correctly

echo "🔍 Testing RLS Policy Fixes..."
echo "================================="

# Check if policies exist
echo "Checking for required RLS policies..."

# Test 1: Check if key policies exist
echo ""
echo "1. Checking policy existence:"
psql $DATABASE_URL -c "
SELECT schemaname, tablename, policyname
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('claims', 'listing_ownership', 'subscription_invoices', 'listing_owners', 'listings')
ORDER BY tablename, policyname;
" 2>/dev/null || echo "❌ Could not connect to database. Check DATABASE_URL."

# Test 2: Verify column existence
echo ""
echo "2. Verifying table columns:"
psql $DATABASE_URL -c "
SELECT table_name, column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('claims', 'listing_ownership', 'subscription_invoices', 'listing_owners', 'listings', 'user_profiles')
  AND column_name IN ('user_id', 'business_email', 'owner_id', 'id')
ORDER BY table_name, column_name;
" 2>/dev/null || echo "❌ Could not connect to database. Check DATABASE_URL."

# Test 3: Check RLS is enabled
echo ""
echo "3. Checking RLS status on tables:"
psql $DATABASE_URL -c "
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('claims', 'listing_ownership', 'subscription_invoices', 'listing_owners', 'listings', 'user_profiles')
ORDER BY tablename;
" 2>/dev/null || echo "❌ Could not connect to database. Check DATABASE_URL."

echo ""
echo "✅ RLS Policy Test Complete"
echo "Next: Test actual functionality by attempting operations as different user types"