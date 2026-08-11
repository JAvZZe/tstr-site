# Hydrogen-Embrittlement Showcase Listing — Execution Plan

> **For Hermes:** Use subagent-driven-development skill to implement task-by-task.
> **Status:** PLAN ONLY — no execution yet. Several open decisions below require user sign-off (esp. the DB write path).

**Goal:** Build ONE exemplary "Premium" lab listing (Hydrogen Embrittlement) that (a) surfaces a lab's real certifications/standards/services in rich, filterable, citable detail, and (b) is reachable via a working search path — so we can sell the lab a paid listing and prove to buyers TSTR is where to find them.

**Architecture:** Enhance the existing `listing/[slug].astro` detail page + add a capability-detail component that reads the already-present-but-empty `listing_capabilities.specifications` (JSON) and `certifications` tables. Backfill those fields for ONE showcase lab (Assured Testing Services). Make the existing `/api/search/by-standard` API reachable from the UI so buyers can filter by standard + parameter + location. Build the showcase as a reusable TEMPLATE (any premium lab that populates `specifications`/`certifications` gets the same treatment) — the template IS the sellable product.

**Tech Stack:** Astro 6 + React 18 + Tailwind (frontend), Supabase Postgres (data), Cloudflare Pages (deploy). No new runtime deps.

---

## 1. Verified Ground Truth (from live read-only probe, 2026-08-11)

- 9 labs carry hydrogen-embrittlement capability: TÜV SÜD, Element Materials, Element "Embrittlement Lab", CSA Group, SwRI, Kiwa, WHA, Powertech, **Assured Testing Services** (`slug: hydrogen-embrittlement-testing-astm-f519-assured-testing-services-1994`).
- `standards` catalog is real but polluted with junk generic rows: `EMBRITTLEMENT`, `H2-TANK`, `H2-SAFETY` (these poison search + look amateur).
- `listing_capabilities.specifications` is `{}` and `notes` mostly NULL on every sampled row; only 1/3 were `verified`. → The filterable detail we need is absent today.
- `certifications` table exists (`issuing_body`, `name`, `issued_date`, `expiry_date`, `confidence`, `source`) and is essentially unused.
- `/api/search/by-standard?standard=ISO%2011114-4` works and returns labs; UI never exposes parameter filtering (`specifications` contains query is supported server-side but not surfaced).
- Detail page (`listing/[slug].astro`, 613 lines) renders capabilities as a flat 2-col grid of code+name. No test method, scope, equipment, accreditation badge, or FAQ. JSON-LD has a basic FAQPage but generic.

## 2. DECISIONS TAKEN (judgement, correct me if wrong)

- **Showcase lab = Assured Testing Services.** Rationale: our buyer is the *lab*; the most persuasive asset is showing a *small specialist peer* we made premium + findable — not a famous TÜV/SGS that wouldn't buy.
- **Build as reusable template, not one-off.** The decorated rendering keys off `listing_capabilities.specifications` + `certifications`; Assured is merely the first fully-populated instance.
- **Decorate with publicly-published facts only** (standard test methods, ISO 17025 accreditation bodies) — no fabricated claims. Showcase must carry a visible "Featured Showcase" badge so buyers aren't misled.

## 3. OPEN QUESTIONS FOR USER (blockers / corrections)

