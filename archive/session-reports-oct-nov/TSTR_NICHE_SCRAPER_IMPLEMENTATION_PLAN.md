# TSTR.site Niche Scraper Implementation Plan
**Created:** 2025-11-02
**Status:** Planning Phase - Ready for Execution
**Strategy:** Research-backed, niche-by-niche implementation

---

## Executive Summary

Transform generic scrapers into **niche-specific intelligence collectors** that extract competitive differentiators for 4 high-value testing industry segments. Current scrapers collect commodity data (name, address, phone). Enhanced scrapers will extract **28 custom fields** that buyers actually filter by (certifications, capabilities, turnaround times, specializations).

**Business Impact:**
- **Differentiation**: Listings show 7 unique capabilities vs. generic info
- **Search Precision**: Filter by "FDA-certified + GMP + 24hr turnaround" vs. just location
- **Lead Quality**: 3x higher intent when buyers find exact capabilities
- **SEO Value**: Structured data for rich snippets

---

## Phase 1: Architecture Foundation

### 1.1 location_parser.py Module
**Priority:** HIGH (foundation for all scrapers)
**Time:** 2-3 hours
**Dependencies:** libpostal (installed at /home/al/.local/share/libpostal)

**Purpose:** Consistent address normalization across all scrapers

**Interface:**
```python
class LocationParser:
    def __init__(self, supabase_client):
        self.postal = postal
        self.supabase = supabase_client
        self.cache = {}  # In-memory location cache

    def parse_address(self, raw_address: str) -> dict:
        """
        Parse using libpostal, returns:
        {
            'house_number': '123',
            'road': 'Main Street',
            'city': 'Houston',
            'state': 'Texas',
            'country': 'United States',
            'postcode': '77001'
        }
        """

    def find_or_create_location(self, components: dict, lat: float = None, lng: float = None) -> UUID:
        """
        Navigate locations hierarchy:
        1. Find country (or create if new)
        2. Find/create state/region under country
        3. Find/create city under state
        4. Return city location_id

        Uses cache to minimize DB queries
        """

    def validate_location_hierarchy(self, location_id: UUID) -> bool:
        """Verify location has valid parent chain to Global"""
```

**Testing Strategy:**
- Unit tests with 20 sample addresses from existing listings
- Edge cases: PO boxes, international formats, missing components
- Performance: Batch 100 addresses, should complete <5 seconds

---

### 1.2 Base Scraper Architecture
**Priority:** HIGH
**Time:** 3-4 hours
**Dependencies:** location_parser.py, URL validator, Supabase client

**Interface:**
```python
class BaseNicheScraper:
    """Abstract base for all niche-specific scrapers"""

    def __init__(self, category_slug: str, source_name: str):
        self.category_id = self._get_category_id(category_slug)
        self.source = source_name
        self.location_parser = LocationParser(supabase)
        self.url_validator = URLValidator()
        self.custom_field_map = self._load_custom_fields()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self._get_user_agent()})

    # STANDARD EXTRACTION (all niches)
    def extract_standard_fields(self, soup: BeautifulSoup, url: str) -> dict:
        """
        Returns:
        {
            'business_name': str,
            'description': str,
            'address': str,
            'location_id': UUID,  # via location_parser
            'phone': str,
            'email': str,
            'website': str,
            'latitude': float,
            'longitude': float,
            'source': str,
            'source_url': str
        }
        """

    # NICHE-SPECIFIC EXTRACTION (override in subclass)
    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> dict:
        """
        Override per niche. Returns:
        {
            'field_name': value,  # Must match custom_fields.field_name
            ...
        }
        """
        raise NotImplementedError("Subclass must implement extract_custom_fields()")

    # SAVE TO DATABASE
    def save_listing(self, standard_fields: dict, custom_fields: dict):
        """
        1. Insert into listings table
        2. Insert custom field values into listing_custom_field_values
        3. Handle duplicates (check by website URL)
        """

    # RATE LIMITING
    def respect_rate_limit(self, domain: str):
        """Enforce 2-second delay per domain"""

    # ROBOTS.TXT COMPLIANCE
    def check_robots_allowed(self, url: str) -> bool:
        """Check robots.txt before scraping"""
```

**Design Decisions:**
- **Cache location lookups**: Reduce DB queries by 80%
- **Session management**: Reuse connections, rotate User-Agents
- **Error handling**: Retry 3x with exponential backoff, then log and skip
- **Duplicate detection**: Check existing website URLs before inserting

---

## Phase 2: Niche-Specific Implementation

