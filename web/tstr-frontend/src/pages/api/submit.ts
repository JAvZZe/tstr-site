import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

// Load Supabase credentials from your .env file
// Ensure SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are set for secure server-side writes
const supabase = createClient(
  import.meta.env.PUBLIC_SUPABASE_URL || process.env.PUBLIC_SUPABASE_URL || '',
  import.meta.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY || ''
);

export const POST: APIRoute = async ({ request }) => {
  try {
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
      return new Response(JSON.stringify({ error: 'Database error occurred.' }), {
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
    return new Response(JSON.stringify({ error: 'Invalid request format.' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
