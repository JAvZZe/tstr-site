# PayPal Integration Troubleshooting Log

This document tracks the systematic efforts to resolve issues with the PayPal subscription flow on TSTR.directory.

## 📋 Summary of Efforts

| Step | Issue | Root Cause Identified | Fix Implemented | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Redirect Loop | `redirect` vs `redirect_to` mismatch | Unified parameter names | ✅ FIXED |
| 2 | Tier Parameter Loss | URL params stripped during OAuth | `sessionStorage` persistence | ✅ FIXED |
| 3 | Auth Flow Stop | `history.replaceState` stripped hash | Hash preservation (incorrect assumption) | ❌ REPLACED |
| 4 | Auth Flow Stop | `history.replaceState` stripped `?code=` | Surgical query param preservation | ✅ FIXED |
| 4 | Invalid JWT Error | Frontend used Publishable Key instead of JWT | Switched to Anon JWT via CLI | ✅ FIXED |
| 5 | Database Error | `.single()` crash + `email` vs `billing_email` mismatch | `.maybeSingle()` + column name update | ✅ FIXED |

---

## 🔍 Detailed Incident History

### 1. The "Vanishing Parameter" Issue
- **Symptom**: After LinkedIn login, the user lands on `/pricing` but nothing happens.
- **Investigation**: Supabase's OAuth redirect strips arbitrary custom parameters from the `redirectTo` URL.
- **Resolution**: Implemented `sessionStorage` to store the `pendingSubscriptionTier` before the login redirect. The pricing page now checks this storage upon return.

### 2. The PKCE Code Stripping (The "Real" Redirect Loop)
- **Symptom**: Even with `sessionStorage`, the flow didn't auto-trigger. 
- **Investigation** (via Browser Agent): The `history.replaceState(null, '', window.location.pathname)` call was stripping the `?code=...` parameter used by Supabase PKCE flow before the client could exchange it for a session.
- **Resolution**: Updated the cleanup logic to use the `URL` API, removing only the `tier` parameter and preserving the `code`.

### 3. The Edge Function Remote Gate
- **Symptom**: Error: `Failed to start checkout: Edge Function returned a non-2xx status code.`
- **Investigation**: Previous attempts failed due to JWT validation at the Supabase Gateway level.
- **Resolution**: Implemented direct `fetch` with explicit headers (bypass `supabase-js` automatic injection) and specific Anon JWT.

### 4. The "Invalid JWT" Roadblock
- **Symptom**: Error: `Failed to start checkout: Invalid JWT`.
- **Investigation**: The Supabase Gateway requires a valid **JWT** signature in the `Authorization: Bearer` header. The frontend was incorrectly passing a **Publishable Key** (`sb_publishable_...`), which the Gateway rejected before the Edge Function could even execute.
- **Resolution**: Used Supabase CLI (`supabase projects api-keys`) to retrieve the project's actual **Anon JWT**. Updated `supabase-browser.ts` to export this JWT and used it explicitly for Edge Function calls.

### 5. The "Database Error" Chain
- **Symptom**: Error: `Failed to start checkout: Database error: column user_profiles.email does not exist`.
- **Investigation**: 
    1. **Query Crash**: The code used `.single()` for user profile lookup. If the user didn't exist (first-time subscriber), Supabase threw a 406/500 error instead of returning null, crashing the function before it could reach the "Create Profile" logic.
    2. **Schema Mismatch**: The actual database schema uses `billing_email`.
- **Resolution**: 
    1. Changed `.single()` to `.maybeSingle()` to handle missing profiles gracefully.
    2. Updated all references from `email` to `billing_email` in the Edge Function code.

---

## 🏗️ PayPal Sandbox Behavior Notes

During verification, the following behaviors were observed in the PayPal Sandbox environment:
- **"Pay with Card" Option**: Clicking the "Pay with Card" button may cause the inline form to disappear, leaving only the email field for "Check Out as a guest."
- **Guest Checkout Flow**: Entering an email address and continuing successfully leads to the PayPal sandbox page: "Pay with debit or credit card."
- **Tier Activation**: The approval URL generation is now 100% reliable across both Professional and Premium tiers.

---

## 🛠️ Verification Checklist

- [x] Click "Subscribe" -> Redirects to Login
- [x] Login via LinkedIn -> Redirects back to Pricing (or caught by Safety Net)
- [x] Console shows `[Auth] Session established, triggering subscription`
- [x] Edge Function returns `approval_url` (200 OK)
- [x] Redirect to PayPal Sandbox ✅ VERIFIED

## 📖 Lessons Learned
- **Never Assume Root Cause**: The assumption about hash fragments vs query parameters cost two iterations. Browser-based evidence collection is the only definitive way to debug OAuth.
- **URL Manipulations**: Using `history.replaceState` with `window.location.pathname` is destructive to query strings. Always use `new URL()` for surgical updates.
