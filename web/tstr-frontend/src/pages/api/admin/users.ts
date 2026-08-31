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

async function verifySuperAdmin(request: Request, key: string | null) {
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
  return role === 'super_admin' ? user : null;
}

export const GET: APIRoute = async ({ request, locals }) => {
  const admin = getAdmin(locals);
  if (!admin) return new Response('Service key not configured', { status: 500 });

  const user = await verifySuperAdmin(request, getServiceKey(locals));
  if (!user) return new Response('Unauthorized: Super Admin Access Required', { status: 403 });

  try {
    const {
      data: { users },
      error,
    } = await admin.auth.admin.listUsers();
    if (error) throw error;

    const staffUsers = users.filter(
      (u) => u.app_metadata?.role === 'staff' || u.app_metadata?.role === 'super_admin'
    );

    return new Response(JSON.stringify({ users: staffUsers }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};

export const POST: APIRoute = async ({ request, locals }) => {
  const admin = getAdmin(locals);
  if (!admin) return new Response('Service key not configured', { status: 500 });

  const user = await verifySuperAdmin(request, getServiceKey(locals));
  if (!user) return new Response('Unauthorized: Super Admin Access Required', { status: 403 });

  try {
    const body = await request.json();
    const { email, password, role } = body;

    if (!email || !password || !role) {
      return new Response(JSON.stringify({ error: 'Missing fields' }), { status: 400 });
    }

    const { data, error } = await admin.auth.admin.createUser({
      email,
      password,
      email_confirm: true,
      app_metadata: { role },
    });

    if (error) throw error;

    return new Response(JSON.stringify({ user: data.user }), { status: 200 });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};

export const DELETE: APIRoute = async ({ request, locals }) => {
  const admin = getAdmin(locals);
  if (!admin) return new Response('Service key not configured', { status: 500 });

  const user = await verifySuperAdmin(request, getServiceKey(locals));
  if (!user) return new Response('Unauthorized: Super Admin Access Required', { status: 403 });

  try {
    const url = new URL(request.url);
    const id = url.searchParams.get('id');

    if (!id) return new Response('Missing ID', { status: 400 });

    const { error } = await admin.auth.admin.deleteUser(id);
    if (error) throw error;

    return new Response(JSON.stringify({ success: true }), { status: 200 });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};

export const PUT: APIRoute = async ({ request, locals }) => {
  const admin = getAdmin(locals);
  if (!admin) return new Response('Service key not configured', { status: 500 });

  const user = await verifySuperAdmin(request, getServiceKey(locals));
  if (!user) return new Response('Unauthorized: Super Admin Access Required', { status: 403 });

  try {
    const body = await request.json();
    const { id, role, password } = body;

    if (!id) return new Response('Missing ID', { status: 400 });

    const updates: any = {};
    if (role) updates.app_metadata = { role };
    if (password) updates.password = password;

    const { data, error } = await admin.auth.admin.updateUserById(id, updates);
    if (error) throw error;

    return new Response(JSON.stringify({ user: data.user }), { status: 200 });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
};
