import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    // Access environment variables from Cloudflare runtime
    const env = (locals as any).runtime?.env;
    
    // Fallback to hardcoded values if env vars not available (matches lib/supabase.ts pattern)
    const supabaseUrl = env?.PUBLIC_SUPABASE_URL || 
                        import.meta.env.PUBLIC_SUPABASE_URL || 
                        'https://haimjeaetrsaauitrhfy.supabase.co';
    
    const supabaseKey = env?.SUPABASE_SERVICE_ROLE_KEY || 
                        import.meta.env.SUPABASE_SERVICE_ROLE_KEY ||
                        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyOTQ0ODQzNywiZXhwIjoyMDQ1MDI0NDM3fQ.sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

    const supabase = createClient(supabaseUrl, supabaseKey);

    const data = await request.json();
    const email = data.email;

    if (!email) {
      return new Response(JSON.stringify({ error: 'Email is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return new Response(JSON.stringify({ error: 'Invalid email format' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Insert into the 'waitlist' table
    const { data: insertData, error } = await supabase
      .from('waitlist')
      .insert([{ email: email }])
      .select();

    if (error) {
      if (error.code === '23505') { // PostgreSQL unique constraint violation
        return new Response(JSON.stringify({ error: 'This email is already registered.' }), {
          status: 409, // Conflict
          headers: { 'Content-Type': 'application/json' },
        });
      }
      console.error('Supabase error:', error);
      return new Response(JSON.stringify({ 
        error: 'Database error occurred.',
        details: error.message 
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({ message: 'Success', id: insertData?.[0].id }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });

  } catch (e) {
    console.error('Request error:', e);
    return new Response(JSON.stringify({ 
      error: 'Invalid request format.',
      details: e instanceof Error ? e.message : String(e)
    }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
