# 🚀 PayPal Go-Live Sequence for TSTR.directory

> **Warning**: accurate execution of this sequence is critical for processing real payments.

## 1. Prerequisites (User Action Required)
Before the AI agent can execute the switch, YOU (the User) must provide the following from the **PayPal Developer Dashboard (Live Mode)**:

1.  **Client ID** (Live) : AfuakLhKAegLft9ZWgjQQL4vy-2t8wl-Y03UCJqnsnlSNmeKaGqgXXM4ouFMM3ntn26JiZY-J7pPSZW5
2.  **Client Secret** (Live) :  EP3GD2DzpsrPJBle7DjoTmlOkuwHg8fqfoePt2ZDCEMtBvGhQcHdxcEBh8iMtNZXwLIOx_ywaB-qgkUh
3.  **Webhook ID** (Live)
    *   Create a NEW Webhook in Live mode.
    *   URL: `https://haimjeaetrsaauitrhfy.supabase.co/functions/v1/paypal-webhook` : Done, active
    *   Events: `BILLING.SUBSCRIPTION.*`, `PAYMENT.SALE.*`
4.  **Professional Plan ID** (Live) : P-08U50096BE7109405NFVAIIA
5.  **Premium Plan ID** (Live) : P-6GA992471E0438453NFVAIMQ

## 2. Configuration & Secrets (Agent Task)
Once credentials are ready, the agent will:

1.  **Update Supabase Secrets** (Production)
    *   Run `supabase secrets set` commands to update:
        *   `PAYPAL_CLIENT_ID`
        *   `PAYPAL_CLIENT_SECRET`
        *   `PAYPAL_MODE` -> `live`
        *   `PAYPAL_WEBHOOK_ID`
        *   `PAYPAL_PLAN_PROFESSIONAL`
        *   `PAYPAL_PLAN_PREMIUM`

2.  **Update Frontend Environment**
    *   Update `web/tstr-frontend/.env` (and `.env.production` if exists)
    *   Required to ensure the frontend initiates the flow with the correct Plan IDs (though the backend is the source of truth, often the frontend needs the Client ID for the SDK).
    *   *Note*: The TSTR implementation uses the Backend to generate the subscription, so `PAYPAL_CLIENT_ID` in frontend might only be used for "Pay with Card" fields if implemented. Check if checking `PAYPAL_MODE` in frontend code affects anything.

3.  **Redeploy Edge Functions**
    *   `npx supabase functions deploy paypal-create-subscription`
    *   `npx supabase functions deploy paypal-webhook`
    *   `npx supabase functions deploy paypal-cancel-subscription`

## 3. Deployment (CD)
1.  **Commit Config Changes**
    *   Commit updated `.env.example` (do not commit secrets).
    *   Push to `main`.
2.  **Cloudflare Build**
    *   Trigger a new build on Cloudflare Pages to pick up any `PUBLIC_` env var changes (specifically `PAYPAL_MODE` if it's public).
    *   *Critical*: Ensure Cloudflare Pages Environment Variables are updated in the Cloudflare Dashboard if they are defined there.

## 4. Verification
1.  **Live Test**: Perform a real transaction (can be $1 or request refund after).
2.  **Webhook Verify**: Check Supabase Function logs for 200 OK on webhook delivery.
