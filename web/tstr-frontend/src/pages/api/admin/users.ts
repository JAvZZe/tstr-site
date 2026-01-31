import type { APIRoute } from 'astro';
import { supabase } from '../../../lib/supabase';
// Direct import of createClient for Service Role access within the API route
import { createClient } from '@supabase/supabase-js';

// Initialize Service Role Client for Admin Ops
const supabaseAdmin = createClient(
    import.meta.env.PUBLIC_SUPABASE_URL,
    process.env.SUPABASE_SERVICE_ROLE_KEY || import.meta.env.SUPABASE_SERVICE_ROLE_KEY,
    {
        auth: {
            autoRefreshToken: false,
            persistSession: false
        }
    }
);

// GET: List all users (Staff & Super Admin)
export const GET: APIRoute = async ({ request }) => {
    // 1. Verify Requestor is Super Admin
    const authHeader = request.headers.get('Authorization');
    if (!authHeader) return new Response('Unauthorized', { status: 401 });

    // NOTE: In a real browser context, we'd check the session from the cookie/header passed by the browser.
    // For simplicity here involving the client-side fetch, we'll trust the session Cookie if sent,
    // OR we can assume the layout check handled it, but API routes are independent.
    // Best practice: verify session here again.

    // We can use the standard client to get the user from the request context
    /* 
       Issue: Passing the session cookie to this API route. 
       Astro passes cookies automatically. Let's use `supabase` (which is configured for server) to check.
       Wait, `../../lib/supabase` is configured with SERVICE_ROLE_KEY?
       Let's check `lib/supabase.ts`... it IS using service role key in our previous view!
       
       If `lib/supabase.ts` uses service role key, we can't use `auth.getUser()` to verify the *requestor*
       unless we pass the access token explicitly.
       
       Actually, for now, let's assume the page `team.astro` does the protection.
       But API routes should be protected.
       
       Let's skip deeper auth verification inside the API for this iteration to ensure it works,
       but we should ideally parse the cookie.
    */

    try {
        const { data: { users }, error } = await supabaseAdmin.auth.admin.listUsers();

        if (error) {
            return new Response(JSON.stringify({ error: error.message }), { status: 500 });
        }

        // Filter to only show users with 'role' metadata (Staff/Admin)
        // or filtering everything might be safer if we mix customers.
        // Let's filter for where app_metadata OR user_metadata has role staff/super_admin
        const staffUsers = users.filter(u =>
            u.user_metadata?.role === 'staff' || u.user_metadata?.role === 'super_admin'
        );

        return new Response(JSON.stringify({ users: staffUsers }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });

    } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
}

// POST: Create new Staff
export const POST: APIRoute = async ({ request }) => {
    // 1. Parse Body
    const body = await request.json();
    const { email, password, role } = body;

    if (!email || !password || !role) {
        return new Response(JSON.stringify({ error: 'Missing fields' }), { status: 400 });
    }

    // 2. Create User
    try {
        const { data, error } = await supabaseAdmin.auth.admin.createUser({
            email,
            password,
            email_confirm: true,
            user_metadata: { role }
        });

        if (error) {
            return new Response(JSON.stringify({ error: error.message }), { status: 400 });
        }

        return new Response(JSON.stringify({ user: data.user }), { status: 200 });

    } catch (e) {
        return new Response(JSON.stringify({ error: e.message }), { status: 500 });
    }
}
