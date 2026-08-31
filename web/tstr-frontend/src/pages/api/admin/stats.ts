import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';
import { getServiceKey } from '../../../lib/supabase-admin';

const SUPABASE_URL =
  import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';

function getAdmin(locals: unknown) {
  const key = getServiceKey(locals);
  if (!key) return null;
  return createClient(SUPABASE_URL, key);
}

export const GET: APIRoute = async ({ request, locals }) => {
  const admin = getAdmin(locals);
  if (!admin) return new Response('Service key not configured', { status: 500 });

  const authHeader = request.headers.get('Authorization');
  if (!authHeader) return new Response('Unauthorized', { status: 401 });

  const token = authHeader.replace('Bearer ', '');
  const {
    data: { user },
    error: authError,
  } = await admin.auth.getUser(token);

  if (authError || !user) return new Response('Invalid Token', { status: 401 });

  const role = user.app_metadata?.role;
  if (role !== 'staff' && role !== 'super_admin') return new Response('Forbidden', { status: 403 });

  try {
    const lastWeek = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

    const [
      { data: listings },
      { data: claims },
      { data: failedUrls },
      { data: clicks },
      { data: categories },
    ] = await Promise.all([
      admin
        .from('listings')
        .select(
          'id, business_name, created_at, status, category:category_id(name), source_script, script_location'
        ),
      admin.from('claims').select('*').order('created_at', { ascending: false }),
      admin.from('pending_research').select('*', { count: 'exact', head: true }),
      admin.from('clicks').select('id, created_at, listing_id').gte('created_at', lastWeek),
      admin.from('categories').select('id, name'),
    ]);

    const totalListings = listings?.length || 0;
    const pendingCount = listings?.filter((l: any) => l.status === 'pending').length || 0;
    const totalClaims = claims?.length || 0;
    const pendingClaims = claims?.filter((c: any) => c.status === 'pending').length || 0;

    const recentListings =
      (listings || [])
        .filter((l: any) => l.status === 'active')
        .sort(
          (a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        )
        .slice(0, 5) || [];

    const responseData = {
      metrics: {
        totalListings,
        pendingCount,
        totalClaims,
        pendingClaims,
        recentClicks: clicks?.length || 0,
        failedUrls: failedUrls?.length || 0,
      },
      recentListings,
      claims: claims?.slice(0, 5) || [],
      categories: categories || [],
    };

    const { count: failedCount } = await admin
      .from('pending_research')
      .select('*', { count: 'exact', head: true });

    responseData.metrics.failedUrls = failedCount || 0;

    return new Response(JSON.stringify(responseData), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};
