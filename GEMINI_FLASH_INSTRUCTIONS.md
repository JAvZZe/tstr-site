# GEMINI FLASH INSTRUCTIONS: Fix PayPal Subscription Logic

**Objective**: Fix the "Failed to start checkout" error on the subscription page by aligning the PayPal logic with the working implementation from the Pricing page.

**Target File**: `web/tstr-frontend/src/pages/account/subscription.astro`

## Context
The current implementation of `handlePayPalSubscribe` in `subscription.astro` incorrectly uses the user's session token for the Edge Function call and fails to pass the required `userId` in the body. The working implementation in `pricing.astro` uses the anonymous JWT and explicitly passes the user ID.

## Task 1: Update PayPal Logic
Locate the `handlePayPalSubscribe` function (around line 708) and replace it with the robust version below. This version:
1.  Imports `supabaseAnonJwt` (already present).
2.  Uses `supabaseAnonJwt` for the `Authorization` header.
3.  Includes `userId` in the request body.
4.  Adds proper error handling and logging.

```javascript
    window.handlePayPalSubscribe = async function(tier, button) {
      const originalText = button.textContent;
      button.textContent = 'Processing...';
      button.disabled = true;

      try {
        const { data: { session } } = await supabaseBrowser.auth.getSession();
        if (!session) throw new Error('No active session. Please log in again.');

        console.log('[PayPal] Starting checkout for tier:', tier);

        // Call Edge Function
        // Uses supabaseAnonJwt to avoid RLS issues, passing userId explicitly in body
        const { data, error } = await fetch('https://haimjeaetrsaauitrhfy.supabase.co/functions/v1/paypal-create-subscription', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${supabaseAnonJwt}` 
          },
          body: JSON.stringify({
            tier,
            userId: session.user.id,
            return_url: window.location.origin + '/checkout/success',
            cancel_url: window.location.origin + '/checkout/cancel'
          })
        }).then(res => res.json().then(data => ({ data, error: !res.ok ? data : null })));

        if (error) {
          console.error('[PayPal] Edge Function Error:', error);
          throw new Error(error.error || error.message || 'Failed to create subscription');
        }

        console.log('[PayPal] Subscription created:', data);

        // Redirect to PayPal
        if (data.approval_url) {
          window.location.href = data.approval_url;
        } else {
          throw new Error('No approval URL returned from server');
        }

      } catch (error) {
        console.error('[PayPal] Subscription error:', error);
        alert(`Failed to start checkout. ${error.message}`);
        button.textContent = originalText;
        button.disabled = false;
      }
    }
```

## Task 2: Execution Steps

1.  **Pull Latest**: `git pull origin main --rebase`.
2.  **Apply Logic Fix**: specific replace of `window.handlePayPalSubscribe`.
3.  **Verify**: Ensure the file compiles.
4.  **Push**: `git commit -m "FIX: Align PayPal subscription logic with pricing page implementation" && git push origin main`.
