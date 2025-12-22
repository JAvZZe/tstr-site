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
                        'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';

    const supabase = createClient(supabaseUrl, supabaseKey);

    const data = await request.json();

    if (!data.id || !data.status) {
      return new Response(JSON.stringify({
        error: 'Missing required fields: id and status are required'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Validate status
    if (!['approved', 'rejected', 'pending'].includes(data.status)) {
      return new Response(JSON.stringify({
        error: 'Invalid status. Must be approved, rejected, or pending'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Update claim status
    const { data: updateData, error } = await supabase
      .from('claims')
      .update({ status: data.status })
      .eq('id', data.id)
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
      message: 'Claim status updated successfully',
      claim: updateData?.[0]
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