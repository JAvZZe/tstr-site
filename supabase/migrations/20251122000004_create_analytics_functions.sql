-- Create function for efficient top listings query
-- This is much faster than doing aggregation in JavaScript

CREATE OR REPLACE FUNCTION get_top_clicked_listings(limit_count INTEGER DEFAULT 10)
RETURNS TABLE (
  listing_id UUID,
  business_name TEXT,
  website TEXT,
  category_name TEXT,
  clicks BIGINT,
  last_click TIMESTAMPTZ
)
LANGUAGE SQL
STABLE
AS $$
  SELECT
    l.id as listing_id,
    l.business_name,
    l.website,
    c.name as category_name,
    COUNT(cl.id) as clicks,
    MAX(cl.created_at) as last_click
  FROM clicks cl
  JOIN listings l ON cl.listing_id = l.id
  LEFT JOIN categories c ON l.category_id = c.id
  GROUP BY l.id, l.business_name, l.website, c.name
  ORDER BY clicks DESC, last_click DESC
  LIMIT limit_count;
$$;

-- Grant execute permission to authenticated users
GRANT EXECUTE ON FUNCTION get_top_clicked_listings TO authenticated;

-- Create function to get click stats by date range
CREATE OR REPLACE FUNCTION get_click_stats(days_back INTEGER DEFAULT 30)
RETURNS TABLE (
  date DATE,
  clicks BIGINT,
  unique_listings BIGINT
)
LANGUAGE SQL
STABLE
AS $$
  SELECT
    DATE(created_at) as date,
    COUNT(*) as clicks,
    COUNT(DISTINCT listing_id) as unique_listings
  FROM clicks
  WHERE created_at >= NOW() - (days_back || ' days')::INTERVAL
  GROUP BY DATE(created_at)
  ORDER BY date DESC;
$$;

-- Grant execute permission
GRANT EXECUTE ON FUNCTION get_click_stats TO authenticated;

-- Create view for dead link detection
CREATE OR REPLACE VIEW potential_dead_links AS
SELECT
  l.id,
  l.business_name,
  l.website,
  c.name as category,
  COUNT(cl.id) as click_attempts,
  MAX(cl.created_at) as last_attempt,
  l.status
FROM listings l
LEFT JOIN clicks cl ON l.id = cl.listing_id
LEFT JOIN categories c ON l.category_id = c.id
WHERE l.website IS NOT NULL
GROUP BY l.id, l.business_name, l.website, c.name, l.status
HAVING COUNT(cl.id) > 0  -- Only listings that have been clicked
ORDER BY click_attempts DESC;

-- Grant select permission
GRANT SELECT ON potential_dead_links TO authenticated;

-- Comment for documentation
COMMENT ON FUNCTION get_top_clicked_listings IS 'Returns top N listings by click count with aggregated metrics';
COMMENT ON FUNCTION get_click_stats IS 'Returns daily click statistics for the last N days';
COMMENT ON VIEW potential_dead_links IS 'Listings with clicks - useful for monitoring and dead link detection';
