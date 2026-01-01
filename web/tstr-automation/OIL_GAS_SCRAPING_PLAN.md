# Oil & Gas Testing Services - Scraping Plan

**Date:** November 4, 2025
**Target Niche:** Oil & Gas Testing (Petroleum, Chemical, NDT, Inspection)
**Status:** Planning Phase

---

## Source Analysis & Scraping Strategy

### 🟢 HIGH PRIORITY - Scrapable Directories

#### 1. **MOGA Directory** (South Africa/Africa)
**URL:** https://moga.saoga.org.za/directory
**Type:** Industry association member directory
**Scrapability:** ⭐⭐⭐⭐⭐ EXCELLENT
**Approach:** Standard HTML scraper
**Expected Data:**
- Company names
- Services offered
- Contact information
- Geographic coverage

**Action:** Build custom scraper (similar to A2LA materials scraper)

---

### 🟡 MEDIUM PRIORITY - Corporate Service Directories

#### 2. **Intertek Petroleum Testing**
**URLs:**
- Global: https://www.intertek.com/petroleum/testing/
- South Africa: https://www.intertek.com/petroleum/south-africa/

**Type:** Corporate service pages with location finder
**Scrapability:** ⭐⭐⭐ MODERATE
**Approach:**
- Check for location/office API endpoints
- Scrape location pages if directory structure exists
- May have PDF brochures with lab listings

**Expected Data:**
- Lab locations (global network)
- Service capabilities by location
- Accreditations

**Action:** Investigate site structure first (check for JSON endpoints, location finder)

#### 3. **SGS Oil, Gas & Chemical Testing**
**URL:** https://www.sgs.com/en-za/service-groups/oil-gas-and-chemical-testing
**Type:** Global network of 200+ laboratories
**Scrapability:** ⭐⭐⭐⭐ GOOD
**Approach:**
- Find location/office directory
- Check for "Find a Lab" or "Contact Us" pages
- May have structured location data

**Expected Data:**
- 200+ lab locations worldwide
- Service specializations
- Accreditations and certifications

**Action:** High value target - investigate directory structure

#### 4. **Saybolt (Core Laboratories)**
**URL:** https://www.corelab.com/saybolt/
**Type:** Corporate site with network directory
**Scrapability:** ⭐⭐⭐ MODERATE
**Approach:**
- Check for locations/offices page
- May require manual extraction if directory not structured

**Expected Data:**
- Lab locations
- Petroleum testing services
- Independent inspection capabilities

**Action:** Investigate - may need manual download + parsing

#### 5. **DEKRA Laboratory Services**
**URL:** https://www.dekra.com/en/laboratory-services/
**Type:** European network, corporate site
**Scrapability:** ⭐⭐⭐ MODERATE
**Approach:**
- Check for lab directory
- Likely has downloadable brochures (PDF extraction)

**Expected Data:**
- European lab locations
- Chemical analysis capabilities
- Materials testing services

**Action:** Check for directory structure, evaluate PDF extraction

#### 6. **Applus+ Oil and Gas NDT**
**URL:** https://www.applus.com/global/en/what-we-do/market/oil-and-gas
**Type:** Corporate service pages
**Scrapability:** ⭐⭐ LOW-MODERATE
**Approach:**
- Check for locations/contact pages
- May require manual data extraction

**Expected Data:**
- NDT and inspection locations
- Service capabilities
- Certifications

**Action:** Low priority - assess after other sources

#### 7. **Certispec Petroleum Testing**
**URL:** https://certispec.com/laboratory/petroleum/
**Type:** Single laboratory, South African
**Scrapability:** ⭐⭐⭐⭐⭐ EASY
**Approach:** Manual entry (single location)

**Expected Data:**
- One lab location
- Petroleum testing services
- Contact information

**Action:** Manual entry - not worth scraper for 1 listing

---

## Recommended Approach

### Phase 1: High-Value Automated Scraping
**Target:** 200-500 listings from scrapable directories

1. **MOGA Directory** (Priority 1)
   - Build custom scraper
   - Expected: 50-100 South African/African listings
   - Timeline: 2-3 hours development

2. **SGS Lab Directory** (Priority 2)
   - Investigate location finder/directory
   - Expected: 200+ global labs
   - Timeline: 3-4 hours (if directory structured)

3. **Intertek Location Finder** (Priority 3)
   - Check for office/lab directory
   - Expected: 100+ global locations
   - Timeline: 2-3 hours

