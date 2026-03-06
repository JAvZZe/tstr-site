import type { APIRoute } from 'astro';
import { supabase } from '../../lib/supabase';

export const POST: APIRoute = async ({ request }) => {
  try {
    const { firstName, lastName, email } = await request.json();

    if (!firstName || !lastName || !email) {
      return new Response(JSON.stringify({ error: 'All fields are required' }), { status: 400 });
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return new Response(JSON.stringify({ error: 'Invalid email address' }), { status: 400 });
    }

    const { error } = await supabase
      .from('newsletter_subscribers' as any)
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
