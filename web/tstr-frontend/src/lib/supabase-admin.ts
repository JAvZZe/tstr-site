import { createClient, SupabaseClient } from '@supabase/supabase-js';

const SUPABASE_URL =
  import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';

/**
 * Get the Supabase service-role key.
 *
 * Cloudflare Pages injects secrets at runtime. Try multiple sources:
 * 1. locals.runtime.env (Astro Cloudflare adapter way)
 * 2. process.env (Cloudflare Workers native way)
 * 3. import.meta.env (build-time, for local dev)
 */
export function getServiceKey(locals?: unknown): string | null {
  // Astro Cloudflare adapter way
  if (locals) {
    const env = (locals as { runtime?: { env?: Record<string, string> } }).runtime?.env;
    if (env?.SUPABASE_SERVICE_ROLE_KEY) return env.SUPABASE_SERVICE_ROLE_KEY;
  }

  // Cloudflare Workers native way
  if (typeof process !== 'undefined' && process.env?.SUPABASE_SERVICE_ROLE_KEY) {
    return process.env.SUPABASE_SERVICE_ROLE_KEY;
  }

  // Build-time fallback (local dev)
  if (import.meta.env.SUPABASE_SERVICE_ROLE_KEY) {
    return import.meta.env.SUPABASE_SERVICE_ROLE_KEY;
  }

  return null;
}

export function createAdminClient(locals?: unknown): SupabaseClient | null {
  const key = getServiceKey(locals);
  if (!key) return null;
  return createClient(SUPABASE_URL, key);
}

export async function verifyAdminAuth(
  request: Request,
  locals?: unknown
): Promise<{ id: string; email?: string; app_metadata?: Record<string, unknown> } | null> {
  const key = getServiceKey(locals);
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

  return user as { id: string; email?: string; app_metadata?: Record<string, unknown> };
}
