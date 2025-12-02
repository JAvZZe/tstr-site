-- Fix SECURITY DEFINER view issue for potential_dead_links
-- Change to SECURITY INVOKER to respect RLS policies

ALTER VIEW potential_dead_links SET (security_invoker = true);

-- Re-grant permissions to ensure they still work
GRANT SELECT ON potential_dead_links TO authenticated;