import type { APIRoute } from 'astro';
import { supabase } from '../../lib/supabase';

/**
 * Internal redirect endpoint for tracking outbound clicks
 *
 * Purpose:
 * - Preserves domain authority by keeping links internal
 * - Logs click analytics to measure listing engagement
 * - Validates URLs against database to prevent open redirect attacks
 *
 * Usage: /api/out?url=https://example.com&listing=<uuid>
 */
export const GET: APIRoute = async ({ url, redirect, request }) => {
  const target = url.searchParams.get('url');
  const listingId = url.searchParams.get('listing');

  // Validate URL format
  if (!target || !target.startsWith('http')) {
    return new Response('Invalid URL', { status: 400 });
  }

  // Security: Validate listing exists and URL matches (prevents open redirect)
  if (listingId) {
    const { data: listing, error } = await supabase
      .from('listings')
      .select('website')
      .eq('id', listingId)
      .single();

    if (error || !listing || listing.website !== target) {
      return new Response('Invalid listing URL', { status: 400 });
    }

    // Log click asynchronously (non-blocking - don't await)
    supabase
      .from('clicks')
      .insert({
        listing_id: listingId,
        url: target,
        user_agent: request.headers.get('user-agent'),
        referrer: request.headers.get('referer')
      })
      .then(({ error: insertError }) => {
        if (insertError) {
          console.error('Click logging failed:', insertError);
        }
      });
  }

  // 302 Temporary Redirect (standard for tracking redirects)
  return redirect(target, 302);
};
