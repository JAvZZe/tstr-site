# Static Prerendering Standard for Listing Pages

**Date**: 2025-11-23
**Status**: ✅ IMPLEMENTED & DEPLOYED
**Applies to**: All listing detail pages (`/listing/[slug]`)

---

## Problem Statement

**Before**: Listing pages used SSR (Server-Side Rendering) with `prerender: false`

**Issues**:
1. Google crawls slower (SSR = dynamic content, less trust)
2. ISO standards hidden from HTML source (no SEO value)
3. Page generation happens at request time (slower TTFB)
4. No static HTML for search engines to index

**SEO Impact**: "ISO 19880-3 testing TÜV SÜD" searches wouldn't find individual lab pages

---

## Solution: Static Shell + Client-Side Vault

**Architecture** (recommended by Gemini 2.5 Pro):

### Static Shell (Build Time - Server)
Generate prerendered HTML containing **public "teaser" data**:
- ✅ Business name
- ✅ Description (full text for keyword ranking)
- ✅ Location/address (local SEO)
- ✅ Website URL (link authority)
- ✅ **ISO standards & certifications** (CRITICAL for SEO keywords)

### Client-Side Vault (Runtime - Browser)
Use Astro Islands to gate **sensitive data**:
- ❌ Phone number (privacy)
- ❌ Email address (privacy)
- Future: Use `<PremiumContactInfo client:visible>` component to check auth and fetch via API

**Result**: SEO gets all content it needs, sensitive data protected via client-side checks.

---

## Implementation

### 1. Enable Prerendering

```typescript
// src/pages/listing/[slug].astro
export const prerender = true; // Changed from false

export async function getStaticPaths() {
  const { data: listings } = await supabase
    .from('listings')
    .select('slug')
    .eq('status', 'active')
    .order('created_at', { ascending: false });

  return listings.map(listing => ({
    params: { slug: listing.slug }
  }));
}
```

### 2. Fetch Standards/Capabilities

**CRITICAL**: Listings have TWO sources of certifications:

```typescript
// Custom fields (category-specific)
const { data: customFieldValues } = await supabase
  .from('listing_custom_fields')
  .select(`
    value,
    custom_field:custom_field_id (field_name, field_label, field_type)
  `)
  .eq('listing_id', listing.id);

// Standards (ISO/SAE codes) ← MUST FETCH FOR SEO
const { data: capabilities } = await supabase
  .from('listing_capabilities')
  .select(`
    standard:standard_id (code, name, description)
  `)
  .eq('listing_id', listing.id);

// Combine both
const customFields = customFieldValues?.map(cf => ({
  name: cf.custom_field.field_label,
  value: formatFieldValue(cf.value),
  type: cf.custom_field.field_type
})) || [];

const standards = capabilities?.map(cap => ({
  name: cap.standard.code,     // e.g., "ISO 19880-3"
  value: cap.standard.name,     // e.g., "Hydrogen Valves"
  type: 'standard'
})) || [];

const allCertifications = [...customFields, ...standards];
```

### 3. Set Visibility Rules (SEO-First)

```typescript
// SEO-optimized for static build
const canViewFullAddress = true;     // Show for local SEO
const canViewPhone = false;          // Hide (can gate client-side)
const canViewEmail = false;          // Hide (can gate client-side)
const canViewWebsite = true;         // Always show (public + SEO)
const canViewCertifications = true;  // Always show (ISO keywords)

// Show full description (not truncated preview)
const descriptionPreview = listing.description || null;
```

### 4. Render Certifications Section

```astro
{allCertifications.length > 0 && (
  <div class="custom-fields">
    <h2>Certifications & Capabilities</h2>
    {allCertifications.map(field => (
      <div class="field-item">
        <div class="field-name">{field.name}</div>
        <div class="field-value">{field.value}</div>
      </div>
    ))}
  </div>
)}
```

---

## SEO Benefits

### Before (SSR)
```html
<!-- Dynamic rendering, no static HTML -->
<script>fetch('/api/listing/...')</script>
```

### After (SSG)
```html
<!-- Static HTML, instant indexing -->
<h1>TÜV SÜD - Hydrogen Testing</h1>
<p>Global leader in hydrogen infrastructure testing...</p>
<div class="field-item">
  <div class="field-name">ISO 19880-3</div>
  <div class="field-value">Hydrogen Valves Testing</div>
</div>
<div class="field-item">
  <div class="field-name">ISO 11114-4</div>
  <div class="field-value">Embrittlement Testing</div>
</div>
```

**Google sees**: "ISO 19880-3", "ISO 11114-4", "TÜV SÜD", "hydrogen testing" in HTML source.

---

## Build Output

