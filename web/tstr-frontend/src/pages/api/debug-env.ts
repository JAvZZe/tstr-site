import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ locals }) => {
  const env = (locals as any).runtime?.env;
  
  const debug = {
    hasRuntime: !!(locals as any).runtime,
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
