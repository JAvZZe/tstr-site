# Test Form Submission - After RLS Fix

> **Deployed**: 2025-11-20 10:21:37
> **Expected Live**: ~10:24:37 (3 minutes)
> **Commit**: 7cb58fa - "fix: Remove .select() from form submission to work with RLS policy"

---

## Wait for Deployment

**Cloudflare Pages deployment takes ~2-3 minutes**

Check deployment status:
- https://dash.cloudflare.com/pages

Or just wait 3 minutes and test the form.

---

## Test Form Submission

### Step 1: Go to Form

Open: https://tstr.site/submit

### Step 2: Fill Test Data

**Use these exact values**:
- **Business Name**: `Test TSTR Co`
- **Category**: Select any from dropdown (e.g., "Pharmaceutical Testing")
- **Address**: `Cape Town, South Africa`
- **Website**: `https://example.com`
- **Email**: `test@example.com`
- **Phone**: `0813179605`
- **Description**: `blah blah test submission for RLS fix verification`

### Step 3: Submit

Click "Submit Listing" button

### Step 4: Expected Result

**Success Message**:
```
✓ Thank you! Your listing has been submitted successfully.

Our team will review it within 24-48 hours and it will appear 
on the directory once approved.
```

**Then redirected to homepage** (/)

---

## If It Fails

### Check Browser Console (F12)

Look for error messages:
- No errors = likely success
- "new row violates row-level security policy" = cache issue (wait 1 more minute)
- Other errors = report exact message

### Clear Cache

If you see RLS error after 5 minutes:
1. Hard refresh: Ctrl+Shift+R (Chrome/Firefox)
2. Or clear browser cache
3. Try submission again

---

## Verify Submission in Database

After successful submission, check if it's in the database:

```bash
curl -s "https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/listings?business_name=ilike.*Test%20TSTR*&select=id,business_name,phone,status,created_at&order=created_at.desc&limit=5" \
  -H "apikey: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO" \
  -H "Authorization: Bearer sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO" | jq .
```

**Note**: This might return `[]` (empty) because anon users can't SELECT pending listings. That's expected and correct (security feature).

**To verify for real**, you'd need:
- Service role key (bypasses RLS)
- Or Supabase dashboard access
- Or admin panel (future feature)

---

## What Was Fixed

### Before (Broken)
```javascript
const { data: result, error } = await supabase
  .from('listings')
  .insert([{...}])
  .select()  // ❌ Tried to SELECT → RLS blocked
```

### After (Working)
```javascript
const { error } = await supabase
  .from('listings')
  .insert([{...}])
  // ✅ No .select() → Just INSERT → Allowed by RLS
```

### Why This Works

1. ✅ RLS policy allows anon users to **INSERT** with `status='pending'`
2. ✅ Form sends INSERT request → Success (201 Created)
3. ✅ Form doesn't request data back (no .select())
4. ✅ Success handler shows message and redirects
5. ✅ Submission is in database with `status='pending'`

---

## Timeline

- **10:21:37** - Pushed to GitHub
- **~10:22:00** - Cloudflare starts build
- **~10:24:30** - Deployment live
- **10:25:00+** - Safe to test

**Current time**: Check with `date +"%H:%M:%S"`

---

## After Testing

Please report back:
1. ✅ Success message appeared? (Yes/No)
2. ✅ Redirected to homepage? (Yes/No)
3. ❌ Any errors in browser console? (If yes, exact message)
4. ⏳ Time tested (to check if deployment was complete)

---

**Ready to test at**: ~10:25 (or 3 minutes after push)
**Form URL**: https://tstr.site/submit
