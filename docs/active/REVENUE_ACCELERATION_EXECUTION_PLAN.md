# Revenue Acceleration Execution Plan

> **Owner**: Codex strategic lead
> **Created**: 2026-05-04
> **Status**: Active execution plan
> **Goal**: Move TSTR.directory closer to revenue by increasing buyer RFQs, lab profile claims, and listing trust density.

---

## Strategic Thesis

TSTR.directory is no longer just a generic testing directory. It has three monetizable assets:

1. **High-intent search pages** for standards, industries, and regions.
2. **Sparse but growing listings** that can become procurement-grade profiles.
3. **Hydrogen infrastructure testing** as the strongest premium niche, with standards, pages, and capability mappings already progressed.

The next sprint must improve conversion and perceived value. Do not add broad features until the core buyer journey is clearer:

`Search need -> credible listing/landing page -> RFQ submitted -> lab claim or paid upgrade`.

---

## Non-Negotiable Guardrails

- **Do not merge `hydrogen-standards`**. It is a stale branch with high-value standards data. Manually inspect and extract useful data only.
- **Do not invent certifications, capabilities, contact data, or accreditation claims**. Every enriched field must have a source, confidence, or `needs_verification` marker.
- **Do not make a new marketing landing page before improving the actual search/listing/RFQ experience**.
- **Do not bury the RFQ action**. Buyer-facing pages should make quote/contact submission obvious.
- **Do not optimize for vanity traffic alone**. The sprint metric is RFQs and claims, not page count.
- **Update `PROJECT_STATUS.md` after successful work** and document changes that affect the live site.

---

## Current Baseline

Known from project docs and source:

- Frontend: Astro + React on Cloudflare Pages.
- Database: Supabase.
- Active listings: `781` reported in `PROJECT_STATUS.md`.
- Categories: `33+ specialized (+3 Hydrogen)`.
- Hydrogen page: `web/tstr-frontend/src/pages/hydrogen-testing.astro`.
- Listing template: `web/tstr-frontend/src/pages/listing/[slug].astro`.
- Browse/search: `web/tstr-frontend/src/pages/browse.astro`.
- PSEO route: `web/tstr-frontend/src/pages/testing/[industry]/[slug].astro`.
- RFQ modal: `web/tstr-frontend/src/components/ContactLabModal.tsx`.
- Enrichment automation exists: `web/tstr-automation/enrich_listings.py` and `web/tstr-automation/ENRICHMENT_AUTOMATION_HANDOFF.md`.
- Hydrogen taxonomy/capability migration exists: `supabase/migrations/20260417_hydrogen_taxonomy_final.sql`.
- IAF verification plan exists: `docs/active/IAF_API_INTEGRATION_PLAN.md`.

---

## Sprint Outcome

After this sprint, a buyer should be able to land on TSTR, understand what it is, find a relevant testing provider, trust why that provider is listed, and submit an RFQ with low friction.

A lab owner should see enough profile value and lead potential to claim or upgrade a profile.

---

## Track A: Listing Value Density

**Objective**: Make listings feel procurement-grade instead of sparse.

### Agent Assignment

Use a data/enrichment agent. Good fit: Gemini Pro or local CLI agent with Supabase/read-only database access.

### Tasks

1. Create a listing completeness audit.
   - Score active listings by populated fields:
     - `description`
     - `website`
     - `website_verified`
     - `phone`
     - `email`
     - `category`
     - `location`
     - `listing_capabilities`
     - `listing_custom_fields`
     - `claimed`
     - `trust_score`
   - Output top gaps by category and region.

2. Prioritize enrichment targets.
   - First priority: Hydrogen infrastructure listings.
   - Second priority: Materials/A2LA listings.
   - Third priority: Europe and Middle East listings added in v2.6.0.

3. Define the public profile fields.
   - At minimum:
     - Accreditation body
     - Certificate or standard code
     - Capability/scope summary
     - Source URL
     - Last checked date
     - Confidence level
     - Claim status

4. Improve the listing page template.
   - Add an **At a Glance** block.
   - Add **Accreditation Evidence** when sourced data exists.
   - Add **Testing Capabilities** in a scannable matrix/list.
   - Add a visible **Request Quote** CTA near the top and in the sidebar.
   - Keep claim CTA, but make it secondary to buyer RFQ for unclaimed listings.

### Acceptance Criteria

- At least one completeness report exists.
- Listing page can show richer fields without breaking sparse records.
- Sparse records show useful fallback states, not empty panels.
- Hydrogen listings visibly communicate why they are valuable.

