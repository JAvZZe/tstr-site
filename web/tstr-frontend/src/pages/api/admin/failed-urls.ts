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
    const { data: failedUrls, error: failedError } = await admin
      .from('pending_research')
      .select('id, website, validation_error, business_name, created_at')
      .order('created_at', { ascending: false });

    if (failedError) throw failedError;

    let correctedUrls: string[] = [];
    if (failedUrls && failedUrls.length > 0) {
      const websites = failedUrls.map((item) => item.website).filter(Boolean);

      if (websites.length > 0) {
        const { data: listings } = await admin
          .from('listings')
          .select('website')
          .in('website', websites)
          .eq('status', 'active');

        if (listings) {
          correctedUrls = listings.map((l) => l.website);
        }
      }
    }

    return new Response(JSON.stringify({ failedUrls, correctedUrls }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};