### 2.1 Oil & Gas Well Testing Scraper
**Priority:** 1 (clearest patterns, high value)
**Time:** 4-6 hours
**Source:** Rigzone.com/directory

#### 2.1.1 Source Analysis

**Target URL:** https://www.rigzone.com/directory/?category=Inspection+%26+Testing

**Data Availability:**
- Company profiles with services, locations, contacts
- Searchable by service type
- Company detail pages with descriptions

**robots.txt Compliance:**
```
User-agent: *
Crawl-delay: 2
Disallow: /admin
```
✓ Scraping allowed with 2-second delay

**Custom Fields Mapping:**

| Custom Field | Extraction Strategy | Example Values |
|-------------|-------------------|----------------|
| testing_types | Extract from services description | "Well Logging", "Production Testing", "Flow Assurance" |
| real_time_analytics | Keyword search: "real-time", "live monitoring" | TRUE/FALSE |
| equipment_brands | Extract brand names from text | "Schlumberger", "Halliburton" |
| coverage_type | Search: "offshore", "onshore" | ["Onshore", "Offshore"] |
| certifications | Regex: API \d+, ISO \d+, ASME | ["API", "ISO 17025"] |
| rapid_deployment | Keyword: "rapid", "24/7", "emergency" | TRUE/FALSE |
| recent_projects | Extract from case studies/projects section | Free text |

**Implementation Class:**
```python
class RigzoneOilGasScraper(BaseNicheScraper):
    def __init__(self):
        super().__init__(
            category_slug='oil-gas-testing',
            source_name='Rigzone Directory'
        )

    def scrape_category_page(self, url: str) -> list:
        """
        Extract company listing URLs from category page
        Returns: ['https://rigzone.com/companies/123', ...]
        """

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> dict:
        """
        Oil & Gas specific extraction logic
        """
        description = soup.get_text().lower()

        return {
            'testing_types': self._extract_testing_types(soup),
            'real_time_analytics': any(kw in description for kw in ['real-time', 'live monitoring']),
            'equipment_brands': self._extract_brands(soup),
            'coverage_type': self._extract_coverage(description),
            'certifications': self._extract_certifications(soup),
            'rapid_deployment': any(kw in description for kw in ['rapid', '24/7', 'emergency']),
            'recent_projects': self._extract_projects(soup)
        }

    def _extract_testing_types(self, soup) -> list:
        """Match against predefined testing type keywords"""
        keywords = {
            'Well Logging': ['well logging', 'wireline', 'formation evaluation'],
            'Production Testing': ['production testing', 'well testing', 'flow testing'],
            'Flow Assurance': ['flow assurance', 'multiphase', 'pipeline'],
            'Pressure Testing': ['pressure test', 'hydrostatic', 'pressure vessel'],
            'NDT Inspection': ['NDT', 'non-destructive', 'ultrasonic', 'radiographic']
        }
        found_types = []
        text = soup.get_text().lower()
        for type_name, type_keywords in keywords.items():
            if any(kw in text for kw in type_keywords):
                found_types.append(type_name)
        return found_types
```

**Challenges:**
- JavaScript-rendered content (use requests-html or Selenium if needed)
- Pagination (scrape all pages, not just first)
- Company detail pages may have varied layouts

**Success Criteria:**
- Scrape 50-100 companies
- 80%+ have at least 3 custom fields populated
- No more than 5% duplicates

---

### 2.2 Environmental Testing Scraper
**Priority:** 2 (official database, high data quality)
**Time:** 3-4 hours
**Source:** TNI LAMS (lams.nelac-institute.org/search)

#### 2.2.1 Source Analysis

**Target URL:** https://lams.nelac-institute.org/search

**Data Availability:**
- NELAP accredited environmental labs
- Searchable by state, matrix (water/soil/air), method, analyte
- Each lab has: Name, TNI code, location, accreditation body, scope

**robots.txt Compliance:**
```
User-agent: *
Disallow: /admin
```
✓ Scraping allowed

**Custom Fields Mapping:**

| Custom Field | Extraction Strategy | Source Field |
|-------------|-------------------|-------------|
| test_types | Extract from "Matrix" field | Matrix: "Drinking Water" → "Water Quality" |
| field_lab_services | Parse from scope/services | Scope description |
| esg_reporting | Keyword search in scope | TRUE/FALSE |
| sampling_equipment | Extract from scope details | Free text |
| compliance_standards | Always includes "NELAC", check for others | ["ISO 14001", "EPA", "NELAC"] |
| monitoring_tech | Extract from methods list | Free text |
| custom_programs | Check scope description | TRUE/FALSE |

