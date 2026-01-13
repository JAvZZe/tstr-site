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

    const { tier, checkoutData } = await request.json()

    if (!tier || !['professional', 'premium'].includes(tier)) {
      return new Response(JSON.stringify({ error: 'Invalid subscription tier' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Generate secure token for recovery
    const pendingToken = crypto.randomUUID()
    const expiresAt = new Date(Date.now() + 30 * 60 * 1000) // 30 minutes

    const { error: updateError } = await supabase
      .from('user_profiles')
      .update({
        pending_subscription_data: {
          tier,
          checkoutData,
          created_at: new Date().toISOString()
        },
        pending_subscription_token: pendingToken,
        pending_subscription_expires_at: expiresAt.toISOString()
      })
      .eq('id', user.id)

    if (updateError) {
      console.error('Database update error:', updateError)
      return new Response(JSON.stringify({ error: 'Failed to save pending subscription' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    return new Response(JSON.stringify({
      success: true,
      pending_token: pendingToken,
      expires_at: expiresAt.toISOString()
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('Save pending subscription error:', error)
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}