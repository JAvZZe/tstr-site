# Task: Fix PayPal Cancellation Flow

- [x] Refactor `paypal-cancel-subscription` Edge Function <!-- id: 1 -->
    - [x] Remove header-based `getUser()` validation <!-- id: 2 -->
    - [x] Implement `userId` extraction from request body <!-- id: 3 -->
    - [x] Use `SUPABASE_SERVICE_ROLE_KEY` for database access <!-- id: 4 -->
    - [x] Verify user existence and subscription ID via database lookup <!-- id: 5 -->
- [x] Update Frontend `subscription.astro` <!-- id: 6 -->
    - [x] Import `supabaseAnonJwt` <!-- id: 7 -->
    - [x] update `handleCancelSubscription` to send `userId` in body <!-- id: 8 -->
    - [x] Use `Authorization: Bearer ${supabaseAnonJwt}` for Edge Function call <!-- id: 9 -->
- [x] Verify Changes <!-- id: 10 -->
    - [x] Review code for pattern matching with `paypal-create-subscription` <!-- id: 11 -->
    - [x] Manual verification via Browser Subagent (optional/if needed) <!-- id: 12 -->for User Testing) <!-- id: 105 -->
