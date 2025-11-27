import type { APIRoute } from 'astro';
import { supabase } from '../../../lib/supabase';

export const GET: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  const standard = url.searchParams.get('standard');
  const category = url.searchParams.get('category');
  const specsParam = url.searchParams.get('specs');
  const location = url.searchParams.get('location');

  // Validate required parameter
  if (!standard) {
    return new Response(
      JSON.stringify({
        error: 'Missing required parameter: standard',
        example: '/api/search/by-standard?standard=ISO%2019880-3'
      }),
      {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }

  try {
    // Parse specs if provided
    let specs = {};
    if (specsParam) {
      try {
        specs = JSON.parse(specsParam);
      } catch (e) {
        return new Response(
          JSON.stringify({
            error: 'Invalid specs parameter: must be valid JSON',
            example: '{"max_pressure_bar": 700}'
          }),
          {
            status: 400,
            headers: { 'Content-Type': 'application/json' }
          }
        );
      }
    }

    // Build the query to search by standard and optionally by location
    let query = supabase
      .from('listings')
      .select(`
        id,
        business_name,
        website,
        address,
        verified,
        location:location_id (
          id,
          name,
          level,
          parent:parent_id (
            id,
            name,
            level,
            parent:parent_id (
              id,
              name,
              level
            )
          )
        ),
        listing_capabilities!inner(
          standard:standard_id!inner(
            id,
            code,
            name
          ),
          specifications,
          verified
        )
      `)
      .eq('status', 'active')
      .eq('listing_capabilities.standard.code', standard)

    // Add category filter if provided
    if (category) {
      query = query.eq('category_id', category)
    }

    // Add location filter if provided
    if (location) {
      // Search in both location hierarchy and address field
      query = query.or(`location.name.ilike.%${location}%,location.parent.name.ilike.%${location}%,location.parent.parent.name.ilike.%${location}%,address.ilike.%${location}%`)
    }

    // Add specifications filter if provided
    if (Object.keys(specs).length > 0) {
      query = query.contains('listing_capabilities.specifications', specs)
    }

    const { data, error } = await query
      .order('listing_capabilities.verified', { ascending: false })
      .order('is_featured', { ascending: false })
      .order('created_at', { ascending: false })

    if (error) {
      console.error('Supabase query error:', error);
      return new Response(
        JSON.stringify({
          error: 'Database query failed',
          details: error.message
        }),
        {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }

    // Transform the results to match the expected format
    const transformedResults = data?.map(item => ({
      listing_id: item.id,
      business_name: item.business_name,
      website: item.website,
      address: item.address,
      verified: item.verified,
      standard_code: item.listing_capabilities[0]?.standard?.code || standard,
      standard_name: item.listing_capabilities[0]?.standard?.name || '',
      specifications: item.listing_capabilities[0]?.specifications || {}
    })) || []

    // Return results
    return new Response(
      JSON.stringify({
        standard,
        category: category || 'all',
        location: location || null,
        specs,
        count: transformedResults.length,
        results: transformedResults
      }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'public, max-age=300' // Cache for 5 minutes
        }
      }
    );
  } catch (err) {
    console.error('Unexpected error:', err);
    return new Response(
      JSON.stringify({
        error: 'Internal server error',
        message: err instanceof Error ? err.message : 'Unknown error'
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
};
