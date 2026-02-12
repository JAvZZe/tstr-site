import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { Database } from '../types.ts'

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
  console.log('🚀🚀🚀 PAYPAL EDGE FUNCTION CALLED - VERSION 33 - FINAL DEBUG 🚀🚀🚀')
  console.log('Timestamp:', new Date().toISOString())
  console.log('Request method:', req.method)
  console.log('Request URL:', req.url)
  console.log('Request headers keys:', Array.from(req.headers.keys()))
  console.log('Authorization header present:', req.headers.has('Authorization'))
  console.log('Content-Type header:', req.headers.get('Content-Type'))

  // Immediate test response to verify function is being called
  if (req.method === 'GET') {
    console.log('GET request received - returning test response')
    return new Response(JSON.stringify({
      status: 'ok',
      message: 'Edge Function is responding',
      version: '33',
      timestamp: new Date().toISOString()
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }

  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    console.log('Handling CORS preflight')
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    console.log('=== ENTERING TRY BLOCK ===')
    console.log('=== PARSING REQUEST BODY ===')
    let requestBody
    try {
      console.log('About to parse JSON...')
      requestBody = await req.json()
      console.log('✅ Successfully parsed request body:', requestBody)
    } catch (parseError) {
      console.error('❌ Failed to parse request body as JSON:', parseError)
      console.error('Raw request body attempt...')
      try {
        const rawBody = await req.text()
        console.error('Raw body:', rawBody)
      } catch (textError) {
        console.error('Could not read raw body either:', textError)
      }
      return new Response(JSON.stringify({
        error: 'Invalid JSON in request body',
        details: parseError.message
      }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    const { tier, userId, return_url, cancel_url, pendingToken } = requestBody

    console.log('=== EXTRACTED PARAMETERS ===')
    console.log('tier:', tier, 'type:', typeof tier)
    console.log('userId:', userId, 'type:', typeof userId)
    console.log('return_url:', return_url)
    console.log('cancel_url:', cancel_url)
    console.log('pendingToken:', pendingToken, 'type:', typeof pendingToken)
    console.log('Request headers:', Object.fromEntries(req.headers.entries()))

    if (!userId) {
      console.log('ERROR: Missing userId in request')
      return new Response(JSON.stringify({
        error: 'Missing user ID',
        details: 'User ID must be provided in request body'
      }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    console.log('=== DATABASE VALIDATION ===')
    console.log('SUPABASE_URL:', Deno.env.get('SUPABASE_URL'))
    console.log('SUPABASE_SERVICE_ROLE_KEY present:', !!Deno.env.get('SUPABASE_SERVICE_ROLE_KEY'))

    // Create service role client for database operations and user validation
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    ) as unknown as ReturnType<typeof createClient<Database>>

    console.log('Created Supabase client, validating user...')

    // Validate user exists and get their details
    let { data: user, error: userError } = await supabase
      .from('user_profiles')
      .select('id, billing_email')
      .eq('id', userId)
      .maybeSingle()

    console.log('User lookup result:', { user: !!user, error: userError })

    if (userError) {
      console.error('User lookup error details:', userError)
      return new Response(JSON.stringify({
        error: `Database error: ${userError.message || JSON.stringify(userError)}`,
        details: userError,
        code: userError.code
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    if (!user) {
      console.error('User not found in user_profiles for ID:', userId)
      console.log('Checking if user exists in auth.users...')

      // Check if user exists in auth.users
      const { data: authUser, error: authError } = await supabase.auth.admin.getUserById(userId)

      if (authError || !authUser) {
        console.error('User not found in auth.users either:', authError)
        return new Response(JSON.stringify({
          error: 'User not found',
          details: `User ${userId} does not exist in the system`
        }), {
          status: 404,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
      }

      console.log('User exists in auth but not user_profiles, creating profile...')
      // User exists in auth but not in user_profiles, create the profile
      const { data: newProfile, error: createError } = await supabase
        .from('user_profiles')
        .insert({
          id: userId,
          billing_email: authUser.user.email
        })
        .select('id, billing_email')
        .single()

      if (createError) {
        console.error('Failed to create user profile:', createError)
        return new Response(JSON.stringify({
          error: 'Failed to create user profile',
          details: createError.message
        }), {
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
      }

      console.log('✅ Created and validated user profile:', { id: newProfile.id, email: newProfile.billing_email })
      // Use the newly created profile
      user = newProfile
    } else {
      console.log('✅ User validated successfully:', { id: user.id, email: user.billing_email })
    }

    // Handle pending subscription recovery
    let finalTier = tier
    if (pendingToken) {
      console.log('=== PENDING TOKEN VALIDATION ===')
      const { data: profile, error: pendingError } = await supabase
        .from('user_profiles')
        .select('pending_subscription_data, pending_subscription_expires_at')
        .eq('id', userId)
        .eq('pending_subscription_token', pendingToken)
        .gt('pending_subscription_expires_at', new Date().toISOString())
        .single()

      if (pendingError || !profile) {
        console.error('Invalid or expired pending token:', pendingError)
        return new Response(JSON.stringify({
          error: 'Invalid or expired pending token',
          details: 'The subscription recovery link has expired or is invalid'
        }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        })
      }

      console.log('✅ Valid pending token found, using stored data')
      finalTier = profile.pending_subscription_data.tier
      console.log('Using tier from pending data:', finalTier)
    }

    console.log('PLAN_IDS:', PLAN_IDS)
    console.log('PLAN_IDS[tier]:', PLAN_IDS[tier])
    console.log('Environment check:', {
      PAYPAL_PLAN_PROFESSIONAL: Deno.env.get('PAYPAL_PLAN_PROFESSIONAL'),
      PAYPAL_PLAN_PREMIUM: Deno.env.get('PAYPAL_PLAN_PREMIUM')
    })

    if (!finalTier || !PLAN_IDS[finalTier]) {
      console.log('Invalid tier or missing plan ID')
      return new Response(JSON.stringify({
        error: 'Invalid tier',
        debug: {
          requestedTier: tier,
          finalTier,
          availableTiers: Object.keys(PLAN_IDS),
          planId: PLAN_IDS[finalTier],
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
        plan_id: PLAN_IDS[finalTier],
        subscriber: {
          email_address: user.billing_email,
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
    const approvalUrl = subscription.links.find((link: { rel: string; href: string }) => link.rel === 'approve')?.href

    // Clear pending subscription state on successful creation
    if (pendingToken) {
      console.log('Clearing pending subscription state...')
      const { error: clearError } = await supabase
        .from('user_profiles')
        .update({
          pending_subscription_data: null,
          pending_subscription_token: null,
          pending_subscription_expires_at: null
        })
        .eq('id', userId)

      if (clearError) {
        console.error('Failed to clear pending subscription state:', clearError)
        // Don't fail the subscription creation for this
      } else {
        console.log('✅ Cleared pending subscription state')
      }
    }

    console.log('✅ SUCCESS: Returning approval URL')
    return new Response(JSON.stringify({
      subscription_id: subscription.id,
      approval_url: approvalUrl,
      status: subscription.status,
      version: '30-pending-state'
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('💥💥💥 UNHANDLED ERROR IN EDGE FUNCTION 💥💥💥')
    console.error('Error type:', typeof error)
    console.error('Error message:', error?.message)
    console.error('Error stack:', error?.stack)
    console.error('Error object:', error)
    return new Response(JSON.stringify({
      error: 'Internal server error',
      details: error?.message || 'Unknown error',
      timestamp: new Date().toISOString()
    }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})