### Phase 2: Manual Enrichment
**Target:** Corporate sites with PDFs/brochures

- Download PDFs from Intertek, DEKRA, Saybolt
- Extract location data from PDFs (semi-automated)
- Manual entry for single-location labs (Certispec)

### Phase 3: Data Enrichment
**Target:** Add missing data (phone, website, services)

- Google Places API enrichment
- Manual verification of high-value listings
- Website scraping for service details

---

## Scraper Specifications

### Data Model Requirements

**Each listing represents ONE physical location:**
```
Business Name: "SGS - Durban Laboratory"
Parent Company: "SGS" (stored in custom field)
Address: "123 Example St, Durban, KwaZulu-Natal, South Africa"
Location: Durban, KwaZulu-Natal (normalized via libpostal)
Category: Oil & Gas Testing
```

**For multi-location companies, create separate listings:**
- SGS - Durban Laboratory → listing ID 1001
- SGS - Cape Town Laboratory → listing ID 1002
- SGS - Houston Laboratory → listing ID 1003

**Custom field links them:**
- `parent_company`: "SGS" (allows filtering "all SGS locations")
- `location_type`: "Laboratory", "Office", "Service Center"
- `corporate_website`: "https://www.sgs.com"
- `location_page`: "https://www.sgs.com/en-za/locations/durban"

### Custom Fields for Oil & Gas Testing

**Service Type Fields:**
- `petroleum_testing` (boolean)
- `chemical_analysis` (boolean)
- `ndt_inspection` (boolean)
- `materials_testing` (boolean)
- `safety_inspection` (boolean)
- `environmental_monitoring` (boolean)

**Capability Fields:**
- `crude_oil_testing` (text)
- `refined_products_testing` (text)
- `petrochemical_testing` (text)
- `pipeline_inspection` (boolean)
- `offshore_services` (boolean)
- `onshore_services` (boolean)

**Compliance Fields:**
- `iso_17025_accredited` (boolean)
- `astm_certified` (boolean)
- `api_certified` (boolean)
- `iaf_accredited` (boolean)
- `industry_standards` (text[]) - e.g., ASTM, API, ISO

**Geographic Fields:**
- `service_area` (text) - "Global", "Africa", "Regional"
- `mobile_lab_services` (boolean)
- `onsite_sampling` (boolean)

---

## Expected Output

### Target Listings: 300-500+

**IMPORTANT:** Each listing = one physical location/laboratory, not one company.
- Example: "SGS - Durban Laboratory" is ONE listing
- Example: "SGS - Cape Town Laboratory" is SEPARATE listing
- Example: "Intertek - Houston Office" is ONE listing

**By Geography:**
- Global: 200+ individual labs (Intertek, SGS, Saybolt)
- Europe: 50+ individual labs (DEKRA)
- Africa: 100+ individual labs/offices (MOGA members, SGS-SA, Intertek-SA, Certispec)
- Americas: 50+ individual labs (Applus+, Core Labs)

**By Parent Company:**
- SGS: 200+ individual laboratory locations
- Intertek: 100+ individual office/lab locations
- DEKRA: 50+ individual lab locations
- MOGA members: 50-100 individual companies (some with multiple locations)
- Saybolt: 20-50 individual locations
- Others: 50+ combined

**By Service Type:**
- Petroleum Testing: 300+ locations
- Chemical Analysis: 250+ locations
- NDT/Inspection: 150+ locations
- Materials Testing: 100+ locations

---

## Development Timeline

### Week 1: Investigation & Scraper Development
- Day 1: Analyze MOGA directory structure
- Day 2: Build MOGA scraper
- Day 3: Test and validate MOGA data

### Week 2: Major Directories
- Day 1-2: SGS directory investigation and scraping
- Day 3-4: Intertek location scraping
- Day 5: Data validation and deduplication

### Week 3: Data Enrichment
- Manual PDF extraction
- Google Places enrichment
- Service capability validation

---

## Questions to Answer (Investigation Phase)

### For Each Source:
1. **Does a directory/location finder exist?**
   - Look for: "Find a Lab", "Locations", "Office Finder", "Contact Us"
   - Check for: Interactive maps, search tools, filterable lists

2. **What granularity is available?**
   - ✅ **Perfect:** Individual lab pages with full address, phone, services
   - ⚠️ **Acceptable:** Location list with addresses (may need to crawl each)
   - ❌ **Insufficient:** Only regional offices or HQ addresses

