# 🚨 FIX CLOUDFLARE ENVIRONMENT VARIABLES - STEP BY STEP

**Time Required**: 5 minutes  
**Difficulty**: Easy  
**What This Fixes**: "Invalid API key" error on https://tstr.site

---

## 🎯 What You're Doing

Adding two Supabase API keys to Cloudflare so your website frontend can connect to the database.

---

## 📋 Step-by-Step Instructions

### Step 1: Open Cloudflare Dashboard

**Click this link** (or copy-paste into browser):
```
https://dash.cloudflare.com/93bc6b669b15a454adcba195b9209296/pages/view/tstr-site/settings/environment-variables
```

**You should see**:
- Cloudflare Pages dashboard
- Project: "tstr-site"
- Tab: "Settings"
- Section: "Environment variables"

---

### Step 2: Add First Variable (Supabase URL)

**Click the button**: `"Add variable"` (blue button on the right)

**A form will appear with two fields:**

**Field 1 - Variable name:**
```
PUBLIC_SUPABASE_URL
```
↑ Copy exactly as shown (case-sensitive, underscores included)

**Field 2 - Value:**
```
https://haimjeaetrsaauitrhfy.supabase.co
```
↑ Copy exactly as shown (entire URL)

**Environment**: Make sure "Production" is selected (it should be by default)

**Click**: The checkmark ✓ or "Save" button next to the fields

---

### Step 3: Add Second Variable (Supabase Public Key)

**Click the button again**: `"Add variable"`

**A new form will appear:**

**Field 1 - Variable name:**
```
PUBLIC_SUPABASE_ANON_KEY
```
↑ Copy exactly as shown (case-sensitive)

**Field 2 - Value:**
```
sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO
```
↑ Copy exactly as shown (entire key, starts with "sb_")

**Environment**: Make sure "Production" is selected

**Click**: The checkmark ✓ or "Save" button

---

### Step 4: Save Changes

**Scroll down** to the bottom of the page

**Click the big button**: `"Save"` or `"Save changes"`

---

### Step 5: Redeploy (CRITICAL)

**After clicking Save, you'll see a prompt:**
```
"These changes require a new deployment to take effect.
Would you like to redeploy now?"
```

**Click**: `"Redeploy"` or `"Create deployment"` (YES!)

**What happens now:**
- Cloudflare starts rebuilding your site
- Takes 2-5 minutes
- You'll see a progress indicator

---

### Step 6: Wait for Build to Complete

**Watch for**:
- Progress bar or spinner
- Status: "Building..." → "Deploying..." → "Success"
- Should take 2-5 minutes

**Do NOT close the browser** until you see "Success" or "Active"

---

### Step 7: Verify the Fix

**After deployment completes:**

1. Open a new browser tab
2. Go to: `https://tstr.site`
3. **Press Ctrl + Shift + R** (hard refresh, clears cache)

**You should now see**:
- ✅ No "Invalid API key" error
- ✅ Categories display
- ✅ Listings show up (20 listings)
- ✅ Numbers at top (Testing Categories, Global Locations, Verified Labs)

---

## ✅ Success Checklist

After completing all steps, you should have:

- [ ] Two environment variables added:
  - `PUBLIC_SUPABASE_URL`
  - `PUBLIC_SUPABASE_ANON_KEY`
- [ ] Clicked "Save"
- [ ] Clicked "Redeploy"
- [ ] Waited for build to complete (green "Success" status)
- [ ] Visited https://tstr.site and saw no errors
- [ ] Site displays categories and listings

---

## 🚨 Troubleshooting

### Problem: Can't find "Add variable" button
**Solution**: Scroll down on the Settings page, look for "Environment variables" section

### Problem: Variables not saving
**Solution**: Make sure you clicked the checkmark ✓ after entering each variable, THEN click the main "Save" button at bottom

### Problem: No "Redeploy" prompt appeared
**Solution**: 
1. Go to "Deployments" tab (top of page)
2. Find the latest deployment
3. Click the "..." menu
4. Select "Retry deployment"

### Problem: Build failed
**Solution**: 
1. Check if you copied the keys correctly (no extra spaces)
2. Variable names must match exactly (case-sensitive)
3. Try redeploying again

### Problem: Site still shows error after redeploy
**Solution**:
1. Wait 5 more minutes (DNS/CDN cache)
2. Hard refresh: Ctrl + Shift + R
3. Try incognito/private browser window
4. Clear browser cache completely

### Problem: Lost during the process
**Solution**: Take a screenshot of where you're stuck and I'll help navigate

---

## 📸 What You're Looking For (Visual Cues)

### Environment Variables Section:
```
Environment variables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Configure environment variables for use in your Pages Functions.

[Add variable] button (blue/gray button on right)

Variable name    Value           Environment
─────────────────────────────────────────────
(You should see your two variables here after adding)
```

### After Adding Both Variables:
```
Variable name              Value                          Environment
─────────────────────────────────────────────────────────────────────
PUBLIC_SUPABASE_URL        https://haimjeae...            Production
PUBLIC_SUPABASE_ANON_KEY   sb_publishable_EFS...         Production
```

---

## 🎯 Quick Copy-Paste Reference

**Variable 1 Name:**
```
PUBLIC_SUPABASE_URL
```

**Variable 1 Value:**
```
https://haimjeaetrsaauitrhfy.supabase.co
```

**Variable 2 Name:**
```
PUBLIC_SUPABASE_ANON_KEY
```

**Variable 2 Value:**
```
sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO
```

---

## ⏱️ Timeline

- **Step 1-4**: Add variables (2 minutes)
- **Step 5**: Click save and redeploy (30 seconds)
- **Step 6**: Wait for build (2-5 minutes)
- **Step 7**: Verify (1 minute)

**Total**: ~5-8 minutes

---

## 🎉 What Happens After This Works

Once the environment variables are set and the site redeploys:

1. **Frontend connects to Supabase** ✅
2. **Categories load from database** ✅
3. **20 listings display** ✅
4. **Search/filter works** ✅
5. **"Invalid API key" error gone** ✅

Then we can decide:
- Launch with 20 listings (MVP)
- OR import remaining 114 listings first

---

## 📞 Need Help?

**If stuck at any step:**
1. Take a screenshot
2. Note which step number you're on
3. Tell me what you see vs. what you expected

**Common questions:**
- "Where's the Add variable button?" → Scroll down to Environment variables section
- "Which environment?" → Production (should be selected by default)
- "Do I click Save after each variable?" → Click checkmark after EACH variable, then main Save at bottom
- "How long should I wait?" → 2-5 minutes for build, up to 10 minutes for full propagation

---

## ✅ YOU'RE READY

**Open this link now:**
```
https://dash.cloudflare.com/93bc6b669b15a454adcba195b9209296/pages/view/tstr-site/settings/environment-variables
```

**Follow Steps 1-7 above**

**Report back when:**
- ✅ Build shows "Success"
- ✅ You've verified https://tstr.site loads without errors

Good luck! 🚀
