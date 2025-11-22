# Handoff: Standards-Based Search System
**Date**: 2025-11-20  
**Session Duration**: ~2 hours  
**Tokens Used**: 69k / 200k (34.5%)  
**Status**: Phase 1 Complete (Database), Phase 2 Ready (API + Frontend)

---

## Executive Summary

Built universal standards-based search system for TSTR.site. Users can now search testing labs by specific certifications/standards (e.g., "ISO 19880-3", "USP <797>") instead of just browsing by location/category.

**Applies to ALL testing categories** (not just Hydrogen):
- Hydrogen, Oil & Gas, Pharmaceutical, Biotech, Environmental, Materials

**Database ready, API + Frontend needed next.**

---

## What Was Completed This Session

### 1. Design Document ✅
**File**: `STANDARDS_SEARCH_DESIGN.md`
- Complete architecture for universal standards search
- Database schema with JSONB for flexible technical specs
- 4-phase implementation plan
- Category coverage (all 6 categories)

### 2. Database Schema ✅
**Migration**: `supabase/migrations/20251120000001_add_standards_and_capabilities.sql`

**Tables Created**:
```sql
standards (
  id, code, name, description,
  issuing_body, category_id, standard_type,
  url, revision, is_active, timestamps
)

listing_capabilities (
  id, listing_id, standard_id,
  specifications JSONB,  -- Flexible tech specs per category
  verified, verified_at, verified_by,
  notes, display_order, timestamps
)
```

**Indexes**: 7 indexes for search optimization  
**RLS Policies**: Public read, authenticated write  
**Helper Function**: `search_by_standard(p_standard_code, p_category_id, p_min_specs)`

**Status**: Applied to production database ✅

### 3. Seed Data ✅
**File**: `supabase/seed_standards_initial.sql`

**30 Standards Inserted**:
- **Hydrogen (5)**: ISO 19880-3, SAE J2601, ISO 11114-1, ISO 14687, ISO 19881
- **Oil & Gas (5)**: API 571, API 580, ISO 17020, ASTM D7042, NACE MR0175
- **Pharmaceutical (5)**: USP <797>, USP <71>, FDA 21 CFR Part 211, ISO 13485, ICH Q7
- **Biotech (5)**: ISO 10993, FDA 21 CFR Part 210, ISO 20387, USP <1046>, ISO 13408
- **Environmental (5)**: EPA Method 1664, ISO 17025, ISO 14001, ASTM D5174, EPA Method 8260
- **Materials (5)**: ASTM E8, ISO 6892-1, ASTM D638, ISO 148-1, ASTM E3

**Verified**: 
```bash
curl "https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/standards?select=count"
# Returns: [{"count":30}]
```

### 4. Git Commits ✅
- `916e729` - feat(db): Add universal standards-based search schema
- `d62a0f0` - chore(seed): Add initial standards data across all categories

**Pushed to**: `main` branch at https://github.com/JAvZZe/tstr-site.git

---

## Current Database State

### Production Tables
```
standards: 30 rows
listing_capabilities: 0 rows (ready for data)
listings: 175 rows (existing, unchanged)
categories: 5 rows (existing)
```

### Example Standard
```json
{
  "code": "ISO 19880-3",
  "name": "Hydrogen Fuelling Stations - Part 3: Valves",
  "description": "Testing requirements for valves...",
  "issuing_body": "ISO",
  "standard_type": "test_method",
  "url": "https://www.iso.org/standard/71940.html"
}
```

### Example Capability (Future)
```json
{
  "listing_id": "uuid-of-lab",
  "standard_id": "uuid-of-iso-19880-3",
  "specifications": {
    "max_pressure_bar": 700,
    "state": "gaseous",
    "equipment": ["blast_bunker", "cryostat"]
  },
  "verified": true
}
```

---

## What Needs to Be Done Next (Phase 2)

### Priority 1: Search API Endpoint (2-3 hours)

**File to Create**: `web/tstr-frontend/src/pages/api/search/by-standard.ts`

**Endpoint**: `GET /api/search/by-standard`

**Query Parameters**:
- `standard` (required) - Standard code (e.g., "ISO 19880-3")
- `category` (optional) - Category slug to filter by
- `specs` (optional) - JSON object with minimum specs

**Example Request**:
```
/api/search/by-standard?standard=ISO_19880-3&specs={"min_pressure":700}
```

