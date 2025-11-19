# Google AdSense Setup Guide for TSTR Hub

**Created:** 2025-10-29
**Agent:** Claude Code (Sonnet 4.5) - avztest8@gmail.com
**Purpose:** Apply for and integrate Google AdSense on tstr.site

---

## Why Google AdSense?

✅ **No minimum traffic** - Can apply immediately
✅ **Excellent B2B targeting** - Auto-shows lab equipment, testing services, industrial ads
✅ **68% revenue share** - Industry standard
✅ **PCI compliant** - No payment handling on your end
✅ **Auto-optimizes** - Machine learning finds best ad placements
✅ **Free to use** - No upfront costs

**Expected Revenue:**
- Current traffic (~1k visitors/month): $6-20/month
- At 10k visitors/month: $60-150/month
- At 50k visitors/month: $300-700/month

---

## Prerequisites

Before applying, ensure:
- ✅ Site is live and publicly accessible (tstr.site ✓)
- ✅ Has original, quality content (127 listings ✓)
- ✅ Has privacy policy (❌ NEED TO ADD)
- ✅ Domain is older than 6 months (verify age)
- ✅ Site has navigation and multiple pages (✓ home + submit)

**CRITICAL:** Need to add Privacy Policy page before applying!

---

## Step 1: Create Privacy Policy Page

**Why Required:** Google requires transparency about data collection.

**Quick Template:**
```markdown
# Privacy Policy - TSTR Hub

**Effective Date:** [Date]

## Information We Collect
TSTR Hub collects:
- Business contact information submitted via forms
- Analytics data (Google Analytics)
- Advertising data (Google AdSense)

## How We Use Information
- Display laboratory listings in our directory
- Improve site functionality
- Show relevant advertisements

## Third-Party Services
We use:
- Google AdSense for advertising
- Google Analytics for site analytics
- Supabase for data storage

## Cookies
We use cookies for:
- Site functionality
- Analytics
- Advertising personalization

## Contact
Email: [your-email]

## GDPR Compliance
Users in EU have the right to:
- Access their data
- Request deletion
- Opt-out of advertising cookies
```

**Action:** Create `/home/al/tstr-site-working/web/tstr-frontend/src/pages/privacy.astro` with this content (formatted).

---

## Step 2: Apply for Google AdSense

### 2.1 Create/Login to Google Account

**Recommended:** Use tstr.site1@gmail.com (same as Supabase account for consistency)

**URL:** https://www.google.com/adsense/start/

### 2.2 Start Application

1. Click "Sign Up Now"
2. Enter:
   - **Website URL:** https://tstr.site (NOT www.tstr.site)
   - **Email:** tstr.site1@gmail.com
   - **Country:** [Your country]
3. Accept Terms of Service

### 2.3 Connect Your Site

Google will provide a verification code:

```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
     crossorigin="anonymous"></script>
```

**Where to add:** In the `<head>` section of your site.

**File location:** `/home/al/tstr-site-working/web/tstr-frontend/src/pages/index.astro` (and all other pages)

**Better approach:** Create a layout component to avoid repeating code.

### 2.4 Wait for Approval

- **Typical wait time:** 1-3 days (sometimes up to 2 weeks)
- **What they check:**
  - Site has quality content
  - Privacy policy exists
  - No prohibited content (adult, drugs, weapons, etc.)
  - Site is navigable and functional
  - Sufficient content volume

**Common rejection reasons:**
- ❌ Insufficient content (need 20+ pages ideally)
- ❌ No privacy policy
- ❌ Site under construction
- ❌ Duplicate content
- ❌ Domain too new (< 6 months)

**If rejected:** Fix issues, wait 2 weeks, reapply.

---

## Step 3: Ad Placement Strategy

Once approved, place ads strategically:

### Recommended Placements:

#### 1. Between Listings (Every 10th listing)
**Why:** Native, doesn't interrupt user flow
**Format:** 728×90 (Leaderboard) or Responsive
**Expected RPM:** $2-4

#### 2. Sidebar (if adding sidebar layout)
**Why:** Always visible, doesn't block content
**Format:** 300×250 (Medium Rectangle) or 300×600 (Half Page)
**Expected RPM:** $3-6

#### 3. Below Header (Optional)
**Why:** High visibility
**Format:** 728×90 (Leaderboard)
**Expected RPM:** $1-3
**Warning:** Can be annoying, test user feedback

#### 4. In-Feed Native Ads
**Why:** Blends with listings
**Format:** Native (Custom)
**Expected RPM:** $4-8 (best performing)

**AVOID:**
- ❌ Popups/Interstitials (violates policy, annoys users)
- ❌ More than 3 ads above the fold
- ❌ Ads that hide content
- ❌ Auto-playing video ads

---

## Step 4: Implementation

### Option A: Manual Ad Code (Simple)

Add to `index.astro` between listings:

```astro
{listings.map((lab, index) => (
  <>
    <!-- Listing display -->
    <div class="listing-card">
      <h3>{lab.business_name}</h3>
      <!-- ... rest of listing ... -->
    </div>

    <!-- Ad every 10th listing -->
    {(index + 1) % 10 === 0 && (
      <div class="ad-container" style="margin: 2rem 0; text-align: center;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX"
             crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:block"
             data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
             data-ad-slot="YYYYYYYYYY"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
      </div>
    )}
  </>
))}
```

### Option B: Auto Ads (Easiest)

Google automatically places ads based on machine learning:

