# IMMEDIATE FIX: Configure Cloudflare Pages Environment Variables

## The Problem
Your waitlist form returns HTTP 500 because Cloudflare Pages doesn't have the Supabase API keys configured.

---

## OPTION 1: Via Cloudflare Dashboard (Fastest - 2 minutes)

### Step 1: Go to Cloudflare Pages Settings
https://dash.cloudflare.com/

Navigate to: **Pages → tstr-site → Settings → Environment variables**

### Step 2: Add These 3 Variables (Production environment)

**Variable 1:**
```
Name:  PUBLIC_SUPABASE_URL
Value: https://haimjeaetrsaauitrhfy.supabase.co
```

**Variable 2:**
```
Name:  PUBLIC_SUPABASE_ANON_KEY
Value: sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2
```

**Variable 3 (CRITICAL):**
```
Name:  SUPABASE_SERVICE_ROLE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDQzNjU4NSwiZXhwIjoyMDc2MDEyNTg1fQ.zd47WtS1G1XzjP1obmr_lxHU_xJWtlhhu4ktm9xC5hA
```

### Step 3: Save and Redeploy

**Important:** Saving variables isn't enough - you MUST trigger a rebuild!

Go to: **Deployments → View build → Retry deployment**

Or push a new commit to trigger rebuild automatically.

### Step 4: Test (after 2-3 minutes)

```bash
curl -X POST https://tstr.site/api/submit \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

Should return:
```json
{"message":"Success","id":"..."}
```

---

## OPTION 2: Via Wrangler CLI (If you have API token)

### Prerequisites:
```bash
export CLOUDFLARE_ACCOUNT_ID='your-account-id'
export CLOUDFLARE_API_TOKEN='your-api-token'
```

### Run the script:
```bash
./CONFIGURE_CLOUDFLARE_PAGES.sh
```

---

## OPTION 3: Via GitHub Secrets (Automated)

If your Cloudflare Pages is connected to GitHub and builds automatically:

### Step 1: Add GitHub Secrets

Go to: https://github.com/JAvZZe/tstr-site/settings/secrets/actions

Add these secrets:
- `CF_ACCOUNT_ID`
- `CF_API_TOKEN`

### Step 2: Create GitHub Action

File: `.github/workflows/configure-cloudflare.yml`

```yaml
name: Configure Cloudflare Pages

on:
  workflow_dispatch:

jobs:
  configure:
    runs-on: ubuntu-latest
    steps:
      - name: Set Environment Variables
        run: |
          curl -X PATCH "https://api.cloudflare.com/client/v4/accounts/${{ secrets.CF_ACCOUNT_ID }}/pages/projects/tstr-site" \
            -H "Authorization: Bearer ${{ secrets.CF_API_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{
              "deployment_configs": {
                "production": {
                  "env_vars": {
                    "PUBLIC_SUPABASE_URL": {"value": "https://haimjeaetrsaauitrhfy.supabase.co"},
                    "PUBLIC_SUPABASE_ANON_KEY": {"value": "${{ secrets.SUPABASE_ANON_KEY }}"},
                    "SUPABASE_SERVICE_ROLE_KEY": {"value": "${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}"}
                  }
                }
              }
            }'
```

---

## Verification Steps

### 1. Check if variables are set:

Go to: **Cloudflare Pages → Settings → Environment variables**

You should see all 3 variables listed under "Production".

### 2. Test API endpoint:

```bash
# Should return 200, not 500
curl -i -X POST https://tstr.site/api/submit \
  -H "Content-Type: application/json" \
  -d '{"email":"verify@test.com"}'
```

### 3. Test form on website:

1. Go to: https://tstr.site/waitlist
2. Enter email
3. Submit
4. Should see: "✅ Success! We will notify you."

### 4. Verify in database:

Run in Supabase SQL Editor:
```sql
SELECT * FROM waitlist ORDER BY created_at DESC LIMIT 5;
```

---

## Files Created

I've created these files to help:

1. **`.dev.vars`** - Local development environment variables (gitignored)
2. **`CONFIGURE_CLOUDFLARE_PAGES.sh`** - Automated configuration script
3. **This file** - Manual instructions

---

## What I Cannot Do

I cannot directly access your Cloudflare dashboard or API tokens. You must either:

1. **Manually add the variables** via Cloudflare dashboard (RECOMMENDED - takes 2 minutes)
2. **Provide API credentials** so I can use the CLI/API
3. **Run the script yourself** with your credentials

---

## TL;DR - Fastest Fix

1. Go to: https://dash.cloudflare.com/
2. Pages → tstr-site → Settings → Environment variables
3. Add the 3 variables listed in Option 1
4. Click "Save"
5. Go to Deployments → Retry deployment
6. Wait 2-3 minutes
7. Done! ✅

---

**Once variables are set and site is redeployed, the waitlist form will work immediately.**
