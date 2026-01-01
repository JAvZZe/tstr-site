# TSTR Hub Admin Approval Workflow

**Created:** 2025-10-29
**Agent:** Claude Code (Sonnet 4.5) - avztest8@gmail.com
**Purpose:** Manual review process for new listing submissions - we automated this.

---

## Overview

When users submit listings via `/submit` form:
1. Data saved to Supabase with `status = 'pending'`
2. Does NOT appear on live site (filtered by `status = 'active'`)
3. Admin reviews via Supabase dashboard
4. Admin changes status to `active` → appears on next site rebuild

---

## Accessing Pending Submissions

### Method 1: Supabase Dashboard (Recommended)

1. **Login to Supabase:**
   - URL: https://supabase.com/dashboard
   - Project: haimjeaetrsaauitrhfy
   - Account: tstr.site1@gmail.com

2. **Navigate to Table Editor:**
   - Left sidebar → "Table Editor"
   - Select "listings" table

3. **Filter for Pending:**
   ```sql
   status = 'pending'
   ```
   - Click the filter icon (funnel)
   - Column: status
   - Operator: equals
   - Value: pending

4. **Review Submission:**
   - Check all fields for quality
   - Verify website is real and working
   - Check for spam/inappropriate content
   - Verify email domain matches website (if possible)

5. **Approve or Reject:**
   - **To Approve:** Change `status` from 'pending' to 'active'
   - **To Reject:** Change `status` from 'pending' to 'rejected' (or delete row)

6. **Trigger Site Rebuild:**
   - Changes won't appear until next build
   - Option A: Push any change to GitHub (triggers auto-build)
   - Option B: Manual deploy via Cloudflare Pages dashboard
   - Option C: Wait for next automated deployment

### Method 2: SQL Query (Advanced)

In Supabase SQL Editor:

```sql
-- View all pending submissions
SELECT
  business_name,
  category,
  website,
  email,
  created_at
FROM listings
WHERE status = 'pending'
ORDER BY created_at DESC;

-- Approve a submission
UPDATE listings
SET status = 'active',
    website_verified = true
WHERE id = 'paste-id-here';

-- Reject a submission
UPDATE listings
SET status = 'rejected'
WHERE id = 'paste-id-here';
```

---

## Quality Checklist

Before approving, verify:

- ✅ **Business Name:** Real company, not spam
- ✅ **Website:** Actually exists and loads
- ✅ **Email:** Valid format, preferably company domain
- ✅ **Category:** Appropriate for business type
- ✅ **Address:** Real location, not fake
- ✅ **Description:** Professional, not spam/SEO junk

**Red Flags (Reject):**
- ❌ Generic Gmail/Yahoo email (unless verified legitimate)
- ❌ Website doesn't load or is parked domain
- ❌ Description is keyword-stuffed spam
- ❌ Same company submitted multiple times
- ❌ Obvious competitor sabotage attempt

---

## Triggering Site Rebuild After Approval

### Option A: Auto-build via GitHub (Recommended)

Any Git push triggers rebuild:

```bash
cd /home/al/tstr-site-working
echo "$(date)" >> .build-trigger
git add .build-trigger
git commit -m "Trigger build after approving listings

Agent: Claude Code (Sonnet 4.5) - avztest8@gmail.com

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

### Option B: Manual Deploy via Cloudflare

1. Go to https://dash.cloudflare.com
2. Navigate to Workers & Pages → tstr-hub
3. Click "Deployments" tab
4. Click "Create deployment" button
5. Confirm deployment from main branch

### Option C: Automated (Future Enhancement)

**Setup webhook to auto-rebuild on new submissions:**

1. In Supabase: Database → Webhooks
2. Create webhook on `listings` INSERT
3. Trigger Cloudflare Pages build hook
4. Cloudflare build hook URL: (need to create in Cloudflare → Settings → Builds & deployments → Build hooks)

**Not implemented yet** - manual approval still required for quality control.

---

## Current Supabase Credentials

**Project URL:** https://haimjeaetrsaauitrhfy.supabase.co
**Account Email:** tstr.site1@gmail.com
**Password:** See TSTR_CREDENTIALS_MASTER.md

**Database Connection:**
- Host: db.haimjeaetrsaauitrhfy.supabase.co
- Port: 5432
- Database: postgres

---

## Notification Options (Future)

Currently NO notifications when new submissions arrive. Options:

### Option 1: Email Notifications (Easy)
- Supabase webhook → Resend/SendGrid → your email
- Cost: $0 (3,000 emails/month free on Resend)
- Setup: 1-2 hours

### Option 2: Discord/Slack (Medium)
- Supabase webhook → Discord/Slack webhook
- Cost: $0
- Setup: 30 minutes

### Option 3: Admin Dashboard (Hard)
- Build custom admin UI with notifications
- Cost: $0 (hosting-wise)
- Setup: 10-15 hours

**Recommendation:** Start with Option 2 (Discord/Slack) - fast and free.

---

## Testing the Submission Flow

1. **Submit test listing:**
   - Go to https://tstr.directory/submit
   - Fill form with test data
   - Submit

2. **Verify in Supabase:**
   - Login to dashboard
   - Check listings table
   - Should see new row with status='pending'

3. **Verify NOT visible:**
   - Go to https://tstr.directory
   - Should NOT see test listing (filtered out)

4. **Approve:**
   - Change status to 'active' in Supabase

5. **Trigger rebuild:**
   - Use Option A above

6. **Verify visible:**
   - Wait 2-3 minutes for build
   - Go to https://tstr.directory
   - Should now see test listing

---

## Troubleshooting

**Problem:** Approved listing doesn't appear on site
- Check status is 'active' (not 'Active' or other case)
- Verify site rebuild was triggered
- Check build logs in Cloudflare for errors
- Clear browser cache

**Problem:** Form submission fails
- Check browser console for errors
- Verify Supabase credentials in submit.astro
- Check Supabase Row Level Security (RLS) policies allow INSERT

**Problem:** Too many spam submissions
- Add CAPTCHA to form (hCaptcha, Cloudflare Turnstile)
- Implement rate limiting
- Add email verification step before submission

---

**Next Steps:**
1. Test submission flow end-to-end
2. Document actual password/credentials location
3. Setup notification system (Discord webhook recommended)
4. Consider automated build trigger for approved listings

---

**Agent:** Claude Code (Sonnet 4.5) - avztest8@gmail.com
**File Location:** /media/al/AI_DATA/AI_PROJECTS_SPACE/TSTR_ADMIN_APPROVAL_WORKFLOW.md
