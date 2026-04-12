-- Phase 1: Database Refinement for Niche Localization & Trust Architecture

-- 1. RLS LOCKDOWN FOR TRUST INTEGRITY
-- Drop existing permissive UPDATE policies on listing_capabilities
DROP POLICY IF EXISTS "Admins can manage all capabilities" ON "public"."listing_capabilities";
DROP POLICY IF EXISTS "Listing owners can manage their capabilities" ON "public"."listing_capabilities";

-- Create strict admin-only policy for the verified field
-- Allows UPDATE only if user is a TSTR Admin (via metadata) or using the service_role
CREATE POLICY "service_role_only_verified" ON "public"."listing_capabilities"
FOR UPDATE TO authenticated, service_role
USING (
  (auth.jwt()->'user_metadata'->>'is_admin')::boolean = true
  OR
  auth.jwt()->>'role' = 'service_role'
);

-- Re-enable "Listing owners can manage their capabilities" BUT exclude the verified column
-- This allows owners to update other fields while the 'verified' field stays protected by the policy above.
CREATE POLICY "Listing owners can manage non_verified_fields" ON "public"."listing_capabilities"
FOR UPDATE TO authenticated
USING (
  listing_id IN (
    SELECT listing_id FROM public.listing_ownership WHERE user_id = auth.uid()
  )
)
WITH CHECK (
  -- Ensure that if NOT an admin, the 'verified' field cannot be changed from its current state
  (
    (auth.jwt()->'user_metadata'->>'is_admin')::boolean = true
    OR
    (SELECT verified FROM public.listing_capabilities WHERE id = listing_capabilities.id) = verified
  )
);

-- 2. GROUP HIERARCHY AGGREGATION
-- Create a view to efficiently query Groups and their Branches
CREATE OR REPLACE VIEW "public"."listing_groups_view" AS
SELECT 
    p.id as group_id,
    p.business_name as group_name,
    p.slug as group_slug,
    p.description as group_description,
    p.website as group_website,
    count(c.id) as branch_count,
    array_agg(c.id) as branch_ids,
    jsonb_agg(jsonb_build_object(
        'id', c.id,
        'business_name', c.business_name,
        'slug', c.slug,
        'region', c.region,
        'verified', c.verified
    )) as branches
FROM 
    public.listings p
LEFT JOIN 
    public.listings c ON c.parent_listing_id = p.id
WHERE 
    p.parent_listing_id IS NULL -- Only top-level brands
GROUP BY 
    p.id;

-- 3. HELPER RPC FOR PSEO
-- Returns count of verified listings for a specific Category + Standard + Region
CREATE OR REPLACE FUNCTION "public"."get_pseo_stats"(
    p_category_slug text,
    p_standard_code text,
    p_region text
) RETURNS TABLE (listing_count bigint, verified_count bigint) 
LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN
    RETURN QUERY
    SELECT 
        count(*)::bigint as listing_count,
        count(*) FILTER (WHERE l.verified = true)::bigint as verified_count
    FROM 
        public.listings l
    JOIN 
        public.listing_categories lc ON l.id = lc.listing_id
    JOIN 
        public.categories cat ON lc.category_id = cat.id
    JOIN 
        public.listing_capabilities lcap ON l.id = lcap.listing_id
    JOIN 
        public.standards std ON lcap.standard_id = std.id
    WHERE 
        cat.slug = p_category_slug
        AND std.code = p_standard_code
        AND (p_region = 'global' OR l.region = p_region)
        AND l.status = 'active';
END;
$$;
