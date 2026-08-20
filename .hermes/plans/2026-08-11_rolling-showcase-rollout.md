# Plan — Roll the Hydrogen-Embrittlement Showcase Pattern to All Listings

**Date:** 2026-08-11  ·  **Author:** Hermes  ·  **Status:** PLAN (not yet executed)
**End goal (pinned so we don't drift):** Make every TSTR listing a verifiable,
searchable, AI-citable profile — proving to labs we can sell them a paid listing and
to buyers that TSTR is where to find accredited testing. The Assured HE listing is the
reference template; this plan replicates its data + docs pattern across the DB.

---

## Ground truth (read-only survey, this session)
- 793 listings total · 155 have ≥1 capability · 30 have certifications.
- 549 capability rows · 384 verified=true · 165 unverified.
- 241 standards in catalog · **3 are junk**: `EMBRITTLEMENT`, `H2-TANK`, `H2-SAFETY`
  (poison search — must be quarantined/hidden, not deleted).
- 64 listings verified=true · 770 have a website (researchable).
- Frontend template ALREADY EXISTS from the Assured build (no new component code needed):
  `AccreditationBadges.astro`, `CapabilityDetail.astro`, `testing/standards/[code].astro`,
  definitional intro, FAQ JSON-LD, Markdown-for-Agents (auto).
- BLOCKER (prereq): `certificate_url` column not in live DB. Migration staged at
  `web/tstr-frontend/supabase/migrations/0005_certifications_url.sql`. Needs a ONE-CLICK
  apply in Supabase SQL editor (DDL can't run from this host — DB port firewalled, CLI
  tunnel won't take stdin). Until applied, cert "View" links fall back to the lab's own
  accreditations page (already live and acceptable).

## Hard guardrails (from earlier correction)
- NEVER state a cert's scope covers a method it doesn't (e.g. A2LA coatings scope ≠ F519).
  Mark lab self-declared methods `verified=false` + `claim_source='lab_website'`.
- Every DB write is scoped (by listing_id) and reversible. No destructive ops.
- Credentials stay [REDACTED]; service-role key in web/tstr-frontend/.env is LIVE and used.
- Verify, don't assert: confirm each write with a read-back before moving on.

---

## Tiering (scale realism)
793 listings can't all be hand-researched in one pass. Three tiers:

**Tier A — Strategic (do first, highest sales value):** the 9 HE-capable labs
(TÜV SÜD, Element Materials, CSA Group, SwRI, Kiwa, WHA, Powertech, Assured [done],
Element — Embrittlement Lab). Full research + rich specs + certs + .md doc each.

**Tier B — Already-populated (enrich):** the other 154 labs with capabilities but no/weak
specs or no certs. Backfill `specifications` JSON from existing data; add certs where the
lab's site publishes them; lighter .md doc (auto-generated summary + verification note).

**Tier C — Bulk (lightest):** the remaining ~638 with no capability data. Two options,
decide in morning:
  (C1) Leave as-is (scraper stub) — lowest effort, honest "listed, scope pending."
  (C2) Light enrichment from website only (no deep research) — medium effort.
  Recommend: C1 for now; revisit after Tier A/B prove the sales motion.

---

## Execution phases

### Phase 0 — Data hygiene (SAFE, run autonomously; reversible)
1. Quarantine junk standards: set `standards.active=false` (or add a `hidden` flag if
   column exists) for `EMBRITTLEMENT`, `H2-TANK`, `H2-SAFETY`. Verify search no longer
   surfaces them. (If no such column, flag for schema add — don't delete.)
2. De-dupe certifications: any listing with >1 identical (issuing_body,name) cert row →
   keep one. (Assured had this; others may too.)
3. Read-back all three changes; report counts.

### Phase 1 — Tier A: 9 HE-capable labs (full treatment)
For each lab (Assured already done):
1. Research: fetch site accreditations/scope pages (crawler like the Assured one).
   Save genuine cert PDFs → `research/listings/<slug>/certs/`, screenshot page →
   `research/listings/<slug>/assets/`.
2. Verify: vision-check each cert is real + note its ACTUAL scope (so we don't overclaim).
3. Populate DB:
   - `certifications`: issuer, name, expiry, source='backfill' (or 'manual').
     `certificate_url` once column applied.
   - `listing_capabilities`: set `specifications` JSON (scope_note, test_methods,
     related_standards), `notes`, `verified` (true only if scraper-asserted or cert-backed),
     `claim_source`.
4. Docs: write `research/listings/<slug>/SHOWCASE.md` — verified certs, honest scope
   caveats, standards covered, buyer-facing definitional blurb, FAQ seeds.
5. Live-verify the listing renders badges + rich cards + Markdown-for-Agents.

### Phase 2 — Tier B: 154 enriched labs
1. For each: pull its capability rows; if `specifications` empty, derive a minimal
   structured spec from `standard.name`/`description` (no fabrication — only what the
   standard record states). Set `specifications={note: <standard description>}`.
2. Add `certifications` only where the lab's public site/published scope confirms one.
3. Light `.md` doc: auto-summary (name, accreditations found, standards, verification
   status) + explicit "not independently verified" note where applicable.
4. Spot-check 10% live.

### Phase 3 — docs + search completeness
1. Ensure every populated listing's `testing/standards/[code]` reverse-link resolves
   (already built; just confirm for Tier A/B codes).
2. Per-lab `.md` docs committed to repo under `research/listings/<slug>/`.
3. Update `CERTIFICATION_RESEARCH.md`-style master index mapping lab→certs→standards.

### Phase 4 — build + deploy + verify (per batch)
- `npm ci && npm run build` green; `prettier --check` clean.
- Commit + push (pre-push gate: secret scan + prettier).
- Live-verify a sample of listings + Markdown-for-Agents + JSON-LD.

---

## Definition of done (success criteria)
- Junk standards no longer appear in search.
- Every Tier A listing: ≥1 real cert rendered as badge + ≥1 rich capability card +
  `.md` doc + Markdown-for-Agents reflects it.
- Tier B: capabilities carry at least a non-empty `specifications` note; certs added where
  evidenced.
- Build green; no secrets leaked; all writes read-back verified.
- A short evidence report per tier (counts changed, sample URLs).

## Open decision for morning (NOT blocking Phase 0/1)
- Tier C scope: C1 (leave stubs) vs C2 (light website enrichment) vs full.
- Apply `certificate_url` migration (unlocks direct PDF links) — needs your one click, or
  I can write the exact SQL for you to paste.
- Sales framing: which labs to approach first with the finished showcase.
