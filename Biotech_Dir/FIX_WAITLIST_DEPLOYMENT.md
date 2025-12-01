# Fix Waitlist Form - Missing Environment Variables

## 🔴 Problem Identified

**API Endpoint Status:** HTTP 500 (Server Error)  
**Root Cause:** Environment variables not configured on deployment platform

The API code is trying to access:
- `import.meta.env.PUBLIC_SUPABASE_URL`
- `import.meta.env.SUPABASE_SERVICE_ROLE_KEY`

These are undefined on the server, causing the Supabase client to fail.

---

## ✅ Solution: Add Environment Variables

### For Netlify:

1. **Go to Netlify Dashboard:**
   - https://app.netlify.com/sites/YOUR_SITE_NAME/settings/deploys#environment

2. **Click "Environment variables"**

3. **Add these three variables:**

   **Variable 1:**
   ```
   Key:   PUBLIC_SUPABASE_URL
   Value: https://haimjeaetrsaauitrhfy.supabase.co
   ```

   **Variable 2:**
   ```
   Key:   PUBLIC_SUPABASE_ANON_KEY
   Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjAxNTksImV4cCI6MjA3NTYzNjE1OX0.1SoHZoMAeap4p2Fy4HxzHJ4IRZWZ78VamGd0JWQ0OqM
   ```

   **Variable 3 (CRITICAL):**
   ```
   Key:   SUPABASE_SERVICE_ROLE_KEY
   Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyOTQ0ODQzNywiZXhwIjoyMDQ1MDI0NDM3fQ.sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2
   ```

4. **Trigger Redeploy:**
   - Go to: Deploys tab
   - Click "Trigger deploy" → "Deploy site"
   - Wait 2-3 minutes for rebuild

---

### For Cloudflare Pages:

1. **Go to Cloudflare Dashboard:**
   - https://dash.cloudflare.com/
   - Select your project

2. **Navigate to Settings → Environment Variables**

3. **Add the same three variables** (from above)

4. **Choose "Production" environment**

5. **Save and Redeploy:**
   - Go to Deployments tab
   - Click "Retry deployment" on latest deploy

---

## 🧪 Test After Deployment

### Test 1: API Endpoint
```bash
curl -X POST https://tstr.site/api/submit \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

**Expected Response:**
```json
{"message":"Success","id":"123e4567-e89b-12d3-a456-426614174000"}
```

If you get this, it's working! ✅

### Test 2: Form on Website
1. Go to: https://tstr.site/waitlist
2. Enter any email
3. Click "Join Waitlist"
4. Should see: "✅ Success! We will notify you."

### Test 3: Verify in Database
Run this in Supabase SQL Editor:
```sql
SELECT * FROM waitlist ORDER BY created_at DESC LIMIT 5;
```

Should show the test email.

---

## 🔍 If Still Not Working

### Check Deployment Logs:

**Netlify:**
- Go to: Deploys → Click on latest deploy → Function logs
- Look for errors mentioning "supabase" or "undefined"

**Cloudflare Pages:**
- Go to: Deployments → Click latest → View logs
- Check for build/runtime errors

### Common Issues:

**Issue 1: "JWTExpired" error**
- Service role key is expired
- Get new one from: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/settings/api

**Issue 2: "Invalid API key"**
- Key was copied incorrectly
- Make sure no extra spaces or line breaks

**Issue 3: Still getting 500**
- Clear browser cache
- Try in incognito/private window
- Check deployment logs for actual error

---

## 📊 Environment Variables Summary

| Variable | Where Used | Purpose | Required |
|----------|-----------|---------|----------|
| `PUBLIC_SUPABASE_URL` | Client & Server | API endpoint | ✅ Yes |
| `PUBLIC_SUPABASE_ANON_KEY` | Client-side | Read-only access | ✅ Yes |
| `SUPABASE_SERVICE_ROLE_KEY` | Server-side only | Write access | ✅ Yes |

**Security Note:** The `SUPABASE_SERVICE_ROLE_KEY` should NEVER be exposed to the client. It's only used in the API route (`/api/submit.ts`) which runs server-side.

---

## 🎯 Quick Copy-Paste for Netlify/Cloudflare

### All Three Variables in One Block:

```
PUBLIC_SUPABASE_URL=https://haimjeaetrsaauitrhfy.supabase.co

PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjAxNTksImV4cCI6MjA3NTYzNjE1OX0.1SoHZoMAeap4p2Fy4HxzHJ4IRZWZ78VamGd0JWQ0OqM

SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyOTQ0ODQzNywiZXhwIjoyMDQ1MDI0NDM3fQ.sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2
```

**Note:** Some platforms allow you to paste this format directly. Others require you to add each variable individually.

---

## ⏱️ After Adding Variables:

1. **Trigger redeploy** (don't just save - must rebuild!)
2. **Wait 2-3 minutes** for build to complete
3. **Test the form** at https://tstr.site/waitlist
4. **Verify in database** using SQL query

---

**Once environment variables are added and site is redeployed, the waitlist form will work!** ✅
