# TODO: Create Filtered Views by Country and City

**Created:** 2025-10-29
**Agent:** Claude Code (Sonnet 4.5) - avztest8@gmail.com
**Priority:** MEDIUM (after database migration)
**Estimated Time:** 2-3 hours

---

## User Request

"Countries and Cities should each be a category, filtered as you suggested earlier."

**Current state:**
- All 127 listings displayed on homepage
- International Coverage section shows up to 8 countries (extracted from addresses)
- No filtering functionality yet

**Desired state:**
- Countries as filterable categories
- Cities as filterable categories
- Listings NOT shown on homepage by default
- Only show listings when filtered by geography/category/city

---

## Implementation Options

### Option A: Separate Static Pages (Best for SEO)

Create individual pages for each country and city:

```
/country/united-states
/country/united-kingdom
/country/singapore
/city/new-york
/city/london
/city/singapore
```

**Pros:**
- ✅ SEO-friendly URLs
- ✅ Fast loading (static pages)
- ✅ Easy to crawl for Google
- ✅ Can pre-generate all pages at build time

**Cons:**
- ⚠️ Many pages to create (~10-20 countries, 50-100 cities)
- ⚠️ Requires dynamic route generation in Astro

**Implementation:**
1. Create `[country].astro` and `[city].astro` dynamic routes
2. Generate static paths for all unique countries/cities
3. Filter listings by country/city on each page
4. Update homepage to link to these pages

---

### Option B: Single Browse Page with Client-Side Filtering

One page `/browse` with JavaScript filtering:

**Pros:**
- ✅ Simple - one page
- ✅ Dynamic filtering without page reload
- ✅ Easy to maintain

**Cons:**
- ❌ Less SEO-friendly
- ❌ Requires JavaScript
- ❌ Slower initial load (all data loaded)

**Implementation:**
1. Create `/browse` page
2. Load all listings
3. Add filter dropdowns/buttons for country/city/category
4. Use JavaScript to show/hide listings

---

### Option C: Hybrid Approach (RECOMMENDED)

Static pages for major markets + browse page for all:

```
/browse                    (all listings, filterable)
/browse/united-states     (static page for USA)
/browse/singapore         (static page for Singapore)
/browse/united-kingdom    (static page for UK)
```

**Pros:**
- ✅ SEO-friendly for major markets
- ✅ Flexible browse page for smaller markets
- ✅ Best of both worlds

**Cons:**
- ⚠️ Slightly more complex
- ⚠️ Need to maintain both approaches

---

## Required Data Extraction

### 1. Extract Countries from Addresses

**Already done** (index.astro lines 30-48):
```javascript
const extractCountry = (address) => {
  // Returns last meaningful part (country name)
}
```

### 2. Extract Cities from Addresses

**Need to add:**
```javascript
const extractCity = (address) => {
  const parts = address.split(',').map(p => p.trim())
  if (parts.length < 2) return null

  // Second-to-last or third-to-last is usually city
  // "Street, City, State, PostalCode, Country"
  // Return city part
  if (parts.length >= 3) {
    return parts[parts.length - 3] // State/City before country
  }
  return parts[0] // First part if short address
}
```

### 3. Create Country/City Lists

```javascript
const countries = [...new Set(listings.map(l => extractCountry(l.address)))].filter(Boolean).sort()
const cities = [...new Set(listings.map(l => extractCity(l.address)))].filter(Boolean).sort()
```

---

## Homepage Changes

### Remove Listings Section

Current homepage shows all 127 listings. Change to:

1. **Stats** - Keep as-is
2. **International Coverage** - Keep, but make countries clickable
3. **Browse by Category** - Keep, make clickable
4. **Browse by Location** - New section with popular cities
5. **CTA** - Keep

**Remove:** Full listings display

**Add:** "Browse All Listings" button → `/browse`

---

## Implementation Steps

### Phase 1: Data Extraction (30 min)

1. Add `extractCity()` function
2. Create countries and cities arrays
3. Test extraction accuracy

