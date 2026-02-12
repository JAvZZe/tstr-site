# TSTR.site Revenue & Development Plan

## Business Strategy Document

Here is your comprehensive business plan in markdown format:

```markdown
# TSTR.site Revenue Optimization & AI Protection Plan

## Executive Summary
B2B niche directory for testing service providers in high-margin industries. Focus on subscription revenue from providers while protecting proprietary data from AI crawlers.

## Revenue Model Tiers

### Tier 1: Immediate Revenue (0-30 Days)
#### 1.1 Provider Subscription Tiers
- **Free**: Name, 1-sentence description, general location only
- **Professional: $295/month**: Full profile, contact info, 3 case studies, basic analytics
- **Premium: $795/month**: Priority ranking, lead notifications, custom content, monthly reports
- **Enterprise: $2,500/month**: Category exclusivity, API feed, co-marketing, dedicated manager

#### 1.2 Pay-Per-Qualified-Lead
- Buyer submits screened RFQ form
- Screening criteria: Company email, >$5K budget, <12 month timeline
- Pricing: $45-$150 per lead ($250 for exclusive)
- Promotion: 3 months free leads with Premium subscription

### Tier 2: Scalable Revenue (30-90 Days)
#### 2.1 Verified & Tested Certification
- **Initial audit**: $2,500-$5,000 (equipment, certifications, insurance verification)
- **Annual renewal**: $1,200/year
- **Benefits**: Verified badge, filter option, +15% ranking boost

#### 2.2 RFP/RFQ Marketplace
- Buyer posting: Free basic, $500 featured
- Provider access: Premium subscribers get instant alerts
- Success fee: 3-5% of awarded contract value

#### 2.3 Market Intelligence Reports
- Aggregate directory data into industry reports
- Pricing: $750-$1,500 per report, $2,400/year subscription
- Custom research: $5,000-$15,000 per project

### Tier 3: Strategic Moat (90+ Days)
#### 3.1 Procurement Team Subscriptions
- $300/month per seat for buyer intelligence platform
- Access to verified database, RFP templates, market rates

#### 3.2 API for Procurement Software
- $500-$1,500/month per integration partner
- Returns only verified, non-sensitive summaries

#### 3.3 Sponsored Content
- Webinars: $3,000 per event
- Whitepapers: $5,000 sponsor fee
- Annual summit: $15,000 sponsor packages

## AI Crawler Protection

### Robots.txt Configuration
```
User-agent: *
Disallow: /provider-profile/
Disallow: /api/v1/providers/details
Disallow: /api/v1/leads/
Allow: /api/v1/providers/schema
Allow: /industry-reports/
Allow: /category/
```

### Dynamic Content Gating
- Public pages show: 3-line teasers only
- Subscriber pages show: Full contact info, certifications, equipment
- Force login for profile updates (creates freshness moat)

### Structured Data for AI
```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "TSTR Testing Provider Directory",
  "description": "Curated directory of verified testing service providers",
  "variableMeasured": "Provider count by category",
  "temporalCoverage": "2024-01-01/2025-01-01",
  "isAccessibleForFree": "false"
}
```

## 90-Day Implementation Roadmap

### Days 1-14: Foundation
- [ ] Implement Stripe payment flow
- [ ] Build subscription management dashboard
- [ ] Create "Profile Views" analytics tracking
- [ ] Implement contact-gating forms

### Days 15-30: Tier 1 Launch
- [ ] Migrate providers to Free tier structure
- [ ] Email campaign: "Upgrade to Professional - 1st month free"
- [ ] Launch PPL pilot with 5 top providers
- [ ] Set up lead screening form

### Days 31-60: Tier 2 Development
- [ ] Design "Verified" certification workflow
- [ ] Recruit first 10 providers for verification pilot
- [ ] Publish first Market Intelligence Report
- [ ] Launch RFP marketplace MVP (manual process)

### Days 61-90: Scale & Moat
- [ ] Automate verification audit scheduling
- [ ] Build API beta for procurement partners
- [ ] Host first sponsored webinar
- [ ] Implement provider update notification system

## Key Metrics & Targets
- **Break-even**: 10 Professional + 20 Premium subscribers = $18,850 MRR
- **Goal**: 126 Premium subscribers = $100K MRR
- **Market penetration**: 10-15% of North American testing providers
```

---

