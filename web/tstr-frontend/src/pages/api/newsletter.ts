import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const POST: APIRoute = async ({ request }) => {
  try {
    const { firstName, lastName, email } = await request.json();

    if (!firstName || !lastName || !email) {
      return new Response(JSON.stringify({ error: 'All fields are required' }), { status: 400 });
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return new Response(JSON.stringify({ error: 'Invalid email address' }), { status: 400 });
    }

    // Create a server-side Supabase client using secrets
    // Note: In Cloudflare/Astro, environment variables are accessed differently
    const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL;
    const supabaseKey = import.meta.env.SUPABASE_SERVICE_ROLE_KEY;

    if (!supabaseUrl || !supabaseKey) {
      console.error('Missing Supabase configuration');
      return new Response(JSON.stringify({ error: 'Server configuration error' }), { status: 500 });
    }

    const supabase = createClient(supabaseUrl, supabaseKey);

    const { error } = await supabase
      .from('newsletter_subscribers')
      .insert([
        { 
          first_name: firstName, 
          last_name: lastName, 
          email: email.toLowerCase() 
        }
      ]);

    if (error) {
      if (error.code === '23505') { // Unique constraint violation (duplicate email)
        return new Response(JSON.stringify({ error: 'Email already subscribed' }), { status: 400 });
      }
      throw error;
    }

    return new Response(JSON.stringify({ message: 'Subscribed successfully!' }), { status: 200 });
  } catch (error: any) {
    console.error('Newsletter Signup Error:', error);
    return new Response(JSON.stringify({ error: 'Failed to subscribe' }), { status: 500 });
  }
};
