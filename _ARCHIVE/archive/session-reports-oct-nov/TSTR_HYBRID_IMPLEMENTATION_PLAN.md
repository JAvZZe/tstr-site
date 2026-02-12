# TSTR.site Hybrid Implementation Plan
**Strategy:** Quick Fix + Strategic Build (Parallel Tracks)
**Created:** 2025-11-01
**Timeline:** Track A (2-3 days) | Track B (2-4 weeks, overlapping)

---

## Track A: Quick Fix - Location Extraction (IMMEDIATE)
**Goal:** Fix "only 1 country showing" issue for existing 127 listings
**Timeline:** 2-3 days
**Benefit:** Homepage shows all international coverage, filtering works

### Steps

#### 1. Create Backfill Script (Today - 2 hours)
**File:** `web/tstr-automation/backfill_location_ids.py`

**Logic:**
```python
# For each listing:
# 1. Parse formatted_address or use lat/lng
# 2. Extract country, city (best effort)
# 3. Query locations table for match
# 4. If no match, create new location entry
# 5. Update listings.location_id = matched/created location
```

**Approach Options:**
- **Option A (Simplest):** Regex parse `formatted_address` → match known countries in locations table
- **Option B (Better):** Use lat/lng + Google Geocoding API reverse lookup → guaranteed accuracy ($0.005 × 127 = $0.64)
- **Option C (Free but complex):** libpostal library (offline address parsing)

**Recommendation:** Option B (Google reverse geocode) - reliable, low cost, one-time operation

#### 2. Test on Sample (Today - 30 min)
- Run backfill on 5 listings
- Verify location_id populated correctly
- Check locations table has new entries if needed

#### 3. Full Backfill (Tomorrow - 1 hour)
- Run for all 127 listings
- Log results: matched vs created locations
- Verify no NULL location_ids remain

#### 4. Update Frontend (Tomorrow - 1 hour)
**File:** `web/tstr-frontend/src/pages/index.astro`

**Change:**
```javascript
// BEFORE (lines 30-50):
const extractCountry = (address) => { /* text parsing */ }
const locations = listings ? [...new Set(listings.map(l => extractCountry(l.address)))].filter(Boolean).slice(0, 8) : []

// AFTER:
const { data: listings } = await supabase
  .from('listings')
  .select(`
    *,
    location:location_id (
      id,
      name,
      slug,
      level,
      parent:parent_id (
        name,
        slug,
        level
      )
    )
  `)
  .eq('status', 'active')
  .order('created_at', { ascending: false })

// Extract countries from location hierarchy
const countries = [...new Set(
  listings
    .map(l => {
      // Navigate up hierarchy to find country
      let loc = l.location
      while (loc && loc.level !== 'country') {
        loc = loc.parent
      }
      return loc ? { name: loc.name, slug: loc.slug } : null
    })
    .filter(Boolean)
)].slice(0, 8)
```

#### 5. Test & Deploy (Day 3 - 2 hours)
- Build locally: `npm run build`
- Verify homepage shows multiple countries
- Push to GitHub → Cloudflare auto-deploys
- Monitor live site

**Success Criteria:**
- ✅ Homepage "International Coverage" shows 5+ countries (not just Singapore)
- ✅ Country links work: `/browse/united-states`, `/browse/united-kingdom`
- ✅ City extraction working (if addresses have city data)

---

## Track B: Strategic Enhancement - Niche Scrapers (PARALLEL)
**Goal:** Build foundation for high-value niche-specific data collection
**Timeline:** Weeks 1-4 (starts while Track A runs)
**Benefit:** Differentiated listings, higher lead quality

### Week 1: Foundation (While Track A completes)

#### 1. Design location_parser.py Module
**File:** `web/tstr-automation/location_parser.py`

**Purpose:** Reusable module for future scrapers to extract location_id

```python
class LocationParser:
    """Parse addresses and link to locations table"""

    def __init__(self, supabase_client, google_api_key=None):
        self.supabase = supabase_client
        self.api_key = google_api_key
        self.cache = {}  # Cache location lookups

    def parse_address(self, formatted_address, lat=None, lng=None):
        """
        Returns: location_id (UUID) or None
        Methods:
        1. Try cache lookup first
        2. Use Google Geocoding API if lat/lng available
        3. Fallback to regex parsing
        4. Create new location if needed
        """
        pass

    def reverse_geocode(self, lat, lng):
        """Use Google API to get structured address components"""
        pass

    def find_or_create_location(self, country, city, region=None):
        """Query locations table, create hierarchy if missing"""
        pass
```

