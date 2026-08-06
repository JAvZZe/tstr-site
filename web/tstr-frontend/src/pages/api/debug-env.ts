import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ locals }) => {
  // SECURITY: debug endpoints must never be reachable in production.
  // Opt-in only via PUBLIC_DEBUG_ENDPOINTS=true (dev/diagnostics). See SECURITY_FINDINGS_FRONTEND_SECRETS.md.
  if (import.meta.env.PUBLIC_DEBUG_ENDPOINTS !== 'true') {
    return new Response(JSON.stringify({ error: 'not_found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const env = (locals as { runtime?: { env?: Record<string, string> } }).runtime?.env;

  const debug = {
    hasRuntime: !!(locals as { runtime?: unknown }).runtime,
    hasEnv: !!env,
    envKeys: env ? Object.keys(env) : [],
    importMetaEnvKeys: Object.keys(import.meta.env),
    hasPublicUrl: !!import.meta.env.PUBLIC_SUPABASE_URL,
    hasServiceKey: !!import.meta.env.SUPABASE_SERVICE_ROLE_KEY,
    runtimeEnvHasPublicUrl: env?.PUBLIC_SUPABASE_URL ? 'yes' : 'no',
    runtimeEnvHasServiceKey: env?.SUPABASE_SERVICE_ROLE_KEY ? 'yes' : 'no',
  };

  return new Response(JSON.stringify(debug, null, 2), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};
