# 🚀 DEPLOY TO NETLIFY - DO THIS NOW!

**Your code is ready!** ✅ Follow these steps to go live.

---

## ✅ STEP 1: Create GitHub Repository (3 minutes)

1. **Go to**: https://github.com/new

2. **Fill in**:
   - Repository name: `tstr-site`
   - Description: `Testing Laboratory Directory with Automated Scrapers`
   - Visibility: **Private** (recommended)
   - **DO NOT** check "Initialize with README" (we already have files)

3. **Click**: "Create repository"

---

## ✅ STEP 2: Push Your Code to GitHub (2 minutes)

GitHub will show you commands. **Copy your GitHub username** from the URL, then run:

```powershell
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site

# Replace YOUR-USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR-USERNAME/tstr-site.git

git branch -M main

git push -u origin main
```

**Example**: If your username is `johnsmith`, use:
```powershell
git remote add origin https://github.com/johnsmith/tstr-site.git
```

---

## ✅ STEP 3: Deploy to Netlify (5 minutes)

### 3a. Import from GitHub

1. **Go to**: https://app.netlify.com
2. **Click**: "Add new site" → "Import an existing project"
3. **Choose**: "Deploy with GitHub"
4. **Authorize**: Allow Netlify to access your GitHub
5. **Select**: Your `tstr-site` repository

### 3b. Configure Build Settings

**IMPORTANT**: Netlify needs to know where your website is!

In the deployment settings, configure:

```
Base directory:     web/tstr-frontend
Build command:      npm run build
Publish directory:  web/tstr-frontend/dist
```

**Node version** (click "Show advanced"):
```
Environment variable: NODE_VERSION
Value: 18
```

### 3c. Add Environment Variables

**CRITICAL**: Before clicking "Deploy", add these:

Click **"Add environment variables"**, then add:

**Variable 1:**
```
Key:   PUBLIC_SUPABASE_URL
Value: https://haimjeaetrsaauitrhfy.supabase.co
```

**Variable 2:**
```
Key:   PUBLIC_SUPABASE_ANON_KEY
Value: [REDACTED_SECRET]
```

### 3d. Deploy!

Click **"Deploy site"** and wait 2-3 minutes.

---

## ✅ STEP 4: Get Your Live URL!

After deployment completes:

1. Netlify will give you a URL like: `https://random-name-12345.netlify.app`
2. **Visit it** - you should see your 19 testing laboratories!
3. **Copy the URL** - this is your live website!

---

## ✅ STEP 5: Setup Auto-Rebuild (3 minutes)

### 5a. Create Netlify Build Hook

1. In Netlify, go to: **Site settings** → **Build & deploy** → **Build hooks**
2. Click **"Add build hook"**
3. Settings:
   - Name: `Supabase Listings Update`
   - Branch: `main`
4. Click **"Save"**
5. **COPY THE WEBHOOK URL** (looks like: `https://api.netlify.com/build_hooks/xxxxx`)

### 5b. Create Supabase Webhook

1. Go to: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
2. Click: **Database** → **Webhooks**
3. Click: **"Create a new hook"** (or **"Enable Webhooks"** first if needed)
4. Configure:
   - **Name**: `Netlify Rebuild on New Listings`
   - **Table**: `listings`
   - **Events**: ✅ `INSERT` ✅ `UPDATE`
   - **Type**: `HTTP Request`
   - **Method**: `POST`
   - **URL**: [Paste your Netlify build hook URL here]
5. Click: **"Confirm"**

---

## 🎉 YOU'RE DONE!

### **What You Now Have**:

✅ **Website live on internet** (your Netlify URL)  
✅ **Shows all 19 verified testing labs**  
✅ **Auto-updates when scrapers run** (every 3 days)  
✅ **Professional, fast, secure**  
✅ **Costs: $1.04/month** (no change!)

### **The Full Automation**:

```
Cloud Scraper runs (every 3 days @ 2am)
    ↓
Adds new listings to Supabase
    ↓
Supabase webhook fires
    ↓
Netlify rebuilds site (2-3 minutes)
    ↓
New listings appear automatically ✅
```

---

## ✅ VERIFY IT WORKS

1. **Visit your Netlify URL**
2. **Check you see**:
   - ✅ TSTR.site header
   - ✅ Stats showing "19 Verified Labs"
   - ✅ All 19 testing laboratories listed
   - ✅ Contact information for each lab

3. **Test the webhook** (optional):
```bash
# Replace YOUR-HOOK-ID with actual ID from Netlify
curl -X POST https://api.netlify.com/build_hooks/YOUR-HOOK-ID
```

Watch Netlify dashboard - it should start rebuilding!

---

## 📊 DEPLOYMENT CHECKLIST

After following all steps:

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Netlify site created
- [ ] Build settings configured (base dir: `web/tstr-frontend`)
- [ ] Environment variables set in Netlify
- [ ] Site deployed successfully
- [ ] Website shows 19 listings
- [ ] Netlify build hook created
- [ ] Supabase webhook configured
- [ ] Auto-rebuild tested

---

## 🆘 TROUBLESHOOTING

### **Build Fails on Netlify**:
1. Check base directory is `web/tstr-frontend`
2. Check build command is `npm run build`
3. Check publish directory is `web/tstr-frontend/dist`
4. Verify environment variables are set

### **Site Shows No Data**:
1. Open browser console (F12)
2. Check for Supabase connection errors
3. Verify environment variables in Netlify
4. Make sure variables start with `PUBLIC_`

### **Webhook Doesn't Work**:
1. Verify Supabase webhook URL matches Netlify build hook
2. Check webhook is enabled in Supabase
3. Test manually with curl command
4. Check Netlify build logs for webhook triggers

---

## 💰 FINAL COSTS

**Monthly Operating Costs**:
```
Cloud Functions:   $0.00  (FREE tier)
Cloud Scheduler:   $0.90  (3 jobs)
Storage/Network:   $0.14
Netlify:          $0.00  (FREE tier)
─────────────────────────
TOTAL:            $1.04/month
```

**No increase!** Everything stays in free tiers! ✅

---

## 🎯 NEXT STEPS (Optional)

### **After Deployment**:

1. **Custom Domain** (optional, ~$12/year):
   - Purchase `tstr.site` domain
   - Configure in Netlify dashboard
   - Free SSL certificate included

2. **Monitoring**:
   - Check Netlify deploy notifications
   - Monitor Supabase webhook logs
   - Review Google Cloud Function logs

3. **Scaling**:
   - Add more scraper categories
   - Expand to more regions
   - Add search/filter functionality

---

## 🎊 CONGRATULATIONS!

**Once deployed, your system will**:
- ✅ Run scrapers automatically every 3 days
- ✅ Update database with new listings
- ✅ Rebuild website automatically
- ✅ Show fresh data to visitors
- ✅ Require ZERO manual maintenance

**You built a fully automated directory platform!** 🚀

---

**Questions?** Check:
- Full guide: `GITHUB_DEPLOY_GUIDE.md`
- Project status: `PROJECT_STATUS.md`
- Netlify docs: https://docs.netlify.com

**Ready? Start with Step 1 above!** ⬆️
