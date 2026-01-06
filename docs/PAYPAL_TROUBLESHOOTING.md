# PayPal Integration Troubleshooting Log

This document tracks the systematic efforts to resolve issues with the PayPal subscription flow on TSTR.directory.

## 📋 Summary of Efforts

| Step | Issue | Root Cause Identified | Fix Implemented | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Redirect Loop | `redirect` vs `redirect_to` mismatch | Unified parameter names | ✅ FIXED |
| 2 | Tier Parameter Loss | URL params stripped during OAuth | `sessionStorage` persistence | ✅ FIXED |
| 3 | Auth Flow Stop | `history.replaceState` stripped hash | Hash preservation (incorrect assumption) | ❌ REPLACED |
| 4 | Auth Flow Stop | `history.replaceState` stripped `?code=` | Surgical query param preservation | ✅ FIXED |
| 5 | Checkout Failure | Edge Function returns Non-2xx | TBD (Credential Check/Plan ID) | 🚧 ACTIVE |

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

### 3. The Edge Function Roadblock (Current)
- **Symptom**: Error: `Failed to start checkout: Edge Function returned a non-2xx status code.`
- **Current Hypothesis**: 
    1. **401 Unauthorized**: The user session established on the frontend is not being recognized by the Edge Function (JWT validation failure).
    2. **400 Bad Request**: The PayPal Plan ID in environment variables is missing or invalid.
- **Action Taken**: Updated Edge Function to return detailed PayPal error bodies and updated frontend to display them. However, Supabase's `invoke` wrapper is currently catching the error and returning a generic `FunctionsHttpError` message.

---

## 🛠️ Verification Checklist

- [x] Click "Subscribe" -> Redirects to Login
- [x] Login via LinkedIn -> Redirects back to Pricing
- [x] URL shows `?code=...` briefly then cleans up `tier` but keeps `code`
- [x] Console shows `[Auth] Session established, triggering subscription`
- [ ] Edge Function returns `approval_url`
- [ ] Redirect to PayPal Sandbox

## 📖 Lessons Learned
- **Never Assume Root Cause**: The assumption about hash fragments vs query parameters cost two iterations. Browser-based evidence collection is the only definitive way to debug OAuth.
- **URL Manipulations**: Using `history.replaceState` with `window.location.pathname` is destructive to query strings. Always use `new URL()` for surgical updates.
