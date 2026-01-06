# PAYPAL_SUBSCRIPTION_FIX_INSTRUCTIONS.md

**For**: Gemini Flash / Opencode Grok Fast 1
**Priority**: HIGH
**Created**: 2026-01-06 by Claude Opus
**Issue**: PayPal subscription flow breaks after LinkedIn OAuth login

---

## Problem
Users clicking "Subscribe" on `/pricing` are redirected to login. After LinkedIn OAuth, they land on `/account` instead of returning to complete the subscription.

## Root Cause
1. `pricing.astro` uses query param `redirect` but `login.astro` expects `redirect_to`.
2. The `tier` parameter (e.g., `professional`) is not preserved through OAuth.

---

## Fix Required (2 edits in `pricing.astro`)

### Edit 1: Fix redirect URL (Line ~604)

**Find** (in `handleSubscribe` function):
```javascript
window.location.href = `/login?redirect=/pricing&tier=${tier}`
```

**Replace with**:
```javascript
window.location.href = `/login?redirect_to=${encodeURIComponent('/pricing?tier=' + tier)}`
```

### Edit 2: Add auto-trigger on page load (After line ~663)

**Add this code** inside the `<script>` tag, after the button click handlers:

```javascript
// Auto-trigger subscription if returning from login with tier param
document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const tierFromUrl = urlParams.get('tier');
  if (tierFromUrl && (tierFromUrl === 'professional' || tierFromUrl === 'premium')) {
    // Clean URL to prevent re-trigger on refresh
    history.replaceState(null, '', window.location.pathname);
    // Small delay to ensure Supabase client is ready
    await new Promise(r => setTimeout(r, 500));
    handleSubscribe(tierFromUrl);
  }
});
```

---

## Test Plan

1. Run `npm run dev` from `web/tstr-frontend/`
2. Open `http://localhost:4321/pricing`
3. Click "Subscribe Now - $295/mo"
4. Should redirect to `/login?redirect_to=%2Fpricing%3Ftier%3Dprofessional`
5. Complete login (email/password or LinkedIn)
6. Should return to `/pricing` with PayPal checkout initiated

---

## After Completion

1. Commit: `git add . && git commit -m "fix: Preserve subscription tier through OAuth redirect"`
2. Push: `git push origin main`
3. Update `PROJECT_STATUS.md` with v2.4.9 entry:
   ```
   ### **v2.4.9** - January 6, 2026
   - 🔧 **PayPal Subscription Flow Fixed**: Resolved OAuth redirect losing tier parameter
     - Fixed query param name mismatch (`redirect` → `redirect_to`)
     - Added URL encoding for nested query params
     - Added auto-trigger logic on pricing page load when returning from login
   ```

---

**File to edit**: `web/tstr-frontend/src/pages/pricing.astro`
