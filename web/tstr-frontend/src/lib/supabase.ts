import { createClient } from '@supabase/supabase-js'

// Fallback to hardcoded values if env vars not available (Cloudflare Pages issue)
const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';

// For SSG (Static Site Generation), use service role key to access all data
// The service role key is only used at build time and doesn't get exposed to clients
// For CSR (Client Side Rendering), would use anon key instead
const supabaseKey = import.meta.env.SUPABASE_SERVICE_ROLE_KEY ||
                    import.meta.env.PUBLIC_SUPABASE_SERVICE_ROLE_KEY ||
                    'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2';  // Service role key for SSG

console.log('Supabase URL:', supabaseUrl);
console.log('Supabase key:', supabaseKey ? 'present' : 'missing');
console.log('Using service role key for SSG build');

export const supabase = createClient(supabaseUrl, supabaseKey)