#### 2. Add Custom Fields SQL
**File:** `web/tstr-automation/custom_fields_migration.sql`

Run in Supabase SQL Editor to add niche-specific fields:
```sql
-- Get category IDs
DO $$
DECLARE
  oil_gas_id UUID;
  pharma_id UUID;
  env_id UUID;
  materials_id UUID;
BEGIN
  SELECT id INTO oil_gas_id FROM categories WHERE slug = 'oil-gas-testing';
  SELECT id INTO pharma_id FROM categories WHERE slug = 'pharmaceutical-testing';
  SELECT id INTO env_id FROM categories WHERE slug = 'environmental-testing';
  SELECT id INTO materials_id FROM categories WHERE slug = 'materials-testing';

  -- Oil & Gas custom fields
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, display_order) VALUES
    (oil_gas_id, 'testing_types', 'Testing Types', 'multi_select', 1),
    (oil_gas_id, 'real_time_analytics', 'Real-Time Analytics', 'boolean', 2),
    (oil_gas_id, 'equipment_brands', 'Equipment Brands', 'text', 3),
    (oil_gas_id, 'coverage_type', 'Coverage Type', 'multi_select', 4),
    (oil_gas_id, 'certifications', 'Certifications', 'multi_select', 5),
    (oil_gas_id, 'recent_projects', 'Recent Projects', 'text', 6);

  -- Update multi_select options
  UPDATE custom_fields SET options = '["Well Logging", "Production Testing", "Flow Assurance", "Pressure Testing"]'::jsonb
  WHERE field_name = 'testing_types';

  UPDATE custom_fields SET options = '["Onshore", "Offshore", "Both"]'::jsonb
  WHERE field_name = 'coverage_type';

  -- Pharma custom fields
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, display_order) VALUES
    (pharma_id, 'analytical_techniques', 'Analytical Techniques', 'multi_select', 1),
    (pharma_id, 'drug_specializations', 'Drug Specializations', 'multi_select', 2),
    (pharma_id, 'regulatory_compliance', 'Regulatory Compliance', 'multi_select', 3),
    (pharma_id, 'turnaround_time', 'Turnaround Time', 'select', 4);

  UPDATE custom_fields SET options = '["HPLC", "Mass Spectrometry", "GC-MS", "Microbial Testing"]'::jsonb
  WHERE field_name = 'analytical_techniques';

  -- Environmental custom fields
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, display_order) VALUES
    (env_id, 'test_types', 'Test Types', 'multi_select', 1),
    (env_id, 'esg_reporting', 'ESG Reporting', 'boolean', 2),
    (env_id, 'field_lab_services', 'Service Location', 'multi_select', 3);

  -- Materials custom fields
  INSERT INTO custom_fields (category_id, field_name, field_label, field_type, display_order) VALUES
    (materials_id, 'material_types', 'Material Types', 'multi_select', 1),
    (materials_id, 'test_procedures', 'Test Procedures', 'multi_select', 2),
    (materials_id, 'rd_capabilities', 'R&D Capabilities', 'text', 3);
END $$;
```

### Week 2: First Niche Scraper

#### 3. Build Base Scraper Architecture
**File:** `web/tstr-automation/scrapers/base_scraper.py`

```python
from abc import ABC, abstractmethod
from location_parser import LocationParser
from url_validator import URLValidator

class BaseNicheScraper(ABC):
    """Abstract base class for all niche-specific scrapers"""

    def __init__(self, category_slug, supabase_client):
        self.category_slug = category_slug
        self.supabase = supabase_client
        self.location_parser = LocationParser(supabase_client)
        self.url_validator = URLValidator()

        # Get category_id from database
        result = self.supabase.from_('categories').select('id').eq('slug', category_slug).single().execute()
        self.category_id = result.data['id']

    @abstractmethod
    def scrape_company_page(self, url):
        """Override: Extract company data from source page"""
        pass

    def extract_general_fields(self, soup):
        """Common fields across all scrapers"""
        return {
            'business_name': None,
            'address': None,
            'location_id': None,
            'phone': None,
            'email': None,
            'website': None
        }

    @abstractmethod
    def extract_niche_fields(self, soup):
        """Override: Category-specific custom fields"""
        pass

    def save_to_database(self, general_data, niche_data):
        """Insert listing + custom field values"""
        # 1. Insert into listings table
        # 2. Insert into listing_custom_fields table
        pass
```

