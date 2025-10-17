import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL;
const supabaseKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY;

console.log('Supabase Env Vars Loaded:', { 
  url: typeof supabaseUrl, 
  key: typeof supabaseKey 
});

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase credentials:', { supabaseUrl: !!supabaseUrl, supabaseKey: !!supabaseKey })
}

export const supabase = createClient(supabaseUrl || '', supabaseKey || '')
