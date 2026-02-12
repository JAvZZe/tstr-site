-- Function to calculate listing usage and billing details
-- Returns:
-- category_count: Total categories listing is in
-- location_count: 1 (for now, unless multiple locations implemented)
-- base_tier: The current tier stored in listings table (avg user input/admin set)
-- calculated_monthly_price: Base price + extra categories
-- extra_category_cost: The cost added for extra categories

CREATE OR REPLACE FUNCTION public.calculate_listing_billing(p_listing_id uuid)
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
DECLARE
    v_category_count integer;
    v_base_tier text;
    v_base_price numeric := 0;
    v_extra_cost numeric := 0;
    v_total_price numeric := 0;
    v_included_categories integer := 1; -- Default included
    v_extra_category_price numeric := 150.00;
BEGIN
    -- Get current billing tier and basic info
    SELECT billing_tier INTO v_base_tier
    FROM public.listings
    WHERE id = p_listing_id;

    -- Count categories
    SELECT COUNT(*) INTO v_category_count
    FROM public.listing_categories
    WHERE listing_id = p_listing_id;

    -- Determine base price based on tier (hardcoded for now as per known plans)
    -- Professional: $295, Premium: $795
    CASE v_base_tier
        WHEN 'professional' THEN v_base_price := 295.00;
        WHEN 'premium' THEN v_base_price := 795.00;
        WHEN 'enterprise' THEN v_base_price := 0; -- Custom
        ELSE v_base_price := 0; -- Free/Standard
    END CASE;

    -- Calculate Extra Cost (Only applies if not Enterprise and not Free)
    IF v_base_tier IN ('professional', 'premium') THEN
        IF v_category_count > v_included_categories THEN
            v_extra_cost := (v_category_count - v_included_categories) * v_extra_category_price;
        END IF;
    END IF;

    v_total_price := v_base_price + v_extra_cost;

    RETURN jsonb_build_object(
        'listing_id', p_listing_id,
        'billing_tier', v_base_tier,
        'category_count', v_category_count,
        'included_categories', v_included_categories,
        'base_price', v_base_price,
        'extra_category_cost', v_extra_cost,
        'total_monthly_price', v_total_price
    );
END;
$$;

ALTER FUNCTION public.calculate_listing_billing(uuid) OWNER TO postgres;
COMMENT ON FUNCTION public.calculate_listing_billing(uuid) IS 'Calculates monthly billing based on tier and active category count.';
