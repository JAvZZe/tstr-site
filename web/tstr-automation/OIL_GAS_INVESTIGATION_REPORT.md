# Oil & Gas Testing Sources - Investigation Report

**Date:** November 4, 2025
**Status:** Investigation Complete
**Investigator:** Claude Code

---

## Executive Summary

Investigated 7 potential sources for Oil & Gas testing laboratory data. Found **1 highly scrapable source** with 170 petroleum testing labs.

### Key Findings:
- ✅ **Contract Laboratory Directory:** 170 labs, highly scrapable, excellent data structure
- ❌ **Corporate networks (SGS, Intertek, DEKRA):** Block automated access or lack structured location directories
- ❌ **MOGA:** Training providers, not testing labs (wrong niche)
- ❌ **Saybolt:** Directory only in mobile app (not web-scrapable)

### Recommendation:
**Focus on Contract Laboratory directory** - single source provides 170 petroleum testing labs with addresses, locations, and profile pages for detailed data extraction.

---

## Detailed Findings by Source

### ✅ 1. Contract Laboratory Directory (HIGH VALUE)

**URL:** https://www.contractlaboratory.com/directory/laboratories/by-industry.cfm?i=45

**Scrapability:** ⭐⭐⭐⭐⭐ EXCELLENT

**Data Available:**
- **170 petroleum testing laboratories** across 15 pages
- Name, full address, location (city, state, country)
- Member join dates
- Profile links for detailed information
- Structured HTML with consistent CSS classes
- JSON-LD schema markup

**Pagination:**
- 12 labs per page
- Standard URL pattern: `/page/[n]/?_sort=featured_vendor__desc`
- 15 total pages

**Data Structure:**
```html
.hp-vendor--view-block (card container)
  - Lab name (linked)
  - Street address
  - City, County, State, Country
  - Member since date
  - Logo/image
  - "Send Message" button
```

**Scraping Approach:**
1. Iterate through 15 pages
2. Extract basic data from list view (name, location, address)
3. Optionally crawl individual profile pages for:
   - Testing services offered
   - Certifications/accreditations
   - Equipment/capabilities
   - Contact information
   - Website URLs

**Expected Output:**
- 170 petroleum testing labs
- Global coverage (USA, India, Costa Rica, etc.)
- Clean, structured data
- Development time: 3-4 hours for basic scraper
- Additional 2-3 hours for profile page crawling

**Limitations:**
- List view lacks service details (requires profile crawling)
- Contact info may require login/"Send Message" action
- No direct phone numbers visible in list view

**Recommendation:** **AUTOMATE - HIGH PRIORITY**

---

### ❌ 2. SGS Oil, Gas & Chemical Testing

**URLs Tested:**
- https://www.sgs.com/en-za/service-groups/oil-gas-and-chemical-testing
- https://www.sgs.com

**Scrapability:** ❌ BLOCKED

**Findings:**
- WebFetch returns 403 Forbidden
- Site blocks automated access
- Cannot verify if "Find a Lab" directory exists

**Recommendation:** **SKIP - BLOCKED**

**Alternative Approach:**
- Manual browser inspection (not automated)
- Contact SGS for location data export
- Use Google Maps API to find SGS lab locations
- Check if SGS has a public API or data feed

---

### ❌ 3. Intertek Petroleum Testing

**URL:** https://www.intertek.com/petroleum/testing/

**Scrapability:** ⭐⭐ LOW

