-- Fix mutable search_path in make_user_admin function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.make_user_admin(user_email TEXT) SET search_path = public, pg_catalog;