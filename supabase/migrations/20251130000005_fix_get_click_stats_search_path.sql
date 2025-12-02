-- Fix mutable search_path in get_click_stats function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.get_click_stats(days_back INTEGER) SET search_path = public, pg_catalog;