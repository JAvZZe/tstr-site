import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';
import { requiredString } from '../../lib/validate';

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    // Access environment variables from Cloudflare runtime
    const env = (locals as { runtime?: { env?: Record<string, string> } }).runtime?.env;

    // Fallback to hardcoded values if env vars not available (matches lib/supabase.ts pattern)
    const supabaseUrl = env?.PUBLIC_SUPABASE_URL ||
      import.meta.env.PUBLIC_SUPABASE_URL ||
      'https://haimjeaetrsaauitrhfy.supabase.co';

    const supabaseKey = env?.SUPABASE_SERVICE_ROLE_KEY ||
      import.meta.env.SUPABASE_SERVICE_ROLE_KEY ||
      import.meta.env.SUPABASE_SERVICE_ROLE_KEY;

    const supabase = createClient(supabaseUrl, supabaseKey);

    const emailR = requiredString((await request.json()).email, 'Email', { max: 200, email: true });
    if (!emailR.ok) {
      return new Response(JSON.stringify({ error: emailR.error }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }
    const email = emailR.data;

    // Insert into the 'waitlist' table
    const { data: insertData, error } = await supabase
      .from('waitlist')
      .insert([{ email }])
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
        error: 'Database error occurred.'
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
      error: 'Invalid request format.'
    }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
