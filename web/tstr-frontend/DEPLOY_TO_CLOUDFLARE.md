# 🚀 Deploy TSTR.site to Cloudflare Pages

**Time**: ~5 minutes
**Cost**: FREE (Cloudflare Pages free tier)

---

## ✅ Current Status

- ✅ **Site Live**: https://tstr.site
- ✅ **GitHub Connected**: `JAvZZe/tstr-site` → Auto-deploys on push
- ✅ **Framework**: Astro with Cloudflare adapter (SSR)
- ✅ **Database**: Supabase integration working
- ✅ **Listings**: 127 verified labs displayed

---

## 📋 Deployment Configuration

### **Cloudflare Pages Settings**

| Setting | Value |
|---------|-------|
| **Project Name** | `tstr-site` |
| **GitHub Repo** | `JAvZZe/tstr-site` |
| **Production Branch** | `main` |
| **Framework Preset** | `Astro` |
| **Build Command** | `npm run build` |
| **Build Output Directory** | `dist` |
| **Root Directory** | `web/tstr-frontend` |
| **Node Version** | `18` |

### **Environment Variables** (CRITICAL)

Set in Cloudflare Dashboard → Pages → tstr-site → Settings → Environment variables:

| Variable | Value |
|----------|-------|
| `PUBLIC_SUPABASE_URL` | `https://haimjeaetrsaauitrhfy.supabase.co` |
| `PUBLIC_SUPABASE_ANON_KEY` | `sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO` |

---

## 🔄 Auto-Deployment Status

- ✅ **GitHub Push**: Triggers Cloudflare build (~1-2 minutes)
- ✅ **Build Success**: Deploys to https://tstr.site
- ✅ **Data Fresh**: Shows latest 127 listings from Supabase

```bash
# Set Supabase URL
netlify env:set PUBLIC_SUPABASE_URL "https://haimjeaetrsaauitrhfy.supabase.co"

# Set Supabase Anon Key
netlify env:set PUBLIC_SUPABASE_ANON_KEY "sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO"
```

Or set them in the Netlify dashboard:
1. Go to Site Settings → Environment Variables
2. Add:
   - `PUBLIC_SUPABASE_URL` = `https://haimjeaetrsaauitrhfy.supabase.co`
    - `PUBLIC_SUPABASE_ANON_KEY` = `sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO`

### **Step 5: Deploy!** (3 minutes)

---

## 🛠️ Troubleshooting CI/CD Issues

If GitHub pushes don't trigger Cloudflare builds:

### **Reconnect GitHub Repository**

1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Pages → tstr-site → Settings → Builds & deployments
3. Click **Edit configuration** or **Reconnect**
4. Select repository: `JAvZZe/tstr-site`
5. Branch: `main`
6. Save changes

### **Manual Build Trigger**

1. Cloudflare Dashboard → Pages → tstr-site → Deployments
2. Click **Create deployment**
3. Branch: `main`
4. Click **Save and Deploy**

---

## 🔄 Setup Auto-Rebuild After Scraper Runs

### **Create Cloudflare Build Hook**

1. Cloudflare Pages → tstr-site → Settings → Builds & deployments
2. Scroll to **Build hooks**
3. Click **Create build hook**
4. Name: `Supabase Data Update`
5. Branch: `main`
6. **Copy the webhook URL**

### **Create Supabase Webhook**

1. Supabase Dashboard → Project → Database → Webhooks
2. Click **Create webhook**
3. Configure:
   - **Name**: `Trigger Cloudflare Rebuild`
   - **Table**: `listings`
   - **Events**: INSERT, UPDATE
   - **Type**: HTTP Request
   - **Method**: POST
   - **URL**: [Cloudflare build hook URL]
4. Click **Create**

**Result**: Oracle scraper updates → Supabase webhook → Cloudflare rebuild → Site shows new data automatically.

---

## ✅ Test the Auto-Rebuild

### **Manual Test**:

```bash
# Trigger the Cloudflare build hook manually
curl -X POST -d {} https://api.cloudflare.com/YOUR-HOOK-ID
```

### **Automated Test** (wait for next scraper run):

1. Wait for Oracle scraper to run (daily at 2 AM GMT)
2. Scraper adds new listing to Supabase
3. Supabase webhook triggers Cloudflare
4. Cloudflare rebuilds site (2-3 minutes)
5. New listing appears on website!

---

## ✅ Deployment Checklist

After deployment, verify:

- [x] Site is live at https://tstr.site
- [x] Shows 127 verified listings
- [x] Stats show correct numbers
- [x] All links work
- [x] Environment variables set in Cloudflare Pages
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
