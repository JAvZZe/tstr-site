import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

// Hardcoded Service Key (as referenced in automation scripts)
// In production, this should be a secure environment variable.
const SUPABASE_URL = 'https://haimjeaetrsaauitrhfy.supabase.co';
const SERVICE_KEY = 'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

const supabaseAdmin = createClient(SUPABASE_URL, SERVICE_KEY, {
    auth: {
        autoRefreshToken: false,
        persistSession: false
    }
});

export const POST: APIRoute = async ({ request }) => {
    try {
        const body = await request.json();
        const { email, password } = body;

        // 1. Basic Validation
        if (!email || !password) {
            return new Response(JSON.stringify({ error: 'Email and password required' }), { status: 400 });
        }

        // 2. Perform Login via Service Role (Bypasses Captcha)
        const { data, error } = await supabaseAdmin.auth.signInWithPassword({
            email,
            password
        });

        if (error) {
            return new Response(JSON.stringify({ error: error.message }), { status: 401 });
        }

        if (!data.session || !data.user) {
            return new Response(JSON.stringify({ error: 'No session returned' }), { status: 500 });
        }

        // 3. Security: Check if user is actually Staff/Admin
        // We don't want regular customers using this endpoint to bypass captcha
        const role = data.user.user_metadata?.role;
        if (role !== 'staff' && role !== 'super_admin') {
            // Allow specific overrides if needed (legacy check), but mostly rely on role
            return new Response(JSON.stringify({ error: 'Unauthorized: Staff access only' }), { status: 403 });
        }

        // 4. Return Session
        return new Response(JSON.stringify({
            session: {
                access_token: data.session.access_token,
                refresh_token: data.session.refresh_token,
                user: data.user
            }
        }), { status: 200 });

    } catch (e: any) {
        return new Response(JSON.stringify({ error: e.message || 'Internal Server Error' }), { status: 500 });
    }
};
