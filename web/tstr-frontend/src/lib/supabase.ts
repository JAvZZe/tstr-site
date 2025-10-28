import { createClient } from '@supabase/supabase-js'

// Fallback to hardcoded values if env vars not available (Cloudflare Pages issue)
const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';
const supabaseKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjAxNTksImV4cCI6MjA3NTYzNjE1OX0.1SoHZoMAeap4p2Fy4HxzHJ4IRZWZ78VamGd0JWQ0OqM';

console.log('Supabase URL:', supabaseUrl);
console.log('Supabase key:', supabaseKey ? 'present' : 'missing');

export const supabase = createClient(supabaseUrl, supabaseKey)