**Implementation Class:**
```python
class TNIEnvironmentalScraper(BaseNicheScraper):
    def __init__(self):
        super().__init__(
            category_slug='environmental-testing',
            source_name='TNI LAMS Directory'
        )

    def scrape_by_state(self, state: str) -> list:
        """
        Search TNI LAMS by state
        Returns: List of lab IDs to scrape detail pages
        """

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> dict:
        """Environmental testing specific extraction"""
        return {
            'test_types': self._map_matrix_to_test_types(soup),
            'field_lab_services': self._parse_scope(soup),
            'esg_reporting': self._check_esg_keywords(soup),
            'sampling_equipment': self._extract_equipment(soup),
            'compliance_standards': ['NELAC'] + self._find_additional_standards(soup),
            'monitoring_tech': self._extract_methods(soup),
            'custom_programs': self._check_custom_programs(soup)
        }

    def _map_matrix_to_test_types(self, soup) -> list:
        """
        Matrix field mapping:
        - "Drinking Water" → "Water Quality"
        - "Solids and Chemical" → "Soil Testing"
        - "Air" → "Air Quality"
        """
```

**Challenges:**
- Form-based search (need to POST requests)
- Pagination in results
- Detail pages may require multiple requests

**Success Criteria:**
- Scrape 100-200 labs across multiple states
- 90%+ have test_types and compliance_standards populated
- Location data from state field

---

### 2.3 Materials Testing Scraper
**Priority:** 3
**Time:** 4-5 hours
**Source:** A2LA Directory (customer.a2la.org)

#### 2.3.1 Source Analysis

**Target URL:** https://customer.a2la.org/index.cfm?event=directory.index

**Data Availability:**
- ISO/IEC 17025 accredited labs
- Searchable by keyword, program, location
- Shows: Cert #, name, location, commercial availability, program type

**Custom Fields Mapping:**

| Custom Field | Extraction Strategy |
|-------------|-------------------|
| material_types | Search keyword matches: "metals", "polymers", "composites" |
| test_procedures | Extract from scope: "tensile", "fatigue", "corrosion" |
| instrumentation | Parse from scope details |
| industry_sectors | Match keywords: "aerospace", "automotive", "semiconductor" |
| custom_test_dev | Keyword search: "custom", "R&D", "development" |
| rd_capabilities | Extract from lab description |
| project_lead_time | Parse from scope or estimate based on services |

**Implementation Class:**
```python
class A2LAMaterialsScraper(BaseNicheScraper):
    def __init__(self):
        super().__init__(
            category_slug='materials-testing',
            source_name='A2LA Directory'
        )

    def search_materials_testing(self) -> list:
        """
        Search A2LA for mechanical testing, materials testing
        Returns: List of cert numbers to fetch details
        """

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> dict:
        """Materials testing specific extraction"""
        scope_text = self._get_scope_text(soup).lower()

        return {
            'material_types': self._match_material_types(scope_text),
            'test_procedures': self._extract_procedures(scope_text),
            'instrumentation': self._extract_instrumentation(soup),
            'industry_sectors': self._match_industries(scope_text),
            'custom_test_dev': any(kw in scope_text for kw in ['custom', 'r&d', 'development']),
            'rd_capabilities': self._extract_rd_capabilities(soup),
            'project_lead_time': self._estimate_lead_time(scope_text)
        }
```

**Challenges:**
- Scope documents may be PDFs (need PDF parsing)
- Certificate details on separate pages
- Contact info may not be on listing page

**Success Criteria:**
- Scrape 50-100 labs
- 70%+ have material_types and test_procedures populated
- Industry sectors identified for 60%+

---

### 2.4 Pharmaceutical Testing Scraper
**Priority:** 4 (most complex, regulatory sensitive)
**Time:** 5-7 hours
**Sources:**
- FDA ASCA Accredited Testing Labs
- A2LA Directory (clinical testing category)
- Individual major labs (Nelson Labs, RSSL, RD Labs)

#### 2.4.1 Source Analysis

**Target URL 1:** https://www.fda.gov/medical-devices/division-standards-and-conformity-assessment/asca-accredited-testing-laboratories

**Data Availability:**
- List of ASCA accredited labs
- Lab name, accreditation body, scope link

**Target URL 2:** A2LA Directory (clinical testing filter)

**Custom Fields Mapping:**

| Custom Field | Extraction Strategy |
|-------------|-------------------|
| analytical_techniques | Match: "HPLC", "mass spec", "GC-MS", "ELISA" |
| drug_specializations | Match: "biologics", "small molecules", "gene therapy" |
| regulatory_compliance | Check: "FDA", "EMA", "GMP", "GLP" |
| lab_accreditations | Extract: "ISO 17025", "CAP", "CLIA" |
| turnaround_time | Parse from scope or services description |
| electronic_reporting | Keyword: "electronic", "LIMS", "data portal" |
| consultancy_services | Check for consulting/advisory services |

