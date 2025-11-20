import type { APIRoute } from 'astro';
import { supabase } from '../../../lib/supabase';

export const GET: APIRoute = async ({ request }) => {
  const url = new URL(request.url);
  const standard = url.searchParams.get('standard');
  const category = url.searchParams.get('category');
  const specsParam = url.searchParams.get('specs');

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

    // Call the search_by_standard RPC function
    const { data, error } = await supabase.rpc('search_by_standard', {
      p_standard_code: standard,
      p_category_id: category || null,
      p_min_specs: specs
    });

    if (error) {
      console.error('Supabase RPC error:', error);
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

    // Return results
    return new Response(
      JSON.stringify({
        standard,
        category: category || 'all',
        specs,
        count: data?.length || 0,
        results: data || []
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