**Findings:**
- Has "Locations & Contacts" section
- Has "Petroleum Chemical Locations" link
- Location page (https://www.intertek.com/petroleum/locations/) shows:
  - Alphabetical list of countries (hyperlinked)
  - No actual addresses or contact details
  - Requires clicking each country link

**Country Page Example (South Africa):**
- Lists city names only: "Durban, Cape Town, Johannesburg, Port Elizabeth, Richards Bay"
- No addresses, phone numbers, or emails
- Generic contact form and UK phone number
- No structured location data

**Data Structure:**
- Hierarchical: Country → City names only
- No individual lab pages
- No contact details at location level

**Recommendation:** **SKIP - INSUFFICIENT DATA**

**Why:**
- Only city names, no addresses
- No lab-specific contact information
- Would require manual research for each city mentioned
- Not worth scraping effort for minimal data

---

### ❌ 4. MOGA (Mechanical & Oilfield Goods Association)

**URL:** https://moga.saoga.org.za/directory

**Scrapability:** ⭐⭐⭐ MODERATE (but wrong niche)

**Findings:**
- **This is a TRAINING PROVIDER directory**, not testing laboratories
- 34 training providers listed
- Searchable with filters (Region, Area of Delivery, Type)
- Structured HTML, paginated (10 per page)

**Data Available:**
- Company name, region, description
- "Read more" links to full profiles
- No direct contact info in list view

**Recommendation:** **SKIP - WRONG NICHE**

**Why:**
- We need testing labs, not training providers
- Different business model and services
- Not relevant to tstr.directory's target audience

---

### ❌ 5. DEKRA Laboratory Services

**URL:** https://www.dekra.com/en/laboratory-services/

**Scrapability:** ⚠️ UNKNOWN (CSS-only response)

**Findings:**
- WebFetch returned only CSS styling code
- No visible HTML content or navigation
- Cannot determine if location directory exists

**Recommendation:** **SKIP - INSUFFICIENT INVESTIGATION**

**Alternative:**
- Manual browser check required
- Likely has location directory but requires JavaScript rendering
- Would need Selenium/Playwright for proper scraping
- Lower priority given Contract Laboratory success

---

### ❌ 6. Saybolt (Core Laboratories)

**URL:** https://www.corelab.com/saybolt/

**Scrapability:** ❌ NOT SCRAPABLE

**Findings:**
- Headquarters address provided: Vlaardingen, Netherlands
- Mentions "Directory app" at esaybolt.corelab.com/public/html/directoryapp.html
- Directory app is **mobile-only** (iOS app download page)
- No web-based directory accessible

**Directory App Page:**
- Only shows "Download on App Store" button
- "Android version coming soon"
- No location data on webpage
- Data exists only inside mobile app

**Recommendation:** **SKIP - APP-ONLY DATA**

**Alternative:**
- Manual entry of known Saybolt locations
- Check LinkedIn/Google Maps for office locations
- Contact Saybolt for location list export

---

### ❌ 7. Applus+ Oil and Gas NDT

**URL:** https://www.applus.com/global/en/what-we-do/market/oil-and-gas

**Scrapability:** ❌ 404 ERRORS

**Findings:**
- Main page mentions "Locations Directory" and "Offices by country"
- Attempted URLs return 404:
  - https://www.applus.com/global/en/locations (404)
  - https://www.applus.com/global/en/contact (404)
- Cannot access location directory

**Recommendation:** **SKIP - INACCESSIBLE**

**Alternative:**
- Check Applus+ website manually in browser
- May have different URL structure
- Lower priority given Contract Laboratory success

---

## Summary Table

| Source | Labs Available | Scrapability | Data Quality | Recommendation |
|--------|---------------|--------------|--------------|----------------|
| **Contract Laboratory** | **170** | ⭐⭐⭐⭐⭐ | **Excellent** | **AUTOMATE** |
| SGS | 200+? | ❌ Blocked | Unknown | Skip |
| Intertek | 100+? | ⭐⭐ Low | City names only | Skip |
| MOGA | 34 | ⭐⭐⭐ Moderate | Wrong niche | Skip |
| DEKRA | 50+? | ⚠️ Unknown | Unknown | Skip |
| Saybolt | 20-50? | ❌ App-only | Not accessible | Skip |
| Applus+ | 50+? | ❌ 404 errors | Not accessible | Skip |

---

## Recommended Implementation Plan

### Phase 1: Contract Laboratory Scraper (Week 1)

**Objective:** Extract all 170 petroleum testing labs

**Development Tasks:**
1. Build pagination scraper (15 pages)
2. Extract basic data from list view:
   - Lab name
   - Full address
   - City, state, country
   - Member join date
3. Normalize locations with libpostal
4. Load into Supabase

**Expected Output:**
- 170 listings with addresses
- Geographic distribution: USA, international
- Development time: 3-4 hours
- Testing & validation: 1-2 hours
- **Total: 4-6 hours**

### Phase 2: Profile Page Crawling (Week 2)

**Objective:** Enrich data with service details

**Development Tasks:**
1. Crawl individual lab profile pages
2. Extract:
   - Testing services offered
   - Certifications/accreditations
   - Equipment/capabilities
   - Contact information (if available)
   - Website URLs
3. Update custom fields in database

**Expected Output:**
- Service capabilities for 170 labs
- Certifications/accreditations
- Website URLs
- Development time: 2-3 hours
- **Total: 2-3 hours**

### Phase 3: Data Enrichment (Week 3)

**Objective:** Add missing contact data

**Options:**
1. Google Places API (phone, website)
2. Manual verification of high-value listings
3. LinkedIn company pages
4. Manual research for top 50 labs

**Expected Output:**
- Phone numbers for 50%+ of labs
- Website URLs for 80%+ of labs
- Email addresses where available

---

## Budget Estimate

### Development Costs

**Phase 1: Basic Scraper**
- Development: 4 hours × $50/hr = $200
- Testing: 1 hour × $50/hr = $50
- **Subtotal: $250**

**Phase 2: Profile Enrichment**
- Development: 2 hours × $50/hr = $100
- Testing: 1 hour × $50/hr = $50
- **Subtotal: $150**

**Phase 3: Data Enrichment**
- Google Places API: $0 (free tier)
- Manual verification: 5 hours × $30/hr = $150
- **Subtotal: $150**

**Total Development Cost: $550**

**Cost Per Listing:** $550 ÷ 170 = **$3.24 per listing**

### Comparison to Manual Entry

**Manual entry cost:**
- 170 labs × 15 min/lab = 42.5 hours
- 42.5 hours × $30/hr = **$1,275**

**Savings with automation: $725 (57% reduction)**

---

## Technical Specifications

### Scraper Architecture

**Language:** Python 3.x
**Libraries:**
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `supabase-py` - Database integration
- `postal` (libpostal) - Address normalization
- `time` - Rate limiting

**Rate Limiting:**
- 1-2 second delay between requests
- Respect robots.txt
- User-agent: "tstr.directory scraper (contact@tstr.directory)"

**Error Handling:**
- Retry on network failures (3 attempts)
- Log failed pages
- Continue on individual parsing errors
- Checkpoint progress every 10 pages

### Database Schema

**New Custom Fields for Oil & Gas:**

```sql
-- Add to custom_fields table
INSERT INTO custom_fields (category_id, field_name, field_type, field_label) VALUES
  ((SELECT id FROM categories WHERE slug = 'oil-gas-testing'), 'parent_company', 'text', 'Parent Company'),
  ((SELECT id FROM categories WHERE slug = 'oil-gas-testing'), 'petroleum_testing', 'boolean', 'Petroleum Testing'),
  ((SELECT id FROM categories WHERE slug = 'oil-gas-testing'), 'chemical_analysis', 'boolean', 'Chemical Analysis'),
  ((SELECT id FROM categories WHERE slug = 'oil-gas-testing'), 'ndt_inspection', 'boolean', 'NDT Inspection'),
  ((SELECT id FROM categories WHERE slug = 'oil-gas-testing'), 'iso_17025', 'boolean', 'ISO 17025 Accredited'),
  ((SELECT id FROM categories WHERE slug = 'oil-gas-testing'), 'astm_certified', 'boolean', 'ASTM Certified'),
  ((SELECT id FROM categories WHERE slug = 'oil-gas-testing'), 'member_since', 'date', 'Member Since');
```

**Listing Data Model:**
```
business_name: "ABC Petroleum Testing Laboratory"
category: "Oil & Gas Testing"
address: "123 Lab St, Pasadena, TX, USA"
location_id: [normalized via libpostal]
phone: "+1-xxx-xxx-xxxx" (from profile or enrichment)
website: "https://example.com" (from profile)
description: [from profile page]
certification_number: null (unless accredited)
source: "Contract Laboratory"
```

---

## Risk Assessment

### Low Risks:
- ✅ Contract Laboratory is public directory (intended for lead generation)
- ✅ Data is freely accessible (no authentication required)
- ✅ Structured HTML makes scraping reliable
- ✅ Pagination is standard and predictable

### Medium Risks:
- ⚠️ List view lacks service details (need profile crawling)
- ⚠️ Contact info may be limited (need enrichment)
- ⚠️ Rate limiting may be enforced (add delays)
- ⚠️ Site structure may change (requires monitoring)

### Mitigation:
- Implement rate limiting (1-2 sec delays)
- Add error handling and logging
- Save raw HTML for re-parsing if structure changes
- Checkpoint progress to resume if interrupted

---

## Alternative Sources (Future Investigation)

If Contract Laboratory proves insufficient, consider:

1. **Industry Association Directories:**
   - American Petroleum Institute (API) members
   - ASTM International testing labs
   - ILAC accredited petroleum labs

2. **Government/Regulatory Databases:**
   - State environmental testing lab registries
   - EPA-approved petroleum testing facilities
   - International petroleum testing standards bodies

3. **Commercial Directories:**
   - ThomasNet industrial suppliers
   - Kompass business directory
   - Global Testing Laboratory Network

4. **Web Search + Extraction:**
   - Google Maps API: "petroleum testing laboratory"
   - LinkedIn company search: "petroleum testing"
   - Industry publications and trade journals

---

## Next Steps

### Immediate (This Week):
1. ✅ Investigation complete
2. **Get user approval** to proceed with Contract Laboratory scraper
3. Build scraper prototype (4 hours)
4. Test on first 2 pages (24 labs)
5. Validate data quality

### Short-term (Next 2 Weeks):
6. Run full scrape (170 labs)
7. Load into Supabase
8. Deploy to tstr.directory
9. Validate on production

### Long-term (Month 2):
10. Implement profile page crawling
11. Data enrichment (Google Places API)
12. Monitor for new labs (monthly re-scrape)

---

## Success Metrics

### Minimum Viable Dataset:
- 100+ petroleum testing labs loaded
- 80%+ with full address data
- 50%+ with contact information
- 40%+ with service capabilities

### Target Dataset:
- 170 petroleum testing labs loaded
- 95%+ with full address data
- 70%+ with contact information
- 60%+ with detailed service capabilities
- 50%+ with certifications/accreditations

---

## Conclusion

**Investigation reveals ONE high-value scrapable source:** Contract Laboratory directory with 170 petroleum testing labs.

**Recommendation:** Proceed with Contract Laboratory scraper development immediately. This single source provides sufficient data for a strong Oil & Gas testing launch on tstr.directory.

**ROI:** High - 170 labs for ~6 hours development time ($550), vs. 42.5 hours manual entry ($1,275). Saves $725 and 36.5 hours.

**Risk:** Low - public directory, structured data, straightforward scraping.

**Timeline:** 1-2 weeks from approval to production deployment.

---

**Prepared by:** Claude Code
**Date:** November 4, 2025
**Status:** Ready for user review and approval
