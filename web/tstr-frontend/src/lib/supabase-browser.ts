import { createClient } from '@supabase/supabase-js'

// Browser-side Supabase client for authentication
// Uses anon key (safe to expose to client)

const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co'

// Anon key - safe for client-side use (RLS policies protect data)
const supabaseAnonKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY ||
  'sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2'

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
