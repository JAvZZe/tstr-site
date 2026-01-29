import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

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
      'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

    const supabase = createClient(supabaseUrl, supabaseKey);

    const data = await request.json();

    // Basic Validation
    if (!data.business_email || !data.provider_name || !data.contact_name) {
      return new Response(JSON.stringify({
        error: 'Missing required fields: provider_name, contact_name, and business_email are required'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.business_email)) {
      return new Response(JSON.stringify({ error: 'Invalid email format' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Insert claim into database
    const { data: insertData, error } = await supabase
      .from('claims')
      .insert([{
        provider_name: data.provider_name,
        contact_name: data.contact_name,
        business_email: data.business_email,
        phone: data.phone || null
      }])
      .select();

    if (error) {
      console.error('Supabase error:', error);
      return new Response(JSON.stringify({
        error: 'Database error occurred.',
        details: error.message
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response(JSON.stringify({
      message: 'Claim received successfully',
      id: insertData?.[0].id
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });

  } catch (e) {
    console.error('Request error:', e);
    return new Response(JSON.stringify({
      error: 'Invalid request format.',
      details: e instanceof Error ? e.message : String(e)
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
