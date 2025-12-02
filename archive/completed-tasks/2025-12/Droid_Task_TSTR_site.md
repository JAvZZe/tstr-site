# Droid Task: TSTR.site - Hydrogen Niche MVP Build

**Context:**
We are building a high-margin "Hydrogen Infrastructure Compatibility" testing directory.
**Constraint:** One feature per session.
**Method:** Pareto (80/20) - Focus on the "Search by Standard" functionality.
**Safety:** Commit to Git after each completed checkpoint.

---

## PHASE 1: Database & Schema Setup (The Foundation)
**Objective:** Create the relational structure to support specific testing capabilities.

1.  **Create `Providers` Table:**
    * `id`, `name`, `website`, `accreditation_status` (Boolean).
2.  **Create `Standards` Table (The SEO Keys):**
    * `code` (e.g., "ISO 19880-3"), `description` (e.g., "Valves for H2 Stations").
3.  **Create `Capabilities` Table (The Junction):**
    * `provider_id`, `standard_id`.
    * *Crucial Metadata Columns:* `max_pressure_bar` (Integer), `state` (Enum: Gaseous, Liquid), `special_equipment` (Array: ["Blast Bunker", "Cryostat"]).

**Action:** Scaffold these tables/models.
**Checkpoint:** `git commit -m "feat(db): scaffold hydrogen provider schema"`

---

## PHASE 2: Seed Data Injection (The Content)
**Objective:** Populate with high-value initial data to validate the search logic.

1.  **Inject Standards:**
    * ISO 19880-3 (Valves)
    * ISO 11114-1 (Embrittlement)
    * SAE J2601 (Fueling Protocols)
2.  **Inject Providers (Seed List):**
    * *TÜV SÜD:* Caps: [ISO 19880-3, 700 Bar, Gaseous]
    * *Powertech Labs:* Caps: [SAE J2601, 1000 Bar, Gaseous]
    * *NPL:* Caps: [ISO 14687, 0 Bar, Purity Analysis]

**Action:** Write a seed script or manually insert these records.
**Checkpoint:** `git commit -m "chore(seed): inject hydrogen standards and providers"`

---

## PHASE 3: The "Standard-First" Search Logic (The Feature)
**Objective:** Users/Agents search by *Problem* (Standard), not *Company*.

1.  **Backend/API:**
    * Endpoint: `GET /api/search?standard=ISO_19880-3&min_pressure=700`
    * Logic: Filter `Capabilities` where `standard_id` matches AND `max_pressure_bar` >= 700. Return joined Provider data.
2.  **Frontend (MVP):**
    * Simple Dropdown: "Select Test Standard" (Populated from DB).
    * Toggle Switch: "High Pressure (>700 bar) Only".
    * Result List: Display Provider Name + specific matching Capability details.

**Action:** Implement the search logic and basic UI.
**Checkpoint:** `git commit -m "feat(search): implement standard-based filtering"`

---

## PHASE 4: AI-Ready Schema Markup (The Moat)
**Objective:** Ensure AI agents (Perplexity, Gemini) can read the data structure.

1.  **Implement JSON-LD on Provider Profile Pages:**
    * Use Schema.org `Laboratories` or `Organization`.
    * Key Property: `serviceType` mapped to the specific Standard Name.
    * Key Property: `areaServed` (Global/Region).

**Action:** Add dynamic JSON-LD injection to the provider detail template.
**Checkpoint:** `git commit -m "feat(seo): add json-ld schema for providers"`

**STOP.** Await user validation of the Hydrogen search flow.
