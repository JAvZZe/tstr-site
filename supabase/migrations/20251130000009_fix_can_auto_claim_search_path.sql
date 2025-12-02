-- Fix mutable search_path in can_auto_claim function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.can_auto_claim(user_email TEXT, listing_website TEXT) SET search_path = public, pg_catalog;