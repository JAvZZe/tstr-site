# Qwen3-Coder CLI Instructions: PayPal Payments Integration

> **Project**: TSTR.directory (`/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working`)
> **Frontend**: `web/tstr-frontend/` (Astro + React + Tailwind, deployed on Cloudflare Pages)
> **Database**: Supabase (https://haimjeaetrsaauitrhfy.supabase.co)
> **Backend**: Supabase Edge Functions (to be created)

---

## CRITICAL CONTEXT

Read `TSTR.md` and `PAYPAL_IMPLEMENTATION_PLAN.md` in the project root before starting.

The user has:
- PayPal Business account with sandbox + live credentials
- Existing `/pricing.astro` page with 4 tiers (Free, Professional $295/mo, Premium $795/mo, Enterprise)
- Existing `/account/subscription.astro` page
- Database fields: `subscription_tier`, `subscription_status` in `user_profiles` table

---

## TASK 1: Database Migration

Create a Supabase migration to add payment tracking fields.

**File**: `web/tstr-frontend/supabase/migrations/20251229_add_payment_fields.sql`

```sql
-- Add payment tracking columns to user_profiles
ALTER TABLE public.user_profiles 
ADD COLUMN IF NOT EXISTS paypal_subscription_id TEXT,
ADD COLUMN IF NOT EXISTS subscription_start_date TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS subscription_end_date TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS last_payment_date TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT NULL;

-- Create payment history table
CREATE TABLE IF NOT EXISTS public.payment_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    status TEXT NOT NULL CHECK (status IN ('completed', 'pending', 'failed', 'refunded')),
    paypal_transaction_id TEXT,
    paypal_subscription_id TEXT,
    tier TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_payment_history_user_id ON public.payment_history(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_history_created_at ON public.payment_history(created_at DESC);

-- RLS policies
ALTER TABLE public.payment_history ENABLE ROW LEVEL SECURITY;

-- Users can only see their own payment history
CREATE POLICY "Users can view own payment history" ON public.payment_history
    FOR SELECT USING (auth.uid() = user_id);

-- Only service role can insert (webhooks)
CREATE POLICY "Service role can insert payments" ON public.payment_history
    FOR INSERT WITH CHECK (true);
```

---

## TASK 2: Supabase Edge Functions

Create 3 Edge Functions for PayPal integration.

### 2.1 Create Subscription Function

**File**: `web/tstr-frontend/supabase/functions/paypal-create-subscription/index.ts`

```typescript
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
    // Get user from Supabase auth
    const authHeader = req.headers.get('Authorization')!
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      { global: { headers: { Authorization: authHeader } } }
    )

    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError || !user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Get requested tier from body
    const { tier, return_url, cancel_url } = await req.json()
    
    if (!tier || !PLAN_IDS[tier]) {
      return new Response(JSON.stringify({ error: 'Invalid tier' }), {
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
      return new Response(JSON.stringify({ error: 'Failed to create subscription' }), {
        status: 500,
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
```

### 2.2 Webhook Handler Function

**File**: `web/tstr-frontend/supabase/functions/paypal-webhook/index.ts`

```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const PAYPAL_WEBHOOK_ID = Deno.env.get('PAYPAL_WEBHOOK_ID')!
const PAYPAL_CLIENT_ID = Deno.env.get('PAYPAL_CLIENT_ID')!
const PAYPAL_CLIENT_SECRET = Deno.env.get('PAYPAL_CLIENT_SECRET')!
const PAYPAL_MODE = Deno.env.get('PAYPAL_MODE') || 'sandbox'
const PAYPAL_API_URL = PAYPAL_MODE === 'live' 
  ? 'https://api-m.paypal.com'
  : 'https://api-m.sandbox.paypal.com'

// Map PayPal plan IDs to tiers (fill after creating plans)
const PLAN_TO_TIER: Record<string, string> = {
  [Deno.env.get('PAYPAL_PLAN_PROFESSIONAL') || '']: 'professional',
  [Deno.env.get('PAYPAL_PLAN_PREMIUM') || '']: 'premium',
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

async function verifyWebhookSignature(req: Request, body: string): Promise<boolean> {
  const accessToken = await getPayPalAccessToken()
  
  const verifyResponse = await fetch(`${PAYPAL_API_URL}/v1/notifications/verify-webhook-signature`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      auth_algo: req.headers.get('paypal-auth-algo'),
      cert_url: req.headers.get('paypal-cert-url'),
      transmission_id: req.headers.get('paypal-transmission-id'),
      transmission_sig: req.headers.get('paypal-transmission-sig'),
      transmission_time: req.headers.get('paypal-transmission-time'),
      webhook_id: PAYPAL_WEBHOOK_ID,
      webhook_event: JSON.parse(body)
    })
  })
  
  const result = await verifyResponse.json()
  return result.verification_status === 'SUCCESS'
}

serve(async (req) => {
  try {
    const body = await req.text()
    
    // Verify webhook signature in production
    if (PAYPAL_MODE === 'live') {
      const isValid = await verifyWebhookSignature(req, body)
      if (!isValid) {
        console.error('Invalid webhook signature')
        return new Response('Invalid signature', { status: 401 })
      }
    }

    const event = JSON.parse(body)
    console.log('Webhook event:', event.event_type)

    // Use service role for database updates
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    )

    const resource = event.resource
    const userId = resource.custom_id // We stored Supabase user ID here
    const subscriptionId = resource.id || resource.billing_agreement_id

    switch (event.event_type) {
      case 'BILLING.SUBSCRIPTION.ACTIVATED': {
        // Subscription activated - upgrade user
        const planId = resource.plan_id
        const tier = PLAN_TO_TIER[planId] || 'professional'
        
        await supabase.from('user_profiles').update({
          subscription_tier: tier,
          subscription_status: 'active',
          paypal_subscription_id: subscriptionId,
          subscription_start_date: new Date().toISOString(),
          payment_method: 'paypal'
        }).eq('id', userId)

        console.log(`User ${userId} upgraded to ${tier}`)
        break
      }

      case 'PAYMENT.SALE.COMPLETED': {
        // Payment received - log it
        const amount = resource.amount?.total || resource.amount?.value
        
        await supabase.from('payment_history').insert({
          user_id: userId,
          amount: parseFloat(amount),
          currency: resource.amount?.currency || 'USD',
          status: 'completed',
          paypal_transaction_id: resource.id,
          paypal_subscription_id: subscriptionId,
          tier: PLAN_TO_TIER[resource.billing_agreement_id] || 'unknown',
          description: 'Monthly subscription payment'
        })

        // Update last payment date
        await supabase.from('user_profiles').update({
          last_payment_date: new Date().toISOString()
        }).eq('id', userId)

        console.log(`Payment recorded for user ${userId}: $${amount}`)
        break
      }

      case 'BILLING.SUBSCRIPTION.CANCELLED':
      case 'BILLING.SUBSCRIPTION.EXPIRED': {
        // Subscription ended - set end date (keep tier until end of period)
        await supabase.from('user_profiles').update({
          subscription_status: 'cancelled',
          subscription_end_date: new Date().toISOString()
        }).eq('paypal_subscription_id', subscriptionId)

        console.log(`Subscription ${subscriptionId} cancelled/expired`)
        break
      }

      case 'BILLING.SUBSCRIPTION.SUSPENDED': {
        // Payment failed - mark as past_due, begin 7-day grace period
        await supabase.from('user_profiles').update({
          subscription_status: 'past_due'
        }).eq('paypal_subscription_id', subscriptionId)

        console.log(`Subscription ${subscriptionId} suspended - past due`)
        break
      }

      case 'BILLING.SUBSCRIPTION.PAYMENT.FAILED': {
        // Log failed payment
        await supabase.from('payment_history').insert({
          user_id: userId,
          amount: 0,
          status: 'failed',
          paypal_subscription_id: subscriptionId,
          tier: 'unknown',
          description: 'Payment failed'
        })
        break
      }

      default:
        console.log(`Unhandled event: ${event.event_type}`)
    }

    return new Response('OK', { status: 200 })

  } catch (error) {
    console.error('Webhook error:', error)
    return new Response('Error', { status: 500 })
  }
})
```

### 2.3 Cancel Subscription Function

**File**: `web/tstr-frontend/supabase/functions/paypal-cancel-subscription/index.ts`

```typescript
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
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Verify user
    const authHeader = req.headers.get('Authorization')!
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      { global: { headers: { Authorization: authHeader } } }
    )

    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError || !user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Get user's subscription ID
    const { data: profile } = await supabase
      .from('user_profiles')
      .select('paypal_subscription_id')
      .eq('id', user.id)
      .single()

    if (!profile?.paypal_subscription_id) {
      return new Response(JSON.stringify({ error: 'No active subscription' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

    // Cancel subscription in PayPal
    const accessToken = await getPayPalAccessToken()
    const { reason } = await req.json()

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

    if (cancelResponse.status === 204) {
      // Update local status
      await supabase.from('user_profiles').update({
        subscription_status: 'cancelled'
      }).eq('id', user.id)

      return new Response(JSON.stringify({ success: true }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    } else {
      const error = await cancelResponse.json()
      console.error('PayPal cancel error:', error)
      return new Response(JSON.stringify({ error: 'Failed to cancel subscription' }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      })
    }

  } catch (error) {
    console.error('Error:', error)
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    })
  }
})
```

---

## TASK 3: Frontend - Checkout Success Page

**File**: `web/tstr-frontend/src/pages/checkout/success.astro`

```astro
---
export const prerender = false
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Payment Successful - TSTR Hub</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card {
      background: white;
      border-radius: 16px;
      padding: 3rem;
      max-width: 500px;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }
    .icon { font-size: 4rem; margin-bottom: 1.5rem; }
    h1 { color: #333; margin-bottom: 1rem; font-size: 2rem; }
    p { color: #666; margin-bottom: 2rem; line-height: 1.6; }
    .btn {
      display: inline-block;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 1rem 2rem;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">✅</div>
    <h1>Welcome to TSTR Hub!</h1>
    <p>Your subscription is now active. You have full access to all your plan features. Check your email for a confirmation receipt.</p>
    <a href="/account" class="btn">Go to My Account</a>
  </div>
</body>
</html>
```

---

## TASK 4: Frontend - Checkout Cancel Page

**File**: `web/tstr-frontend/src/pages/checkout/cancel.astro`

```astro
---
export const prerender = false
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Checkout Cancelled - TSTR Hub</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f5f5f5;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card {
      background: white;
      border-radius: 16px;
      padding: 3rem;
      max-width: 500px;
      text-align: center;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .icon { font-size: 4rem; margin-bottom: 1.5rem; }
    h1 { color: #333; margin-bottom: 1rem; font-size: 1.8rem; }
    p { color: #666; margin-bottom: 2rem; line-height: 1.6; }
    .buttons { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }
    .btn {
      display: inline-block;
      padding: 1rem 2rem;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 600;
      transition: transform 0.2s;
    }
    .btn-primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    .btn-secondary {
      background: white;
      color: #667eea;
      border: 2px solid #667eea;
    }
    .btn:hover { transform: translateY(-2px); }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">↩️</div>
    <h1>Checkout Cancelled</h1>
    <p>No worries! Your payment was not processed. You can try again whenever you're ready, or contact us if you have questions.</p>
    <div class="buttons">
      <a href="/pricing" class="btn btn-primary">View Plans</a>
      <a href="/" class="btn btn-secondary">Go Home</a>
    </div>
  </div>
</body>
</html>
```

---

## TASK 5: Update Pricing Page

**File**: `web/tstr-frontend/src/pages/pricing.astro`

Find and replace the Professional and Premium tier buttons. Keep Free and Enterprise unchanged.

**FIND (Professional tier around line 412):**
```html
<a href={MAILTO_LINKS.professionalPlan} class="cta-button">Contact Sales</a>
```

**REPLACE WITH:**
```html
<button id="btn-professional" class="cta-button" data-tier="professional">Subscribe Now - $295/mo</button>
```

**FIND (Premium tier around line 434):**
```html
<a href={MAILTO_LINKS.premiumPlan} class="cta-button">Contact Sales</a>
```

**REPLACE WITH:**
```html
<button id="btn-premium" class="cta-button" data-tier="premium">Subscribe Now - $795/mo</button>
```

**ADD this script before closing `</body>` tag:**

```html
<script>
  import { supabaseBrowser } from '../lib/supabase-browser'

  async function handleSubscribe(tier) {
    const button = document.querySelector(`[data-tier="${tier}"]`)
    const originalText = button.textContent
    button.textContent = 'Processing...'
    button.disabled = true

    try {
      // Check if user is logged in
      const { data: { session } } = await supabaseBrowser.auth.getSession()
      
      if (!session) {
        // Redirect to login with return URL
        window.location.href = `/login?redirect=/pricing&tier=${tier}`
        return
      }

      // Call Edge Function to create subscription
      const { data, error } = await supabaseBrowser.functions.invoke('paypal-create-subscription', {
        body: { 
          tier,
          return_url: window.location.origin + '/checkout/success',
          cancel_url: window.location.origin + '/checkout/cancel'
        }
      })

      if (error) throw error

      // Redirect to PayPal
      if (data.approval_url) {
        window.location.href = data.approval_url
      } else {
        throw new Error('No approval URL returned')
      }

    } catch (error) {
      console.error('Subscription error:', error)
      alert('Failed to start checkout. Please try again or contact support.')
      button.textContent = originalText
      button.disabled = false
    }
  }

  // Attach click handlers
  document.getElementById('btn-professional')?.addEventListener('click', () => handleSubscribe('professional'))
  document.getElementById('btn-premium')?.addEventListener('click', () => handleSubscribe('premium'))
</script>
```

---

## TASK 6: Environment Variables

**Add to `.env` and Cloudflare Pages dashboard and Supabase Edge Function secrets:**

```env
# PayPal Configuration
PAYPAL_CLIENT_ID=your_client_id_here
PAYPAL_CLIENT_SECRET=your_client_secret_here
PAYPAL_MODE=sandbox
PAYPAL_WEBHOOK_ID=your_webhook_id_here

# PayPal Plan IDs (create these in PayPal Dashboard first)
PAYPAL_PLAN_PROFESSIONAL=P-XXXXXXXXXXXXXXXXXXXXX
PAYPAL_PLAN_PREMIUM=P-XXXXXXXXXXXXXXXXXXXXX
```

**For Supabase Edge Functions, set secrets via CLI:**
```bash
supabase secrets set PAYPAL_CLIENT_ID=xxx
supabase secrets set PAYPAL_CLIENT_SECRET=xxx
supabase secrets set PAYPAL_MODE=sandbox
supabase secrets set PAYPAL_WEBHOOK_ID=xxx
supabase secrets set PAYPAL_PLAN_PROFESSIONAL=P-xxx
supabase secrets set PAYPAL_PLAN_PREMIUM=P-xxx
```

---

## TASK 7: Deploy Edge Functions

```bash
cd web/tstr-frontend
supabase functions deploy paypal-create-subscription
supabase functions deploy paypal-webhook
supabase functions deploy paypal-cancel-subscription
```

---

## PayPal Dashboard Setup (Manual Steps)

1. Go to https://developer.paypal.com/dashboard/applications
2. Create a new app (or use existing)
3. Copy Client ID and Secret to `.env`
4. Go to "Subscriptions" → "Create Plan"
5. Create **Professional Plan**: $295/month, billing cycle monthly
6. Create **Premium Plan**: $795/month, billing cycle monthly
7. Copy Plan IDs to `.env`
8. Go to "Webhooks" → Add webhook
9. URL: `https://haimjeaetrsaauitrhfy.supabase.co/functions/v1/paypal-webhook`
10. Subscribe to events:
    - BILLING.SUBSCRIPTION.ACTIVATED
    - BILLING.SUBSCRIPTION.CANCELLED
    - BILLING.SUBSCRIPTION.EXPIRED
    - BILLING.SUBSCRIPTION.SUSPENDED
    - PAYMENT.SALE.COMPLETED
    - BILLING.SUBSCRIPTION.PAYMENT.FAILED
11. Copy Webhook ID to `.env`

---

## Testing Checklist

- [ ] Run migration: `supabase db push`
- [ ] Deploy functions (see Task 7)
- [ ] Set PAYPAL_MODE=sandbox
- [ ] Click "Subscribe Now" on pricing page
- [ ] Log in if prompted
- [ ] Complete PayPal sandbox checkout
- [ ] Verify redirect to /checkout/success
- [ ] Check Supabase: user's subscription_tier updated
- [ ] Check payment_history table for new record

---

## Notes for Qwen3-Coder

1. **Read existing files first** before modifying - especially `pricing.astro` and `subscription.astro`
2. **Keep Enterprise tier unchanged** - it should still use mailto link
3. **Preserve all existing styles** - only add/modify the subscription buttons
4. **Test locally** with `npm run dev` before committing
5. User will provide PayPal credentials separately - use placeholder values
