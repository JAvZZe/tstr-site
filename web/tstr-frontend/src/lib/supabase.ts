import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL;
const supabaseKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY;

// Debug: Log all import.meta.env to see what's available
console.log('All import.meta.env:', import.meta.env);
console.log('PUBLIC_SUPABASE_URL:', supabaseUrl);
console.log('PUBLIC_SUPABASE_ANON_KEY:', supabaseKey ? 'present' : 'missing');

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase credentials:', { supabaseUrl: !!supabaseUrl, supabaseKey: !!supabaseKey })
}

export const supabase = createClient(supabaseUrl || '', supabaseKey || '')
