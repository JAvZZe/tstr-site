import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://haimjeaetrsaauitrhfy.supabase.co';
const SERVICE_KEY = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

const supabaseAdmin = createClient(SUPABASE_URL, SERVICE_KEY);

async function verifySuperAdmin(request: Request) {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) return null;
    const token = authHeader.replace('Bearer ', '');
    const { data: { user }, error } = await supabaseAdmin.auth.getUser(token);
    if (error || !user) return null;
    const role = user.user_metadata?.role;
    return role === 'super_admin' ? user : null;
}

export const GET: APIRoute = async ({ request }) => {
    const user = await verifySuperAdmin(request);
    if (!user) return new Response('Unauthorized: Super Admin Access Required', { status: 403 });

    try {
        const { data: { users }, error } = await supabaseAdmin.auth.admin.listUsers();
        if (error) throw error;

        const staffUsers = users.filter(u =>
            u.user_metadata?.role === 'staff' || u.user_metadata?.role === 'super_admin'
        );

        return new Response(JSON.stringify({ users: staffUsers }), {
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (e: any) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
}

export const POST: APIRoute = async ({ request }) => {
    const user = await verifySuperAdmin(request);
    if (!user) return new Response('Unauthorized: Super Admin Access Required', { status: 403 });

    try {
        const body = await request.json();
        const { email, password, role } = body;

        if (!email || !password || !role) {
            return new Response(JSON.stringify({ error: 'Missing fields' }), { status: 400 });
        }

        const { data, error } = await supabaseAdmin.auth.admin.createUser({
            email,
            password,
            email_confirm: true,
            user_metadata: { role }
        });

        if (error) throw error;

        return new Response(JSON.stringify({ user: data.user }), { status: 200 });
    } catch (e: any) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
}