## CLI Execution Plan for AI Assistants

Here is the hallucination-proof, incremental development plan:

```markdown
# TSTR.site CLI Execution Plan

## Critical Rules for AI Assistants
1. **NEVER write more than one file before testing**
2. **ALWAYS verify the previous step works before proceeding**
3. **NEVER implement features not explicitly listed in current phase**
4. **ALWAYS create tests before moving to next feature**
5. **KEEP all credentials in .env file only**

---

## Phase 0: Project Setup & Verification

### Step 0.1: Create project structure
```bash
# Create this exact structure
mkdir -p tstr-site/{app,components,lib,tests,pages/api}
cd tstr-site
touch .env.local .gitignore README.md
```

### Step 0.2: Initialize Next.js with specific version
```bash
# Use exact versions to prevent dependency issues
npx create-next-app@14.0.4 . --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

### Step 0.3: Verify installation
```bash
# Run development server and confirm it starts
npm run dev
# Expected: Server runs on http://localhost:3000 without errors
```

### Step 0.4: Add core dependencies (one at a time)
```bash
# Install and test each dependency before next
npm install @stripe/stripe-js@2.2.0
npm install lucide-react@0.303.0
npm install @prisma/client@5.7.1
npm install next-auth@4.24.5

# Verify each installs without peer dependency warnings
```

**Verification command after each install:**
```bash
npm run build
# Expected: Build completes without errors
```

---

## Phase 1: Database Schema (DO NOT PROCEED UNTIL PHASE 0 VERIFIED)

### Step 1.1: Create Prisma schema file
**File:** `tstr-site/prisma/schema.prisma`

```prisma
// Content will be provided in next command
```

**AI: Generate only this file, then run:**
```bash
npx prisma generate
# Expected: Client generation successful
```

### Step 1.2: Create initial migration
```bash
# Run immediately after Step 1.1
npx prisma migrate dev --name init
# Expected: Migration created and applied
```

### Step 1.3: Seed minimal test data
**File:** `tstr-site/prisma/seed.ts`
```typescript
// Insert exactly 3 test providers, 1 test user
// No more, no less
```

**Run seed:**
```bash
npx prisma db seed
# Expected: "Seeding completed. 3 providers, 1 user created."
```

**Verification query:**
```bash
npx prisma studio
# Expected: Open browser, see exactly 3 providers in database
```

---

## Phase 2: Authentication (DO NOT PROCEED UNTIL PHASE 1 VERIFIED)

### Step 2.1: Create auth configuration
**File:** `tstr-site/lib/auth.ts`

```typescript
// Implement ONLY NextAuth.js basic config
// DO NOT add providers yet
// DO NOT add callbacks yet
```

### Step 2.2: Create API auth endpoint
**File:** `tstr-site/app/api/auth/[...nextauth]/route.ts`

```typescript
// Import and export auth config only
```

### Step 2.3: Test auth
**File:** `tstr-site/tests/auth.test.ts`
```typescript
// Test that /api/auth/signin returns 200
```

**Run test:**
```bash
npm test
# Expected: 1 test passes
```

**Manual verification:**
- Navigate to `/api/auth/signin`
- Expected: See NextAuth default sign-in page

---

## Phase 3: Provider Model & Free Tier (DO NOT PROCEED UNTIL PHASE 2 VERIFIED)

### Step 3.1: Create Provider TypeScript interface
**File:** `tstr-site/lib/types/provider.ts`
```typescript
// Define EXACTLY these fields:
// id, name, description, location, category, subscriptionTier
// NOTHING ELSE in this step
```

### Step 3.2: Create provider service functions
**File:** `tstr-site/lib/services/providerService.ts`
```typescript
// Implement ONLY 2 functions:
// getAllProviders() - returns public fields only
// getProviderById() - returns public fields only
```

### Step 3.3: Create public provider list page
**File:** `tstr-site/app/providers/page.tsx`
```typescript
// Display ONLY name, location, truncated description (100 chars)
// NO contact info
// NO filters yet
```

### Step 3.4: Verify data protection
**Manual test:**
1. Open browser dev tools
2. Check Network tab for API response
3. **Confirm**: Response does NOT include contact info, even in hidden fields

---

## Phase 4: Subscription Tiers (DO NOT PROCEED UNTIL PHASE 3 VERIFIED)

