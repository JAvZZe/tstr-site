-- Fix mutable search_path in can_view_contact_info function
-- Set stable search_path for security and consistency

ALTER FUNCTION public.can_view_contact_info(user_uuid UUID) SET search_path = public, pg_catalog;