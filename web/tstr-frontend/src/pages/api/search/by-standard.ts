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
      } catch (_e) {
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

    // --- Phase 1: Identification ---
    // Fetch matching listing IDs based on standard and specifications
    let capsQuery = supabase
      .from('listing_capabilities')
      .select('listing_id, specifications, verified, standard:standard_id!inner(id, code, name)')
      .eq('standard.code', standard);

    if (Object.keys(specs).length > 0) {
      capsQuery = capsQuery.contains('specifications', specs);
    }

    const { data: capData, error: capError } = await capsQuery;

    if (capError) {
      console.error('Phase 1 (Capabilities) error:', capError);
      return new Response(JSON.stringify({ error: 'Failed to identify capability matches', details: capError.message }), { status: 500, headers: { 'Content-Type': 'application/json' } });
    }

    if (!capData || capData.length === 0) {
      return new Response(
        JSON.stringify({ standard, category: category || 'all', location: location || null, specs, count: 0, results: [] }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const listingIds = Array.from(new Set(capData.map((c: any) => c.listing_id)));

    // --- Phase 2: Hydration ---
    // Fetch full business and location details for identified IDs
    let listQuery = supabase
      .from('listings')
      .select(`
        id,
        business_name,
        website,
        address,
        verified,
        category_id,
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
        )
      `)
      .eq('status', 'active')
      .in('id', listingIds);

    if (category) {
      listQuery = listQuery.eq('category_id', category);
    }

    let { data: listingsData, error: listError } = await listQuery
      .order('is_featured', { ascending: false })
      .order('created_at', { ascending: false });

    if (listError) {
      console.error('Phase 2 (Hydration) error:', listError);
      return new Response(JSON.stringify({ error: 'Database query failed (Phase 2)', details: listError.message }), { status: 500, headers: { 'Content-Type': 'application/json' } });
    }

    let filteredData = listingsData || [];

    // Manual JS filtering for location since Supabase OR across embedded resources is problematic
    if (location && filteredData.length > 0) {
      const locLower = location.toLowerCase();
      filteredData = filteredData.filter((item: any) => {
        const addressMatch = (item.address?.toLowerCase() || '').includes(locLower);
        const nameMatch = (item.location?.name?.toLowerCase() || '').includes(locLower);
        const parentMatch = (item.location?.parent?.name?.toLowerCase() || '').includes(locLower);
        const pParentMatch = (item.location?.parent?.parent?.name?.toLowerCase() || '').includes(locLower);
        
        return addressMatch || nameMatch || parentMatch || pParentMatch;
      });
    }

    // Map capability data back to listings for the response
    const transformedResults = filteredData.map((listing: any) => {
      // Find the relevant capability for this standard for the specific listing
      const cap = capData.find((c: any) => c.listing_id === listing.id);
      return {
        listing_id: listing.id,
        business_name: listing.business_name,
        website: listing.website,
        address: listing.address,
        verified: listing.verified || cap?.verified,
        standard_code: cap?.standard?.code || standard,
        standard_name: cap?.standard?.name || '',
        specifications: cap?.specifications || {}
      };
    });

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
