# DEPLOY TO CLOUDFLARE PAGES - STEP BY STEP

## Step 1: Create Cloudflare Account (if needed)

1. **Go to:** https://dash.cloudflare.com/sign-up

2. **Sign up with:**
   - Email: tstr.site@gmail.com (or your preferred email)
   - Password: Create a strong password
   
3. **Verify your email**

4. **Skip any upsells** - we're using the FREE plan

---

## Step 2: Create New Pages Project

1. **Go to:** https://dash.cloudflare.com

2. **In the left sidebar, click:** "Workers & Pages"

3. **Click:** "Create application"

4. **Click:** "Pages" tab

5. **Click:** "Connect to Git"

6. **Click:** "Connect GitHub"

7. **Authorize Cloudflare** to access your GitHub
   - Click "Authorize Cloudflare"
   - You may need to enter your GitHub password

8. **Select your repository:**
   - Find and click: `JAvZZe/tstr-site`

9. **Click:** "Begin setup"

---

## Step 3: Configure Build Settings

On the setup page, enter these EXACT settings:

**Project name:** `tstr-site`

**Production branch:** `main`

**Framework preset:** Select "Astro" from dropdown

**Build command:** (should auto-fill as)
```
npm run build
```

**Build output directory:** (should auto-fill as)
```
dist
```

---

## Step 4: Add Environment Variables

This is CRITICAL - your site needs to connect to Supabase!

**Scroll down to "Environment variables"**

**Click:** "Add variable"

**Add these TWO variables:**

**Variable 1:**
- Variable name: `PUBLIC_SUPABASE_URL`
- Value: `https://haimjeaetrsaauitrhfy.supabase.co`

**Click:** "Add variable" again

**Variable 2:**
- Variable name: `PUBLIC_SUPABASE_ANON_KEY`
- Value: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjAxNTksImV4cCI6MjA3NTYzNjE1OX0.1SoHZoMAeap4p2Fy4HxzHJ4IRZWZ78VamGd0JWQ0OqM`

**IMPORTANT:** Make sure there are NO spaces before or after the values!

---

## Step 5: Deploy!

1. **Click:** "Save and Deploy"

2. **Wait 2-3 minutes** - you'll see:
   - ⏳ Initializing build environment
   - ⏳ Cloning repository
   - ⏳ Installing dependencies
   - ⏳ Building application
   - ⏳ Deploying to Cloudflare's global network

3. **When complete, you'll see:**
   - ✅ Success! Your site is live!
   - A URL like: `https://tstr-site.pages.dev`

4. **Click the URL** to see your live site!

---

## Step 6: Verify Your Live Site

Your site should show:
- ✅ TSTR.site header
- ✅ 5 testing categories (from Supabase)
- ✅ Global locations
- ✅ Professional design

**If you see this, YOUR SITE IS LIVE ON THE INTERNET!** 🎉

---

## TROUBLESHOOTING

### Build fails with "command not found"
**Fix:** Check that build command is exactly `npm run build`

### Build succeeds but site shows errors
**Fix:** Check environment variables are set correctly (no spaces)

### Categories don't show
**Fix:** Environment variables missing or incorrect

### "Module not found" errors
**Fix:** In Cloudflare dashboard, go to Settings → Functions → Compatibility flags → Add `nodejs_compat`

---

## NEXT: CUSTOM DOMAIN

Once your site is live at `tstr-site.pages.dev`, we'll point your actual domain `tstr.site` to it.

Come back and tell me: **"Site is live at pages.dev!"**

Then I'll help you configure the custom domain.
