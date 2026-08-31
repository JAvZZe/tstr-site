import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';
import { sendEmail, createClaimStatusEmail } from '../../../lib/email';

const SUPABASE_URL =
  import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';

function getServiceKey(locals: unknown): string | null {
  const env = (locals as { runtime?: { env?: Record<string, string> } }).runtime?.env;
  return env?.SUPABASE_SERVICE_ROLE_KEY || import.meta.env.SUPABASE_SERVICE_ROLE_KEY || null;
}

async function verifyAuth(request: Request, serviceKey: string | null) {
  if (!serviceKey) return null;
  const authHeader = request.headers.get('Authorization');
  if (!authHeader) return null;
  const token = authHeader.replace('Bearer ', '');
  const supabaseAdmin = createClient(SUPABASE_URL, serviceKey);
  const {
    data: { user },
    error,
  } = await supabaseAdmin.auth.getUser(token);
  if (error || !user) return null;
  const role = user.app_metadata?.role;
  if (role !== 'staff' && role !== 'super_admin') return null;
  return user;
}

export const GET: APIRoute = async ({ request, locals }) => {
  const serviceKey = getServiceKey(locals);
  const user = await verifyAuth(request, serviceKey);
  if (!user) return new Response('Unauthorized', { status: 401 });

  const supabaseAdmin = createClient(SUPABASE_URL, serviceKey!);
  const { data: claims, error } = await supabaseAdmin
    .from('claims')
    .select('id, provider_name, contact_name, business_email, phone, created_at, status')
    .order('created_at', { ascending: false });

  if (error) return new Response(JSON.stringify({ error: error.message }), { status: 500 });

  return new Response(JSON.stringify(claims), { headers: { 'Content-Type': 'application/json' } });
};

export const POST: APIRoute = async ({ request, locals }) => {
  const serviceKey = getServiceKey(locals);
  const user = await verifyAuth(request, serviceKey);
  if (!user) return new Response('Unauthorized', { status: 401 });

  try {
    const body = await request.json();
    const { id, status } = body;

    if (!id || !['approved', 'rejected'].includes(status)) {
      return new Response('Invalid Request', { status: 400 });
    }

    const supabaseAdmin = createClient(SUPABASE_URL, serviceKey!);
    const { data: claim, error: fetchError } = await supabaseAdmin
      .from('claims')
      .select('id, provider_name, business_email, status')
      .eq('id', id)
      .single();

    if (fetchError || !claim) {
      return new Response(JSON.stringify({ error: 'Claim not found' }), { status: 404 });
    }

    const { error } = await supabaseAdmin.from('claims').update({ status }).eq('id', id);

    if (error) return new Response(JSON.stringify({ error: error.message }), { status: 500 });

    if (claim.business_email) {
      const emailTemplate = createClaimStatusEmail(
        claim.provider_name,
        status as 'approved' | 'rejected'
      );
      await sendEmail(claim.business_email, emailTemplate);
    }

    return new Response(JSON.stringify({ success: true }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 400 });
  }
};
