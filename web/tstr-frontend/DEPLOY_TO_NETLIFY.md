# 🚀 Deploy TSTR.site to Netlify

**Time**: ~10 minutes  
**Cost**: FREE (Netlify free tier)

---

## ✅ Pre-Deployment Checklist

Before deploying, make sure you have:
- [x] Updated `index.astro` to fetch from `listings` table ✅
- [x] Created `netlify.toml` configuration ✅
- [x] Supabase URL and Anon Key ready

---

## 📋 Step-by-Step Deployment

### **Step 1: Install Netlify CLI** (2 minutes)

```bash
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site\web\tstr-frontend
npm install -g netlify-cli
```

### **Step 2: Login to Netlify** (1 minute)

```bash
netlify login
```

This will open your browser to authenticate.

### **Step 3: Initialize Netlify** (1 minute)

```bash
netlify init
```

When prompted:
1. **Create & configure a new site?** → Yes
2. **Team?** → Choose your team
3. **Site name?** → `tstr-site` (or your preference)
4. **Build command?** → `npm run build` (should be detected)
5. **Deploy directory?** → `dist` (should be detected)

### **Step 4: Set Environment Variables** (3 minutes)

**IMPORTANT**: Set these in Netlify (not in .env file for security)

```bash
# Set Supabase URL
netlify env:set PUBLIC_SUPABASE_URL "https://haimjeaetrsaauitrhfy.supabase.co"

# Set Supabase Anon Key
netlify env:set PUBLIC_SUPABASE_ANON_KEY "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"
```

Or set them in the Netlify dashboard:
1. Go to Site Settings → Environment Variables
2. Add:
   - `PUBLIC_SUPABASE_URL` = `https://haimjeaetrsaauitrhfy.supabase.co`
   - `PUBLIC_SUPABASE_ANON_KEY` = `sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2`

### **Step 5: Deploy!** (3 minutes)

```bash
netlify deploy --prod
```

This will:
1. Build your site
2. Upload to Netlify
3. Give you a live URL!

---

## 🎉 Your Site Will Be Live!

You'll get a URL like:
```
https://tstr-site.netlify.app
```

Or your custom domain if configured.

---

## 🔄 Setup Auto-Rebuild on Data Updates

### **Step 6: Get Build Hook** (2 minutes)

1. Go to Netlify Dashboard → Site Settings → Build & Deploy → Build Hooks
2. Click "Add build hook"
3. Name: `Supabase Data Update`
4. Branch: `main` (or your default branch)
5. **Copy the webhook URL** (looks like: `https://api.netlify.com/build_hooks/...`)

### **Step 7: Create Supabase Webhook** (3 minutes)

1. Go to Supabase Dashboard: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
2. Navigate to: Database → Webhooks
3. Click "Enable Webhooks" (if not enabled)
4. Click "Create a new hook"
5. Configure:
   - **Name**: `Netlify Rebuild on Listings Update`
   - **Table**: `listings`
   - **Events**: Check `INSERT` and `UPDATE`
   - **Type**: `HTTP Request`
   - **Method**: `POST`
   - **URL**: Paste your Netlify build hook URL
6. Click "Create webhook"

---

## ✅ Test the Auto-Rebuild

### **Manual Test**:

```bash
# Trigger the Netlify build hook manually
curl -X POST -d {} https://api.netlify.com/build_hooks/YOUR-HOOK-ID
```

### **Automated Test** (wait for next scraper run):

1. Wait for cloud scraper to run (every 3 days)
2. Scraper adds new listing to Supabase
3. Supabase webhook triggers Netlify
4. Netlify rebuilds site (2-3 minutes)
5. New listing appears on website!

---

## 🎯 Deployment Checklist

After deployment, verify:

- [ ] Site is live and accessible
- [ ] Shows your 19 verified listings
- [ ] Stats show correct numbers
- [ ] All links work
- [ ] Environment variables set in Netlify
- [ ] Build hook created
- [ ] Supabase webhook configured
- [ ] Test manual rebuild works

---

## 📊 Expected Results

### **Before**:
```
❌ Site not accessible
❌ Data in Supabase but not visible
❌ Manual updates only
```

### **After**:
```
✅ Site live at https://tstr-site.netlify.app
✅ Shows all 19 verified listings
✅ Auto-rebuilds when scrapers add data (2-3 min)
✅ Always fresh and current
```

---

## 🔧 Troubleshooting

### **Build Fails**:
```bash
# Check build logs
netlify logs

# Test build locally first
npm run build
```

### **Environment Variables Not Working**:
```bash
# Verify they're set
netlify env:list

# Redeploy after setting
netlify deploy --prod
```

### **Listings Not Showing**:
1. Check Supabase connection in browser console
2. Verify environment variables are correct
3. Check that listings table has `website_verified = true`

---

## 💰 Costs

**Netlify Free Tier Includes**:
- 100 GB bandwidth/month
- 300 build minutes/month
- Continuous deployment
- HTTPS/SSL
- Custom domain support

**Your Usage**:
- ~90 builds/month (30 scrapes × 3 rebuilds)
- ~2 min/build = 180 min/month
- Well within free tier! ✅

---

## 🎉 Success!

Once deployed:
1. Your site will be live 24/7
2. Scrapers will update database every 3 days
3. Webhook will trigger rebuild
4. Site will show fresh data automatically
5. Zero manual work required!

---

**Ready? Run the commands above and you'll be live in 10 minutes!** 🚀