1. **DB WRITE PATH (CRITICAL).** On-disk Supabase service-role key is dead (post-2026-08-10 rotation). `listing_capabilities.specifications` / `certifications` backfill = writes. Options: (a) run seed on OCI where scraper env is live (`ssh opc@84.8.139.90`), (b) user provides a valid service-role key, (c) stage as a migration file the user applies. Plan cannot execute Phase 1 until resolved.
2. Is backfilling Assured's real published capabilities + accreditation (badged "Featured Showcase") acceptable, or do you want a clearly-fictional demo tenant instead?
3. Scope: just the one showcase listing, or also build the reusable template (recommended — it's the actual product)?

## 4. PHASE 0 — Data hygiene (prerequisite, no UI)

### Task 0.1: Quarantine junk `standards` rows
**Objective:** Remove `EMBRITTLEMENT` / `H2-TANK` / `H2-SAFETY` generic rows from search/catalog.
**Files:** `web/tstr-frontend/supabase/migrations/`, new `NNNN_quarantine_junk_standards.sql`
**Step 1:** `UPDATE standards SET is_active = false WHERE code IN ('EMBRITTLEMENT','H2-TANK','H2-SAFETY');` (keep rows to avoid FK breakage; just hide).
**Step 2:** Verify: `curl -s "$B/rest/v1/standards?is_active=eq.true&category_id=eq.f29966a2-...&select=code"` returns only real codes.
**Step 3:** Commit migration.
**RISK:** Any capability row pointing at junk codes becomes orphaned in UI — re-map those 3 capabilities to the proper standard_id before hiding (check first).

### Task 0.2: Define canonical `specifications` schema (doc)
**Objective:** One shared JSON key set so every embrittlement capability renders consistently.
**Files:** `docs/capability_specifications_schema.md` (new)
**Schema (proposed):**
```json
{
  "test_methods": ["Slow Strain Rate (SSR)", "Rising Load"],
  "max_pressure_bar": 1050,
  "temperature_range_c": "-70 to 200",
  "sample_geometry": "Notched round tensile, C-ring",
  "standards_scope": "ASTM F519 Method A/B",
  "accreditation": "ISO/IEC 17025 (A2LA)",
  "turnaround_days": 10,
  "quote_based": true
}
```
**Step:** Commit doc. Used by Task 2.1 rendering.

## 5. PHASE 1 — Backfill showcase data (BLOCKED on open Q1)

### Task 1.1: Seed Assured `listing_capabilities` rich rows
**Objective:** Populate `specifications` + `notes` + `verified=true` for Assured's real embrittlement standards.
**Files:** migration/seed `NNNN_seed_assured_showcase.sql` (or OCI script).
**Step:** For `listing_id = 04b5c9ae-470c-420b-8ce9-4a50897cd653`, upsert capabilities for ASTM F519 (`4e470799-...`), ASTM F1459-06 (`09ec64cd-...`), ASTM G142 (`27ca1599-...`), ISO 11114-4 (`53fe12cc-...`) with the schema from 0.2.
**Verify:** `curl ".../listing_capabilities?listing_id=eq.04b5c9ae...&select=specifications,verified"` shows populated JSON.

### Task 1.2: Seed Assured `certifications`
**Objective:** Surface accreditation as trust badges.
**Files:** same seed script.
**Step:** Insert `certifications` rows: `ISO/IEC 17025` (issuing_body A2LA), `NADCAP` (if public), each with `listing_id` + `source='showcase'`.
**Verify:** `curl ".../certifications?listing_id=eq.04b5c9ae..."` returns rows.

## 6. PHASE 2 — Detail page enhancement (the product)

### Task 2.1: New `CapabilityDetail` component
**Objective:** Render a rich capability card from `specifications` JSON.
**Files:** Create `web/tstr-frontend/src/components/CapabilityDetail.tsx` (or `.astro`).
**Step 1 (failing test):** `tests/CapabilityDetail.test.tsx` — renders method/pressure/temp/turnaround when `specs` present; renders simple fallback when `specs={}`.
**Step 2:** Implement component: code + name (from `standard.code/name`), description, spec chips (pressure bar, temp range, methods), accreditation line, `verified` check, "Request Quote" → `ContactLabModal`.
**Step 3:** `npm run test` → PASS.
**Step 4:** Commit.

### Task 2.2: Wire into `listing/[slug].astro`
**Objective:** Replace flat grid (lines 311–334) with `CapabilityDetail` map; keep fallback for labs without specs.
**Files:** Modify `web/tstr-frontend/src/pages/listing/[slug].astro:311-334`.
**Step:** Map `capabilities` → `<CapabilityDetail specs={cap.specifications} ... />`; when `specifications` empty, old simple card.
**Verify:** `npm run build` exit 0; local render (or node predicate) shows specs for Assured, simple card for others.

### Task 2.3: Definitional intro + FAQ
**Objective:** Add a 1–2 sentence plain-answer intro ("A hydrogen-embrittlement testing lab performs…") + FAQPage JSON-LD targeting buyer Qs ("What does ASTM F519 measure?", "How do I verify a lab's ISO 17025 scope for H2?").
**Files:** Modify `listing/[slug].astro` (intro block near hero; extend FAQPage JSON-LD at lines 214–234). Seed Q/A inline for embrittlement category; make it category-driven for reuse.
**Verify:** `curl -s <live>/listing/hydrogen-embrittlement-testing-astm-f519-assured-testing-services-1994 | grep -o 'application/ld+json'` present; FAQ block in HTML.

### Task 2.4: `certifications` trust badges
**Objective:** Render issuing_body + scope as badges in sidebar/hero.
**Files:** Modify `listing/[slug].astro` (fetch `certifications` like `capabilities` at top; render in hero/contact area); add small `TrustBadge` usage (exists at `src/components/TrustBadge.tsx`).
**Verify:** Assured page shows "ISO/IEC 17025 — A2LA" badge.

### Task 2.5: Working "search this standard" links
**Objective:** Replace `/browse?standard=CODE` (Task rel. standards, lines 336–362) with links to the new search route (Phase 3) carrying standard + parameters.
**Files:** Modify `listing/[slug].astro:336-362`.
**Verify:** Link hits `/testing/standards/ISO-11114-4` and returns labs.

## 7. PHASE 3 — Search path (findable)

### Task 3.1: Public filtered search page
**Objective:** A buyer can filter "ASTM F519 + ≥700 bar + Germany" and get labs.
**Files:** Create `web/tstr-frontend/src/pages/testing/standards/[code].astro` (or enhance `/browse`). Calls `/api/search/by-standard?standard=CODE&specs={"max_pressure_bar":700}` + location.
**Step 1 (test):** `tests/searchByStandard.test.ts` — API returns Assured for `ASTM F519` + `max_pressure_bar` contains.
**Step 2:** Build page with param filters (pressure slider/input, method select, location) → results cards linking to listings.
**Step 3:** `npm run test` PASS; build exit 0. Commit.

### Task 3.2: Reverse link listing → search
**Objective:** Each capability card "See N labs with this standard" → search page. (Completes Task 2.5.)
**Files:** `CapabilityDetail.tsx` + `listing/[slug].astro`.
**Verify:** Click flows listing → search → another listing.

### Task 3.3: Internal linking + canonical
**Objective:** listing → standard hub → hydrogen hub → region. Set canonical on filtered facets (`noindex` low-value).
**Files:** `sitemap.xml.ts` already filters empties — verify showcase + new search routes included.
**Verify:** `curl -s https://tstr.directory/sitemap.xml | grep assured` and `grep standards`.

## 8. PHASE 4 — SEO/GEO (buyers find it)

### Task 4.1: JSON-LD audit on showcase
**Objective:** Confirm LocalBusiness + ProfessionalService + FAQPage present & valid.
**Files:** `listing/[slug].astro` JSON-LD (lines 190–236).
**Verify:** `curl ... | python3 -c "import json,sys; ..."` parses @graph.
### Task 4.2: `/llms.txt` entry
**Objective:** Steer ChatGPT/Perplexity to showcase + hydrogen hub.
**Files:** Create/append `web/tstr-frontend/public/llms.txt` or Astro route.
### Task 4.3: Buyer-query spot check
**Objective:** Search "hydrogen embrittlement testing lab ASTM F519" style queries; record if TSTR cited.
**Verify:** manual/tool check post-deploy.

## 9. PHASE 5 — Verify & Deploy

### Task 5.1: Build
`cd web/tstr-frontend && npm ci && npm run build` → exit 0. (Lockfile regen if deps change — see tstr-frontend skill gotcha.)
### Task 5.2: Smoke test
`npm run test` (Playwright) green for showcase route; or node predicate if preview unsupported (Cloudflare adapter has no `astro preview`).
### Task 5.3: Deploy + live verify
`git push origin main` → Cloudflare native build. **Do NOT trust the GitHub "Cloudflare Pages" check** (build status only). Verify live via `curl` matching current source title/JSON-LD (per memory deploy-verify rule).

## 10. Risks / Tradeoffs
- **R1 (BLOCKER):** DB writes (Phase 1) need a live write path — on-disk key dead. Must resolve Q1 first.
- **R2:** Never fabricate accreditation scope as real — only public/published facts; badge "Featured Showcase" for honesty.
- **R3:** Junk `standards` rows may have capability FK references — re-map before hiding (Task 0.1).
- **R4:** Build-time N+1 — `getStaticPaths` already fetches all slugs; adding `certifications` fetch per-listing is fine (single query) but watch build time.

## 11. Success Criteria (the "is it done" bar)
- [ ] Showcase listing (Assured) renders: rich capability specs, accreditation badges, definitional intro, FAQ.
- [ ] Buyer can search "ASTM F519 + pressure + location" and land on Assured (and the other 8 labs).
- [ ] JSON-LD valid; showcase appears in sitemap + llms.txt.
- [ ] Build green; deployed; live `curl` confirms (not just GH check).
- [ ] Reusable: any lab with populated `specifications`/`certifications` gets the same treatment.
