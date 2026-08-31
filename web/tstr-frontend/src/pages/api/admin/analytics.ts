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
    error,
  } = await admin.auth.getUser(token);
  if (error || !user) return new Response('Unauthorized', { status: 401 });
  const role = user.app_metadata?.role;
  if (role !== 'staff' && role !== 'super_admin')
    return new Response('Unauthorized', { status: 401 });

  try {
    const now = new Date();
    const last30Days = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
    const last7Days = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

    const [
      { count: totalClicks },
      { count: clicks30d },
      { count: clicks7d },
      { data: recentClicks },
      { data: dailyClicks },
      { data: topListingsByRPC },
    ] = await Promise.all([
      admin.from('clicks').select('*', { count: 'exact', head: true }),
      admin
        .from('clicks')
        .select('*', { count: 'exact', head: true })
        .gte('created_at', last30Days.toISOString()),
      admin
        .from('clicks')
        .select('*', { count: 'exact', head: true })
        .gte('created_at', last7Days.toISOString()),
      admin
        .from('clicks')
        .select(
          `
            id, url, user_agent, created_at,
            listings ( business_name, category:category_id(name) )
        `
        )
        .order('created_at', { ascending: false })
        .limit(20),
      admin
        .from('clicks')
        .select('created_at')
        .gte('created_at', last30Days.toISOString())
        .order('created_at', { ascending: true }),
      admin.rpc('get_top_clicked_listings', { limit_count: 10 }),
    ]);

    let topListingsData = topListingsByRPC;
    if (!topListingsData) {
      const { data: clicksWithListings } = await admin
        .from('clicks')
        .select(`listing_id, listings ( id, business_name, website, category:category_id(name) )`)
        .not('listing_id', 'is', null)
        .order('created_at', { ascending: false });

      const listingCounts = new Map();
      clicksWithListings?.forEach((click) => {
        const id = click.listing_id;
        if (!listingCounts.has(id)) {
          listingCounts.set(id, {
            listing: click.listings,
            count: 0,
          });
        }
        listingCounts.get(id).count++;
      });

      topListingsData = Array.from(listingCounts.values())
        .sort((a: any, b: any) => b.count - a.count)
        .slice(0, 10);
    }

    const clicksByDay = new Map();
    dailyClicks?.forEach((click: any) => {
      const date = new Date(click.created_at).toISOString().split('T')[0];
      clicksByDay.set(date, (clicksByDay.get(date) || 0) + 1);
    });
    const chartData = Array.from(clicksByDay.entries()).map(([date, count]) => ({ date, count }));

    const metrics = {
      totalClicks: totalClicks || 0,
      clicks30d: clicks30d || 0,
      clicks7d: clicks7d || 0,
      avgPerDay: clicks30d ? Math.round(clicks30d / 30) : 0,
    };

    return new Response(
      JSON.stringify({
        metrics,
        recentClicks,
        topListings: topListingsData,
        chartData,
      }),
      {
        headers: { 'Content-Type': 'application/json' },
      }
    );
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};
