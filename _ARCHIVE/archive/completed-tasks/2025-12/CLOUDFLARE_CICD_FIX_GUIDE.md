# Fix Cloudflare Pages CI/CD - Step-by-Step Guide

**Issue**: Pushing to GitHub `main` branch does NOT trigger Cloudflare Pages rebuild
**Impact**: Site shows 19 old listings despite 127 in database
**Time to Fix**: ~5 minutes

---

## Prerequisites

- Access to Cloudflare dashboard (account: tstr.site1@gmail.com)
- GitHub repository: `JAvZZe/tstr-site`

---

## Step 1: Access Cloudflare Pages Dashboard

1. Go to https://dash.cloudflare.com
2. Log in with: **tstr.site1@gmail.com**
3. Click **Workers & Pages** in left sidebar
4. Click on **tstr-site** project

---

## Step 2: Check Current GitHub Connection

1. Click **Settings** tab
2. Scroll to **Build & deployments** section
3. Look for **Source** - should show GitHub connection
4. Note if it shows "Connected" or any error

---

## Step 3: Reconnect GitHub Repository

### Option A: Quick Reconnect (if available)

1. In Settings → Builds & deployments
2. Look for **Reconnect** or **Edit configuration** button
3. Click it
4. Select repository: `JAvZZe/tstr-site`
5. Branch: `main`
6. Click **Save**

### Option B: Full Disconnect/Reconnect (if needed)

1. Click **Disconnect** next to GitHub source
2. Confirm disconnection
3. Click **Connect to Git** button
4. Select **GitHub**
5. Authorize Cloudflare (if prompted)
6. Select repository: `JAvZZe/tstr-site`
7. Configure:
   - **Production branch**: `main`
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Root directory**: `web/tstr-frontend`
8. Click **Save and Deploy**

---

## Step 4: Verify Build Configuration

Ensure these settings are correct:

| Setting | Value |
|---------|-------|
| Framework preset | **Astro** |
| Build command | `npm run build` |
| Build output directory | `dist` |
| Root directory | `web/tstr-frontend` |
| Node version | 18 or higher |

### Environment Variables (CRITICAL)

Make sure these are set in **Settings → Environment variables**:

| Variable | Value |
|----------|-------|
| `PUBLIC_SUPABASE_URL` | `https://haimjeaetrsaauitrhfy.supabase.co` |
| `PUBLIC_SUPABASE_ANON_KEY` | `sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO` |

---

## Step 5: Test the Connection

### Method 1: Trigger Manual Build

1. Go to **Deployments** tab
2. Click **Create deployment** button
3. Branch: `main`
4. Click **Save and Deploy**
5. Watch build logs - should show:
   - Installing dependencies
   - Building with Astro
   - Querying Supabase (should fetch 127 listings)
   - Deployment success

### Method 2: Test with Git Push

```bash
# Make a small change
echo "\n# CI/CD test" >> README.md

# Commit
git add README.md
git commit -m "Test CI/CD pipeline"

# Push
git push origin main
```

**Expected**: Within 1-2 minutes, Cloudflare should:
- Detect the push
- Start a new build
- Deploy automatically

---

## Step 6: Verify Deployment Success

1. Wait for build to complete (~2-3 minutes)
2. Visit https://tstr.site
3. Check the stats card - should show **127 Verified Labs** (not 19)
4. First listing should be **WOUNDCHEK Laboratories BV** (Biopharma & Life Sciences)
5. Not **Element Singapore** (Materials Testing)

---

## Troubleshooting

### Build Fails with "Cannot find module"

**Fix**: Check Node version in Cloudflare settings
- Go to Settings → Environment variables
- Add: `NODE_VERSION` = `18`

### Build Succeeds but Shows 19 Listings

**Issue**: Environment variables not set correctly

**Fix**:
1. Settings → Environment variables
2. Verify both Supabase variables are present
3. Redeploy

### GitHub Push Doesn't Trigger Build

**Fix**:
1. Settings → Builds & deployments
2. Check **Branch deployments** is enabled
3. Verify `main` branch is set as production branch
4. Try disconnect/reconnect again

---

## Alternative: Set Up Auto-Rebuild After Scraper Runs

If you want the site to rebuild automatically when Oracle scraper adds data:

### Create Cloudflare Build Hook

1. Cloudflare Pages → tstr-site → Settings
2. Builds & deployments → Build hooks
3. Click **Add build hook**
4. Name: `Supabase Data Update`
5. Branch: `main`
6. **Copy the webhook URL** (looks like: `https://api.cloudflare.com/...`)

### Create Supabase Database Webhook

1. Go to https://supabase.com/dashboard
2. Select project: `haimjeaetrsaauitrhfy`
3. Database → Webhooks
4. Click **Enable Webhooks** (if needed)
5. Click **Create webhook**
6. Configure:
   - **Name**: `Trigger Cloudflare Rebuild`
   - **Table**: `listings`
   - **Events**: ✓ INSERT, ✓ UPDATE
   - **Type**: HTTP Request
   - **Method**: POST
   - **URL**: [Paste Cloudflare build hook URL]
7. Click **Create**

**Result**: Every time Oracle scraper adds/updates listings, Supabase triggers Cloudflare rebuild (2-3 min later, site shows new data).

---

## Expected Outcome

After fixing CI/CD:
- ✅ Git push → Auto-deploy to Cloudflare
- ✅ Site shows all 127 listings
- ✅ New scraper data appears automatically (if webhook set up)
- ✅ No manual intervention needed

---

## File Locations for Reference

- **Cloudflare API Token**: `/media/al/.../TSTR.directory/.env.github-copilot`
- **Supabase Keys**: `/media/al/.../TSTR.directory/web/tstr-frontend/.env`
- **Scraper Code**: `/media/al/.../TSTR.directory/web/tstr-automation/dual_scraper.py`
- **Frontend Source**: `/media/al/.../TSTR.directory/web/tstr-frontend/`

---

**After fixing, update**:
- `/media/al/.../TSTR.site/SESSION_STATE.json` - Change `"deployment_issue"` to `"RESOLVED"`
- `/media/al/AI_DATA/AI_PROJECTS_SPACE/` - Run `./checkpoint.sh "CI/CD fixed - auto-deploy working"`
