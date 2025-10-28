import { createClient } from '@supabase/supabase-js'

// Fallback to hardcoded values if env vars not available (Cloudflare Pages issue)
const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';
const supabaseKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY || 'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO';

console.log('Supabase URL:', supabaseUrl);
console.log('Supabase key:', supabaseKey ? 'present' : 'missing');

export const supabase = createClient(supabaseUrl, supabaseKey)
