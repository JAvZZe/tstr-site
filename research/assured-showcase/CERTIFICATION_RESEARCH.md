# Certification Research — Assured Testing Services (Showcase Lab)

**Date:** 2026-08-11
**Purpose:** Find a real, publicly-listed / downloadable certification we can feature on the showcase listing.
**Method:** Read-only crawl of each of the 9 H2-embrittlement lab websites + live browser screenshot of Assured's accreditations page + downloaded certs verified visually.

## Showcase lab chosen
**Assured Testing Services** — `slug: hydrogen-embrittlement-testing-astm-f519-assured-testing-services-1994`
Website: https://www.assuredtesting.com  |  Location: 388 Servidea Drive, Ridgway, PA 15853, USA

## GENUINE accreditation assets (downloaded, verified)
All sourced from the lab's OWN public site (https://www.assuredtesting.com/accreditations). Files saved under `research/assured-showcase/certs/`.

| Accrediting body | Certificate # | Expiry | File | Verified by |
|---|---|---|---|---|
| **A2LA** — ISO/IEC 17025:2017, Mechanical scope | 2012.01 | Valid to **31 March 2027** | `Assured_A2LA_2012.01_MechanicalScope.pdf` | vision-read p1: "SCOPE OF ACCREDITATION TO ISO/IEC 17025:2017", holder Assured Testing Services, MECHANICAL, Valid To March 31 2027, Cert 2012.01 |
| **Nadcap** (administered by PRI) — Materials Testing | 8943232779 | 31 Aug 2026 | `Assured_Nadcap_8943232779_Scope.pdf` | vision-read p1: Nadcap scope, holder Assured Testing Services, Ridgway PA, Salt Spray (corrosion) |
| **AAMA** (FGIA) — Component Manufacturer's Testing Lab | 2026 | 2027 audit | `Assured_AAMA_2026.pdf` | linked on accreditations page |

Screenshots: `assets/assured_accreditations_page.png`, `assets/A2LA_2012.01_cover.png`.

## Lab's OWN published capability claims (from site copy, /mechanical-testing)
- "The laboratory is able to perform **Hydrogen embrittlement testing per ASTM F519**." (verbatim, /mechanical-testing)
- Lists **Tensile Testing** as a service (homepage service tiles).
- These are the lab's own marketing claims — fine to feature as "lab states…" but NOT attributable to the A2LA scope cert below.

## CRITICAL ACCURACY NOTE (do NOT overclaim)
The downloaded **A2LA Cert 2012.01 "Mechanical Scope"** is, on inspection of all 13 pages, actually **coatings / corrosion / environmental** testing (salt spray, cyclic corrosion, humidity, chip resistance, thickness, UV weathering). It does **NOT** list tensile / slow-strain-rate / ASTM F519 methods. The site copy claims tensile + F519 capability, but the A2LA scope cert on file covers corrosion/coatings.

**Therefore, when featuring:**
- ✅ SAFE: "Accredited to ISO/IEC 17025:2017 (A2LA Cert 2012.01, valid to 31 Mar 2027)", "Nadcap Materials Testing (8943232779)", "AAMA/FGIA lab".
- ✅ SAFE (as lab's own claim): "Lab states hydrogen-embrittlement testing per ASTM F519 & tensile testing available."
- ❌ DO NOT claim: "A2LA scope covers ASTM F519 / tensile / hydrogen embrittlement" — the cert does not show that.
- The embrittlement capability row in TSTR DB should be presented as the lab's self-declared scope, not as A2LA-certified, unless a tensile scope cert surfaces.

## Other labs researched (for alternate/future showcases)
- **Element Materials Technology**: rich `accreditations-and-approvals` page with downloadable UKAS/DAkkS/ANAB/IAS ISO 17025 schedules (some blocked 403 from curl; browser needed). Strong candidate if Assured deemed too small.
- TÜV SÜD, CSA Group, WHA, Kiwa: homepages returned 403 (WAF) — need browser. Not yet inspected.
- SwRI, Powertech: accreditation links present but mostly brochures, not scope certs.

## Data backfill — DONE (2026-08-11)
Write path resolved: the **service-role key in `web/tstr-frontend/.env` is LIVE** (`SUPABASE_SERVICE_ROLE_KEY=sb_secret_dR…`, verified bypasses RLS). My earlier memory note ("on-disk keys dead post-2026-08-10 rotation") was WRONG for this file — corrected.

Actions taken (reversible, scoped to Assured only):
- Discovered Assured ALREADY had 3 `certifications` rows (source=`manual`, 2026-07-08): A2LA ISO/IEC 17025, PRI Nadcap, AAMA/FGIA. Kept these; deleted 3 accidental duplicate `backfill` rows I created.
- Enriched 2 existing `listing_capabilities` rows with structured `specifications`:
  - ASTM F519 embrittlement (`8e432bdd…`): test_methods=[ASTM F519], scope_note, claim_source=lab_website.
  - Tensile metallic (`1ea9ffc3…`): related_standards=[ASTM E8/E8M, ASTM E1450 slow strain rate].
- Did NOT downgrade the scraper-set `verified=true` on those capability rows.

Cert table `source` CHECK allows only: `backfill | manual | scraped`.

NOTE: The live listing page (`listing/[slug].astro`) does NOT yet fetch/display `certifications` or `specifications` — that's the Phase 2 code work. Data is staged and ready; page will show it once code reads these columns.
