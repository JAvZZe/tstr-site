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

    const { data: claims, error } = await supabaseAdmin
        .from('claims')
        .select('id, provider_name, contact_name, business_email, phone, created_at, status')
        .order('created_at', { ascending: false });

    if (error) return new Response(JSON.stringify({ error: error.message }), { status: 500 });

    return new Response(JSON.stringify(claims), { headers: { 'Content-Type': 'application/json' } });
};

export const POST: APIRoute = async ({ request }) => {
    const user = await verifyAuth(request);
    if (!user) return new Response('Unauthorized', { status: 401 });

    try {
        const body = await request.json();
        const { id, status } = body;

        if (!id || !['approved', 'rejected'].includes(status)) {
            return new Response('Invalid Request', { status: 400 });
        }

        const { error } = await supabaseAdmin
            .from('claims')
            .update({ status })
            .eq('id', id);

        if (error) return new Response(JSON.stringify({ error: error.message }), { status: 500 });

        return new Response(JSON.stringify({ success: true }), { headers: { 'Content-Type': 'application/json' } });
    } catch (e: any) {
        return new Response(JSON.stringify({ error: e.message }), { status: 400 });
    }
}
