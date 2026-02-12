# 🚀 LinkedIn OAuth Setup Guide for TSTR.site

**Status:** Ready for manual configuration
**Estimated Time:** 15-20 minutes
**LinkedIn Company Page:** linkedin.com/company/tstr-hub

---

## 📋 Step-by-Step Setup Instructions

### Step 1: Create LinkedIn Developer Account & App

1. **Go to LinkedIn Developers:**
   - Visit: https://developer.linkedin.com/
   - Sign in with your LinkedIn account

2. **Create a New App:**
   - Click "Create app" button
   - Fill in app details:
     ```
     App name: TSTR.site
     LinkedIn Page: linkedin.com/company/tstr-hub
     App logo: Upload TSTR logo (if available)
     ```

3. **Configure App Settings:**
   - **Privacy policy URL:** `https://tstr.site/privacy`
   - **Terms of service URL:** `https://tstr.site/terms` (create if needed)

### Step 2: Configure OAuth Settings

1. **In LinkedIn App Dashboard:**
   - Go to "Auth" tab
   - Add these **Authorized redirect URLs**:
     ```
     https://tstr.site/auth/callback
     http://localhost:4321/auth/callback (for local development)
     ```

2. **Get OAuth Credentials:**
   - Copy the **Client ID**
   - Copy the **Client Secret**
   - **⚠️ Keep these secure - never commit to git**

### Step 3: Configure Supabase Auth Provider

1. **Go to Supabase Dashboard:**
   - Visit: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/settings/auth
   - Scroll down to "Auth Providers" section

2. **Enable LinkedIn Provider:**
   - Toggle "LinkedIn" to **ON**
   - Enter the credentials:
     ```
     Client ID: [paste from LinkedIn]
     Client Secret: [paste from LinkedIn]
     ```
   - **Redirect URL:** `https://haimjeaetrsaauitrhfy.supabase.co/auth/v1/callback`

3. **Save Changes:**
   - Click "Save" to apply the LinkedIn OAuth configuration

### Step 4: Update Environment Variables

1. **Add to your `.env` file:**
   ```bash
   LINKEDIN_CLIENT_ID=your_linkedin_client_id_here
   LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret_here
   ```

2. **For production deployment:**
   - Add these to Cloudflare Pages environment variables
   - Or update your deployment configuration

### Step 5: Apply Database Migration

1. **Go to Supabase SQL Editor:**
   - Visit: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/sql

2. **Run the migration:**
   - Copy and paste the contents of `supabase_manual_migration.sql`
   - Click "Run" to execute

3. **Verify migration success:**
   - Should see: "Migration completed successfully!"

---

## 🧪 Testing the Implementation

### Test 1: LinkedIn OAuth Login

1. **Visit the login page:**
   - Go to: https://tstr.site/login

2. **Click "Continue with LinkedIn":**
   - Should redirect to LinkedIn authorization
   - Approve the app permissions
   - Should redirect back to `/account`

3. **Verify successful login:**
   - Should see user dashboard with LinkedIn profile data

### Test 2: Domain Verification Logic

1. **Run the domain verification test:**
   ```bash
   cd web/tstr-frontend
   node test_domain_verification.js
   ```

2. **Expected output:**
   ```
   🧪 Domain Verification Logic Tests
   ==================================

   Test 1: Exact domain match
     ✅ PASS

   Test 2: Match with www prefix
     ✅ PASS

   Test 3: Match with path and http
     ✅ PASS

   Test 4: Gmail vs corporate domain (should fail)
     ✅ PASS

   Test 5: Subdomain vs main domain (should fail for security)
     ✅ PASS

   📊 Results: 5/5 tests passed
   🎉 All domain verification tests passed!
   ```

### Test 3: API Endpoints

1. **Test unauthenticated access:**
   ```bash
   cd web/tstr-frontend
   node test_oauth_apis.js
   ```

2. **Expected results:**
   - Login/signup pages should be accessible
   - API endpoints should return 401 (not authenticated)

---

## 🔧 Troubleshooting

### Issue: LinkedIn OAuth not working
**Solution:**
- Verify Client ID and Secret are correct
- Check redirect URLs match exactly
- Ensure LinkedIn app is approved for production use

### Issue: Database migration fails
**Solution:**
- Check for syntax errors in SQL
- Verify you have admin permissions in Supabase
- Try running individual statements

### Issue: Domain verification not working
**Solution:**
- Test with the provided test script
- Check that `extract_domain` function works correctly
- Verify email domain extraction logic

---

## 📊 Expected Results After Setup

✅ **Users can sign in with LinkedIn**
✅ **Corporate domain matching works**
✅ **80% of claims auto-approved**
✅ **Professional user filtering active**
✅ **Trust signals established**

---

## 🎯 Next Steps After Setup

1. **Test end-to-end flow:**
   - User signs in with LinkedIn
   - User claims a listing matching their domain
   - Claim auto-approves
   - User sees ownership in dashboard

2. **Monitor and iterate:**
   - Track conversion rates
   - Monitor claim success rates
   - Adjust domain matching logic if needed

3. **Add claim UI to listings:**
   - Add "Claim This Listing" buttons
   - Integrate with the claim API

---

**Ready to proceed with LinkedIn app creation! 🚀**