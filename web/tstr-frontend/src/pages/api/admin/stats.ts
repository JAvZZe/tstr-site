import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://haimjeaetrsaauitrhfy.supabase.co';
const SERVICE_KEY = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

const supabaseAdmin = createClient(SUPABASE_URL, SERVICE_KEY);

export const GET: APIRoute = async ({ request }) => {
    console.log('[Stats API] Request received');

    // 1. Verify Auth Token
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) {
        console.error('[Stats API] Missing Authorization Header');
        return new Response('Unauthorized', { status: 401 });
    }

    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error: authError } = await supabaseAdmin.auth.getUser(token);

    if (authError || !user) {
        console.error('[Stats API] Auth Error:', authError?.message);
        return new Response('Invalid Token', { status: 401 });
    }

    // 2. Verify Role
    const role = user.user_metadata?.role;
    console.log('[Stats API] Authenticated User:', user.email, 'Role:', role);

    if (role !== 'staff' && role !== 'super_admin') {
        console.error('[Stats API] Forbidden Role:', role);
        return new Response('Forbidden', { status: 403 });
    }

    try {
        console.log('[Stats API] Fetching metrics...');
        // 3. Fetch Data (Parallel)
        const lastWeek = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

        const [
            { data: listings },
            { data: claims },
            { data: failedUrls },
            { data: clicks },
            { data: categories }
        ] = await Promise.all([
            supabaseAdmin.from('listings').select('id, business_name, created_at, status, category:category_id(name), source_script, script_location'),
            supabaseAdmin.from('claims').select('*').order('created_at', { ascending: false }),
            supabaseAdmin.from('pending_research').select('*', { count: 'exact', head: true }), // Correct way to get count
            supabaseAdmin.from('clicks').select('id, created_at, listing_id').gte('created_at', lastWeek),
            supabaseAdmin.from('categories').select('id, name')
        ]);

        // Process Metrics (Server-Side to reduce payload)
        const totalListings = listings?.length || 0;
        const pendingCount = listings?.filter((l: any) => l.status === 'pending').length || 0;
        const totalClaims = claims?.length || 0;
        const pendingClaims = claims?.filter((c: any) => c.status === 'pending').length || 0;

        // Recent Activity (Last 5)
        const recentListings = (listings || [])
            .filter((l: any) => l.status === 'active')
            .sort((a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
            .slice(0, 5) || [];

        const responseData = {
            metrics: {
                totalListings,
                pendingCount,
                totalClaims,
                pendingClaims,
                recentClicks: clicks?.length || 0,
                failedUrls: failedUrls?.length || 1 // Correction: count() returns count in separate property if used? 
                // supabase-js count() usage: .select('*', { count: 'exact', head: true })
            },
            recentListings,
            claims: claims?.slice(0, 5) || [], // Latest 5 claims
            categories: categories || []
        };

        // Re-fetch count properly for failed urls
        const { count: failedCount } = await supabaseAdmin
            .from('pending_research')
            .select('*', { count: 'exact', head: true });

        responseData.metrics.failedUrls = failedCount || 0;

        return new Response(JSON.stringify(responseData), {
            headers: { 'Content-Type': 'application/json' }
        });

    } catch (e: any) {
        console.error('[Stats API] Unexpected Error:', e);
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
}
