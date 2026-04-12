# Architectural Strategy: Niche Localization, Programmatic SEO & Trust Standardization

## 0. Documented Strategy

### Executive Summary
The architecture balances internal flexibility with external rigidity. While a **Faceted Taxonomy (Tags)** handles database filtering, while **Dynamic SSR Landing Pages** capture long-tail SEO traffic. High-margin testing providers require **Standardized Trust Fields** (verified certifications) rather than pure templates. Standardization is the platform's protective moat.

### The "First Principles" Solution (Aggregate vs. Distribute)
1. **Global Level (SSR PSEO):** Create programmatic pages for the *industry concept* (e.g., `tstr.directory/standards/iso-17025/texas`). These pages list *all* matching companies for maximum Information Gain.
2. **Company Level (Mega-Profiles):** A specific branch (e.g., SGS Houston) gets **ONE extremely comprehensive Profile Page** at `/company/[slug]`. Navigation uses anchor links (`#certifications`, `#equipment`). 
3. **Group Level (Parent Brands):** Massive global groups (e.g., SGS) get a "Brand Aggregate Page" at `/group/[slug]`, consolidating global certifications and listing all local physical branches.

### The Monetization Funnel (Trust Tiers)
1. **Tier 1 (Aggregated - Free):** Scraped public data.
2. **Tier 2 (Claimed - Free):** User-reported data via domain-verified claiming.
3. **Tier 3 (TSTR Verified - Premium):** Manual/API verified certifications. Receives the "TSTR Verified" shield, RFP access, and rich media capabilities.

### Pricing Structure: Group vs. Single Company Economics
* **The Mechanism:** Billing is attached to the "Verified Branch" level but managed at the "Parent Group" level.
* **Single Company:** Pays a standard flat monthly fee (e.g., $99/mo) to upgrade their single `/company/[slug]` page to Tier 3.
* **Massive Groups (SGS):** The Parent Group claims the `/group/[slug]` page. We charge a tiered volume discount (e.g., 1-10 branches at 100%, 11-50 at 75%, 51+ at 40%).

---

## 1. Codebase Analysis & Required Changes

### Supabase Changes
**Current State:** Astro SSR is already configured (`output: 'server'`). `parent_listing_id` exists. `listing_capabilities.verified` exists but is currently writable by standard authenticated users.
**Required Updates:**
- **RLS Security Lockdown:** We must explicitly revoke update access to the `verified` column for standard users. 
  ```sql
  -- Drop existing permissive UPDATE policies
  DROP POLICY IF EXISTS "Admins can manage all capabilities" ON listing_capabilities;
  DROP POLICY IF EXISTS "Listing owners can manage their capabilities" ON listing_capabilities;

  -- Create strict admin-only policy for verified field
  CREATE POLICY "service_role_only_verified" ON listing_capabilities
  FOR UPDATE USING (
    (SELECT count(*) FROM auth.users WHERE id = auth.uid() AND raw_user_meta_data->>'is_admin' = 'true') > 0
    OR
    auth.jwt()->>'role' = 'service_role'
  );
  ```
- **Group Query View:** Create a Postgres View or RPC function that aggregates child branches and combined capabilities for a given `parent_listing_id`.

### Cloudflare Pages & Astro Changes
**Current State:** Routing handles `/[category]/index.astro` and `/[category]/[region]/index.astro` via SSR.
**Required Updates:**
- **Expand SSR Routing:** Create `src/pages/[category]/[standard]/[region]/index.astro`.
- **Edge Caching:** Because we use SSR for infinite PSEO route intersections, we **must** implement strict `Cache-Control` headers (e.g., `s-maxage=86400, stale-while-revalidate`) in our Astro responses so Cloudflare caches these at the Edge, preventing Supabase connection exhaustion.
- **Compliance Matrix Component:** Build a strict UI table component mapping verified standards with visual badges.

---

## 2. Recommended Agent Implementation Workflow

1. **Database Refinement (Supabase SQL)**
   - **Agent:** `ask-code` or `omg-executor`
   - **Task:** "Execute the RLS lockdown migration for `listing_capabilities` (service_role/admin only). Create an RPC function to aggregate child branches for Group pages."

2. **Frontend Architecture (Astro SSR & Edge Caching)**
   - **Agent:** `omg-executor`
   - **Task:** "Implement the new SSR routing structure (`/group/[slug]`, `/company/[slug]`, `/[category]/[standard]/[region]`). Implement Cloudflare Edge Cache-Control headers to protect Supabase."

3. **UI / Component Development**
   - **Agent:** `ask-gemini` 
   - **Task:** "Build the 'Compliance Matrix' and the 'Mega-Profile' layout utilizing Tailwind CSS. Ensure Tier 3 verification badges are prominently displayed."

4. **Data Population (Python Scrapers)**
   - **Agent:** `qwen`
   - **Task:** "Update Python scrapers to identify Parent companies vs Branches, and populate the `parent_listing_id`."
