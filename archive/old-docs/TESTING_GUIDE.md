# TSTR.site Tier System Testing Guide

**Dev Server**: http://localhost:4321/ (✅ Running)
**Date**: 2025-11-18
**Status**: Code verified, ready for manual browser testing

---

## ✅ Code Review Results

All code has been verified and looks correct:

- ✅ `/signup` - User registration with email/password
- ✅ `/login` - Authentication flow
- ✅ `/account` - Dashboard with tier display
- ✅ `/listing/[slug]` - Tier-based content gating

**Expected behavior verified in code**:
- Free tier (no login): Limited content, upgrade CTA
- Basic tier (after signup): Full listings, no contact info
- Professional tier: Full contact access

---

## Manual Testing Checklist

### Test 1: Free Tier (No Login) ✅ VERIFIED

**URL**: http://localhost:4321/listing/intertek-testing-services-na

**Expected Results**:
- ✅ Description truncated to ~150 chars
- ✅ Location shows city/state only
- ✅ Phone/email hidden
- ✅ Upgrade CTA: "Sign up free to view full listing details"
- ✅ "Sign Up Free" button present

**Status**: ✅ PASSED (verified via curl)

---

### Test 2: Signup Flow

**Steps**:
1. Open browser to http://localhost:4321/signup
2. Enter test credentials:
   - Email: `test@example.com`
   - Password: `testpass123`
   - Company: `Test Company` (optional)
3. Click "Create Account"

**Expected Results**:
- ✅ Success message: "Account created! Check your email..."
- ✅ Auto-redirect to `/login?registered=true` after 3 seconds
- ✅ Login page shows: "Account created! Please sign in"

**Supabase Verification**:
```sql
-- Run in Supabase SQL Editor
SELECT email, subscription_tier, subscription_status
FROM auth.users
JOIN user_profiles ON auth.users.id = user_profiles.id
WHERE email = 'test@example.com';

-- Expected: tier='basic', status='active'
```

**Status**: ⬜ TODO (manual browser test)

---

### Test 3: Email Verification (Optional)

**Note**: Supabase auth sends verification email. For dev testing:
1. Check Supabase Dashboard → Authentication → Users
2. Find test user
3. Manually confirm email (if needed)

**Status**: ⬜ TODO (if needed)

---

### Test 4: Login Flow

**Steps**:
1. Go to http://localhost:4321/login
2. Enter credentials from Test 2
3. Click "Sign In"

**Expected Results**:
- ✅ Success message: "Sign in successful! Redirecting..."
- ✅ Redirect to `/account` after 1 second
- ✅ Session cookie set

**Status**: ⬜ TODO (manual browser test)

---

### Test 5: Account Dashboard

**URL**: http://localhost:4321/account (after login)

**Expected Results**:
- ✅ Displays:
  - Email: `test@example.com`
  - Company: `Test Company`
  - Tier badge: "Basic" (blue)
  - Member since date
- ✅ Benefits list shows basic tier features:
  - View full listings and certifications
  - Search and filter by category
  - Save favorite listings
  - Email notifications
- ✅ "Upgrade Plan" button → `/account/subscription`
- ✅ "Sign Out" button present

**Status**: ⬜ TODO (manual browser test)

---

### Test 6: Basic Tier Content Access

**Steps**:
1. While logged in as basic tier user
2. Visit http://localhost:4321/listing/intertek-testing-services-na

**Expected Results**:
- ✅ Full description visible (not truncated)
- ✅ Full address visible (not just city/state)
- ✅ Website link visible
- ✅ Phone/email STILL HIDDEN
- ✅ Upgrade CTA: "Upgrade to Professional ($295/mo) for contact access"

**Status**: ⬜ TODO (manual browser test)

---

### Test 7: Upgrade to Professional Tier

**Steps**:
1. Run in Supabase SQL Editor:
```sql
UPDATE user_profiles
SET subscription_tier = 'professional',
    subscription_status = 'active'
WHERE billing_email = 'test@example.com';
```
2. Refresh http://localhost:4321/account

