-- Fix mutable search_path in update_updated_at_column function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.update_updated_at_column() SET search_path = public, pg_catalog;