**Result**: 183 static pages generated (one per active listing)

```
10:48:56 ▶ src/pages/listing/[slug].astro
10:48:57   ├─ /listing/tuv-sud---hydrogen-testing/index.html (+602ms)
10:48:57   ├─ /listing/kiwa-technology---h2-testing/index.html (+601ms)
10:48:58   ├─ /listing/npl---national-physical-laboratory/index.html (+600ms)
10:48:58   ├─ /listing/powertech-labs---h2-tank-testing/index.html (+599ms)
...
10:49:01   └─ /listing/examat-pte-ltd/index.html (+591ms)
```

**Verification**:
```bash
# Check if ISO standards appear in static HTML
cat dist/listing/tuv-sud---hydrogen-testing/index.html | grep "ISO 19880-3"
# Output: ISO 19880-3 ✅
```

---

## Deployment

**GitHub**: Commit changes to `/src/pages/listing/[slug].astro`
**Cloudflare Pages**: Auto-deploys on push to main
**Sitemap**: Automatically updated to include all listing URLs

**Live URLs** (after deployment):
- https://tstr.site/listing/tuv-sud---hydrogen-testing
- https://tstr.site/listing/powertech-labs---h2-tank-testing
- https://tstr.site/listing/element-materials---embrittlement-lab
- + 180 more

---

## Future Enhancements (Optional)

### Client-Side Premium Gating

Create component for sensitive data:

```typescript
// src/components/PremiumContactInfo.tsx
export default function PremiumContactInfo({ listingId }) {
  const [contact, setContact] = useState(null);

  useEffect(() => {
    const token = getAuthToken();
    if (token) {
      fetch(`/api/listings/${listingId}/contact`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(res => res.json())
        .then(setContact);
    }
  }, [listingId]);

  return contact ? (
    <div>
      <p>Phone: {contact.phone}</p>
      <p>Email: {contact.email}</p>
    </div>
  ) : (
    <div>
      <p>Sign up to view contact details</p>
      <a href="/signup">Sign Up Free</a>
    </div>
  );
}
```

Use in Astro:
```astro
<PremiumContactInfo client:visible listingId={listing.id} />
```

---

## Gotchas & Lessons Learned

### 1. Missing Footer Import
**Error**: `Footer is not defined`
**Fix**: Add `import Footer from '../../components/Footer.astro'` at top

### 2. Custom Fields vs Capabilities
**Issue**: Standards weren't showing initially
**Cause**: Fetched only `listing_custom_fields`, not `listing_capabilities`
**Fix**: Fetch both and combine into `allCertifications` array

### 3. Disk Space During Build
**Issue**: Local build failed with "No space left on device"
**Cause**: 183 static pages + node_modules filled 80GB partition
**Impact**: Local builds affected, but Cloudflare Pages builds on their servers (unaffected)
**Prevention**: Monitor with `df -h /home`, clean `dist/` and caches regularly

### 4. Category Assignment Errors
**Issue**: 3 whale labs were in wrong category (Oil & Gas instead of Hydrogen)
**Cause**: Script used wrong `category_id` during bulk insert
**Fix**: SQL UPDATE to correct category
**Prevention**: Always verify `category_id` matches intended `category.slug`

---

## Maintenance

**When adding new listings**:
1. Ensure `status = 'active'` (included in build)
2. Add capabilities via `listing_capabilities` table (not just custom fields)
3. Trigger rebuild: `git commit --allow-empty -m "chore: Trigger rebuild" && git push`

**When updating existing listings**:
1. Changes to database reflected on next build
2. Cloudflare Pages auto-rebuilds on git push
3. No manual rebuild needed for production

**Build time**: ~2 minutes for 183 pages (acceptable)

---

## Success Metrics

**Build**: ✅ 183 pages generated
**Standards visible**: ✅ ISO codes in HTML source
**Deployment**: ✅ Live on https://tstr.site/listing/*
**SEO**: 🔄 Pending Google indexing (24-48 hours)

**Next**: Monitor Search Console for:
- "ISO 19880-3 testing" impressions
- "TÜV SÜD hydrogen" clicks
- Individual listing page indexing

---

## Related Files

- `/src/pages/listing/[slug].astro` - Main listing page template
- `/src/lib/supabase.ts` - Supabase client
- `/src/lib/redirect.ts` - Click tracking for outbound links
- `/src/components/Footer.astro` - Footer component

**Git Commits**:
- `ffdfc49` - Enable static prerendering (2025-11-23)
- `2687c6c` - Trigger rebuild after database fix (2025-11-23)

---

**Standard established**: 2025-11-23
**Status**: Production-ready, deployed, SEO-optimized ✅