### Step 4.1: Create subscription enum
**File:** `tstr-site/lib/constants/subscriptions.ts`
```typescript
// Define: FREE, PROFESSIONAL, PREMIUM, ENTERPRISE
// Define prices: 0, 295, 795, 2500
```

### Step 4.2: Update Prisma schema (incremental)
**File:** `tstr-site/prisma/schema.prisma`
```diff
+ model Subscription {
+   id        String   @id @default(cuid())
+   userId    String
+   tier      String
+   status    String
+   createdAt DateTime @default(now())
+ }
```

```bash
# Run immediately after editing
npx prisma migrate dev --name add_subscriptions
```

### Step 4.3: Create Stripe products (CLI commands)
```bash
# Run these EXACT commands in sequence
stripe products create --name="Professional Tier" --type=service
# Save returned product ID as PROD_PROFESSIONAL

stripe prices create --product=$PROD_PROFESSIONAL --unit-amount=29500 --currency=usd --recurring=monthly

stripe products create --name="Premium Tier" --type=service
# Save as PROD_PREMIUM

stripe prices create --product=$PROD_PREMIUM --unit-amount=79500 --currency=usd --recurring=monthly
```

**Verify in Stripe dashboard before proceeding**

---

## Phase 5: Payment Integration (DO NOT PROCEED UNTIL PHASE 4 VERIFIED)

### Step 5.1: Create Stripe configuration
**File:** `tstr-site/lib/stripe.ts`
```typescript
// Initialize Stripe with publishable key ONLY
// Add comment: "// Secret key to be used in API routes only"
```

### Step 5.2: Create checkout session API endpoint
**File:** `tstr-site/app/api/checkout/route.ts`
```typescript
// Implement ONLY POST handler
// Accept: { tier: 'professional' | 'premium' }
// Return: { sessionId: string }
// NO OTHER LOGIC YET
```

### Step 5.3: Create checkout button component
**File:** `tstr-site/components/CheckoutButton.tsx`
```typescript
// Accept tier prop
// Call /api/checkout on click
// Redirect to Stripe
```

### Step 5.4: Test payment flow
**Manual verification:**
1. Click button for Professional tier
2. Expected: Redirects to Stripe test checkout
3. Use card `4242 4242 4242 4242`
4. Expected: Redirects back to success page

**Check Stripe dashboard:**
- Expected: Payment recorded in test mode
- If not visible, STOP and debug before proceeding

---

## Phase 6: Profile Gating (DO NOT PROCEED UNTIL PHASE 5 VERIFIED)

### Step 6.1: Add user authentication check
**File:** `tstr-site/app/providers/[id]/page.tsx`
```typescript
// Add: const session = await getServerSession()
// Add: if (!session) redirect('/auth/signin')
```

### Step 6.2: Create subscription check middleware
**File:** `tstr-site/middleware.ts`
```typescript
// Protect ONLY /providers/[id] routes
// Check for session.user.subscriptionTier
// Redirect FREE tier to /subscribe
```

### Step 6.3: Update provider detail query
**File:** `tstr-site/lib/services/providerService.ts`
```diff
+ export function getProviderDetails(id: string, tier: string) {
+   if (tier === 'FREE') return basicFields
+   if (tier === 'PROFESSIONAL') return basicFields + contact + caseStudies
+   // etc.
+ }
```

### Step 6.4: Verify gating works
**Test matrix:**
| User Type | Expected Access | Test Result |
|-----------|-----------------|-------------|
| Logged out | Redirect to signin | [ ] |
| Free tier | Sees 3-line teaser only | [ ] |
| Professional | Sees full profile | [ ] |

---

## Phase 7: Analytics & Lead Tracking (DO NOT PROCEED UNTIL PHASE 6 VERIFIED)

### Step 7.1: Create analytics table
**File:** `tstr-site/prisma/schema.prisma`
```diff
+ model Analytics {
+   id          String   @id @default(cuid())
+   providerId  String
+   views       Int      @default(0)
+   date        DateTime
+   unique
+ }
```

```bash
npx prisma migrate dev --name add_analytics
```

### Step 7.2: Create increment view API
**File:** `tstr-site/app/api/analytics/view/route.ts`
```typescript
// Accept: { providerId: string }
// Increment views counter
// Return: { success: true }
```

