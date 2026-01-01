# 🚀 GitHub + Netlify Deployment Guide

**Easiest deployment method - No CLI needed!**  
**Time**: 15 minutes  
**Cost**: FREE

---

## 📋 Step-by-Step Instructions

### **Step 1: Initialize Git Repository** (2 minutes)

```bash
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.directory

# Initialize Git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - TSTR.directory with automated scrapers"
```

---

### **Step 2: Create GitHub Repository** (3 minutes)

1. Go to https://github.com/new
2. Create new repository:
   - **Name**: `tstr-site`
   - **Description**: `Testing Laboratory Directory with Automated Scrapers`
   - **Visibility**: Private (recommended) or Public
   - **DO NOT** initialize with README (we already have files)
3. Click **"Create repository"**

---

### **Step 3: Push to GitHub** (2 minutes)

GitHub will show you commands. Use these:

```bash
# Add remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/tstr-site.git

# Push code
git branch -M main
git push -u origin main
```

**OR** if you prefer SSH:

```bash
git remote add origin git@github.com:YOUR-USERNAME/tstr-site.git
git branch -M main
git push -u origin main
```

---

### **Step 4: Deploy to Netlify** (5 minutes)

#### **4a. Connect GitHub to Netlify**

1. Go to https://app.netlify.com
2. Click **"Add new site"** → **"Import an existing project"**
3. Choose **"Deploy with GitHub"**
4. Authorize Netlify to access your GitHub account
5. Select your repository: `tstr-site`

#### **4b. Configure Build Settings**

Netlify should auto-detect these settings (verify they're correct):

- **Base directory**: `web/tstr-frontend`
- **Build command**: `npm run build`
- **Publish directory**: `web/tstr-frontend/dist`
- **Branch**: `main`

Click **"Show advanced"** and verify Node version:
- **NODE_VERSION**: `18`

#### **4c. Set Environment Variables**

**CRITICAL**: Before deploying, add environment variables:

1. Click **"Add environment variables"**
2. Add these two variables:

```
Key: PUBLIC_SUPABASE_URL
Value: https://haimjeaetrsaauitrhfy.supabase.co

Key: PUBLIC_SUPABASE_ANON_KEY
Value: sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2
```

3. Click **"Deploy site"**

---

### **Step 5: Wait for Deployment** (2-3 minutes)

Netlify will:
1. Clone your repository
2. Install dependencies
3. Build your site
4. Deploy to CDN

**You'll get a URL like**: `https://random-name-12345.netlify.app`

---

### **Step 6: Setup Auto-Rebuild Webhook** (3 minutes)

#### **6a. Get Netlify Build Hook**

1. In Netlify Dashboard, go to: **Site Settings** → **Build & Deploy** → **Build hooks**
2. Click **"Add build hook"**
   - **Name**: `Supabase Listings Update`
   - **Branch to build**: `main`
3. Click **"Save"**
4. **Copy the webhook URL** (looks like: `https://api.netlify.com/build_hooks/xxxxx`)

#### **6b. Create Supabase Webhook**

1. Go to https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
2. Navigate to: **Database** → **Webhooks**
3. Click **"Create a new hook"** (or **"Enable Webhooks"** if first time)
4. Configure:
   - **Name**: `Netlify Rebuild on New Listings`
   - **Table**: `listings`
   - **Events**: Check ✅ `INSERT` and ✅ `UPDATE`
   - **Type**: `HTTP Request`
   - **HTTP Method**: `POST`
   - **URL**: Paste your Netlify build hook URL
   - **HTTP Headers**: Leave empty (not needed)
5. Click **"Confirm"** or **"Create webhook"**

---

## ✅ Verify Deployment

### **Check Your Live Site**:
1. Visit your Netlify URL
2. You should see:
   - ✅ TSTR.directory header
   - ✅ Stats showing 19 verified labs
   - ✅ All 19 testing laboratories listed
   - ✅ Categories section
   - ✅ Locations section

### **Test Auto-Rebuild**:

**Manual Test**:
```bash
# Trigger rebuild manually
curl -X POST -d {} https://api.netlify.com/build_hooks/YOUR-HOOK-ID
```

**Wait for Next Scraper** (automatic test):
- Next scraper run: 3 days from last run
- Will add new listings → Trigger webhook → Rebuild site → Show new data

---

## 🎉 Success Checklist

After deployment, verify:

- [ ] Site is live at Netlify URL
- [ ] Shows 19 verified testing laboratories
- [ ] Stats display correct numbers
- [ ] All links work (phone, email, website)
- [ ] Environment variables are set in Netlify
- [ ] Build hook created in Netlify
- [ ] Webhook configured in Supabase
- [ ] Test manual rebuild (optional)

---

## 🔄 Future Updates

### **To Deploy Code Changes**:

```bash
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.directory

# Make your changes to files
# Then:

git add .
git commit -m "Description of changes"
git push

# Netlify will automatically detect and redeploy!
```

### **Auto-Rebuild Workflow**:

```
1. Cloud Scraper runs (every 3 days)
      ↓
2. Adds listing to Supabase
      ↓
3. Supabase webhook fires
      ↓
4. Netlify rebuilds (2-3 minutes)
      ↓
5. New listing appears on site ✅
```

---

## 💰 Costs

**Netlify Free Tier**:
- ✅ 100 GB bandwidth/month
- ✅ 300 build minutes/month
- ✅ Unlimited sites
- ✅ Automatic SSL/HTTPS
- ✅ Continuous deployment

**Your Usage**:
- ~90 builds/month (from scraper updates)
- ~2 minutes per build
- = ~180 minutes/month
- **Well within free tier!** ✅

**Total Monthly Cost**: **$1.04** (same as before, Netlify is FREE!)

---

## 🛠️ Troubleshooting

### **Build Fails**:
1. Check Netlify build logs (in dashboard)
2. Verify environment variables are set
3. Check base directory is `web/tstr-frontend`
4. Check build command is `npm run build`

### **Site Shows No Data**:
1. Verify environment variables in Netlify dashboard
2. Check browser console for errors (F12)
3. Verify Supabase connection in console
4. Check database has `website_verified = true` listings

### **Webhook Not Working**:
1. Check Supabase webhook is enabled
2. Verify correct Netlify build hook URL
3. Test manually with curl command
4. Check Netlify build logs for webhook triggers

---

## 🎯 What You Get

After following this guide:

✅ **Website live on internet** (Netlify URL)  
✅ **Shows all 19 verified labs**  
✅ **Auto-updates when scrapers run** (2-3 min delay)  
✅ **Zero manual work needed**  
✅ **Professional, fast, secure**  
✅ **Costs $0 extra** (still $1.04/month total)

---

## 📞 Next Steps After Deployment

### **Optional Enhancements**:

1. **Custom Domain** (optional, ~$12/year):
   - Buy `tstr.directory` domain
   - Configure in Netlify dashboard
   - Automatic SSL included

2. **Monitoring**:
   - Setup Netlify deploy notifications
   - Monitor Supabase webhook logs
   - Check Google Cloud Function logs

3. **Scaling**:
   - Add more scraper categories
   - Expand to more regions
   - Add search/filter functionality

---

## 🎉 You're Done!

**Your fully automated testing laboratory directory is now LIVE!**

- ✅ Scrapers run automatically every 3 days
- ✅ Database updates automatically
- ✅ Website rebuilds automatically
- ✅ Fresh data always visible
- ✅ Zero maintenance required

**Congratulations!** 🚀

---

**Need help?** Check:
- Netlify docs: https://docs.netlify.com
- Supabase docs: https://supabase.com/docs
- Or review `PROJECT_STATUS.md` for current state
