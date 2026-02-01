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
        const url = new URL(request.url);
        const statusFilter = url.searchParams.get('status');

        let query = supabaseAdmin
            .from('listings')
            .select('id, business_name, website, category:category_id(name), status, created_at, source_script')
            .order('created_at', { ascending: false });

        if (statusFilter) {
            query = query.eq('status', statusFilter);
        }

        const { data: listings, error } = await query;

        if (error) throw error;

        return new Response(JSON.stringify(listings), {
            headers: { 'Content-Type': 'application/json' }
        });

    } catch (e: any) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
};