**Implementation**:
```typescript
import { supabase } from '../../../lib/supabase'

export async function GET({ request }) {
  const url = new URL(request.url)
  const standard = url.searchParams.get('standard')
  const category = url.searchParams.get('category')
  const specs = url.searchParams.get('specs') ? JSON.parse(url.searchParams.get('specs')) : {}
  
  // Call the search_by_standard() function
  const { data, error } = await supabase.rpc('search_by_standard', {
    p_standard_code: standard,
    p_category_id: category || null,
    p_min_specs: specs
  })
  
  return new Response(JSON.stringify({ results: data }), {
    headers: { 'Content-Type': 'application/json' }
  })
}
```

**Testing**:
```bash
# After implementation, test with:
curl "http://localhost:4321/api/search/by-standard?standard=ISO%2019880-3"
```

### Priority 2: Frontend Search Interface (3-4 hours)

**Option A: New Page** - `web/tstr-frontend/src/pages/search/standards.astro`  
**Option B: Enhance Existing** - Update `browse.astro` with standards filter

**Components Needed**:

1. **Standards Dropdown**:
```typescript
// Populate from database
const { data: standards } = await supabase
  .from('standards')
  .select('code, name, issuing_body')
  .eq('is_active', true)
  .order('issuing_body', { ascending: true })
```

2. **Technical Spec Filters** (category-specific):
```typescript
// Hydrogen example
<div class="spec-filters" id="hydrogen-filters">
  <label>
    Minimum Pressure (bar):
    <input type="number" name="min_pressure" />
  </label>
  <label>
    State:
    <select name="state">
      <option value="">Any</option>
      <option value="gaseous">Gaseous</option>
      <option value="liquid">Liquid</option>
    </select>
  </label>
</div>
```

3. **Results Display**:
```astro
<div class="results">
  {results.map(result => (
    <div class="result-card">
      <h3>{result.business_name}</h3>
      <p><strong>Standard:</strong> {result.standard_code} - {result.standard_name}</p>
      <div class="specs">
        {Object.entries(result.specifications).map(([key, value]) => (
          <span class="spec-tag">{key}: {value}</span>
        ))}
      </div>
      <a href={`/listing/${result.listing_id}`}>View Details</a>
    </div>
  ))}
</div>
```

### Priority 3: Update Existing Filters

**User's Request**: "We should also change the frontend and filters accordingly"

**Files to Update**:
1. `web/tstr-frontend/src/pages/browse.astro`
   - Add "Search by Standard" tab/section
   - Keep existing category/location filters
   - Add standards dropdown

2. `web/tstr-frontend/src/pages/browse/[country].astro`
   - Same standards filter addition

3. `web/tstr-frontend/src/pages/browse/city/[city].astro`
   - Same standards filter addition

**UI Pattern**:
```
┌─────────────────────────────────────┐
│  Browse Testing Laboratories        │
├─────────────────────────────────────┤
│  Filters:                           │
│  ☐ By Location  ☑ By Standard      │
│                                     │
│  [Select Standard ▼]                │
│  ISO 19880-3, SAE J2601, USP <797>  │
│                                     │
│  Technical Specifications:          │
│  [ ] Min Pressure: [___] bar        │
│  [ ] State: [Any ▼]                 │
│                                     │
│  [Search] [Clear Filters]           │
└─────────────────────────────────────┘
```

---

## Implementation Strategy (Next Session)

### Recommended Approach (Pareto 80/20)

**Session 1** (Next): API + Basic Search UI (3-4 hours)
1. Create API endpoint (`/api/search/by-standard`)
2. Test with curl
3. Create basic search page (`/search/standards`)
4. Test with real standards data
5. Commit & deploy

**Session 2** (Future): Enhanced Filters (2-3 hours)
1. Add standards dropdown to existing browse pages
2. Add dynamic technical spec filters
3. Improve results display
4. Commit & deploy

**Session 3** (Future): Polish & SEO (2-3 hours)
1. Add JSON-LD markup
2. Create category landing pages
3. Link existing listings to standards
4. Commit & deploy

### Don't Forget To:
- ✅ Test API endpoint before building UI
- ✅ Use existing `search_by_standard()` function (already in DB)
- ✅ Commit after each working feature
- ✅ Run `npm run build` to verify before deploy
- ✅ Checkpoint frequently

---

## Key Technical Details

### JSONB Specifications Format

**Flexibility is key** - Each category has different technical requirements:

```typescript
// Hydrogen
specifications: {
  max_pressure_bar: 700,
  state: "gaseous" | "liquid",
  equipment: ["blast_bunker", "cryostat"]
}

// Pharmaceutical
specifications: {
  gmp_certified: true,
  sterility_class: "Class 100",
  cleanroom_iso_class: "ISO 5",
  fda_registered: true
}

// Materials
specifications: {
  temperature_range_c: [-196, 1000],
  materials: ["titanium", "inconel", "stainless_steel"],
  tensile_strength_max_mpa: 2000
}
```

