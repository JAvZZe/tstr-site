# Frontend Library Utilities

This directory contains shared utilities and configurations for the TSTR.directory frontend.

## Files

### `contacts.ts` - CENTRALIZED Contact Configuration ⚠️ IMPORTANT

**Purpose**: Single source of truth for ALL contact email addresses across the site.

**What it contains**:
- `CONTACTS` object with all email addresses (sales, support, partnerships, etc.)
- `getMailtoLink()` helper function for generating mailto: links
- `MAILTO_LINKS` pre-configured mailto links for common actions

**Why it exists**:
- Change email address once, updates everywhere
- Prevents hardcoded emails scattered across codebase
- Type-safe email references (TypeScript autocomplete)
- Easy to manage as project scales

**How to use**:

```astro
---
import { CONTACTS, MAILTO_LINKS, getMailtoLink } from '../lib/contacts'
---

<!-- Use pre-configured mailto link -->
<a href={MAILTO_LINKS.professionalPlan}>Upgrade to Professional</a>

<!-- Reference email address directly -->
<p>Contact us at {CONTACTS.support}</p>

<!-- Create custom mailto link -->
<a href={getMailtoLink('sales', 'Custom Subject', 'Email body text')}>
  Custom Link
</a>
```

**CRITICAL RULES**:
1. ✅ **ALWAYS import from** `contacts.ts` when adding contact info
2. ❌ **NEVER hardcode** email addresses like `mailto:email@example.com`
3. ✅ **UPDATE** `contacts.ts` when changing email addresses
4. ❌ **DON'T** create duplicate contact configs elsewhere

**Current email**: All contacts route to `tstr.site1@gmail.com`

---

### `supabase.ts` - Supabase Client (Server-Side)

Server-side Supabase client for use in Astro page frontmatter.

**Usage**:
```astro
---
import { supabase } from '../lib/supabase'

const { data, error } = await supabase
  .from('listings')
  .select('*')
---
```

---

### `supabase-browser.ts` - Supabase Client (Browser-Side)

Client-side Supabase client for use in browser scripts.

**Usage**:
```typescript
import { supabaseBrowser } from '../lib/supabase-browser'

// In client-side script
const { data } = await supabaseBrowser.auth.signIn({ email, password })
```

---

## Adding New Utilities

When adding new shared utilities:

1. Create the file in `src/lib/`
2. Export named exports (not default)
3. Document usage in this README
4. Add TypeScript types for all exports

## Questions?

See project documentation:
- Main docs: `/TSTR.md`
- Monetization: `/MONETIZATION_IMPLEMENTATION.md`
