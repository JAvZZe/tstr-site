# PayPal Payments Integration Plan

> **Created**: 2025-12-29
> **Status**: Ready for implementation
> **Assigned To**: Qwen3-Coder CLI

## Decisions Made

| Decision | Choice |
|----------|--------|
| PayPal Account | ✅ Business account available (sandbox + live) |
| Backend | Supabase Edge Functions (free tier, keeps backend unified) |
| Billing | Monthly only (MVP) |
| Grace Period | 7 days (industry standard) |
| Enterprise | Keep as "Contact Sales" |

## Architecture Overview

```
User clicks "Subscribe" on /pricing
        ↓
Frontend calls Supabase Edge Function
        ↓
Edge Function creates PayPal subscription → Returns approval URL
        ↓
User redirects to PayPal, completes payment
        ↓
PayPal sends webhook to Edge Function
        ↓
Edge Function updates user_profiles.subscription_tier in Supabase
        ↓
User redirects to /checkout/success
```

## Implementation Checklist

### Phase 1: Database
- [ ] Add columns to `user_profiles`: `paypal_subscription_id`, `subscription_start_date`, `subscription_end_date`, `last_payment_date`
- [ ] Create `payment_history` table

### Phase 2: Supabase Edge Functions
- [ ] `paypal-create-subscription` - Creates subscription, returns PayPal approval URL
- [ ] `paypal-webhook` - Handles IPN notifications, updates subscription status
- [ ] `paypal-cancel-subscription` - Cancels active subscription

### Phase 3: PayPal Dashboard Setup
- [ ] Create subscription plans: Professional ($295/mo), Premium ($795/mo)
- [ ] Configure webhook URL pointing to Edge Function
- [ ] Note Plan IDs

### Phase 4: Frontend
- [ ] Update `/pricing.astro` - Add "Subscribe Now" buttons for Professional/Premium
- [ ] Update `/account/subscription.astro` - Add upgrade/cancel UI
- [ ] Create `/checkout/success.astro`
- [ ] Create `/checkout/cancel.astro`

### Phase 5: Testing
- [ ] Test in sandbox mode
- [ ] Verify webhook delivery
- [ ] Test subscription lifecycle (create, renew, cancel)

## PayPal Plan IDs (TO BE FILLED)

```env
# Add to .env after creating plans in PayPal Dashboard
PAYPAL_PLAN_PROFESSIONAL=P-XXXXXXXXXX
PAYPAL_PLAN_PREMIUM=P-XXXXXXXXXX
```

## Files to Create/Modify

| File | Action |
|------|--------|
| `supabase/functions/paypal-create-subscription/index.ts` | NEW |
| `supabase/functions/paypal-webhook/index.ts` | NEW |
| `supabase/functions/paypal-cancel-subscription/index.ts` | NEW |
| `supabase/migrations/YYYYMMDD_add_payment_fields.sql` | NEW |
| `src/pages/pricing.astro` | MODIFY |
| `src/pages/account/subscription.astro` | MODIFY |
| `src/pages/checkout/success.astro` | NEW |
| `src/pages/checkout/cancel.astro` | NEW |
| `.env` | MODIFY (add PayPal credentials) |
