-- Fix mutable search_path in user_owns_listing function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.user_owns_listing(user_uuid UUID, listing_uuid UUID) SET search_path = public, pg_catalog;