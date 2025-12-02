-- Fix mutable search_path in extract_domain function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.extract_domain(url TEXT) SET search_path = pg_catalog, public;