---

## Track B: Hydrogen Revenue Track

**Objective**: Treat Hydrogen as a premium revenue wedge, not just another category.

### Why Hydrogen Is Priority

Hydrogen testing has high commercial intent and low supply. Buyers search by exact standards and equipment constraints:

- `ISO 19880-3`
- `ISO 19880-5`
- `ISO 14687`
- `ISO 11114-4`
- `ASTM G142`
- `SAE J2601`
- `700 bar`
- `hydrogen embrittlement`
- `cryogenic hydrogen`

The existing implementation already has a Hydrogen hub, standards mappings, and archived strategy. The sprint should turn that progress into a buyer journey and outreach asset.

### Agent Assignment

Use a Hydrogen/data agent. Good fit: Gemini Pro for standards/source review, plus a coding agent for template changes.

### Tasks

1. Audit Hydrogen data state.
   - Verify category IDs and standards in:
     - `supabase/migrations/20260417_hydrogen_taxonomy_final.sql`
     - `supabase/migrations/20260319000001_add_hydrogen_standards.sql`
     - `management/verify_hydrogen_category.py`
   - Confirm which Hydrogen listings have actual capabilities.
   - Confirm whether the page count and matrix count match database reality.

2. Extract value from stale branch without merging.
   - Inspect `hydrogen-standards`.
   - Manually extract missing standards, source links, and descriptions.
   - Compare against current `main` standards.
   - Produce a small extraction report before any database or code changes.

3. Improve Hydrogen landing UX.
   - Update `web/tstr-frontend/src/pages/hydrogen-testing.astro`.
   - Make the hero immediately answer:
     - what this page is for,
     - which standards it covers,
     - what buyers can do next.
   - Replace vague premium wording with buyer intent:
     - "Find hydrogen testing labs for ISO 19880-3, 700 bar, embrittlement, purity, and fuel-cell infrastructure."
   - Keep the technical matrix, but add clear RFQ action near it.

4. Build Hydrogen profile density.
   - For each priority lab, show:
     - H2 standards
     - pressure/temperature capabilities where sourced
     - equipment/source evidence
     - region and contact/RFQ path
   - Start with the known premium lab set from the Hydrogen page:
     - TÜV SÜD
     - Powertech Labs
     - Element Materials Technology
     - Kiwa Technology
     - SGS
     - WHA International

5. Create Hydrogen RFQ path.
   - Pre-fill `ContactLabModal` with Hydrogen context.
   - If no exact lab is selected, route to a multi-provider concierge RFQ.
   - Capture standard, pressure requirement, component type, region, and urgency.

### Acceptance Criteria

- Hydrogen page has a clear buyer journey: compare -> select/request quote -> concierge fallback.
- Hydrogen listings show standards/capability evidence where available.
- No stale branch merge occurred.
- Any new standards/capabilities are source-backed.
- At least one Hydrogen RFQ path can be tested end-to-end locally.

---

## Track C: Landing Page and Main UX Clarity

**Objective**: Clarify what TSTR is and reduce friction for buyers.

### Agent Assignment

Use a frontend/conversion agent. File ownership:

- `web/tstr-frontend/src/pages/index.astro`
- `web/tstr-frontend/src/pages/browse.astro`
- `web/tstr-frontend/src/pages/testing/[industry]/[slug].astro`
- `web/tstr-frontend/src/components/ContactLabModal.tsx`

### Tasks

1. Homepage clarity.
   - Use buyer language:
     - "Find accredited testing laboratories and request quotes."
   - Keep "specialist testing" as positioning, but avoid relying on "Testers" as the main noun.
   - Add clear buyer CTA:
     - `Find Testing Labs`
     - `Request a Quote`
   - Add lab-owner CTA:
     - `Claim Your Profile`

2. Browse page conversion.
   - Add `Request Quote` or `Ask TSTR to source providers` to listing cards.
   - Keep `Visit Website`, but do not make it the only strong action.
   - Add visible low-density concierge CTA when filters return few results.

3. RFQ modal friction.
   - Required fields should be minimal:
     - name
     - business email
     - company
     - message/requirement
   - Make industry, role, urgency, and standard optional or pre-filled where route context exists.
   - Preserve buyer account upsell only after successful submission.

4. PSEO page practicality.
   - Replace generic grand copy with useful procurement content:
     - What the standard is.
     - Who needs it.
     - What to ask the lab.
     - What evidence to request.
     - Related standards.
   - Keep FAQ schema, but avoid claims that imply independent verification unless source-backed.

