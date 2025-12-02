-- Fix mutable search_path in search_by_standard function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.search_by_standard(p_standard_code TEXT, p_category_id UUID, p_min_specs JSONB) SET search_path = public, pg_catalog;