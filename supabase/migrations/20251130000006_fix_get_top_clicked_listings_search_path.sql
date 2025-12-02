-- Fix mutable search_path in get_top_clicked_listings function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.get_top_clicked_listings(limit_count INTEGER) SET search_path = public, pg_catalog;