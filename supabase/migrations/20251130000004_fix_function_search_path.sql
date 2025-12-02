-- Fix mutable search_path in handle_new_user function
-- Set stable search_path to prevent security vulnerabilities

ALTER FUNCTION public.handle_new_user() SET search_path = public, pg_catalog;