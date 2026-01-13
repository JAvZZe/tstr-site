import type { APIRoute } from 'astro'
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.SUPABASE_URL
const supabaseServiceKey = import.meta.env.SUPABASE_SERVICE_ROLE_KEY

if (!supabaseUrl || !supabaseServiceKey) {
  throw new Error('Missing Supabase environment variables')
}

const supabase = createClient(supabaseUrl, supabaseServiceKey)

export const POST: APIRoute = async ({ request }) => {
  try {
    // Get authenticated user
    const authHeader = request.headers.get('Authorization')
    if (!authHeader?.startsWith('Bearer ')) {
      return new Response(JSON.stringify({ error: 'Authentication required' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    const token = authHeader.substring(7)
    const { data: { user }, error: authError } = await supabase.auth.getUser(token)

    if (authError || !user) {
      return new Response(JSON.stringify({ error: 'Invalid authentication' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    const { pendingToken } = await request.json()

    if (!pendingToken) {
      return new Response(JSON.stringify({ error: 'Pending token required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    const { data: profile, error } = await supabase
      .from('user_profiles')
      .select('pending_subscription_data, pending_subscription_expires_at')
      .eq('id', user.id)
      .eq('pending_subscription_token', pendingToken)
      .gt('pending_subscription_expires_at', new Date().toISOString())
      .single()

    if (error || !profile) {
      return new Response(JSON.stringify({ error: 'Invalid or expired pending token' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    return new Response(JSON.stringify({
      success: true,
      pending_data: profile.pending_subscription_data,
      expires_at: profile.pending_subscription_expires_at
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('Resume pending subscription error:', error)
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}