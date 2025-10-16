# TSTR.SITE CUSTOM BUILD - STATUS & ACTION PLAN
**Updated: 10 October 2025**

---

## ✅ WHAT'S READY

### Infrastructure
- ✅ Supabase project created: `haimjeaetrsaauitrhfy`
- ✅ Access token configured
- ✅ Database schema designed (ARCHITECTURE.md)
- ✅ SQL setup script ready (SUPABASE_SETUP.sql)

### Architecture Decided
- ✅ **Frontend**: Astro + React + Tailwind
- ✅ **Backend**: Supabase (PostgreSQL + Auth + Storage)
- ✅ **Hosting**: Cloudflare Pages (free tier)
- ✅ **Payments**: Bank transfer → PayPal → Bitcoin → Stripe
- ✅ **Automation**: GitHub Actions + Python scrapers

### Existing Assets
- ✅ Google Maps API key ready
- ✅ Domain: tstr.site (currently pointing to WordPress VM)
- ✅ Python scraping scripts completed
- ✅ Sample data (8 listings CSV)

---

## 🚧 WHAT NEEDS TO BE DONE

### Phase 1: Supabase Database Setup (TODAY - 1 hour)

**Task 1.1: Execute Database Schema**
```bash
# Using Supabase dashboard or CLI
1. Go to: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
2. SQL Editor → New Query
3. Paste contents of SUPABASE_SETUP.sql
4. Execute
```

**Task 1.2: Create Seed Data**
- Categories: Oil & Gas, Pharma, Biotech, Environmental, Materials
- Locations: Global → Regions → Countries → Cities hierarchy
- Custom fields per category (ISO certifications, turnaround times, etc.)

**Task 1.3: Set Up Row Level Security**
- Public read access for active listings
- Authenticated users can manage own listings
- Admin role for manual verification

**Verification:**
- [ ] All tables created successfully
- [ ] Indexes applied
- [ ] RLS policies active
- [ ] Seed categories inserted
- [ ] Location hierarchy created

---

### Phase 2: Initialize Frontend Project (TODAY - 2 hours)

**Task 2.1: Create Astro Project**
```bash
cd C:\Users\alber\OneDrive\Documents\.WORK\
npm create astro@latest tstr-site-frontend

# Choose:
# - Template: Empty
# - TypeScript: Yes, strict
# - Install dependencies: Yes
# - Git: Yes (if not already)
```

**Task 2.2: Install Dependencies**
```bash
cd tstr-site-frontend
npm install @supabase/supabase-js
npm install @astrojs/react @astrojs/tailwind
npm install -D tailwindcss
npm install react react-dom
```

**Task 2.3: Configure Supabase Client**
Create `src/lib/supabase.ts`:
```typescript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL
const supabaseKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseKey)
```

**Task 2.4: Add Environment Variables**
Create `.env`:
```
PUBLIC_SUPABASE_URL=https://haimjeaetrsaauitrhfy.supabase.co
PUBLIC_SUPABASE_ANON_KEY=[Get from Supabase dashboard]
```

**Verification:**
- [ ] Astro project created
- [ ] Dependencies installed
- [ ] Supabase client configured
- [ ] Environment variables set
- [ ] Dev server runs: `npm run dev`

---

### Phase 3: Build Core Pages (TOMORROW - 4 hours)

**Task 3.1: Homepage** (`src/pages/index.astro`)
- Hero section with search bar
- Browse by category cards
- Featured listings carousel
- Recent listings grid
- Footer with categories + locations

**Task 3.2: Category Page** (`src/pages/[category]/index.astro`)
- Dynamic routing for each category
- Filter sidebar (location, custom fields)
- Listing grid with pagination
- SEO meta tags

**Task 3.3: Listing Detail Page** (`src/pages/listing/[slug].astro`)
- Business details
- Contact information
- Custom fields display
- Location map
- Enquiry form
- Related listings

**Task 3.4: Submit Listing Page** (`src/pages/submit.astro`)
- Multi-step form:
  1. Choose category
  2. Select location (cascading)
  3. Business details
  4. Custom fields (dynamic)
  5. Upload images
  6. Choose plan
  7. Payment instructions
- Requires authentication

**Verification:**
- [ ] All pages render correctly
- [ ] Data fetching from Supabase works
- [ ] Forms submit successfully
- [ ] Mobile responsive
- [ ] Fast page loads (<2s)

---

### Phase 4: Authentication & Dashboard (DAY 3 - 3 hours)

**Task 4.1: Implement Supabase Auth**
- Email/password signup
- Login/logout flow
- Password reset
- Protected routes

**Task 4.2: Owner Dashboard** (`src/pages/dashboard.astro`)
- My listings table
- Edit listing button
- View statistics (views, clicks)
- Payment history
- Upgrade to featured

**Task 4.3: Admin Panel** (`src/pages/admin/index.astro`)
- Pending listings queue
- Approve/reject buttons
- Payment verification
- Activate featured status

**Verification:**
- [ ] Users can sign up/login
- [ ] Dashboard shows user listings
- [ ] Admin can approve listings
- [ ] Payments can be verified

---

### Phase 5: Monetisation & Payments (DAY 4 - 2 hours)

**Task 5.1: Pricing Plans Component**
- Display 3 tiers: Free, Featured (£50/mo), Premium (£150/mo)
- "Upgrade" button
- Feature comparison table