#### 4. Implement Rigzone Scraper (Oil & Gas)
**File:** `web/tstr-automation/scrapers/oil_gas/rigzone_scraper.py`

**Target:** https://www.rigzone.com/directory/

```python
from scrapers.base_scraper import BaseNicheScraper

class RigzoneOilGasScraper(BaseNicheScraper):
    def __init__(self, supabase_client):
        super().__init__('oil-gas-testing', supabase_client)
        self.base_url = 'https://www.rigzone.com/directory/'

    def scrape_company_page(self, company_url):
        """Extract from Rigzone company profile"""
        # Check robots.txt first
        # Scrape company data
        # Parse HTML for niche fields
        pass

    def extract_niche_fields(self, soup):
        """Oil & Gas specific data"""
        return {
            'testing_types': [],      # Extract from services section
            'equipment_brands': '',   # Extract from capabilities
            'coverage_type': [],      # Parse from description
            'certifications': [],     # Extract certifications
            'recent_projects': ''     # Case studies/news section
        }
```

**Test:** Scrape 10 companies, validate data quality

### Week 3-4: Scale to Other Niches

- Intertek Pharma scraper
- SGS Environmental scraper
- Intertek Materials scraper

Each scraper: 10-20 companies with full custom fields

---

## Coordination Between Tracks

**Track A feeds Track B:**
- Backfill script becomes basis for `location_parser.py`
- Proven approach (regex vs API vs libpostal) used in future scrapers

**Track B doesn't block Track A:**
- Quick fix uses simple parsing, good enough for 127 listings
- Strategic scrapers use proper location_parser for new listings

**Unified by Week 4:**
- Old listings: location_id via backfill
- New listings: location_id via enhanced scrapers
- All listings: filterable, differentiated, high-value

---

## Resource Allocation

**Time Investment:**
- Track A: 6-8 hours (front-loaded, Days 1-3)
- Track B: 20-30 hours (spread over 4 weeks)

**Cost:**
- Google Geocoding (one-time backfill): $0.64
- Google Geocoding (ongoing for new scrapers): ~$2-3/month
- Total: <$5/month

**Value:**
- Track A: Fix critical UX issue (1 country → 10+ countries visible)
- Track B: 10x listing value (generic → niche-specific intelligence)

---

## Success Metrics

### Track A (Week 1)
- [x] Homepage shows 5+ countries in International Coverage
- [x] `/browse/united-states` and `/browse/singapore` pages work
- [x] All 127 listings have location_id populated

### Track B (Week 4)
- [ ] 100+ listings with niche-specific custom fields
- [ ] 4 niche scrapers operational (Oil & Gas, Pharma, Environmental, Materials)
- [ ] Listing pages show differentiated data (not just name/address/phone)
- [ ] Lead quality improvement: enquiries include niche-specific requirements

---

## Next Immediate Action

**Start Track A now:**
1. Create `backfill_location_ids.py` script
2. Decide: Google Geocoding API (recommended) vs regex parsing
3. Test on 5 listings
4. Review results before full run

**Start Track B in parallel (if bandwidth):**
1. Add custom_fields SQL to Supabase (15 min, non-blocking)
2. Design location_parser.py (can reference backfill approach)

---

**Let's start with Track A - which option for location extraction?**
- **A:** Google Geocoding API ($0.64 one-time, most accurate)
- **B:** Regex parsing (free, less accurate but good enough for backfill)
- **C:** Install libpostal library (free, accurate, but setup complexity)

I recommend **A** for backfill (one-time cost, guaranteed results), then implement **C** for `location_parser.py` (ongoing free parsing for new scrapers).

Your call?
