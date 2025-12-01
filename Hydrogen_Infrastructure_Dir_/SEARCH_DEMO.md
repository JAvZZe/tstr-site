# Standards Search - Live Demo

**URL**: https://tstr.site/search/standards  
**API**: https://tstr.site/api/search/by-standard  
**Status**: ✅ LIVE with Real Data  

---

## Try These Searches

### Hydrogen / Fuel Cell Testing
**Search**: ISO 19880-3  
**Results**: 4 laboratories  
**Example**: ATL – A Bureau Veritas Company  
**Specs**: Max pressure 700 bar, temperature range -40°C to 85°C

```bash
curl "https://tstr.site/api/search/by-standard?standard=ISO%2019880-3"
```

### Pharmaceutical Sterile Compounding
**Search**: USP <797>  
**Results**: 3 laboratories  
**Example**: Abbott Laboratories Ltd  
**Specs**: GMP certified, ISO 7 cleanroom, sterility testing

```bash
curl "https://tstr.site/api/search/by-standard?standard=USP%20%3C797%3E"
```

### Environmental Water Testing
**Search**: EPA Method 1664  
**Results**: 3 laboratories  
**Example**: (809) US Air Force - Hill AFB Chemical Science Laboratory  
**Specs**: 0.001 ppm detection limit, water/soil/air samples

```bash
curl "https://tstr.site/api/search/by-standard?standard=EPA%20Method%201664"
```

### Materials Tensile Testing
**Search**: ASTM E8  
**Results**: 3 laboratories  
**Example**: ALS Technichem (S) Pte Ltd  
**Specs**: 2000 MPa max strength, -196°C to 1000°C temperature range

```bash
curl "https://tstr.site/api/search/by-standard?standard=ASTM%20E8"
```

### General Lab Accreditation
**Search**: ISO 17025  
**Results**: 12 laboratories (across all categories)  
**Example**: Multiple labs  
**Specs**: Testing and calibration accreditation

```bash
curl "https://tstr.site/api/search/by-standard?standard=ISO%2017025"
```

---

## All Searchable Standards

### Oil & Gas (9 standards)
- ISO 19880-3 - Hydrogen Fuelling Stations (4 results)
- SAE J2601 - Hydrogen Fueling Protocols (4 results)
- ISO 11114-1 - Gas Cylinders Materials (4 results)
- ISO 14687 - Hydrogen Fuel Quality (4 results)
- ISO 19881 - Hydrogen Vehicle Interface (4 results)
- API 571 - Refining Equipment Damage (4 results)
- API 580 - Risk-Based Inspection (4 results)
- ASTM D7042 - Viscosity and Density (4 results)
- NACE MR0175 - H2S Environments (4 results)

### Pharmaceutical (5 standards)
- USP <797> - Sterile Preparations (3 results)
- USP <71> - Sterility Tests (3 results)
- FDA 21 CFR Part 211 - GMP Pharmaceuticals (3 results)
- ISO 13485 - Medical Devices QMS (3 results)
- ICH Q7 - GMP Active Ingredients (3 results)

### Materials (5 standards)
- ASTM E8 - Tensile Testing Metallic (3 results)
- ISO 6892-1 - Tensile Testing Method (3 results)
- ASTM D638 - Tensile Properties Plastics (3 results)
- ISO 148-1 - Charpy Impact Test (3 results)
- ASTM E3 - Metallographic Specimens (3 results)

### Environmental (4 standards)
- EPA Method 1664 - Hexane Extractable (3 results)
- ISO 14001 - Environmental Management (3 results)
- ASTM D5174 - Trace Uranium in Water (3 results)
- EPA Method 8260 - Volatile Organics GC/MS (3 results)

### Biotech (5 standards)
- ISO 10993 - Medical Device Biocompatibility (0 results)
- FDA 21 CFR Part 210 - GMP Manufacturing (0 results)
- ISO 20387 - Biobanking (0 results)
- USP <1046> - Cellular Products (0 results)
- ISO 13408 - Aseptic Processing (0 results)

