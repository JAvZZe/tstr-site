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