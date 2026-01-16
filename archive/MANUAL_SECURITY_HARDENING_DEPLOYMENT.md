# Manual Security Hardening Deployment Instructions

## Issue
Applying comprehensive security fixes for search paths and view permissions. CLI push may have sync issues.

## Migration Details
- **File**: `supabase/migrations/20251216000001_security_harden_search_paths.sql`
- **Purpose**: Fix mutable search paths vulnerability and enable performance monitoring

## Manual Deployment Steps

### Supabase Dashboard SQL Editor
1. Go to [Supabase Dashboard](https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy)
2. Navigate to **SQL Editor**
3. Copy and paste the following SQL blocks in order:

**Block 1: Enable Extension**
```sql
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";
```

**Block 2: Fix View**
```sql
ALTER VIEW potential_dead_links SET (security_invoker = true);
```

**Block 3: Fix Search Paths (Run all at once)**
```sql
ALTER FUNCTION public.handle_new_user()
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.get_click_stats(days_back INTEGER)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.get_top_clicked_listings(limit_count INTEGER)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.make_user_admin(user_email TEXT)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.update_website_domain()
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.can_auto_claim(user_email TEXT, listing_website TEXT)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.extract_domain(url TEXT)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.search_by_standard(p_standard_code TEXT, p_category_id UUID, p_min_specs JSONB)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.user_owns_listing(user_uuid UUID, listing_uuid UUID)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.can_view_contact_info(user_uuid UUID)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.get_user_tier(user_uuid UUID)
    SET search_path = pg_catalog, public;

ALTER FUNCTION public.update_updated_at_column()
    SET search_path = pg_catalog, public;
```

## Verification
After deployment, run this query to verify search paths:
```sql
SELECT proname, proconfig 
FROM pg_proc 
WHERE proname IN (
  'handle_new_user', 'get_click_stats', 'get_top_clicked_listings', 
  'make_user_admin', 'update_website_domain', 'can_auto_claim', 
  'extract_domain', 'search_by_standard', 'user_owns_listing', 
  'can_view_contact_info', 'get_user_tier', 'update_updated_at_column'
);
```

Expected: Each function should show `search_path=pg_catalog, public`

## Security Impact
- **Before**: `public, pg_catalog` allowed function shadowing attacks
- **After**: `pg_catalog, public` prevents malicious object creation in public schema

## Status
- Migration file created locally ✅
- Ready for manual deployment