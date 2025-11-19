# TSTR.site Monetization Implementation Plan

**Date**: 2025-11-19
**Status**: Review of existing + roadmap for payment integration

---

## Current State Analysis

### ✅ Already Implemented

**Authentication System**:
- `/signup` - User registration (sets subscription_tier to 'basic')
- `/login` - User login
- `/account` - User dashboard (shows current tier, links to upgrade)
- Supabase auth integrated and working

**Database Schema**:
- `user_profiles` table with `subscription_tier` field
- `payments` table exists (structure unknown)
- Subscription tiers referenced: 'basic', 'free', 'professional', 'premium'

**Profile Gating** (Partial):
- `/listing/[slug]` checks user subscription_tier
- Basic users see limited info, upgrade prompt shown
- References `/account/subscription` page (doesn't exist yet)

**AdSense Placeholder**:
- AdSense code present in index.astro
- Account: ca-pub-7003918988204966
- **Status**: Rejected (low content) - see CONTENT_GROWTH_STRATEGY.md

---

## ❌ Missing for Monetization

### Critical (P0 - Required for Revenue)

1. **Pricing Page** (`/pricing`)
   - Display 4 tiers: Free, Professional ($295/mo), Premium ($795/mo), Enterprise ($2,500/mo)
   - Feature comparison table
   - CTA buttons to signup/upgrade
   - **Blocker**: User's main request

2. **Stripe Payment Integration**
   - Stripe account setup
   - Product/price creation in Stripe
   - Checkout session API endpoint
   - Webhook handler for payment confirmation
   - Subscription management (upgrade/downgrade/cancel)

3. **Subscription Management Page** (`/account/subscription`)
   - Currently referenced but doesn't exist
   - Show current plan, usage, billing history
   - Upgrade/downgrade buttons
   - Cancel subscription option

4. **Claim Listing Flow**
   - Providers find their free listing
   - Click "Claim This Listing"
   - Authenticate + verify ownership (email domain match or phone verification)
   - Upgrade to paid tier to show contact info

### Important (P1 - Enhances Revenue)

5. **Provider Dashboard** (`/account/provider`)
   - Profile views analytics
   - Lead notifications
   - Edit listing info
   - Manage case studies (3 for Professional, unlimited for Premium)

6. **RFQ Submission Form** (`/rfq/submit`)
   - Buyers submit Request for Quote
   - Screening questions (budget, timeline, industry)
   - Distribute to Premium subscribers first
   - Pay-per-lead tracking

7. **Profile Gating Enforcement**
   - Free tier: Name, 1-sentence description, location (no contact)
   - Professional: Full profile + contact info + 3 case studies
   - Premium: Everything + priority ranking + featured badge
   - Enterprise: Category exclusivity

### Nice-to-Have (P2 - Future Revenue)

8. **Verification Badge System**
   - "Verified & Tested" certification
   - Upload compliance docs (ISO 17025, calibration certs, insurance)
   - Manual review process
   - Badge display on listings
   - Filter option for verified providers

9. **Market Intelligence Reports**
   - Generate reports from aggregated directory data
   - Sell to buyers ($750-$1,500 each)
   - AI-safe (no individual provider data)

10. **Procurement Team Subscriptions**
    - B2B2B model - sell to buyers, not just sellers
    - $300/month per seat
    - Advanced search, RFP templates, market rate data

---

## Pricing Page Design

### Page Structure: `/pricing`

**Hero Section**:
```
Find Your Perfect Plan
Choose the tier that matches your business needs.
All plans include listing in our directory. Upgrade anytime.
```

**Pricing Tiers** (4-column layout):

#### Tier 1: Free
**$0 / month**

**What You Get**:
- ✓ Basic listing in directory
- ✓ Company name
- ✓ 1-sentence description
- ✓ General location (city/state only)
- ✗ No contact information shown
- ✗ No analytics

**Limitations**:
- Potential customers cannot contact you directly
- Profile hidden behind "Request Quote" form
- No visibility into who's viewing your profile

**CTA**: "Start Free" → `/signup`

---

#### Tier 2: Professional ⭐ MOST POPULAR
**$295 / month**

**Everything in Free, plus**:
- ✓ Full company profile
- ✓ **Contact information displayed** (phone, email, website)
- ✓ Detailed capabilities & certifications
- ✓ Equipment list
- ✓ Up to 3 case studies
- ✓ Basic analytics (profile views, search appearances)
- ✓ Priority support

**Best For**:
- Testing labs seeking more visibility
- Companies with specialized capabilities
- Labs wanting direct inquiries

**CTA**: "Start 14-Day Trial" → `/signup?tier=professional`

---

#### Tier 3: Premium 🚀 BEST VALUE
**$795 / month**

**Everything in Professional, plus**:
- ✓ **Priority ranking** (top 3 positions in category searches)
- ✓ **Real-time lead notifications** (instant alerts for RFQs)
- ✓ Featured case study section
- ✓ Custom content placement on category pages
- ✓ Monthly performance reports
- ✓ Advanced analytics dashboard
- ✓ First access to qualified RFQ leads (48-hour exclusivity)

**Best For**:
- Market leaders in specific testing categories
- Labs with high customer acquisition targets
- Companies wanting consistent lead flow

**CTA**: "Schedule Demo" → `/contact?interest=premium`

---

#### Tier 4: Enterprise 💼 CUSTOM
**$2,500+ / month**

**Everything in Premium, plus**:
- ✓ **Category exclusivity** (only your lab shows for "X testing in Y region")
- ✓ Full analytics API
- ✓ White-label profile widget for your website
- ✓ Co-branded marketing campaigns
- ✓ Dedicated account manager
- ✓ Custom integration with your CRM
- ✓ Early access to new features

**Best For**:
- Industry-dominant testing providers
- Multi-location lab networks
- Companies requiring custom solutions

**CTA**: "Contact Sales" → `/contact?interest=enterprise`

---

### Feature Comparison Table

| Feature | Free | Professional | Premium | Enterprise |
|---------|------|--------------|---------|------------|
| Directory listing | ✓ | ✓ | ✓ | ✓ |
| Contact info shown | ✗ | ✓ | ✓ | ✓ |
| Case studies | 0 | 3 | Unlimited | Unlimited |
| Profile analytics | ✗ | Basic | Advanced | API Access |
| Search ranking | Standard | Standard | **Priority (Top 3)** | **Exclusive** |
| Lead notifications | ✗ | Email (daily) | **Real-time** | **Real-time + CRM** |
| RFQ access | ✗ | Standard | **48hr early access** | **Exclusive delivery** |
| Verification badge | Optional ($1,200/yr) | Optional ($1,200/yr) | **Included** | **Included** |
| Support | Community | Email | Priority | **Dedicated manager** |

---

### Pricing Page Copy - Key Selling Points

**Section: Why Upgrade?**

**For Free Tier Users**:
> "Your listing is live, but potential customers can't reach you. Upgrade to Professional to show your contact information and start receiving inquiries today."

**Social Proof**:
> "Join 47 testing laboratories already using TSTR Premium to generate qualified leads."

**Guarantee**:
> "14-day money-back guarantee. Cancel anytime, no contracts."

**Add-Ons** (Available to all paid tiers):
- **Verified & Tested Certification**: $2,500 initial + $1,200/year renewal
- **Featured Case Study**: $500/month (homepage placement)
- **Exclusive RFQ Lead**: $250 per exclusive lead delivery

---

### Technical Implementation Notes

**Stripe Products to Create**:
```bash
# Professional Tier
stripe products create \
  --name="TSTR Professional" \
  --description="Full profile with contact info and analytics"

stripe prices create \
  --product=<PRODUCT_ID> \
  --unit-amount=29500 \
  --currency=usd \
  --recurring[interval]=month

# Premium Tier
stripe products create \
  --name="TSTR Premium" \
  --description="Priority ranking + real-time leads"

stripe prices create \
  --product=<PRODUCT_ID> \
  --unit-amount=79500 \
  --currency=usd \
  --recurring[interval]=month

# Enterprise (custom pricing, handled via Stripe invoices)
```

**Subscription Tier Mapping**:
- Database: `user_profiles.subscription_tier`
- Values: `'free'`, `'professional'`, `'premium'`, `'enterprise'`
- Stripe metadata: Store `subscription_tier` in customer metadata

**Profile Gating Logic** (already partially implemented):
```typescript
// In listing/[slug].astro
const userTier = profile?.subscription_tier || 'free'

const contactInfoVisible = ['professional', 'premium', 'enterprise'].includes(userTier)
const analyticsAccess = ['professional', 'premium', 'enterprise'].includes(userTier)
const priorityRanking = ['premium', 'enterprise'].includes(userTier)
```

---

## Implementation Roadmap

### Phase 1: Pricing & Payment Foundation (Week 1)

**Day 1-2: Pricing Page**
- [ ] Create `/pricing.astro` with 4-tier layout
- [ ] Feature comparison table
- [ ] CTA buttons linking to signup with tier parameter
- [ ] Mobile-responsive design

**Day 3-4: Stripe Setup**
- [ ] Create Stripe account (or use existing)
- [ ] Create products for Professional & Premium
- [ ] Generate API keys (test + production)
- [ ] Add keys to `.env` file

**Day 5-7: Payment Integration**
- [ ] Create `/api/checkout.ts` - Stripe checkout session
- [ ] Create `/api/webhook.ts` - Stripe webhook handler
- [ ] Update `user_profiles.subscription_tier` on successful payment
- [ ] Create `/account/subscription.astro` - Manage subscription page
- [ ] Test payment flow end-to-end

**Deliverable**: Users can view pricing, click "Upgrade", pay via Stripe, subscription_tier updates

---

### Phase 2: Profile Gating & Claims (Week 2)

**Day 8-9: Enforce Profile Gating**
- [ ] Update listing pages to hide contact info for free tier
- [ ] Add "Claim This Listing" button for unclaimed listings
- [ ] Implement ownership verification (email domain or phone)

**Day 10-11: Provider Dashboard MVP**
- [ ] Create `/account/provider.astro`
- [ ] Show profile views count (read from analytics table)
- [ ] Edit listing button → edit form
- [ ] Add case study upload (max 3 for Professional)

**Day 12-14: Analytics Tracking**
- [ ] Implement profile view counter
- [ ] Track search appearances
- [ ] Daily email digest for Professional tier (profile views summary)

**Deliverable**: Free tier users see upgrade prompts, providers can claim listings and access analytics

---

### Phase 3: Lead Generation (Week 3-4)

**Day 15-17: RFQ Submission Form**
- [ ] Create `/rfq/submit.astro` - Buyer request form
- [ ] Fields: Test type, industry, budget, timeline, description
- [ ] Store in `rfq_submissions` table with status 'pending'
- [ ] Email notification to admin

**Day 18-20: Lead Distribution**
- [ ] Manual lead review process (screen for quality)
- [ ] Email Premium subscribers first (48hr exclusivity)
- [ ] Then email Professional subscribers
- [ ] Track lead delivery in `lead_distributions` table

**Day 21-28: Lead Notifications**
- [ ] Real-time email alerts for Premium tier (new RFQ posted)
- [ ] Weekly digest for Professional tier
- [ ] Lead analytics in provider dashboard

**Deliverable**: Buyers can submit RFQs, Premium users get instant alerts, lead flow established

---

### Phase 4: Verification & Trust (Week 5-6)

**Day 29-35: Verification Program**
- [ ] Create verification request form (upload certifications)
- [ ] Admin review dashboard (`/admin/verify`)
- [ ] Approve/reject workflow
- [ ] Add "Verified" badge to listings
- [ ] Filter option: "Show verified providers only"

**Day 36-42: Payment for Verification**
- [ ] Stripe product: Verification audit ($2,500)
- [ ] Annual renewal reminder + payment ($1,200)
- [ ] Verification status in provider dashboard

**Deliverable**: Providers can pay for verification, verified badge displays, trust signal established

---

### Phase 5: Advanced Features (Week 7-8)

**Day 43-49: Market Intelligence**
- [ ] Aggregate stats page (e.g., "47 labs in aerospace NDT")
- [ ] Trend reports (RFQ volume by category)
- [ ] Downloadable PDF reports ($750 each)
- [ ] Stripe product for report purchases

**Day 50-56: Enterprise Features**
- [ ] API endpoint for provider data (authenticated)
- [ ] Category exclusivity logic (hide competitors if Enterprise tier)
- [ ] White-label widget (iframe embed for provider websites)
- [ ] Custom CRM integration (Zapier or direct API)

**Deliverable**: Full feature parity with revenue plan, all tiers operational

---

## Database Schema Requirements

### New Tables Needed

**`subscriptions`**:
```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES user_profiles(id),
  stripe_subscription_id TEXT UNIQUE,
  stripe_customer_id TEXT,
  tier TEXT CHECK (tier IN ('free', 'professional', 'premium', 'enterprise')),
  status TEXT CHECK (status IN ('active', 'canceled', 'past_due', 'trialing')),
  current_period_start TIMESTAMPTZ,
  current_period_end TIMESTAMPTZ,
  cancel_at_period_end BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

**`rfq_submissions`**:
```sql
CREATE TABLE rfq_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  buyer_name TEXT,
  buyer_email TEXT,
  company TEXT,
  test_type TEXT,
  industry TEXT,
  budget_range TEXT,
  timeline TEXT,
  description TEXT,
  status TEXT DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT now()
);
```

**`lead_distributions`**:
```sql
CREATE TABLE lead_distributions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rfq_id UUID REFERENCES rfq_submissions(id),
  provider_id UUID REFERENCES listings(id),
  distributed_at TIMESTAMPTZ DEFAULT now(),
  opened BOOLEAN DEFAULT false,
  responded BOOLEAN DEFAULT false,
  exclusive BOOLEAN DEFAULT false,
  price_paid DECIMAL(10,2) -- for tracking PPL revenue
);
```

**`verification_requests`**:
```sql
CREATE TABLE verification_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES listings(id),
  requester_id UUID REFERENCES user_profiles(id),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  documents_urls TEXT[], -- Array of uploaded doc URLs
  admin_notes TEXT,
  payment_id UUID REFERENCES payments(id),
  verified_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ, -- Annual renewal date
  created_at TIMESTAMPTZ DEFAULT now()
);
```

**Update `listings` table**:
```sql
ALTER TABLE listings ADD COLUMN claimed BOOLEAN DEFAULT false;
ALTER TABLE listings ADD COLUMN claimed_by UUID REFERENCES user_profiles(id);
ALTER TABLE listings ADD COLUMN verified BOOLEAN DEFAULT false;
ALTER TABLE listings ADD COLUMN verification_id UUID REFERENCES verification_requests(id);
```

**Update `user_profiles` table** (if needed):
```sql
-- Check if subscription_tier already exists
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS subscription_tier TEXT DEFAULT 'free';
ALTER TABLE user_profiles ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT;
```

---

## Revenue Projections

### Conservative Scenario (Year 1)

**Assumptions**:
- 178 current listings
- 10% conversion to paid tiers
- Mix: 60% Professional, 30% Premium, 10% Enterprise

**Monthly Recurring Revenue (MRR)**:
- Professional: 10 × $295 = $2,950
- Premium: 5 × $795 = $3,975
- Enterprise: 2 × $2,500 = $5,000
- **Total MRR**: $11,925

**Annual Recurring Revenue (ARR)**: $143,100

**Add-On Revenue**:
- Verification: 10 providers × $2,500 = $25,000 (one-time) + $12,000/year renewal
- Pay-per-lead: 50 leads/month × $100 avg = $5,000/mo = $60,000/year
- Market reports: 10 reports/year × $1,000 = $10,000

**Total Year 1 Revenue**: ~$250,000

---

### Aggressive Scenario (Year 2)

**Growth Assumptions**:
- 500 total listings (content growth strategy executed)
- 20% conversion to paid tiers
- Improved mix: 50% Professional, 40% Premium, 10% Enterprise

**MRR**:
- Professional: 50 × $295 = $14,750
- Premium: 40 × $795 = $31,800
- Enterprise: 10 × $2,500 = $25,000
- **Total MRR**: $71,550

**ARR**: $858,600

**Add-On Revenue**:
- Verification: 30 providers × $2,500 + renewals = $75,000
- Pay-per-lead: 200 leads/month × $125 avg = $300,000/year
- Procurement subscriptions: 10 teams × 5 seats × $300 = $15,000/mo = $180,000/year

**Total Year 2 Revenue**: ~$1,413,600

**Path to $100K MRR**: 126 Premium subscribers OR mix of tiers = achievable in 12-18 months

---

## Risks & Mitigations

**Risk: Low conversion to paid tiers**
- Mitigation: Free trial (14 days), freemium model keeps users engaged
- Mitigation: Show ROI - 1 new client from TSTR = 10x subscription cost

**Risk: Stripe compliance/regulatory**
- Mitigation: Use Stripe Billing (handles SCA, tax, compliance)
- Mitigation: Proper terms of service + privacy policy

**Risk: Churn (cancellations)**
- Mitigation: Annual prepay discount (save 2 months)
- Mitigation: Lock-in via verification investment ($2,500 upfront)

**Risk: AdSense still rejected after content growth**
- Mitigation: Don't depend on AdSense - subscriptions are primary revenue
- Mitigation: Alternative: Direct ad sales to equipment manufacturers

---

## Next Immediate Actions

**This Week**:
1. ✅ Review this plan with user
2. [ ] Create `/pricing.astro` page with 4 tiers
3. [ ] Set up Stripe account (test mode)
4. [ ] Create Stripe products for Professional + Premium
5. [ ] Add Stripe keys to `.env`

**Next Week**:
- Implement checkout flow
- Build subscription management page
- Test end-to-end payment

**Checkpoint after 2 weeks**: First paid subscriber or pivot strategy

---

**Last Updated**: 2025-11-19
**Owner**: Claude + User
**Dependencies**: CONTENT_GROWTH_STRATEGY.md (for content volume), Revenue Development Plan.md (for pricing tiers)
