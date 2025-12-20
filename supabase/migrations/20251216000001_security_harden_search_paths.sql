-- Enable pg_stat_statements for performance monitoring
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";

-- Fix SECURITY DEFINER View
-- Ensure it is security_invoker to respect RLS
ALTER VIEW potential_dead_links SET (security_invoker = true);

-- Fix Mutable Search Paths
-- CRITICAL: Must list pg_catalog FIRST to prevent shadowing attacks
-- Previous fixes used 'public, pg_catalog' which is insecure.

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