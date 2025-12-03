import { createClient } from '@supabase/supabase-js'

// Browser-side Supabase client for authentication
// Uses anon key (safe to expose to client)

const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co'

// Anon key - safe for client-side use (RLS policies protect data)
const supabaseAnonKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY ||
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzQ1NDUzMTMsImV4cCI6MjA1MDEyMTMxM30.a4z9mqyKFiB-GgW_1sF5VcNlqjdMD-1h-RIu5WUwCos'

export const supabaseBrowser = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    flowType: 'pkce'
  }
})

// Helper function to get current user
export async function getCurrentUser() {
  const { data: { user }, error } = await supabaseBrowser.auth.getUser()
  if (error) {
    console.error('Error getting user:', error)
    return null
  }
  return user
}

// Helper function to get user profile with subscription tier
export async function getUserProfile(userId: string) {
  const { data, error } = await supabaseBrowser
    .from('user_profiles')
    .select('*')
    .eq('id', userId)
    .single()

  if (error) {
    console.error('Error getting user profile:', error)
    return null
  }
  return data
}

// Helper function to get user tier
export async function getUserTier() {
  const user = await getCurrentUser()
  if (!user) return 'free'

  const profile = await getUserProfile(user.id)
  return profile?.subscription_tier || 'basic'
}