### Search Function Usage

**Already exists in database**:
```sql
-- Basic search
SELECT * FROM search_by_standard('ISO 19880-3', NULL, '{}');

-- With category filter
SELECT * FROM search_by_standard('ISO 19880-3', 'category-uuid', '{}');

-- With technical specs
SELECT * FROM search_by_standard(
  'ISO 19880-3', 
  NULL, 
  '{"max_pressure_bar": 700}'::jsonb
);
```

### Supabase Client Usage

**From frontend**:
```typescript
import { supabase } from '../lib/supabase'

// Call RPC function
const { data, error } = await supabase.rpc('search_by_standard', {
  p_standard_code: 'ISO 19880-3',
  p_category_id: null,
  p_min_specs: { max_pressure_bar: 700 }
})
```

---

## Files Created This Session

```
✅ STANDARDS_SEARCH_DESIGN.md                          (Design doc)
✅ supabase/migrations/20251120000001_...sql           (Schema migration)
✅ supabase/seed_standards_initial.sql                 (Seed data)
✅ HANDOFF_STANDARDS_SEARCH_2025-11-20.md              (This file)
```

---

## Quick Start Commands (Next Session)

### Resume Session
```bash
cd "/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working"
./bootstrap.sh TSTR.site
```

### Verify Database
```bash
# Check standards count
curl "https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/standards?select=count" \
  -H "apikey: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO" \
  -H "Prefer: count=exact"

# List standards
curl "https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/standards?select=code,name&order=code" \
  -H "apikey: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO"
```

### Test Search Function
```bash
# Via Supabase SQL Editor
SELECT * FROM search_by_standard('ISO 19880-3', NULL, '{}');
```

### Start Development Server
```bash
cd web/tstr-frontend
npm run dev
# Opens http://localhost:4321
```

### Create API Endpoint
```bash
mkdir -p web/tstr-frontend/src/pages/api/search
touch web/tstr-frontend/src/pages/api/search/by-standard.ts
# Then implement the endpoint
```

---

## Context for Next Agent

### User Profile
- **Non-technical founder** with AuDHD
- **Decision-making style**: OODA Loop + First Principles + Pareto (80/20)
- **Wants**: Working features, not theater
- **Needs**: Clear explanations, progress updates, token awareness

### Project Status
- **Live site**: http://tstr.site (175 listings)
- **Database**: Supabase (production)
- **Frontend**: Astro + React + Tailwind
- **Deployment**: Netlify (auto-deploy from main branch)

### Session Management
- **Bootstrap**: Use `./bootstrap.sh TSTR.site` (not resume.sh)
- **Checkpoints**: Use `./checkpoint.sh "description"` frequently
- **Token tracking**: Report status at 75%, 50%, 25% remaining
- **Handoff at**: ~20-30k tokens remaining

### User Expectations
1. Test before deploy
2. Commit after each working feature
3. No broken builds
4. Clear progress updates
5. Token awareness for handoff planning

---

## Success Criteria (Phase 2)

**Minimum Viable** (Next Session):
- ✅ API endpoint works (`/api/search/by-standard`)
- ✅ Can search by standard code
- ✅ Returns matching listings (even if 0 results)
- ✅ Basic frontend page displays results

**Nice to Have** (Future):
- ✅ Technical spec filters functional
- ✅ Integrated into existing browse pages
- ✅ JSON-LD markup for SEO
- ✅ Some listings linked to standards

**Long-term Goal**:
- Users find labs by exact technical requirements
- AI agents (Perplexity, Gemini) can discover via search
- TSTR.site becomes "the technical testing directory"

---

## References

**Design Document**: Read `STANDARDS_SEARCH_DESIGN.md` first  
**Original Task**: Read `Droid Task TSTR site.md` for context  
**Database Schema**: See migration file for complete structure  
**Supabase Dashboard**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy

---

## Notes for Next Session

1. **Start with API endpoint** - Foundation for frontend
2. **Test thoroughly** - Use curl before building UI
3. **Keep it simple** - Basic search first, enhance later
4. **Commit frequently** - After each working piece
5. **Watch tokens** - Budget 30-40k for API + basic UI

**This is high-value work** - Standards-based search is unique in this space. Positions TSTR.site as the technical directory where engineers find labs by exact specifications, not just company names.

---

**End of Handoff**  
**Next Agent**: Start with "I've reviewed the handoff. Building the search API endpoint now..."
