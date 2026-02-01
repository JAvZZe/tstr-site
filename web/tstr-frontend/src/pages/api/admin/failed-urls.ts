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
        // Fetch failed URLs
        const { data: failedUrls, error: failedError } = await supabaseAdmin
            .from('pending_research')
            .select('id, website, validation_error, business_name, created_at')
            .order('created_at', { ascending: false });

        if (failedError) throw failedError;

        // Check which URLs are corrected
        let correctedUrls: string[] = [];
        if (failedUrls && failedUrls.length > 0) {
            const websites = failedUrls.map(item => item.website).filter(Boolean);

            if (websites.length > 0) {
                const { data: listings } = await supabaseAdmin
                    .from('listings')
                    .select('website')
                    .in('website', websites)
                    .eq('status', 'active');

                if (listings) {
                    correctedUrls = listings.map(l => l.website);
                }
            }
        }

        return new Response(JSON.stringify({ failedUrls, correctedUrls }), {
            headers: { 'Content-Type': 'application/json' }
        });

    } catch (e: any) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
};
