-- Supabase Security & Performance Diagnostics
-- Run this in Supabase SQL Editor or via psql

-- 1. Check RLS Policies (Security Issues)
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename IN ('listings', 'listing_owners', 'claims', 'clicks', 'user_profiles')
ORDER BY tablename, cmd, roles;

-- 2. Check Table Sizes (Performance Issues)
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_total_relation_size(schemaname||'.'||tablename) as bytes
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN ('listings', 'listing_owners', 'claims', 'clicks', 'user_profiles', 'categories', 'locations')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 3. Check Indexes (Performance Issues)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
    AND tablename IN ('listings', 'listing_owners', 'claims', 'clicks', 'user_profiles')
ORDER BY tablename, indexname;

-- 4. Check Slow Queries (Performance Issues)
SELECT
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
WHERE query LIKE '%listings%' 
   OR query LIKE '%clicks%'
   OR query LIKE '%claims%'
   OR query LIKE '%listing_owners%'
ORDER BY mean_time DESC
LIMIT 10;

-- 5. Check Function Performance (Performance Issues)
SELECT
    schemaname,
    funcname,
    calls,
    total_time,
    self_time,
    mean_time
FROM pg_stat_user_functions
WHERE funcname IN ('get_top_clicked_listings', 'get_click_stats', 'can_auto_claim', 'extract_domain')
ORDER BY mean_time DESC;

-- 6. Check RLS Status on Tables
SELECT
    schemaname,
    tablename,
    rowsecurity as rls_enabled
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename IN ('listings', 'listing_owners', 'claims', 'clicks', 'user_profiles', 'categories', 'locations');
