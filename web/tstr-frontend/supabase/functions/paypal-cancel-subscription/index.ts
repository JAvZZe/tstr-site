import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const PAYPAL_CLIENT_ID = Deno.env.get('PAYPAL_CLIENT_ID')!
const PAYPAL_CLIENT_SECRET = Deno.env.get('PAYPAL_CLIENT_SECRET')!
const PAYPAL_MODE = Deno.env.get('PAYPAL_MODE') || 'sandbox'
const PAYPAL_API_URL = PAYPAL_MODE === 'live'
  ? 'https://api-m.paypal.com'
  : 'https://api-m.sandbox.paypal.com'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

async function getPayPalAccessToken(): Promise<string> {
  const auth = btoa(`${PAYPAL_CLIENT_ID}:${PAYPAL_CLIENT_SECRET}`)
  const response = await fetch(`${PAYPAL_API_URL}/v1/oauth2/token`, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${auth}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'grant_type=client_credentials',
  })
  const data = await response.json()
  return data.access_token
}

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    console.log('🚀 PayPal Cancel Subscription Function Called')

    // Parse request body
    let requestBody
    try {
      requestBody = await req.json()
    } catch (e) {
      return new Response(JSON.stringify({ error: 'Invalid JSON request body' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    const { userId, reason } = requestBody

    if (!userId) {
      return new Response(JSON.stringify({ error: 'Missing userId' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Use Service Role to access database (reliable auth)
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    )

    // Validate user exists
    const { data: profile, error: profileError } = await supabase
      .from('user_profiles')
      .select('id, paypal_subscription_id')
      .eq('id', userId)
      .maybeSingle()

    if (profileError || !profile) {
      console.error('Profile lookup failed:', profileError || 'User not found')
      return new Response(JSON.stringify({ error: 'User profile not found' }), {
        status: 404,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    if (!profile.paypal_subscription_id) {
      console.log('No subscription to cancel for user:', userId)
      return new Response(JSON.stringify({ error: 'No active subscription found' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Cancel subscription in PayPal
    console.log('Cancelling PayPal subscription:', profile.paypal_subscription_id)
    const accessToken = await getPayPalAccessToken()

    const cancelResponse = await fetch(
      `${PAYPAL_API_URL}/v1/billing/subscriptions/${profile.paypal_subscription_id}/cancel`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ reason: reason || 'User requested cancellation' })
      }
    )

    // Treat 204 (Success), 404 (Not Found), and 422 (Unprocessable - usually already cancelled) as effective cancellations
    if (cancelResponse.status === 204 || cancelResponse.status === 404 || cancelResponse.status === 422) {
      console.log(`PayPal cancellation resolved (Status: ${cancelResponse.status}). Updating DB...`)

      // Update local status
      const { error: updateError } = await supabase.from('user_profiles').update({
        subscription_status: 'cancelled',
        subscription_tier: 'free',
        paypal_subscription_id: null
      }).eq('id', userId)

      if (updateError) {
        console.error('Failed to update user profile status:', updateError)
      }

      return new Response(JSON.stringify({ success: true, paypal_status: cancelResponse.status }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    } else {
      const errorData = await cancelResponse.json()
      console.error('PayPal API cancel error:', errorData)
      return new Response(JSON.stringify({
        error: 'Failed to cancel subscription with PayPal',
        details: errorData
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

  } catch (error) {
    console.error('Internal Function Error:', error)
    return new Response(JSON.stringify({ error: 'Internal server error', details: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})