**Implementation Class:**
```python
class PharmaceuticalScraper(BaseNicheScraper):
    def __init__(self):
        super().__init__(
            category_slug='pharmaceutical-testing',
            source_name='FDA ASCA + A2LA'
        )

    def scrape_fda_asca_labs(self) -> list:
        """Extract labs from FDA ASCA page"""

    def scrape_a2la_clinical(self) -> list:
        """Extract clinical testing labs from A2LA"""

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> dict:
        """Pharmaceutical testing specific extraction"""
        text = soup.get_text().lower()

        return {
            'analytical_techniques': self._match_techniques(text),
            'drug_specializations': self._match_drug_types(text),
            'regulatory_compliance': self._extract_compliance(text),
            'lab_accreditations': self._extract_accreditations(soup),
            'turnaround_time': self._parse_turnaround(text),
            'electronic_reporting': any(kw in text for kw in ['electronic', 'lims', 'portal']),
            'consultancy_services': self._extract_consultancy(soup)
        }
```

**Challenges:**
- Multiple sources to combine
- Regulatory sensitivity (must be accurate)
- Contact info may be limited on public listings
- Scope documents on separate pages

**Success Criteria:**
- Scrape 30-50 labs (smaller pool but high quality)
- 85%+ have analytical_techniques and regulatory_compliance
- No false positives on compliance claims

---

## Phase 3: Deployment & Monitoring

### 3.1 Execution Sequence

**Week 1:**
1. Build location_parser.py (Day 1-2)
2. Build base scraper architecture (Day 2-3)
3. Test with mock data (Day 3)

**Week 2:**
4. Implement Oil & Gas scraper (Day 4-5)
5. Test on 10 companies, validate data (Day 5)
6. Run full scrape, import to database (Day 6)

**Week 3:**
7. Implement Environmental scraper (Day 7-8)
8. Test and validate (Day 8)
9. Run full scrape (Day 9)

**Week 4:**
10. Implement Materials scraper (Day 10-11)
11. Implement Pharmaceutical scraper (Day 12-13)
12. Final validation and deployment (Day 14)

### 3.2 Quality Assurance

**Data Validation Rules:**
1. **Minimum field population:** Each listing must have ≥3 custom fields populated
2. **Location validation:** All listings must have valid location_id
3. **URL validation:** All websites must return 200 status
4. **Duplicate detection:** Check website URL and phone for duplicates
5. **Certification claims:** Flag for manual review if FDA/GMP/API mentioned

**Manual Review Sample:**
- 10 random listings per niche
- Verify custom field accuracy against source
- Check for hallucinations (false certifications)

### 3.3 Monitoring & Maintenance

**Scheduled Runs:**
- Oil & Gas: Monthly (Rigzone updates frequently)
- Environmental: Quarterly (NELAP database stable)
- Materials: Quarterly (A2LA updates periodically)
- Pharmaceutical: Bi-monthly (FDA ASCA updates)

**Error Logging:**
- Failed URLs (404, timeout, blocked)
- Parsing errors (missing expected fields)
- Validation failures (invalid location, duplicate)
- Rate limit violations

**Success Metrics:**
- Listings with custom fields: Target 300+ (100/niche after Phase 2)
- Custom field population rate: Target 75%+ (≥5 of 7 fields per listing)
- Duplicate rate: <5%
- Error rate: <10%

---

## Phase 4: Frontend Integration

### 4.1 Listing Detail Pages

**Display Custom Fields:**
```astro
<!-- Example: Oil & Gas listing detail -->
<div class="capabilities">
  <h3>Testing Capabilities</h3>
  {listing.custom_fields.testing_types?.map(type =>
    <span class="badge">{type}</span>
  )}
</div>

<div class="certifications">
  <h3>Certifications</h3>
  {listing.custom_fields.certifications?.map(cert =>
    <span class="cert-badge">{cert}</span>
  )}
</div>

{listing.custom_fields.rapid_deployment &&
  <div class="highlight">⚡ Rapid Deployment Available</div>
}
```

### 4.2 Advanced Filtering

**Filter UI Components:**
- Multi-select for certifications, testing_types, analytical_techniques
- Boolean toggles for rapid_deployment, esg_reporting, electronic_reporting
- Dropdown for turnaround_time, project_lead_time

**Example Filter:**
```
Filter pharma labs by:
☑ GMP Compliance
☑ HPLC
☑ ISO 17025
Turnaround: ≤48 Hours
Location: United Kingdom
```

