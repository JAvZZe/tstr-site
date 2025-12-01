-- Get all biotech listings with their categories and capabilities
SELECT 
    l.id,
    l.business_name,
    l.city,
    l.state,
    l.country,
    l.website,
    c.name as category,
    l.status,
    l.verified
FROM listings l
LEFT JOIN categories c ON l.category_id = c.id
WHERE c.name ILIKE '%biotech%' OR c.name ILIKE '%pharma%'
ORDER BY l.business_name;