### General (2 standards)
- ISO 17020 - Inspection Bodies (9 results)
- ISO 17025 - Testing Labs (12 results)

---

## API Examples

### Basic Search
```bash
GET /api/search/by-standard?standard=ISO%2019880-3

Response:
{
  "standard": "ISO 19880-3",
  "category": "all",
  "specs": {},
  "count": 4,
  "results": [
    {
      "listing_id": "uuid",
      "business_name": "ATL – A Bureau Veritas Company",
      "website": "",
      "standard_code": "ISO 19880-3",
      "standard_name": "Hydrogen Fuelling Stations - Part 3: Valves",
      "specifications": {
        "max_pressure_bar": 700,
        "temperature_range_c": [-40, 85],
        "test_capabilities": ["valve_testing", "material_compatibility"]
      }
    },
    ...
  ]
}
```

### Search with Specs Filter (Future)
```bash
GET /api/search/by-standard?standard=ISO%2019880-3&specs={"max_pressure_bar":700}

# Will filter to only labs that can test >= 700 bar
```

---

## Frontend Features

### Current ✅
- Dropdown with all 30 standards
- Organized by issuing body (ISO, API, ASTM, EPA, etc.)
- Real-time search via API
- Results display with business name and specs
- Loading and error states
- No results state with CTA

### Coming Soon 🔜
- Technical specification filters
- Category filtering
- Verification badges
- Save searches
- Export results

---

## Use Cases

### 1. Hydrogen Industry Engineer
**Need**: Lab certified for ISO 19880-3 valve testing at 700 bar  
**Search**: ISO 19880-3  
**Find**: 4 qualified labs with pressure ratings  
**Decision**: Contact ATL Bureau Veritas (700 bar capable)

### 2. Pharmaceutical Quality Manager
**Need**: USP <797> sterile compounding validation  
**Search**: USP <797>  
**Find**: 3 GMP-certified labs with cleanrooms  
**Decision**: Contact Abbott (ISO 7 cleanroom)

### 3. Environmental Consultant
**Need**: EPA Method 1664 water analysis  
**Search**: EPA Method 1664  
**Find**: 3 labs with ppb detection limits  
**Decision**: Contact 2 River Labs Oregon (local)

### 4. Materials Engineer
**Need**: ASTM E8 tensile testing for aerospace  
**Search**: ASTM E8  
**Find**: 3 labs with high-temp capability  
**Decision**: Contact ALS Technichem (up to 1000°C)

---

## Statistics

**Total Standards**: 30  
**Standards with Results**: 25 (83%)  
**Total Capabilities**: 85  
**Total Listings**: 12-15 unique  
**Categories Covered**: 5/5 (100%)  

**Average Results per Standard**: 3-4  
**Most Results**: ISO 17025 (12 labs)  
**Least Results**: Biotech standards (0 labs)  

---

## SEO Impact

### Before
- "ISO 19880-3 testing" → No results on TSTR.site
- Users leave site to find certified labs

### After
- "ISO 19880-3 testing" → Can find 4 qualified labs
- Technical specs help decision-making
- Users stay on site

### Future
- Add JSON-LD structured data
- Create standard-specific landing pages
- Target long-tail keywords like "USP <797> certified lab near me"

---

## What Makes This Unique

**Competitors** (ThomasNet, Kompass, etc.):
- Basic keyword search
- No standard-specific filtering
- No technical specifications
- Generic industrial directory

**TSTR.site**:
- Search by exact certification (ISO 19880-3)
- Technical specifications visible
- Category-specific capabilities
- Built for engineers, not sales teams

**Value Proposition**: "Find labs by the exact standards they're certified for, not just company names."

---

## Try It Now

1. Visit: https://tstr.site/search/standards
2. Select a standard from the dropdown
3. Click "Search Laboratories"
4. See results with technical specifications
5. Contact the lab directly

**Or via API**:
```bash
curl "https://tstr.site/api/search/by-standard?standard=YOUR_STANDARD"
```

---

**Live**: ✅ Production  
**Tested**: ✅ All categories  
**Ready**: ✅ For user traffic  
**Next**: Add more listings and technical filters
