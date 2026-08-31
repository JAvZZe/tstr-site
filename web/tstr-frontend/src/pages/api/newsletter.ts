import type { APIRoute } from 'astro';
import { supabase } from '../../lib/supabase';
import { requiredString } from '../../lib/validate';

export const POST: APIRoute = async ({ request }) => {
  try {
    const raw = await request.text();
    const parsed = JSON.parse(raw);
    const firstNameR = requiredString(parsed?.firstName, 'First name', { max: 100 });
    const lastNameR = requiredString(parsed?.lastName, 'Last name', { max: 100 });
    const emailR = requiredString(parsed?.email, 'Email', { max: 200, email: true });
    if (!firstNameR.ok)
      return new Response(JSON.stringify({ error: firstNameR.error }), { status: 400 });
    if (!lastNameR.ok)
      return new Response(JSON.stringify({ error: lastNameR.error }), { status: 400 });
    if (!emailR.ok) return new Response(JSON.stringify({ error: emailR.error }), { status: 400 });

    const { error } = await supabase.from('newsletter_subscribers' as any).insert([
      {
        first_name: firstNameR.data,
        last_name: lastNameR.data,
        email: emailR.data.toLowerCase(),
      },
    ]);

    if (error) {
      if (error.code === '23505') {
        // Unique constraint violation (duplicate email)
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
