-- Fix mutable search_path in update_website_domain function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.update_website_domain() SET search_path = public, pg_catalog;