### Phase 2: Homepage Updates (30 min)

1. Remove listings section
2. Make International Coverage countries clickable
3. Add "Browse by Location" section with top 10 cities
4. Add "Browse All Listings" button

### Phase 3: Create Browse Page (1 hour)

1. Create `/browse.astro`
2. Add filter controls (country, city, category dropdowns)
3. Display filtered listings
4. Add URL parameters for deep linking (`/browse?country=USA`)

### Phase 4: Create Static Country Pages (1 hour)

1. Create `/browse/[country].astro` dynamic route
2. Generate static paths for top 5-10 countries
3. Filter listings by country
4. Add breadcrumbs and navigation

### Phase 5: Testing (30 min)

1. Verify all countries/cities display correctly
2. Test filtering works
3. Check SEO meta tags
4. Verify mobile responsiveness

**Total: 3.5 hours**

---

## Sample Address Formats to Handle

Based on typical scraper data:

```
"123 Main St, New York, NY, 10001, United States"
"45 Oxford St, London, W1D 2DZ, United Kingdom"
"10 Orchard Road, Singapore, 238841"
"789 Bay St, Toronto, ON, M5G 2E3, Canada"
```

**Extraction challenges:**
- Different number of parts (3-5 components)
- Postal codes at different positions
- State/province sometimes included
- Need robust parsing

---

## SEO Considerations

### URL Structure

**Good:**
```
/browse/united-states
/browse/singapore
/browse/city/new-york
```

**Bad:**
```
/listings?filter=country&value=USA
/search?location=Singapore
```

### Meta Tags per Page

```html
<title>Testing Laboratories in United States | TSTR Hub</title>
<meta name="description" content="Find verified testing service providers in United States. Oil & Gas, Biopharma & Life Sciences, Environmental testing labs.">
```

### Breadcrumbs

```
Home > Browse > United States
Home > Browse > New York > Testing Labs
```

---

## Database Query Optimization

### Current Query (Loads All)

```javascript
const { data: listings } = await supabase
  .from('listings')
  .select('*')
  .eq('status', 'active')
```

### Filtered Query (For Country Pages)

```javascript
const { data: listings } = await supabase
  .from('listings')
  .select('*')
  .eq('status', 'active')
  .ilike('address', '%United States%')  // Filter by country
```

**Note:** Not ideal - better to add `country` and `city` columns to database.

---

## Future Enhancement: Add Country/City Columns

### Database Schema Update

```sql
ALTER TABLE listings ADD COLUMN country TEXT;
ALTER TABLE listings ADD COLUMN city TEXT;

-- Create indexes for faster filtering
CREATE INDEX idx_listings_country ON listings(country);
CREATE INDEX idx_listings_city ON listings(city);
```

### Populate from Existing Addresses

Run one-time migration script to extract and populate.

**Benefits:**
- ✅ Much faster filtering
- ✅ More accurate queries
- ✅ Can sort/group easily

**Downside:**
- ⚠️ Need to update scraper to populate these fields

---

## Next Session Checklist

When implementing filtered views:

- [ ] Decide: Option A (static pages), B (browse page), or C (hybrid)?
- [ ] Extract cities from all 127 addresses
- [ ] Test city extraction accuracy
- [ ] Update homepage to remove listings
- [ ] Create browse page with filters
- [ ] Test on multiple devices
- [ ] Check SEO meta tags
- [ ] Deploy and verify

---

## Current Status

**Homepage:**
- ✅ International Coverage section shows countries
- ✅ Extracts countries from addresses
- ⚠️ Currently may only show Singapore (extraction needs verification)
- ❌ Countries not clickable yet
- ❌ All listings still displayed on homepage

**Waiting for:**
- Deploy of country extraction fix (commit dc98383)
- Verification that multiple countries now display

---

**Agent:** Claude Code (Sonnet 4.5) - avztest8@gmail.com
**File:** /home/al/AI_PROJECTS_SPACE/FILTERED_VIEWS_TODO.md
**For:** Next session implementation
