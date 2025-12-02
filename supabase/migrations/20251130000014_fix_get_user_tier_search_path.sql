-- Fix mutable search_path in get_user_tier function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.get_user_tier(user_uuid UUID) SET search_path = public, pg_catalog;