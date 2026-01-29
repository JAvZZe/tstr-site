import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ locals }) => {
  const env = (locals as { runtime?: { env?: Record<string, string> } }).runtime?.env;

  const supabaseUrl = env?.PUBLIC_SUPABASE_URL ||
    import.meta.env.PUBLIC_SUPABASE_URL ||
    'FALLBACK_URL';

  const supabaseKey = env?.SUPABASE_SERVICE_ROLE_KEY ||
    import.meta.env.SUPABASE_SERVICE_ROLE_KEY ||
    'FALLBACK_KEY';

  const debug = {
    urlSource: env?.PUBLIC_SUPABASE_URL ? 'runtime.env' :
      (import.meta.env.PUBLIC_SUPABASE_URL ? 'import.meta.env' : 'fallback'),
    keySource: env?.SUPABASE_SERVICE_ROLE_KEY ? 'runtime.env' :
      (import.meta.env.SUPABASE_SERVICE_ROLE_KEY ? 'import.meta.env' : 'fallback'),
    urlValue: supabaseUrl,
    keyFirstPart: supabaseKey.substring(0, 20) + '...',
    keyLength: supabaseKey.length,
    keyLooksValid: supabaseKey.startsWith('eyJ'),
  };

  return new Response(JSON.stringify(debug, null, 2), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};
