import { createClient } from '@supabase/supabase-js'
import type { Database } from '../types/supabase'

// Fallback to hardcoded values if env vars not available (Cloudflare Pages issue)
const supabaseUrl = (import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co').trim();

// For SSG (Static Site Generation), use service role key to access all data
// The service role key is only used at build time and doesn't get exposed to clients
// For CSR (Client Side Rendering), would use anon key instead
const supabaseKey = (
  import.meta.env.SUPABASE_SERVICE_ROLE_KEY ||
  import.meta.env.PUBLIC_SUPABASE_SERVICE_ROLE_KEY ||
  import.meta.env.PUBLIC_SUPABASE_ANON_KEY
)?.trim();

if (!supabaseKey) {
  console.error('Supabase key (Service Role or Anon) is missing!');
  throw new Error('Supabase configuration error: Missing API Key');
}

if (import.meta.env.SUPABASE_SERVICE_ROLE_KEY || import.meta.env.PUBLIC_SUPABASE_SERVICE_ROLE_KEY) {
    console.log('Using service role key for Supabase client');
} else {
    console.log('Using public anon key for Supabase client');
}


console.log('Supabase URL:', supabaseUrl);
console.log('Supabase key:', supabaseKey ? 'present' : 'missing');
console.log('Using service role key for SSG build');

export const supabase = createClient<Database>(supabaseUrl, supabaseKey)
