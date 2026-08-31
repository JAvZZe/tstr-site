import { createClient, SupabaseClient } from '@supabase/supabase-js';

const SUPABASE_URL =
  import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';

/**
 * Get the Supabase service-role key.
 *
 * Cloudflare Pages injects secrets at runtime via locals.runtime.env, NOT
 * import.meta.env (which is build-time only and empty for secrets). Check
 * there first, then fall back to the build-time value for local dev.
 */
export function getServiceKey(locals?: unknown): string | null {
  const env = (locals as { runtime?: { env?: Record<string, string> } } | undefined)?.runtime?.env;
  return env?.SUPABASE_SERVICE_ROLE_KEY || import.meta.env.SUPABASE_SERVICE_ROLE_KEY || null;
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
