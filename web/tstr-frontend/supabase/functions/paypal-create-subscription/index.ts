import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const PAYPAL_CLIENT_ID = Deno.env.get('PAYPAL_CLIENT_ID')!
const PAYPAL_CLIENT_SECRET = Deno.env.get('PAYPAL_CLIENT_SECRET')!
const PAYPAL_MODE = Deno.env.get('PAYPAL_MODE') || 'sandbox'
const PAYPAL_API_URL = PAYPAL_MODE === 'live'
  ? 'https://api-m.paypal.com'
  : 'https://api-m.sandbox.paypal.com'

// Plan IDs from PayPal Dashboard (user must fill these after creating plans)
const PLAN_IDS: Record<string, string> = {
  professional: Deno.env.get('PAYPAL_PLAN_PROFESSIONAL') || '',
  premium: Deno.env.get('PAYPAL_PLAN_PREMIUM') || ''
}

console.log('Edge Function starting...')
console.log('Environment variables check:', {
  PAYPAL_CLIENT_ID: !!PAYPAL_CLIENT_ID,
  PAYPAL_CLIENT_SECRET: !!PAYPAL_CLIENT_SECRET,
  PAYPAL_PLAN_PROFESSIONAL: !!PLAN_IDS.professional,
  PAYPAL_PLAN_PREMIUM: !!PLAN_IDS.premium,
  SUPABASE_URL: !!Deno.env.get('SUPABASE_URL'),
  SUPABASE_ANON_KEY: !!Deno.env.get('SUPABASE_ANON_KEY'),
})
console.log('Actual SUPABASE_URL:', Deno.env.get('SUPABASE_URL'))
console.log('Actual SUPABASE_ANON_KEY starts with:', Deno.env.get('SUPABASE_ANON_KEY')?.substring(0, 20) + '...')

console.log('Edge Function initialized with PLAN_IDS:', PLAN_IDS)

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
    console.log('Edge Function called with method:', req.method)
    console.log('Headers:', Object.fromEntries(req.headers.entries()))

    // Get user from Supabase auth
    const authHeader = req.headers.get('Authorization')
    console.log('Auth header present:', !!authHeader)
    console.log('Auth header value:', authHeader ? authHeader.substring(0, 50) + '...' : 'none')
    console.log('All headers:', Object.fromEntries(req.headers.entries()))

    if (!authHeader) {
      return new Response(JSON.stringify({ error: 'Missing authorization header' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Create Supabase client with proper auth context
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      {
        global: {
          headers: {
            Authorization: authHeader
          }
        }
      }
    )

    // Get user from Supabase auth
    const { data: { user }, error: authError } = await supabase.auth.getUser()

    console.log('Supabase auth result:', {
      user: !!user,
      error: authError?.message,
      userId: user?.id,
      userEmail: user?.email
    })

    if (authError || !user) {
      // Detailed JWT debugging
      let jwtDebug = {}
      try {
        if (authHeader && authHeader.startsWith('Bearer ')) {
          const token = authHeader.substring(7)
          const parts = token.split('.')
          if (parts.length === 3) {
            const payload = JSON.parse(atob(parts[1].replace(/-/g, '+').replace(/_/g, '/')))
            jwtDebug = {
              header: JSON.parse(atob(parts[0].replace(/-/g, '+').replace(/_/g, '/'))),
              payload: {
                iss: payload.iss,
                sub: payload.sub,
                aud: payload.aud,
                exp: payload.exp,
                iat: payload.iat,
                expDate: new Date(payload.exp * 1000).toISOString(),
                iatDate: new Date(payload.iat * 1000).toISOString(),
                isExpired: payload.exp * 1000 < Date.now(),
                timeToExpiry: Math.floor((payload.exp * 1000 - Date.now()) / 1000)
              },
              signature: parts[2].substring(0, 10) + '...'
            }
          }
        }
      } catch (e) {
        jwtDebug = { decodeError: e.message }
      }

      return new Response(JSON.stringify({
        error: 'Invalid JWT',
        details: authError?.message || 'User not authenticated',
        debug: {
          authHeaderPresent: !!authHeader,
          authHeaderLength: authHeader?.length,
          supabaseUrl: Deno.env.get('SUPABASE_URL'),
          jwtDebug
        }
      }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Create service role client for database operations
    const dbSupabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    )

    // Get requested tier from body
    const { tier, return_url, cancel_url } = await req.json()

    console.log('Received request:', { tier, return_url, cancel_url })
    console.log('PLAN_IDS:', PLAN_IDS)
    console.log('PLAN_IDS[tier]:', PLAN_IDS[tier])
    console.log('Environment check:', {
      PAYPAL_PLAN_PROFESSIONAL: Deno.env.get('PAYPAL_PLAN_PROFESSIONAL'),
      PAYPAL_PLAN_PREMIUM: Deno.env.get('PAYPAL_PLAN_PREMIUM')
    })

    if (!tier || !PLAN_IDS[tier]) {
      console.log('Invalid tier or missing plan ID')
      return new Response(JSON.stringify({
        error: 'Invalid tier',
        debug: {
          tier,
          availableTiers: Object.keys(PLAN_IDS),
          planId: PLAN_IDS[tier],
          envVars: {
            professional: Deno.env.get('PAYPAL_PLAN_PROFESSIONAL'),
            premium: Deno.env.get('PAYPAL_PLAN_PREMIUM')
          }
        }
      }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Get PayPal access token
    const accessToken = await getPayPalAccessToken()

    // Create subscription
    const subscriptionResponse = await fetch(`${PAYPAL_API_URL}/v1/billing/subscriptions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
      },
      body: JSON.stringify({
        plan_id: PLAN_IDS[tier],
        subscriber: {
          email_address: user.email,
        },
        custom_id: user.id, // Store Supabase user ID for webhook
        application_context: {
          brand_name: 'TSTR Hub',
          locale: 'en-US',
          shipping_preference: 'NO_SHIPPING',
          user_action: 'SUBSCRIBE_NOW',
          return_url: return_url || 'https://tstr.directory/checkout/success',
          cancel_url: cancel_url || 'https://tstr.directory/checkout/cancel'
        }
      })
    })

    const subscription = await subscriptionResponse.json()

    if (!subscriptionResponse.ok) {
      console.error('PayPal error:', subscription)
      return new Response(JSON.stringify({
        error: 'PayPal subscription creation failed',
        details: subscription
      }), {
        status: subscriptionResponse.status,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Find approval URL
    const approvalUrl = subscription.links.find((link: any) => link.rel === 'approve')?.href

    return new Response(JSON.stringify({
      subscription_id: subscription.id,
      approval_url: approvalUrl,
      status: subscription.status
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('Error:', error)
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})