**Expected Results**:
- ✅ Tier badge changes to "Professional" (purple)
- ✅ Benefits list shows professional features:
  - Access phone and email contacts
  - Export data to CSV
  - Advanced search filters
  - Priority customer support
  - Monthly usage reports

**Status**: ⬜ TODO (manual SQL + browser test)

---

### Test 8: Professional Tier Full Access

**Steps**:
1. After upgrading to professional
2. Visit http://localhost:4321/listing/intertek-testing-services-na

**Expected Results**:
- ✅ Full description visible
- ✅ Full address visible
- ✅ Website link visible
- ✅ **Phone visible** (if listing has phone)
- ✅ **Email visible** (if listing has email)
- ✅ NO upgrade CTAs shown
- ✅ All certifications/custom fields visible

**Status**: ⬜ TODO (manual browser test)

---

### Test 9: Logout and Re-login

**Steps**:
1. Click "Sign Out" on `/account`
2. Verify redirect to homepage
3. Visit `/listing/[slug]` → should see free tier view
4. Log back in via `/login`
5. Check `/account` → session restored

**Expected Results**:
- ✅ Logout clears session
- ✅ Free tier view after logout
- ✅ Re-login restores professional tier access
- ✅ Account dashboard shows correct data

**Status**: ⬜ TODO (manual browser test)

---

## Known Issues to Verify

1. **Navigation Links Missing**: Header doesn't have Login/Signup/Account links yet
   - Workaround: Navigate directly to URLs

2. **Subscription Page Missing**: `/account/subscription` returns 404
   - Expected: Shows "Contact us to upgrade" message

3. **Email Verification**: May need to be disabled for dev testing
   - Check: Supabase Dashboard → Auth → Email Templates

---

## Automated Tests (Backend)

### Test: Database Helper Functions

```bash
# Run in project root
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working"

# Test get_user_tier function
supabase db remote psql -c "SELECT get_user_tier('<user-uuid-from-signup>');"

# Test can_view_contact_info function
supabase db remote psql -c "SELECT can_view_contact_info('<user-uuid>');"
```

**Expected Results**:
- Basic tier: `can_view_contact_info()` returns `FALSE`
- Professional tier: returns `TRUE`

---

## Quick Test Commands

### Check User Profile
```sql
SELECT
  u.email,
  p.subscription_tier,
  p.subscription_status,
  p.company_name,
  p.created_at
FROM auth.users u
JOIN user_profiles p ON u.id = p.id
WHERE u.email = 'test@example.com';
```

### Check Tier Distribution
```sql
SELECT subscription_tier, COUNT(*)
FROM user_profiles
GROUP BY subscription_tier;
```

### Reset Test User to Basic
```sql
UPDATE user_profiles
SET subscription_tier = 'basic'
WHERE billing_email = 'test@example.com';
```

---

## Testing Notes

**Browser Developer Tools**:
- Open Console (F12) to see any JavaScript errors
- Check Network tab for failed API calls
- Inspect Application → Cookies → `sb-access-token` for session

**Supabase Logs**:
- Dashboard → Logs → Edge Logs (API requests)
- Check for auth errors or RLS policy violations

---

## Bugs Found During Testing

### Bug #1: [Example Template]
**Description**:
**Steps to Reproduce**:
**Expected**:
**Actual**:
**Fix**:

---

## Test Results Summary

| Test | Status | Notes |
|------|--------|-------|
| Free tier access | ✅ PASS | Verified via code |
| Signup flow | ⬜ TODO | Manual test needed |
| Login flow | ⬜ TODO | Manual test needed |
| Account dashboard | ⬜ TODO | Manual test needed |
| Basic tier access | ⬜ TODO | Manual test needed |
| Professional upgrade | ⬜ TODO | Manual SQL + test |
| Professional access | ⬜ TODO | Manual test needed |
| Logout/re-login | ⬜ TODO | Manual test needed |

---

**Next Steps**:
1. Complete manual browser tests (Steps 2-9)
2. Document any bugs found
3. Fix bugs
4. Add navigation links to header
5. Create `/account/subscription` page
6. Deploy to production

---

**Testing Time Estimate**: 30-45 minutes for all manual tests