**Task 5.2: Bank Transfer Instructions**
- Show bank details on upgrade
- Upload payment proof form
- Store in `payments` table
- Email admin notification

**Task 5.3: Payment Verification Flow**
- Admin reviews uploaded proofs
- Verify/reject buttons
- Auto-activate featured status
- Send confirmation email to user

**Task 5.4: Auto-Expiry System**
- Daily cron job (GitHub Actions)
- Check `featured_until` date
- Expire and send renewal reminder email

**Verification:**
- [ ] Upgrade flow works end-to-end
- [ ] Bank details display correctly
- [ ] Payment proofs upload successfully
- [ ] Admin can verify payments
- [ ] Featured status activates
- [ ] Auto-expiry works

---

### Phase 6: Content & Launch (DAY 5-7 - Ongoing)

**Task 6.1: Initial Data Import**
```bash
# Run enhanced scraper with Supabase
python scraper_v2.py

# Target: 200-500 seed listings across:
# - Houston (Oil & Gas)
# - Singapore (Oil & Gas)  
# - Basel (Pharma)
# - San Francisco (Biotech)
# - London (Environmental)
```

**Task 6.2: SEO Optimization**
- Meta descriptions for all pages
- Open Graph tags
- Schema.org LocalBusiness markup
- XML sitemap generation
- robots.txt

**Task 6.3: Deploy to Production**
```bash
# Connect GitHub to Cloudflare Pages
1. Push code to GitHub
2. Cloudflare Pages → Create Project
3. Connect repo: tstr-site-frontend
4. Build command: npm run build
5. Output dir: dist
6. Deploy
```

**Task 6.4: DNS Configuration**
- Point tstr.site A record to Cloudflare Pages IP
- Wait for DNS propagation (10-60 minutes)
- Verify HTTPS works

**Task 6.5: Final Testing**
- Test all user journeys
- Mobile testing (iOS + Android)
- Browser testing (Chrome, Safari, Firefox)
- Performance testing (Lighthouse score >90)

**Verification:**
- [ ] 200+ listings live
- [ ] SEO properly configured
- [ ] Site live on tstr.site
- [ ] HTTPS working
- [ ] All features tested
- [ ] Ready for public launch

---

## 📊 SUCCESS METRICS

### Week 1 Targets
- ✅ Database fully set up
- ✅ Frontend deployed to staging
- ✅ Core pages working
- ✅ Authentication functional

### Week 2 Targets
- 200+ seed listings imported
- Site live on tstr.site
- First 5 featured listing sales (£250 revenue)

### Month 1 Targets
- 500+ total listings
- 10 featured listings (£500/month recurring)
- 1,000 monthly visitors
- Google indexed (100+ pages)

---

## 💰 COST TRACKING

### Current Monthly Costs
- Supabase: **£0** (free tier)
- Cloudflare Pages: **£0** (free tier)
- Domain (tstr.site): **£10/year** = £0.83/month
- Google Maps API: **£0** (£200 credit/month)
- GitHub: **£0** (free tier)

**Total: £0.83/month**

### Break-Even
- 1 featured listing @ £50/month = profitable from day 1

### Upgrade Triggers
- Supabase Pro (£20/month): When >20,000 listings or >40,000 visitors/month
- Additional Google Maps credit: When >£200/month usage (unlikely)

---

## 🚀 IMMEDIATE NEXT STEPS (THIS WEEKEND)

### Saturday Morning (3 hours)
1. ✅ Review ARCHITECTURE.md thoroughly
2. Execute SUPABASE_SETUP.sql in Supabase dashboard
3. Create seed categories and locations
4. Verify database is working

### Saturday Afternoon (4 hours)
1. Initialize Astro project
2. Install all dependencies
3. Configure Supabase client
4. Build homepage skeleton
5. Test dev server

### Sunday (6 hours)
1. Build category page
2. Build listing detail page
3. Build submit form
4. Implement search functionality
5. Test end-to-end flow

### Monday (Optional - if time permits)
1. Deploy to Cloudflare Pages staging
2. Run first scraping session
3. Manual verification of scraped data
4. Share staging URL for feedback

---

## ❓ DECISION POINTS

### What happens to WordPress VM?
**Option A: Keep running** (£0/month on free tier)
- Use as staging/testing environment
- Fallback if custom build has issues

**Option B: Shut down**
- Free up Google Cloud quota
- Reduce complexity
- Can always recreate if needed

**Recommendation**: Keep running for 1 month, then shut down once custom site proves stable.

---

## 📚 REFERENCE LINKS

- Supabase Dashboard: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
- Astro Docs: https://docs.astro.build
- Tailwind Docs: https://tailwindcss.com/docs
- Cloudflare Pages: https://pages.cloudflare.com
- Architecture Doc: `C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\ARCHITECTURE.md`

---

## ⚠️ IMPORTANT NOTES

1. **Don't delete existing files** - WordPress setup may have useful data
2. **Work in new directory** - Keep tstr-automation separate from new frontend
3. **Commit frequently** - Git commit after each major step
4. **Test on mobile** - 80% of users will be mobile
5. **Keep costs £0** - Don't upgrade anything until revenue justifies it

---

## 🎯 THE GOAL

**Launch a profitable £0-cost niche directory within 7 days that generates £500/month recurring revenue within 30 days.**

**Ready to start?** Let's execute Phase 1: Supabase Database Setup.

Should I proceed with generating the SQL commands to set up your Supabase database now?