### Step 7.3: Add view tracker to provider page
**File:** `tstr-site/app/providers/[id]/page.tsx`
```typescript
// Add useEffect hook on mount
// POST to /api/analytics/view
```

### Step 7.4: Verify analytics
**Manual test:**
1. Refresh provider page 3 times
2. Check database: `select views from Analytics where providerId = 'x'`
3. Expected: views = 3

---

## Phase 8: AI Crawler Protection (DO NOT PROCEED UNTIL PHASE 7 VERIFIED)

### Step 8.1: Create robots.txt
**File:** `tstr-site/app/robots.ts`
```typescript
// Generate programmatically
// Disallow: /provider-profile/
// Allow: /category/
```

### Step 8.2: Add structured data to category pages
**File:** `tstr-site/app/categories/[slug]/page.tsx`
```typescript
// Add JSON-LD script tag
// Include ONLY aggregate counts, no individual provider data
```

### Step 8.3: Verify crawler behavior
**Test with curl:**
```bash
curl -A "GPTBot" http://localhost:3000/robots.txt
# Expected: Sees Disallow rules

curl http://localhost:3000/api/providers
# Expected: No provider contact data in response
```

---

## Phase 9: Verification Program (DO NOT PROCEED UNTIL PHASE 8 VERIFIED)

### Step 9.1: Create verification checklist model
**File:** `tstr-site/lib/constants/verification.ts`
```typescript
// Array of exactly 10 checklist items:
// - equipmentCalibration
// - technicianCertifications
// - insuranceLiability
// etc.
```

### Step 9.2: Create verification request flow
**File:** `tstr-site/app/verify/request/page.tsx`
```typescript
// Show checklist
// File upload for each item
// Submit button
```

### Step 9.3: Create admin review dashboard (minimal)
**File:** `tstr-site/app/admin/verify/page.tsx`
```typescript
// Protected by admin role
// List pending verifications
// Approve/Reject buttons
// NO OTHER FEATURES
```

---

## Phase 10: RFP Marketplace MVP

### Step 10.1: Create RFP submission form
**File:** `tstr-site/app/rfp/submit/page.tsx`
```typescript
// Fields: category, testType, budget, timeline, description
// Stores in database with status: 'pending'
```

### Step 10.2: Create manual lead distribution
**File:** `tstr-site/scripts/distributeLeads.js`
```typescript
// Query new RFPs
// Email to Premium subscribers manually
// Log distribution in database
```

**Run manually:**
```bash
node scripts/distributeLeads.js
# Expected: Email sent to 3 providers, database updated
```

**DO NOT automate this yet. Run manually for 30 days to refine process.**

---

## Ongoing Development Rules

### Daily Verification Commands
```bash
# Run these before starting work each day
npm run build
npm run lint
npm test
npx prisma studio
```

### Git Commit Rules
- Each commit = ONE phase step ONLY
- Commit message format: `phase-X-step-Y: description`
- Example: `phase-5-step-2: create checkout session API`

### Stop Conditions
**STOP IMMEDIATELY IF:**
- `npm run build` fails
- Test fails
- Stripe payment doesn't appear in dashboard
- Database query returns unexpected data

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass
- [ ] Stripe in live mode with correct product IDs
- [ ] Database migrated in production
- [ ] `robots.txt` configured for production
- [ ] All environment variables set in Vercel/Netlify

### First Deployment
Deploy ONLY Phase 0-3 initially:
- Public provider list
- Free tier only
- No authentication

Verify in production for 24 hours before deploying Phase 4-5 (payments).

---

## Support Protocol

If you encounter errors:
1. Run `git status` to check what changed
2. Run `npm run build` to see exact error
3. Check database: `npx prisma studio`
4. Revert to last working commit if needed: `git reset --hard HEAD~1`
5. Ask human developer for help if error persists >30 minutes

**DO NOT guess. DO NOT skip verification steps.**
```

---

**IMPORTANT NOTE FOR CLI USAGE:**
- This plan is designed for **human developers using AI CLI assistants** as tools, not for unsupervised AI execution
- Each step includes specific verification commands that must be run and confirmed before proceeding
- If you are using Kimi CLI or Claude CLI, **copy and execute one step at a time** and wait for confirmation before proceeding
- Never execute multiple steps in a single command chain
- Always review generated code before moving to the next step
- The `.md` files themselves are documentation—store them in your project root as `business-plan.md` and `execution-plan.md`
