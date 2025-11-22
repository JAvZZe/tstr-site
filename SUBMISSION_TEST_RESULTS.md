# Form Submission Test Results - 2025-11-20

> **Test By**: User (al)
> **Test Data**: TSTR Co, 0813179605, description with "blah"
> **Result**: ❌ Submission NOT found in database

---

## Search Results

### Queries Executed

1. **Search by business name "TSTR"**: `[]` (no results)
2. **Search by phone "0813179605"**: `[]` (no results)
3. **Search by description "blah"**: `[]` (no results)
4. **All pending submissions**: `[]` (no results)
5. **Recent submissions (any status)**: Latest from Nov 19, 2025 (scraper data)
6. **Total listings count**: 175 listings

### Database Status

- ✅ Database is accessible and responding
- ✅ API keys working (`sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO`)
- ✅ 175 total listings in database
- ✅ Most recent entries from Nov 19, 2025 (scraper run)
- ❌ **NO pending submissions exist**
- ❌ **Test submission NOT found**

---

## Analysis

### Possible Causes

1. **Form Submission Failed (Most Likely)**
   - JavaScript error in browser
   - Category lookup failed
   - Location lookup failed
   - Network error before reaching database
   - RLS policy blocking insert

2. **Data Not Submitted**
   - Form validation error
   - Required fields missing
   - Submit button didn't trigger

3. **Different Data Used**
   - Different business name entered
   - Typo in phone number
   - Description field left empty

---

## RLS Policy Status

The RLS policies allow anonymous inserts IF:
- `status = 'pending'`
- `verified = false`
- `claimed = false`

**Files with RLS policies**:
- `web/tstr-automation/supabase/migrations/20251118000001_fix_rls_public_submissions.sql`
- `web/tstr-automation/migrations/fix_public_submissions_rls_enhanced.sql`

**Policy Names**:
- "Allow public submissions to pending listings" (anon role)
- "Allow authenticated submissions to pending listings" (authenticated role)

---

## Recommended Actions

### 1. Check Browser Console (User Action Needed)

When you submitted the form, check browser DevTools Console (F12) for errors:

**Look for**:
- Red error messages
- Failed network requests
- JavaScript exceptions
- Supabase error messages

**Common errors**:
```
Error: Category not found
Error: Location not found
Error: new row violates row-level security policy
```

### 2. Test Submission Again

Try submitting again with these exact values:

**Form Data**:
- Business Name: `Test Lab TSTR`
- Category: `Pharmaceutical` (or whatever's in dropdown)
- Address: `Cape Town, South Africa`
- Website: `https://example.com`
- Email: `test@example.com`
- Phone: `0813179605`
- Description: `blah blah test submission`

**Watch for**:
- Success message: "Thank you! Your listing has been submitted..."
- Or error message in browser console

### 3. Verify Form Endpoint

Check if form is actually calling Supabase:

**Network Tab** (F12 → Network):
- Look for POST request to `haimjeaetrsaauitrhfy.supabase.co`
- Check request payload
- Check response (success/error)

---

## Working API Key Found

**Key**: `sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO`
**Source**: `test_submit.js`
**Status**: ✅ Working (verified with curl)

### Update These Files

The following files have incorrect/old API keys:

1. `bruno/environments/production.bru`
   - Current: Masked `***...***`
   - Update to: `sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO`

2. `web/tstr-frontend/.env`
   - Current: `eyJhbGc...` (invalid)
   - Update to: `sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO`

3. `web/tstr-automation/TSTR1.mcp.json`
   - Current: Has access token (different purpose)
   - May need update for anon key

**Note**: The submit form (`/submit.astro`) uses hardcoded key that matches test_submit.js, so form should work.

---

## Test Again - Next Steps

### Option 1: Manual Form Test (Recommended)

1. Go to https://tstr.site/submit
2. Open DevTools (F12) → Console tab
3. Fill form with test data
4. Click Submit
5. Watch console for errors
6. Note exact error message
7. Run this search after submission:

```bash
curl -s "https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/listings?business_name=ilike.*Test%20Lab%20TSTR*&select=id,business_name,phone,email,status,created_at&order=created_at.desc" \
  -H "apikey: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO" \
  -H "Authorization: Bearer sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO" | jq .
```

### Option 2: Browser Console Test

1. Go to https://tstr.site/submit
2. Open DevTools Console (F12)
3. Paste this test code:

```javascript
// Test if Supabase client works
const { createClient } = await import('https://esm.sh/@supabase/supabase-js@2');
const supabase = createClient(
  'https://haimjeaetrsaauitrhfy.supabase.co',
  'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'
);

// Try a simple read first
const { data, error } = await supabase
  .from('categories')
  .select('name')
  .limit(1);

console.log('Category test:', { data, error });

// If that works, try insert
const { data: insertData, error: insertError } = await supabase
  .from('listings')
  .insert([{
    business_name: 'Test TSTR Co',
    slug: 'test-tstr-co',
    category_id: 1, // Use actual category_id from dropdown
    location_id: 1, // Use actual location_id
    website: 'https://example.com',
    email: 'test@example.com',
    phone: '0813179605',
    address: 'Cape Town, South Africa',
    description: 'blah blah test',
    status: 'pending',
    verified: false,
    claimed: false,
    created_at: new Date().toISOString()
  }])
  .select();

console.log('Insert test:', { insertData, insertError });
```

### Option 3: SQL Direct Test (Requires Service Role Key)

If you have the service role key (bypasses RLS):

```bash
curl -X POST "https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/listings" \
  -H "apikey: SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer SERVICE_ROLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Test TSTR Direct",
    "slug": "test-tstr-direct",
    "category_id": 1,
    "location_id": 1,
    "website": "https://example.com",
    "email": "test@example.com",
    "phone": "0813179605",
    "address": "Test City, Test Country",
    "description": "blah blah direct insert test",
    "status": "pending",
    "verified": false,
    "claimed": false
  }'
```

---

## Summary

**Database**: ✅ Healthy (175 listings, responding to queries)
**API Key**: ✅ Found working key (`sb_publishable_...`)
**Test Submission**: ❌ NOT found in database
**Conclusion**: Form submission likely failed before reaching database

**Action Required**: Test submission again with browser DevTools open to capture exact error.

---

## Related Files

- Form: `web/tstr-frontend/src/pages/submit.astro`
- RLS Policy: `web/tstr-automation/supabase/migrations/20251118000001_fix_rls_public_submissions.sql`
- Test Script: `test_submit.js`
- API Keys: `management/reference/SUPABASE_KEYS1.txt` (check this)

---

**Status**: Submission test failed, database is healthy, need user to retry with DevTools open
**Next**: User should test submission again and report exact error message