### Acceptance Criteria

- Buyer understands the site in 5 seconds from the homepage.
- Main CTAs map to revenue: RFQ, concierge request, claim.
- RFQ modal is shorter and context-aware.
- PSEO pages are practical, not just decorative SEO.

---

## Track D: Verification and Revenue Instrumentation

**Objective**: Make sure improvements can be measured.

### Tasks

1. Verify the lead/RFQ pipeline.
   - Test listing page -> RFQ modal -> `/api/leads`.
   - Test Hydrogen page -> RFQ modal.
   - Test PSEO page `#rfq` deep link.

2. Track conversion events.
   - RFQ opened.
   - RFQ submitted.
   - Website click.
   - Claim CTA clicked.
   - Concierge request clicked.

3. Check visual UX.
   - Use Playwright screenshots at desktop and mobile.
   - Inspect homepage, browse, one listing, Hydrogen page, one PSEO page.
   - Check that CTAs are visible without awkward scrolling or overlap.

4. Check build.
   - Run frontend build in `web/tstr-frontend`.
   - If root lint fails on vendored/archived files, document as unrelated lint debt and do not broaden scope.

### Acceptance Criteria

- Local build succeeds or failure is documented with exact blocker.
- RFQ flow works on at least one representative route.
- Screenshots reviewed for desktop/mobile.
- `PROJECT_STATUS.md` updated.

---

## Execution Sequence

Agents must follow this order:

1. **Audit first**
   - Listing completeness.
   - Hydrogen data state.
   - Existing RFQ path.

2. **Improve templates second**
   - Listing page.
   - Hydrogen page.
   - RFQ modal.
   - Homepage/browse CTAs.

3. **Enrich data third**
   - Hydrogen first.
   - Materials/A2LA second.
   - Europe/Middle East third.

4. **Verify fourth**
   - Build.
   - Screenshots.
   - RFQ submission.
   - No false claims.

5. **Document last**
   - Update `PROJECT_STATUS.md`.
   - Add session notes.
   - Commit with clear scope.

---

## Anti-Drift Rules for Agent Leads

Use this checklist every time an agent reports progress:

- Did this increase RFQ, claim, or profile-upgrade likelihood?
- Did it improve trust density on actual listings?
- Did it preserve source-backed claims?
- Did it include Hydrogen as a premium track?
- Did it avoid merging stale branches?
- Did it avoid unrelated refactors?
- Did it leave a verifiable build/test path?

If the answer is "no" to the first two questions, stop that work and redirect.

---

## Suggested Agent Prompts

### Prompt 1: Listing Completeness Audit

```text
You are the TSTR listing data audit agent. Bootstrap first. Do not edit templates. Query or inspect the code/data paths needed to score active listings for completeness. Prioritize Hydrogen, Materials/A2LA, Europe, and Middle East. Produce a concise report with field coverage, top sparse categories, and the top 50 enrichment targets. Do not invent data. List exact files or queries used.
```

### Prompt 2: Hydrogen Data and Standards Audit

```text
You are the TSTR Hydrogen data agent. Bootstrap first. Inspect current main plus the stale `hydrogen-standards` branch without merging it. Identify missing or better Hydrogen standards, descriptions, source URLs, and lab capability mappings. Produce an extraction report and proposed patch plan. Do not modify production data until reviewed. Do not merge the stale branch.
```

### Prompt 3: Conversion Template Implementation

```text
You are the TSTR conversion frontend agent. Bootstrap first. Own only homepage, browse, listing detail, Hydrogen page, PSEO page, and RFQ modal files. Implement clearer buyer CTAs, lower-friction RFQ, richer listing fallback sections, and Hydrogen buyer journey improvements. Do not touch scrapers or database migrations. Run build and provide screenshots or exact verification notes.
```

### Prompt 4: Verification Agent

```text
You are the TSTR verification agent. Bootstrap first. Review the implementation against the Revenue Acceleration Execution Plan. Test build, RFQ flow, Hydrogen page, listing page, browse page, and one PSEO page. Report only blockers, regressions, missing acceptance criteria, and residual risk.
```

---

## Definition of Done

This plan is done when:

- Hydrogen is visibly treated as a premium niche with credible standards/capability evidence.
- Listing pages feel materially less sparse.
- Buyer RFQ path is obvious and lower friction.
- Homepage and browse clearly communicate the product.
- At least one representative RFQ journey is verified.
- Agents have documented what changed and why in `PROJECT_STATUS.md`.

