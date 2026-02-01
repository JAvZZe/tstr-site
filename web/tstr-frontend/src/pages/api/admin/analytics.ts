import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://haimjeaetrsaauitrhfy.supabase.co';
const SERVICE_KEY = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

const supabaseAdmin = createClient(SUPABASE_URL, SERVICE_KEY);

async function verifyAuth(request: Request) {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) return null;
    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error } = await supabaseAdmin.auth.getUser(token);
    if (error || !user) return null;
    const role = user.user_metadata?.role;
    if (role !== 'staff' && role !== 'super_admin') return null;
    return user;
}

export const GET: APIRoute = async ({ request }) => {
    const user = await verifyAuth(request);
    if (!user) return new Response('Unauthorized', { status: 401 });

    try {
        const now = new Date();
        const last30Days = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        const last7Days = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);

        // parallel requests
        const [
            { count: totalClicks },
            { count: clicks30d },
            { count: clicks7d },
            { data: recentClicks },
            { data: dailyClicks },
            { data: topListingsByRPC }
        ] = await Promise.all([
            supabaseAdmin.from('clicks').select('*', { count: 'exact', head: true }),
            supabaseAdmin.from('clicks').select('*', { count: 'exact', head: true }).gte('created_at', last30Days.toISOString()),
            supabaseAdmin.from('clicks').select('*', { count: 'exact', head: true }).gte('created_at', last7Days.toISOString()),
            supabaseAdmin.from('clicks').select(`
            id, url, user_agent, created_at,
            listings ( business_name, category:category_id(name) )
        `).order('created_at', { ascending: false }).limit(20),
            supabaseAdmin.from('clicks').select('created_at').gte('created_at', last30Days.toISOString()).order('created_at', { ascending: true }),
            supabaseAdmin.rpc('get_top_clicked_listings', { limit_count: 10 })
        ]);

        // Top Listings Fallback Logic
        let topListingsData = topListingsByRPC;
        if (!topListingsData) {
            const { data: clicksWithListings } = await supabaseAdmin
                .from('clicks')
                .select(`listing_id, listings ( id, business_name, website, category:category_id(name) )`)
                .not('listing_id', 'is', null)
                .order('created_at', { ascending: false });

            const listingCounts = new Map();
            clicksWithListings?.forEach(click => {
                const id = click.listing_id;
                if (!listingCounts.has(id)) {
                    listingCounts.set(id, {
                        listing: click.listings,
                        count: 0
                    });
                }
                listingCounts.get(id).count++;
            });

            topListingsData = Array.from(listingCounts.values())
                .sort((a: any, b: any) => b.count - a.count)
                .slice(0, 10);
        }

        // Chart Data Processing
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
            avgPerDay: clicks30d ? Math.round(clicks30d / 30) : 0
        };

        return new Response(JSON.stringify({
            metrics,
            recentClicks,
            topListings: topListingsData,
            chartData
        }), {
            headers: { 'Content-Type': 'application/json' }
        });

    } catch (e: any) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
};
