import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';
import { getServiceKey } from '../../../lib/supabase-admin';

const SUPABASE_URL =
  import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';

function getAdmin(locals: unknown) {
  const key = getServiceKey(locals);
  if (!key) return null;
  return createClient(SUPABASE_URL, key);
}

async function verifyAuth(request: Request, key: string | null) {
  if (!key) return null;
  const authHeader = request.headers.get('Authorization');
  if (!authHeader) return null;
  const token = authHeader.replace('Bearer ', '');
  const supabase = createClient(SUPABASE_URL, key);
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser(token);
  if (error || !user) return null;
  const role = user.app_metadata?.role;
  if (role !== 'staff' && role !== 'super_admin') return null;
  return user;
}

export const GET: APIRoute = async ({ request, locals }) => {
  const admin = getAdmin(locals);
  if (!admin) return new Response('Service key not configured', { status: 500 });

  const user = await verifyAuth(request, getServiceKey(locals));
  if (!user) return new Response('Unauthorized', { status: 401 });

  try {
    const url = new URL(request.url);
    const statusFilter = url.searchParams.get('status');

    let query = admin
      .from('listings')
      .select(
        'id, business_name, website, category:category_id(name), status, created_at, source_script'
      )
      .order('created_at', { ascending: false });

    if (statusFilter) {
      query = query.eq('status', statusFilter);
    }

    const { data: listings, error } = await query;

    if (error) throw error;

    return new Response(JSON.stringify(listings), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};

export const POST: APIRoute = async ({ request, locals }) => {
  const admin = getAdmin(locals);
  if (!admin) return new Response('Service key not configured', { status: 500 });

  const user = await verifyAuth(request, getServiceKey(locals));
  if (!user) return new Response('Unauthorized', { status: 401 });

  try {
    const body = await request.json();
    const { id, ...updates } = body;

    if (!id) return new Response('Missing ID', { status: 400 });

    const allowed = ['business_name', 'status', 'website', 'category_id'];
    const payload: any = {};

    for (const key of allowed) {
      if (updates[key] !== undefined) payload[key] = updates[key];
    }

    const { error } = await admin.from('listings').update(payload).eq('id', id);

    if (error) throw error;

    return new Response(JSON.stringify({ success: true }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};