**SQL Query:**
```sql
SELECT l.* FROM listings l
JOIN listing_custom_field_values lcfv ON l.id = lcfv.listing_id
WHERE l.category_id = 'pharma-testing'
  AND lcfv.field_value @> '["GMP"]'  -- regulatory_compliance contains GMP
  AND lcfv.field_value @> '["HPLC"]'  -- analytical_techniques contains HPLC
  AND l.location_id IN (SELECT id FROM locations WHERE parent_id IN (...))  -- UK locations
```

---

## Technical Specifications

### Dependencies
```
requests==2.31.0
beautifulsoup4==4.12.0
postal==1.1.9  # libpostal Python binding
python-dotenv==1.0.0
supabase==2.23.0
requests-html==0.10.0  # For JS rendering if needed
```

### Environment Variables
```bash
SUPABASE_URL=https://haimjeaetrsaauitrhfy.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sb_secret_...
GOOGLE_MAPS_API_KEY=...  # For geocoding if needed
```

### File Structure
```
/home/al/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/
├── location_parser.py          # Address normalization module
├── base_scraper.py             # Abstract base class
├── scrapers/
│   ├── __init__.py
│   ├── rigzone_oil_gas.py     # Oil & Gas scraper
│   ├── tni_environmental.py   # Environmental scraper
│   ├── a2la_materials.py      # Materials scraper
│   └── pharmaceutical.py       # Pharma scraper (multi-source)
├── config/
│   ├── sources.json           # Source URLs, selectors
│   └── field_mappings.json    # Custom field keyword maps
├── utils/
│   ├── url_validator.py       # URL validation (existing)
│   └── rate_limiter.py        # Rate limiting logic
└── tests/
    ├── test_location_parser.py
    ├── test_base_scraper.py
    └── test_niche_scrapers.py
```

---

## Risk Assessment

### High Risk
1. **False Certification Claims**: Scraper incorrectly attributes FDA/API/GMP certification
   - Mitigation: Flag all compliance claims for manual review
   - Validation: Cross-reference with official databases

2. **Website Structure Changes**: Source sites change HTML, scrapers break
   - Mitigation: Robust CSS selectors, multiple fallback patterns
   - Monitoring: Alert if extraction rate drops below 70%

### Medium Risk
3. **Rate Limiting/IP Blocks**: Scraping too aggressively gets blocked
   - Mitigation: Respect robots.txt, 2-second delays, rotate User-Agents
   - Fallback: Use residential proxy service if needed

4. **Location Parsing Errors**: libpostal fails on unusual addresses
   - Mitigation: Fallback to manual city/state extraction
   - Validation: Flag unparsed addresses for review

### Low Risk
5. **Duplicate Listings**: Same company from multiple sources
   - Mitigation: Deduplicate by website URL + phone
   - Resolution: Merge records, prefer more complete data

6. **Incomplete Custom Fields**: Some listings lack enough data
   - Acceptance: 70%+ population rate is acceptable
   - Strategy: Mark fields as "Contact for details"

---

## Success Criteria

### Phase 1 Complete When:
- ✓ location_parser.py tests pass (20 sample addresses)
- ✓ base_scraper.py abstract methods defined
- ✓ Can save test listing with custom fields to DB

### Phase 2 Complete When:
- ✓ 300+ listings across 4 niches
- ✓ 75%+ custom field population rate
- ✓ <5% duplicate rate
- ✓ All certifications manually verified (sample)

### Phase 3 Complete When:
- ✓ Frontend displays custom fields correctly
- ✓ Advanced filtering functional
- ✓ SEO structured data implemented
- ✓ Scheduled scraper runs configured

### Business Success Metrics (3 months):
- ✓ 500+ listings with niche data
- ✓ 3x increase in enquiry form submissions
- ✓ 50%+ of searches use advanced filters
- ✓ Average session duration up 2x

---

## Next Immediate Steps

1. **Approve this plan** - Review, critique, adjust priorities
2. **Checkpoint current state** - Save plan to project database
3. **Start Phase 1** - Build location_parser.py module
4. **Test foundation** - Validate with sample data
5. **Proceed to Phase 2** - Implement niches sequentially

**Estimated Total Time:** 20-30 hours across 4 niches
**Token Budget:** 100,000-130,000 tokens (well within capacity for multiple sessions)

---

**Created by:** Claude Code (Sonnet 4.5)
**For:** TSTR.site Niche Scraper Enhancement Initiative
**Based on:** Perplexity research + industry analysis
**Ready for:** User approval and execution