3. **Is data in structured format?**
   - ✅ **Best:** JSON API endpoint (e.g., `/api/locations`)
   - ✅ **Good:** Structured HTML with consistent selectors
   - ⚠️ **Moderate:** Structured data but requires JavaScript rendering
   - ❌ **Poor:** PDFs or unstructured text

4. **What data is available per location?**
   - Essential: Address, phone/email, lab name
   - Important: Services offered, certifications, contact person
   - Nice-to-have: Equipment list, turnaround times, pricing

5. **Can we extract service capabilities per location?**
   - Some labs only do petroleum, others do full chemical analysis
   - Each location may have different certifications
   - Services may vary by location within same company

### Priority Investigations:
1. ✅ MOGA - directory structure check (member list with locations)
2. ✅ SGS - "Find a Lab" functionality (200+ locations)
3. ✅ Intertek - location finder API (100+ offices)
4. ⏳ DEKRA - locations page (European focus)
5. ⏳ Saybolt - office directory (20-50 locations)

---

## Manual vs. Automated Decision Matrix

| Source | Expected Listings | Dev Time | Manual Time | Recommendation |
|--------|------------------|----------|-------------|----------------|
| MOGA | 50-100 | 2-3h | 10h | **Automate** |
| SGS | 200+ | 3-4h | 40h+ | **Automate** |
| Intertek | 100+ | 2-3h | 20h+ | **Automate** |
| DEKRA | 50+ | 3-4h | 10h | **Automate if structured** |
| Saybolt | 20-50 | 2h | 4h | **Evaluate** |
| Applus+ | 20-50 | 2h | 4h | **Manual/Low priority** |
| Certispec | 1 | 0 | 5min | **Manual entry** |

**Threshold:** If source has 20+ listings, automate. If <20, manual entry.

---

## Next Actions

### ✅ Investigation Complete (November 4, 2025)

**See detailed findings in:** `/tstr-automation/OIL_GAS_INVESTIGATION_REPORT.md`

**Key Result:** Found Contract Laboratory directory with **170 petroleum testing labs** - highly scrapable.

### Immediate (This Week):
1. ✅ Investigation complete
2. **Get user approval** to proceed with Contract Laboratory scraper
3. Build Contract Laboratory scraper (4-6 hours)
4. Test scraper on first 2 pages (24 labs)

### Short-term (Next 2 Weeks):
5. Run full scrape (170 labs across 15 pages)
6. Load data into Supabase
7. Deploy Oil & Gas category to TSTR.directory
8. Validate on production

### Long-term (Month 2):
9. Implement profile page crawling for service details
10. Data enrichment (Google Places API for phone/website)
11. Custom field validation
12. Monthly re-scrape for new labs

---

## Risk Assessment

**Low Risk:**
- MOGA directory (industry association, public data)
- Corporate "Contact Us" / "Find a Lab" pages

**Medium Risk:**
- PDF extraction (format variations, manual verification needed)
- Large corporate sites (may require rate limiting, robots.txt compliance)

**High Risk:**
- None identified (all sources are public B2B directories)

---

## Success Metrics

### Minimum Viable Dataset:
- 100+ Oil & Gas testing labs
- 50%+ with location data
- 30%+ with service capabilities
- 80%+ with contact information

### Target Dataset:
- 300+ labs globally
- 80%+ with full location data
- 60%+ with detailed service capabilities
- 90%+ with contact information
- 40%+ with accreditation data

---

## Budget Estimate

**Development Time:** 15-20 hours (3 scrapers)
**Manual Data Entry:** 5-10 hours (single locations, PDF extraction)
**Data Validation:** 5 hours
**Total:** 25-35 hours

**Cost Estimate (if outsourced):**
- Development: $750-1000 ($50/hr)
- Manual entry: $150-300 ($30/hr)
- **Total: $900-1300**

**Cost if automated only:** $750-1000 for 300+ listings = **$2.50-3.30 per listing**

---

## Notes

- All sources are public B2B directories or corporate "Find a Lab" pages
- No paywalls or authentication barriers identified
- Industry associations (MOGA) provide member directories intentionally for lead generation
- Large testing companies (SGS, Intertek) want to be found - directories likely scrapable

**Recommendation:** Start with MOGA (highest ROI, cleanest data), then tackle SGS and Intertek.
