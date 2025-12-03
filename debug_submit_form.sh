#!/bin/bash
# Debug script to test submit form database queries
# This simulates what the submit form JavaScript does

echo "🔍 Submit Form Database Query Debug"
echo "===================================="

# Test 1: Check if categories table is accessible
echo ""
echo "1. Testing categories table access:"
psql $DATABASE_URL -c "
SELECT COUNT(*) as total_categories FROM categories;
SELECT name FROM categories LIMIT 5;
" 2>/dev/null || echo "❌ Cannot connect to database"

# Test 2: Check if locations table is accessible
echo ""
echo "2. Testing locations table access:"
psql $DATABASE_URL -c "
SELECT COUNT(*) as total_locations FROM locations;
SELECT name, level FROM locations LIMIT 5;
" 2>/dev/null || echo "❌ Cannot connect to database"

# Test 3: Test the exact queries the submit form makes
echo ""
echo "3. Testing submit form category lookup:"
psql $DATABASE_URL -c "
-- This is what the submit form does for 'Environmental Testing'
SELECT id, name FROM categories WHERE name = 'Environmental Testing';
" 2>/dev/null || echo "❌ Cannot connect to database"

# Test 4: Check RLS policies on reference tables
echo ""
echo "4. Checking RLS policies on reference tables:"
psql $DATABASE_URL -c "
SELECT schemaname, tablename, policyname, permissive, roles, cmd
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN ('categories', 'locations')
ORDER BY tablename, policyname;
" 2>/dev/null || echo "❌ Cannot connect to database"

# Test 5: Check if RLS is enabled on these tables
echo ""
echo "5. Checking RLS status on tables:"
psql $DATABASE_URL -c "
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN ('categories', 'locations', 'listings')
ORDER BY tablename;
" 2>/dev/null || echo "❌ Cannot connect to database"

echo ""
echo "✅ Debug complete. Check results above for issues."