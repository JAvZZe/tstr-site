# Universal Standards-Based Search - Design Document

> **Date**: 2025-11-20
> **Scope**: All testing categories (not just Hydrogen)
> **Approach**: Extend current schema, don't break existing structure
> **Token Status**: 50k remaining - will implement Phase 1 this session

---

## Strategic Vision

### The Problem
Users need to find testing labs by **specific certifications/standards** they can perform:
- "Who can test ISO 19880-3 valves at 700 bar?"
- "Which labs are A2LA accredited for pharmaceutical testing?"
- "Who has SAE J2601 fueling protocol capability?"

### Current State (Weak)
- Browse by category (Pharmaceutical, Oil & Gas)
- Browse by location (United States, Singapore)
- Generic listings with no technical search

### Target State (Powerful)
- **Search by Standard/Certification**: ISO codes, ASTM, SAE, API, etc.
- **Filter by Technical Specs**: Pressure, temperature, materials
- **AI-Discoverable**: Schema.org markup for Perplexity/Gemini
- **SEO Goldmine**: Long-tail technical searches

---

## Database Design

### Option A: Universal Standards Tables (RECOMMENDED)

**Advantage**: Works for ALL categories from day 1

```sql
-- Standards/Certifications (ISO, ASTM, SAE, API, FDA, etc.)
CREATE TABLE standards (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  code TEXT NOT NULL UNIQUE,                    -- "ISO 19880-3", "ASTM D7042"
  name TEXT NOT NULL,                           -- "Hydrogen Valves Testing"
  description TEXT,                             -- Full description
  issuing_body TEXT,                            -- "ISO", "ASTM", "SAE", "FDA"
  category_id UUID REFERENCES categories(id),   -- Which industry (optional)
  standard_type TEXT,                           -- "certification", "test_method", "accreditation"
  url TEXT,                                     -- Link to official standard doc
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Listing capabilities (what each lab can test)
CREATE TABLE listing_capabilities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  standard_id UUID REFERENCES standards(id) ON DELETE CASCADE,
  
  -- Technical specifications (stored as JSONB for flexibility)
  specifications JSONB DEFAULT '{}',            -- {max_pressure_bar: 700, state: "gaseous", equipment: ["blast_bunker"]}
  
  -- Metadata
  verified BOOLEAN DEFAULT FALSE,               -- Admin verified this capability
  verified_at TIMESTAMPTZ,
  verified_by UUID REFERENCES auth.users(id),
  notes TEXT,                                   -- Internal notes
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  UNIQUE(listing_id, standard_id)
);

-- Search optimization index
CREATE INDEX idx_capabilities_standard ON listing_capabilities(standard_id);
CREATE INDEX idx_capabilities_listing ON listing_capabilities(listing_id);
CREATE INDEX idx_capabilities_specs ON listing_capabilities USING GIN(specifications);
```

### Why JSONB for Specifications?

**Different standards need different specs**:
- Hydrogen: `{max_pressure_bar: 700, state: "gaseous", equipment: ["blast_bunker"]}`
- Pharmaceutical: `{gmp_certified: true, sterility_level: "Class 100", fda_registered: true}`
- Materials: `{temperature_range_c: [-196, 1000], materials: ["titanium", "inconel"]}`

**Flexibility**: Each category can have unique technical metadata without schema changes

---

## Implementation Plan

### Phase 1: Database Schema (This Session)

**Tables to Create**:
1. `standards` - Universal standards/certifications table
2. `listing_capabilities` - Junction table with technical specs
3. Indexes for search optimization

**Seed Data** (Initial):
- Hydrogen: ISO 19880-3, SAE J2601, ISO 11114-1
- Pharmaceutical: USP, GMP, FDA 21 CFR Part 11
- Oil & Gas: API 571, API 580, ISO 17020
- Environmental: EPA Method 1664, ISO 17025
- Materials: ASTM E8, ISO 6892-1

**Action**: Create migration file, apply to database

### Phase 2: Search API (Next Session)

**Endpoint**: `/api/search/by-standard`
**Query Params**:
- `standard=ISO_19880-3` (exact match)
- `category=hydrogen` (optional filter)
- `specs={"min_pressure": 700}` (technical filters)

**Returns**: Listings with matching capabilities + technical specs

### Phase 3: Frontend UI (Next Session)

**Components**:
- Standards dropdown (populated from DB)
- Technical spec filters (dynamic based on category)
- Results with capability details

**Pages**:
- Enhanced listing detail pages (show standards)
- Standards-first search page (`/search/standards`)

### Phase 4: SEO/AI Integration (Next Session)

**JSON-LD Markup**:
```json
{
  "@type": "Organization",
  "serviceType": ["ISO 19880-3 Testing", "SAE J2601 Compliance"],
  "additionalProperty": [{
    "@type": "PropertyValue",
    "name": "Max Pressure",
    "value": "700 bar"
  }]
}
```

---

## Impact Analysis

### Current Database Structure
- `listings` (175 records) - Main table
- `categories` (5 categories) - Industry types
- `locations` (hierarchical) - Geographic data
- `custom_fields` (flexible metadata) - Currently unused for standards

### New Structure
- `listings` - **No changes** (backward compatible)
- `standards` - **New** (100-200 records initially)
- `listing_capabilities` - **New** (500+ records as we populate)

### Migration Path
1. ✅ Create new tables (doesn't affect existing)
2. ✅ Seed standards data (read-only operation)
3. ✅ Existing listings continue to work
4. ⏳ Gradually add capabilities to existing listings
5. ⏳ New search interface available alongside existing browse

**Zero Downtime**: New feature doesn't break current site

---

## Categories Covered

### All 5 Current Categories

**1. Oil & Gas Testing**
- Standards: API 571, API 580, ISO 17020, ASTM D7042
- Specs: {pressure_rating, temperature_range, corrosion_types}

**2. Pharmaceutical Testing**
- Standards: USP, GMP, FDA 21 CFR Part 11, ISO 13485
- Specs: {sterility_class, gmp_certified, cleanroom_iso_class}

**3. Biotech Testing**
- Standards: ISO 10993, ICH Q7, FDA 21 CFR Part 210
- Specs: {biosafety_level, cell_line_testing, genetic_analysis}

**4. Environmental Testing**
- Standards: EPA Method 1664, ISO 17025, ISO 14001
- Specs: {sample_types, detection_limits, accreditation}

**5. Materials Testing**
- Standards: ASTM E8, ISO 6892-1, ASTM D638
- Specs: {temperature_range, materials, tensile_strength_max}

**6. Hydrogen** (New - from task document)
- Standards: ISO 19880-3, SAE J2601, ISO 11114-1
- Specs: {max_pressure_bar, state, special_equipment}

---

## Implementation This Session

**Token Budget**: 50k remaining → Use 35k for Phase 1, save 15k for handoff

**Goal**: Complete database schema + initial migration

**Steps**:
1. Create `standards` table
2. Create `listing_capabilities` table
3. Create indexes
4. Write seed data script for initial standards (20-30 standards)
5. Test migration
6. Document for next session

**Checkpoint**: After each major step

**Next Session**: Seed data + API endpoint + frontend

---

Ready to proceed with Phase 1 (database schema)? I'll start with the migration file.
