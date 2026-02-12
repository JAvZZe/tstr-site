# Get Correct Supabase Keys

## The Problem
The JWT I provided might be incorrect because all my local files have redacted keys.

## Solution: Get Keys from Supabase Dashboard

### Step 1: Go to Supabase
https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/settings/api

### Step 2: Copy These Exact Values

**Project URL:**
- Copy the value under "Project URL"
- Should be: `https://haimjeaetrsaauitrhfy.supabase.co`

**Anon Public Key:**
- Copy the value under "Project API keys" → "anon public"
- Should start with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Service Role Key (IMPORTANT):**
- Copy the value under "Project API keys" → "service_role" 
- Click the "Reveal" button to show it
- **This is the critical one that's likely wrong**
- Should start with `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
- Should be 200-300 characters long

### Step 3: Update Cloudflare Pages

Go back to Cloudflare Pages environment variables and REPLACE the `SUPABASE_SERVICE_ROLE_KEY` value with the exact value from Supabase (including the full JWT - don't truncate it).

### Step 4: Redeploy

Trigger a redeploy after updating the key.

---

## Why This Is Needed

The env vars ARE being accessed correctly (`runtime.env` works), but Supabase is rejecting the JWT with "Invalid API key". This means the JWT value itself is wrong - either:
- Truncated
- Has extra spaces/newlines  
- Is from a different Supabase project
- I provided the wrong value

Getting it directly from Supabase ensures it's 100% correct.
