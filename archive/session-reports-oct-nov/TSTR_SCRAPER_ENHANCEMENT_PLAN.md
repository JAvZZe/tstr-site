# TSTR.site Scraper Enhancement Plan
**Created:** 2025-11-01
**Status:** Planning Phase
**Objective:** Fix address parsing + add niche-specific high-value data collection

---

## Problem Statement

### Current Issues
1. **Address Parsing Failure:** 126/127 listings fail country extraction (only Singapore showing)
2. **Schema-Implementation Gap:** Database has `location_id` FK + `locations` table hierarchy, but scrapers populate only `address` TEXT field
3. **Generic Data Only:** Scrapers collect basic company info, missing niche-specific differentiators and value-add intelligence

### Impact
- Homepage shows 1 country instead of international coverage
- No filtering by city/country/region possible
- Listings lack competitive differentiation (all look the same)
- Low lead generation value (buyers can't find specialized capabilities)

---

## Solution Architecture

### Phase 1: Fix Address/Location Extraction (Immediate)

**Scraper Enhancement:**
```python
# Add location parsing module
def parse_and_link_location(formatted_address, lat, lng):
    """
    Parse formatted_address and/or use reverse geocoding to extract:
    - City
    - State/Region
    - Country
    - Match or create entry in locations table
    - Return location_id UUID
    """
    # Option 1: Parse formatted_address string
    # "123 Main St, Houston, TX 77001, United States" → extract components

    # Option 2: Use lat/lng with Google Geocoding API reverse lookup
    # More reliable, costs $0.005 per request

    # Option 3: Use libpostal (free, offline library)
    # Best for privacy + cost, requires installation

    # Query locations table to find match or create new entry
    # Return location_id for insertion into listings.location_id
```

**Database Schema (Already Exists):**
```sql
-- Use existing structure from SUPABASE_SETUP.sql
locations (id, name, slug, parent_id, level, latitude, longitude)
  - level: 'global' | 'region' | 'country' | 'city'
  - Hierarchical: Global → Region → Country → City

listings.location_id → locations.id (FK)
```

**Frontend Change:**
```javascript
// BEFORE (index.astro line 30-50):
const extractCountry = (address) => { /* fragile text parsing */ }

// AFTER:
const { data: listings } = await supabase
  .from('listings')
  .select('*, location:location_id(name, slug, level, parent:parent_id(name, slug))')
  .eq('status', 'active')

// Use location.name for display, location.slug for URL
```

---

### Phase 2: Niche-Specific Data Collection

**Target Niches & Sources:**

#### 1. Oil & Gas Well Testing
**Sources:** Mordor Intelligence, Rigzone, SGS, ScanTech, Enercorp, CETCO, Intertek, TUV Rheinland

**Database Schema Extension:**
```sql
-- Add custom_fields entries for oil-gas-testing category
INSERT INTO custom_fields (category_id, field_name, field_label, field_type) VALUES
  ('oil-gas-testing', 'testing_types', 'Testing Types', 'multi_select'),  -- well logging, production testing, etc.
  ('oil-gas-testing', 'real_time_analytics', 'Real-Time Analytics', 'boolean'),
  ('oil-gas-testing', 'equipment_brands', 'Equipment Brands/Models', 'text'),
  ('oil-gas-testing', 'coverage_type', 'Coverage Type', 'multi_select'),  -- onshore, offshore
  ('oil-gas-testing', 'certifications', 'Certifications', 'multi_select'),  -- API, ISO, etc.
  ('oil-gas-testing', 'rapid_deployment', 'Rapid Deployment Capable', 'boolean'),
  ('oil-gas-testing', 'recent_projects', 'Recent Projects', 'text'),
  ('oil-gas-testing', 'tech_investments', 'Technology Investments', 'text');
```

**Scraper Module:**
```python
# Source-specific parser: rigzone_scraper.py
class RigzoneOilGassScraper:
    def scrape_company_page(self, url):
        """Extract niche-specific data from Rigzone company profile"""
        # General: name, address, contacts
        # Niche: testing types, equipment, certifications
        # Value-add: projects, client segments, capabilities
```

#### 2. Pharmaceutical/Biotech Testing
**Sources:** Intertek Pharma, TUV Rheinland, SGS Pharma

**Custom Fields:**
```sql
INSERT INTO custom_fields (category_id, field_name, field_label, field_type) VALUES
  ('pharmaceutical-testing', 'analytical_techniques', 'Analytical Techniques', 'multi_select'),  -- HPLC, mass spec, etc.
  ('pharmaceutical-testing', 'drug_specializations', 'Drug Type Specializations', 'multi_select'),  -- biologics, gene therapy
  ('pharmaceutical-testing', 'regulatory_compliance', 'Regulatory Compliance', 'multi_select'),  -- FDA, EMA, GMP
  ('pharmaceutical-testing', 'lab_accreditations', 'Lab Accreditations', 'multi_select'),  -- ISO 17025, CAP, CLIA
  ('pharmaceutical-testing', 'turnaround_time', 'Test Turnaround Time', 'select'),
  ('pharmaceutical-testing', 'electronic_reporting', 'Electronic Data Reporting', 'boolean'),
  ('pharmaceutical-testing', 'consultancy_services', 'Consultancy Services', 'text'),
  ('pharmaceutical-testing', 'compliance_support', 'Compliance Support', 'text');
```

#### 3. Environmental Testing
**Custom Fields:**
```sql
INSERT INTO custom_fields (category_id, field_name, field_label, field_type) VALUES
  ('environmental-testing', 'test_types', 'Test Types', 'multi_select'),  -- water, air, soil, noise
  ('environmental-testing', 'field_lab_services', 'Field vs Lab Services', 'multi_select'),
  ('environmental-testing', 'esg_reporting', 'ESG Report Capabilities', 'boolean'),
  ('environmental-testing', 'sampling_equipment', 'Sampling Equipment', 'text'),
  ('environmental-testing', 'compliance_standards', 'Compliance Standards', 'multi_select'),  -- ISO 14001, etc.
  ('environmental-testing', 'monitoring_tech', 'Monitoring Technology', 'text'),
  ('environmental-testing', 'custom_programs', 'Customized Test Programs', 'boolean');
```

#### 4. High-Tech Materials Testing
**Custom Fields:**
```sql
INSERT INTO custom_fields (category_id, field_name, field_label, field_type) VALUES
  ('materials-testing', 'material_types', 'Material Types', 'multi_select'),  -- nanomaterials, composites, metals
  ('materials-testing', 'test_procedures', 'Test Procedures', 'multi_select'),  -- fatigue, corrosion, tensile
  ('materials-testing', 'instrumentation', 'Instrumentation Specs', 'text'),
  ('materials-testing', 'industry_sectors', 'Industry Sectors Served', 'multi_select'),  -- aerospace, semiconductor
  ('materials-testing', 'custom_test_dev', 'Custom Test Development', 'boolean'),
  ('materials-testing', 'rd_capabilities', 'R&D Capabilities', 'text'),
  ('materials-testing', 'project_lead_time', 'Project Lead Time', 'select');
```

---

### Phase 3: Scraper Architecture

**Modular Design:**
```
web/tstr-automation/
├── dual_scraper.py                 # Base scraper (refactor)
├── location_parser.py              # NEW: Address → location_id
├── scrapers/
│   ├── base_scraper.py            # Abstract base class
│   ├── google_maps_scraper.py     # Refactored from dual_scraper
│   ├── oil_gas/
│   │   ├── rigzone_scraper.py
│   │   ├── sgs_oilgas_scraper.py
│   │   └── scantech_scraper.py
│   ├── pharma/
│   │   ├── intertek_pharma_scraper.py
│   │   └── sgs_pharma_scraper.py
│   ├── environmental/
│   │   └── sgs_environmental_scraper.py
│   └── materials/
│       ├── intertek_materials_scraper.py
│       └── cetco_scraper.py
└── config/
    └── scraping_sources.json       # Source URLs, selectors, robots.txt rules
```

**Base Scraper Class:**
```python
class BaseNicheScraper:
    """Abstract base for all niche scrapers"""

    def __init__(self, category_id):
        self.category_id = category_id
        self.location_parser = LocationParser()
        self.url_validator = URLValidator()

    def scrape(self, source_url):
        """Override in subclass"""
        raise NotImplementedError

    def extract_general_fields(self, soup):
        """Common fields: name, address, phone, website, contacts"""
        return {
            'business_name': ...,
            'address': ...,
            'location_id': self.location_parser.parse(...),  # Links to locations table
            'phone': ...,
            'email': ...,
            'website': ...
        }

    def extract_niche_fields(self, soup):
        """Override: category-specific fields"""
        raise NotImplementedError

    def extract_value_add_fields(self, soup):
        """Override: competitive intelligence"""
        raise NotImplementedError
```

---

## Implementation Steps

### Milestone 1: Fix Location Extraction (Week 1)
- [ ] Implement `location_parser.py` module
- [ ] Update `dual_scraper.py` to populate `location_id`
- [ ] Run migration script to backfill `location_id` for existing 127 listings
- [ ] Update `index.astro` to query via location joins
- [ ] Test: Verify all countries now appear in "International Coverage"

### Milestone 2: Schema for Niche Fields (Week 1-2)
- [ ] Add custom_fields entries for 4 niches (SQL scripts)
- [ ] Test custom field retrieval in frontend
- [ ] Design listing detail page to display custom fields

### Milestone 3: Build First Niche Scraper (Week 2)
- [ ] Create base scraper architecture
- [ ] Implement Oil & Gas scraper for Rigzone (highest value, clear structure)
- [ ] Test on 10 companies, validate data quality
- [ ] Insert into database with custom_fields populated

### Milestone 4: Scale to Other Niches (Week 3-4)
- [ ] Pharma scraper (Intertek Pharma)
- [ ] Environmental scraper (SGS Environmental)
- [ ] Materials scraper (Intertek Materials)
- [ ] Validation: 20 listings per niche with full custom fields

### Milestone 5: Production Deployment (Week 4)
- [ ] Schedule scrapers (cron: weekly for each niche)
- [ ] Monitor data quality, deduplication
- [ ] Frontend: Filter by niche-specific attributes
- [ ] Analytics: Track which custom fields drive engagement

---

## Ethical Scraping Compliance

**Per Source:**
1. Check `robots.txt` for each target site
2. Respect rate limits (1-2 seconds between requests)
3. Rotate User-Agents
4. Validate URLs before scraping
5. Log disallowed paths, skip them

**Example robots.txt check:**
```python
from urllib.robotparser import RobotFileParser

def check_robots_txt(base_url, path):
    rp = RobotFileParser()
    rp.set_url(f"{base_url}/robots.txt")
    rp.read()
    return rp.can_fetch("*", path)
```

---

## Cost Estimate

**Google Maps API (for location parsing):**
- Reverse Geocoding: $0.005 per request
- For 127 existing + ~500 new listings/month = ~$3.15/month

**Infrastructure (Oracle Free Tier):**
- $0/month (current setup)

**Total:** ~$3-5/month for high-quality structured data vs. unreliable text parsing

---

## Success Metrics

### Phase 1 (Location Fix)
- ✅ All countries displayed on homepage (currently 1/127 → target 100%)
- ✅ Filterable by country/city
- ✅ SEO: Static pages per country (`/browse/united-states`)

### Phase 2 (Niche Data)
- ✅ 100+ listings with niche-specific custom fields populated
- ✅ Differentiated listing pages (not generic)
- ✅ Buyer engagement: Click-through rate on custom field filters
- ✅ Lead generation: Enquiry form submissions up 3x (specialized capabilities = higher intent)

---

## Next Steps

**Immediate (Today):**
1. Fix location_id population for existing 127 listings (backfill script)
2. Update frontend to use location joins instead of text parsing

**This Week:**
1. Design location_parser.py module
2. Add custom_fields SQL for 4 niches
3. Prototype Oil & Gas scraper for Rigzone

**This Month:**
1. Roll out all 4 niche scrapers
2. Populate 100+ niche-specific listings
3. Deploy filtered views + SEO pages

---

**Created by:** Claude Code (Sonnet 4.5)
**For:** TSTR.site Enhancement Initiative
**Reference:** Perplexity research on testing industry niches
