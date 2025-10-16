# SUPABASE SETUP GUIDE

## Step-by-Step Instructions

### 1. Access Supabase SQL Editor
1. Go to your Supabase project dashboard
2. Click **SQL Editor** in the left sidebar
3. Click **New Query**

### 2. Execute the Setup Script
1. Open the file: `SUPABASE_SETUP.sql`
2. Copy ALL contents (Ctrl+A, Ctrl+C)
3. Paste into Supabase SQL Editor
4. Click **RUN** (or press Ctrl/Cmd + Enter)

**Expected result**: "Success. No rows returned" message at bottom

### 3. Verify Tables Created
1. Click **Table Editor** in left sidebar
2. You should see these tables:
   - ✅ locations (with seed data: Global → USA → Texas → Houston, etc.)
   - ✅ categories (5 categories: Oil & Gas, Pharma, Biotech, etc.)
   - ✅ custom_fields (industry-specific fields)
   - ✅ listings (empty, ready for data)
   - ✅ listing_custom_fields
   - ✅ listing_images
   - ✅ payments
   - ✅ enquiries
   - ✅ search_logs
   - ✅ user_profiles

### 4. Check Seed Data
Click on `locations` table - you should see:
- Global (level: global)
- North America, Europe, Asia (level: region)
- United States, United Kingdom, Singapore (level: country)
- Texas, California, England (level: region within country)
- Houston, San Francisco, London, Singapore (level: city)

Click on `categories` table - you should see 5 categories ready to use.

### 5. Get Your API Keys
1. Click **Project Settings** (gear icon at bottom left)
2. Click **API** in settings menu
3. Copy these values (you'll need them):
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public key**: `eyJhbG...` (long string)
   - **service_role key**: `eyJhbG...` (long string, keep secret!)

### 6. Create Your Admin Account
1. Click **Authentication** in left sidebar
2. Click **Users**
3. Click **Add user** → Create new user
4. Enter your email and password
5. Copy the new user's UUID (you'll need it)

### 7. Make Yourself Admin
1. Go back to **SQL Editor**
2. Run this query (replace `YOUR_USER_ID` with the UUID you copied):

```sql
UPDATE user_profiles
SET role = 'admin'
WHERE id = 'YOUR_USER_ID';
```

### 8. Enable Realtime (Optional)
If you want live updates:
1. Go to **Database** → **Replication**
2. Enable replication for `listings` table

---

## What You've Created

✅ **12 database tables** with proper relationships  
✅ **Row Level Security** (users can only edit their own listings)  
✅ **5 testing categories** with custom fields  
✅ **Global location hierarchy** (ready for worldwide listings)  
✅ **Payment tracking system**  
✅ **Automated triggers** (auto-update timestamps, etc.)  
✅ **Full-text search** indexing

---

## Capacity Check

Your free tier limits:
- **Database size**: 500MB (holds ~25,000 listings)
- **Bandwidth**: 2GB/month (handles ~50,000 visitors)
- **Storage**: 1GB (for listing images)

---

## Common Issues & Solutions

**Error: "function uuid_generate_v4() does not exist"**
- Solution: The script includes `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";` at the top
- If still failing, run that line separately first

**Error: "permission denied"**
- Solution: You're using the anon key instead of service_role key
- Make sure you're running in SQL Editor (has admin privileges)

**No seed data appearing**
- Solution: Check for errors in the DO $$ blocks
- Run each INSERT statement separately to identify which failed

---

## Next Steps

Once setup complete:

1. ✅ Initialize Astro frontend project
2. ✅ Configure Supabase client with your API keys
3. ✅ Run scraper to populate first 100-500 listings
4. ✅ Deploy to Cloudflare Pages

Ready to proceed with frontend initialization?
