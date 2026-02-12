# JSON-LD Fix for Google Search Console Error

**Created**: 2026-01-01
**Status**: ✅ FIX IMPLEMENTED - NEEDS DEPLOY

## Problem

Google Search Console reported:
> `https://tstr.directory/` : Parsing error: Missing '}' or object member name

**Root Cause**: The JSON-LD in `index.astro` used double curly braces `{{` which Astro outputted literally as `{{` instead of valid JSON braces `{`.

## Fix Applied

**File**: `web/tstr-frontend/src/pages/index.astro` (lines 125-135)

**Before** (invalid):
```astro
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  ...
}}
</script>
```

**After** (valid):
```astro
<script type="application/ld+json" set:html={JSON.stringify({
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "TSTR Hub",
  "description": "Specialist Testing Services, Products and Solutions Directory",
  "url": "https://tstr.directory",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://tstr.directory/browse?search={search_term_string}",
    "query-input": "required name=search_term_string"
  }
})} />
```

## Deploy Instructions

```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working

# 1. Verify the fix is in place
grep -A 5 "application/ld+json" web/tstr-frontend/src/pages/index.astro

# 2. Commit the fix
git add web/tstr-frontend/src/pages/index.astro
git commit -m "fix: JSON-LD parsing error - use JSON.stringify for valid output

Fixes Google Search Console error: Missing '}' or object member name
Changed from double braces {{ to JSON.stringify() with set:html directive"

# 3. Push to trigger Cloudflare Pages deployment
git push origin main
```

## Verification

After deploy, validate at: https://search.google.com/test/rich-results?url=https://tstr.directory/

Expected: No JSON-LD parsing errors.

## Notes

- Other pages (`hydrogen-testing.astro`, `iso-19880-3.astro`) use static JSON without Astro expressions - no fix needed
- Build tested locally - succeeds