1. In AdSense dashboard → Ads → Overview
2. Enable "Auto ads"
3. Add single code snippet to `<head>`
4. Google handles placement optimization

**Pros:**
- Zero configuration
- Auto-optimizes over time
- Adapts to different screen sizes

**Cons:**
- Less control over placement
- Can be aggressive initially
- May not match site aesthetics

**Recommendation:** Start with Auto Ads, switch to manual once you understand what works.

---

## Step 5: Ad Settings & Optimization

### Block Unwanted Ad Categories

In AdSense dashboard:
1. Go to **Blocking controls**
2. Block categories:
   - Sensitive categories (e.g., dating, politics, religion)
   - Competitors (if any)
   - Low-quality advertisers

3. **Allow categories:**
   - Business & Industrial
   - Science & Technology
   - Laboratory Equipment
   - Testing Services
   - B2B Services

### Ad Review Center

- Manually review and block specific ads
- Report policy violations
- Improve user experience

### Performance Optimization

**Track metrics:**
- **RPM** (Revenue per 1000 impressions): Target $2-6 for B2B
- **CTR** (Click-through rate): Target 0.5-2%
- **Fill rate**: Should be >90%

**Optimization tips:**
- Place ads "above the fold" (visible without scrolling)
- Use responsive ad units (adapt to screen size)
- A/B test placements (move ads, measure revenue)
- Remove low-performing ad units

---

## Revenue Expectations

### Month 1-3 (Current Traffic ~1k visitors/month):
- **Impressions:** 3,000-5,000/month
- **RPM:** $2-4
- **Revenue:** $6-20/month

### Month 4-6 (Growing to 10k visitors/month):
- **Impressions:** 30,000-50,000/month
- **RPM:** $3-5
- **Revenue:** $90-250/month

### Month 12+ (50k+ visitors/month):
- **Impressions:** 150,000-200,000/month
- **RPM:** $4-6
- **Revenue:** $600-1,200/month

**Plus:** Manual sponsorships can add $500-2,000/month on top of AdSense.

---

## Payment Setup

### Minimum Payout: $100

**Timeline to first payout:**
- At current traffic (~$15/month): ~7 months to reach $100
- At 10k visitors (~$150/month): First payout in month 1
- At 50k visitors (~$800/month): First payout in month 1

### Payment Methods:
- Wire transfer (most countries)
- Check by mail (slower)
- Western Union (some countries)

### Payment Schedule:
- Earnings finalized by month end
- Payment issued 21st of following month
- Example: October earnings paid November 21st

---

## Policy Compliance (CRITICAL)

**Violations can lead to account termination:**

### Prohibited:
- ❌ Clicking your own ads
- ❌ Asking users to click ads
- ❌ Placing ads on error pages
- ❌ Hiding ads behind pop-ups
- ❌ Generating artificial traffic
- ❌ Copyrighted content without permission

### Required:
- ✅ Privacy policy clearly visible
- ✅ Clear navigation
- ✅ Original content
- ✅ Accessible to all users
- ✅ Mobile-friendly design

**If account banned:**
- Very hard to appeal
- Usually permanent
- Cannot create new account
- **Prevention is critical**

---

## Alternative: Manual Sponsorships (Higher Revenue)

Once traffic grows (10k+ visitors/month), approach direct sponsors:

### Target Sponsors:
- Lab equipment manufacturers (Thermo Fisher, Agilent, etc.)
- Testing consumables suppliers
- Software for labs (LIMS systems)
- Industry associations

### Pricing:
- **Banner ad (300×250):** $500-1,000/month
- **Header banner (728×90):** $1,000-2,000/month
- **Sponsored listing (featured):** $500/month
- **Newsletter sponsorship:** $300-500 per send

### Pitch Template:
```
Subject: Advertising Opportunity - TSTR Hub Laboratory Directory

Hi [Name],

TSTR Hub is a B2B directory connecting testing laboratories with industrial clients in Oil & Gas, Pharma, Biotech, and Environmental sectors.

Our audience:
- 10,000 monthly visitors
- Laboratory managers and procurement professionals
- Global reach with focus on [regions]

We offer:
- Banner advertising (multiple formats)
- Featured listings
- Newsletter sponsorships

Would you be interested in discussing advertising opportunities?

Best regards,
[Your name]
```

**Expected response rate:** 5-10% (cold outreach)

**Pro tip:** Once you have 50k+ visitors/month, use platforms like BuySellAds or Carbon Ads for automated sponsorship sales.

---

## Next Steps

1. **Create privacy policy page** (1 hour)
2. **Apply for Google AdSense** (30 minutes)
3. **Add AdSense verification code** (5 minutes)
4. **Wait for approval** (1-14 days)
5. **Implement Auto Ads** (5 minutes)
6. **Monitor performance** (ongoing)
7. **Optimize placements** (after 2-4 weeks of data)

---

## Checklist

- [ ] Privacy policy page created at /privacy
- [ ] Privacy policy link added to footer
- [ ] Applied for Google AdSense
- [ ] AdSense verification code added to site
- [ ] Awaiting approval (1-14 days)
- [ ] Once approved: Enable Auto Ads
- [ ] Once approved: Review ad settings
- [ ] Once approved: Block unwanted categories
- [ ] After 2 weeks: Review performance
- [ ] After 1 month: Optimize placements

---

**Agent:** Claude Code (Sonnet 4.5) - avztest8@gmail.com
**File Location:** /home/al/AI PROJECTS SPACE/TSTR_ADSENSE_SETUP_GUIDE.md
