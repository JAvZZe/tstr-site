# HANDOFF: Search API Location Filter Bug

## Date: 2026-03-19

## Agent: opencode

## Status: UNRESOLVED

---

## Issue Summary

**Critical Bug**: Search API `/api/search/by-standard` fails when `location` parameter is provided.

### Error

```
"failed to parse logic tree ((location.name.ilike.%United States%,location.parent.name.ilike.%United States%,location.parent.parent.name.ilike.%United States%,address.ilike.%United States%))" (line 1, column 13)
```

### Affected URL Pattern

```
/api/search/by-standard?standard=ISO+14687&location=United+States
```

### Works Without Location

```bash
curl "https://tstr.directory/api/search/by-standard?standard=ISO%2014687"
# Returns: {"count": 7, "results": [...]}
```

---

## Root Cause Analysis

**File**: `web/tstr-frontend/src/pages/api/search/by-standard.ts`

The query uses a nested join:

```typescript
let query = supabase
  .from('listings')
  .select(
    `
    ...,
    listing_capabilities(
      standard:standard_id!inner(...)
    )
  `
  )
  .eq('listing_capabilities.standard.code', standard);
```

When `.or()` is applied for location filtering, Supabase cannot parse the combined logic tree due to the `!inner` join on nested `listing_capabilities`.

---

## Fix Attempts (All Failed)

### Attempt 1: String concatenation in .or()

```typescript
query = query.or(`location.name.ilike.%${location}%,...`);
```

**Result**: Same error

### Attempt 2: Method chaining

```typescript
query = query
  .or(`location.name.ilike.%${location}%`)
  .or(`location.parent.name.ilike.%${location}%`)
  ...
```

**Result**: Same error

### Attempt 3: Single condition only

```typescript
query = query.or(`location.name.ilike.%${location}%`);
```

**Result**: Same error

### Attempt 4: ilike on address only

```typescript
query = query.ilike('address', `%${location}%`);
```

**Result**: Code ready in file but Cloudflare not rebuilding with changes

---

## Recommended Solutions

### Option A: Two-Phase Query (Recommended)

1. Fetch listings by standard (no location filter)
2. Filter results in JavaScript by checking location hierarchy

### Option B: Supabase RPC Function

Create a database function to handle complex filtering with joins.

### Option C: Simplify Location Filter

1. Remove location hierarchy search
2. Use only address field for location filtering
3. Note: Code ready in file at line 82-87

---

## Current Code State

**File**: `web/tstr-frontend/src/pages/api/search/by-standard.ts`

**Lines 82-87** (current state - not deployed):

```typescript
if (location) {
  query = query.ilike('address', `%${location}%`);
}
```

**Should be replaced with** (location hierarchy + address):

```typescript
if (location) {
  const locationConditions = [
    `location.name.ilike.%${location}%`,
    `location.parent.name.ilike.%${location}%`,
    `location.parent.parent.name.ilike.%${location}%`,
    `address.ilike.%${location}%`,
  ].join(',');
  query = query.or(locationConditions);
}
```

---

## Test Commands

```bash
# Works - no location
curl "https://tstr.directory/api/search/by-standard?standard=ISO%2014687" | jq '.count'

# Fails - with location
curl "https://tstr.directory/api/search/by-standard?standard=ISO%2014687&location=United%20States" | jq '.count'
```

---

## Related Files

- `/api/search/by-standard.ts` - Main API endpoint (broken)
- `/search/standards.astro` - Frontend page that calls the API
- `supabase/migrations/20260319000001_add_hydrogen_standards.sql` - New standards (working)

---

## Context: What Was Completed

Despite the bug, the following was successfully completed:

1. ✅ **15 new hydrogen standards added** to database (40→55)
2. ✅ **ASTM G142 now exists** in standards table
3. ✅ **Git PRs merged** to main branch
4. ✅ **Cloudflare rebuild triggered** automatically

The bug only affects search when location filter is applied.

---

## Next Agent Actions

1. Fix the location filter in `search/by-standard.ts`
2. Test with: `curl "https://tstr.directory/api/search/by-standard?standard=ISO%2014687&location=United%20States"`
3. Build: `cd web/tstr-frontend && npm run build`
4. Deploy: Push to GitHub
5. Verify at: https://tstr.directory/search/standards
