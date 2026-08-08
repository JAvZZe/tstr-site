# IAF CertSearch Client — Implementation TODOs

**Business model:** SELL NOW, ACTIVATE ON KEY. The IAF Laboratory Verification
plan is already sold on `pricing.astro` (+$150/month) and offered via
`contacts.ts` ("commission us to verify credentials"). The Python client is the
backend that **activates when a paid IAF CertSearch API key is set**. It must
NEVER falsely claim verification — it currently degrades gracefully
(`self.active=False` without `IAF_API_KEY`; `smart_verify_tstr_listing` returns
`iaf_status: 'inactive'`). So the feature is safe to sell today; implementation
below is the activation step, triggered by a customer purchase.

**Status:** `iaf_api_client.py` is a STUB (all real calls are `# TODO`, methods
return `[]` / hardcoded `0.75`). The site's "verify credentials" upsell is
**non-functional at the backend** until these are done AND a paid IAF CertSearch
API key is registered (~$499/yr Basic). This doc is the ready-to-execute
checklist.

**Prerequisites (user action, not code):**
1. Register at iafcertsearch.org → get `IAF_API_KEY` (Basic plan).
2. Read the live IAF CertSearch API docs to confirm: base URL, auth scheme,
   real endpoint paths, and the exact response JSON schema. The code's
   `base_url = "https://api.iafcertsearch.org"` is marked "To be confirmed"
   (line 54) and the TODO endpoints (`/v1/companies/search`, `/v1/companies/verify`)
   are GUESSES — verify before trusting them.

**Code TODOs (in `iaf_api_client.py`):**

- [ ] **Add `import requests`** at top (lines 6-10). The TODO blocks call
      `requests.get/post` but `requests` is NOT imported (it IS in
      `requirements.txt`, so just add the import).
- [ ] **Confirm + set `base_url`** (line 54). Replace the placeholder with the
      verified API base URL from step 2 above.
- [ ] **Implement `search_companies()`** (lines 85-126): uncomment the
      `# TODO` block; map the REAL response fields (the guess uses
      `name/country/city/website/email/phone` — confirm against actual schema).
      Keep the 24h cache.
- [ ] **Implement `verify_company()`** (lines 128-178): uncomment; confirm
      endpoint + `certifications[]` schema (id, standard, scope, issue_date,
      expiry_date, status, issuing_body, certificate_number). Keep credit
      guard + 30-day cache.
- [ ] **Implement `_calculate_confidence()`** (lines 244-251): replace
      hardcoded `return 0.75` with real fuzzy matching (e.g.
      `difflib.SequenceMatcher` on business_name + location + website vs the
      IAF result). The `>= 0.8` threshold in `smart_verify_tstr_listing` depends
      on this being real.
- [ ] **Persist verification to Supabase** in `smart_verify_tstr_listing()`
      (lines 180-243): currently returns an enriched dict but never writes it.
      Add an upsert (follow the `tstr-data-ops` UNIQUE(listing_id) pattern) into
      either the `listings` table (new cols: `iaf_verified`, `iaf_certifications`,
      `iaf_match_confidence`, `iaf_verification_date`) OR a new
      `iaf_verifications` table. Requires a Supabase migration.
- [ ] **Set correct `monthly_credit_limit`** (line 63, currently `150` assumed
      for Basic $499). Confirm the real plan limit after registration.
- [ ] **Add `tests/test_iaf_api_client.py`** mocking the API (no real credits)
      to cover search → match → verify flow + confidence scoring.

**Wiring / ops:**

- [ ] Set `IAF_API_KEY` in OCI environment (and GitHub secret if any CI step
      uses it). NEVER commit the key; use `[REDACTED]`.
- [ ] Hook `smart_verify_tstr_listing` into the scraper cron for new/updated
      listings — batch, rate-limited, credit-aware (the existing
      `_check_credit_availability` guards this).
- [ ] Update `tstr-scraper-agent` skill: flip "Do not claim IAF works" →
      "IAF functional" once the above ships + a live verify succeeds.

**Verification (after implementation):**
- Unit test passes (mocked API, no credits burned).
- A real `smart_verify_tstr_listing` on one known lab writes `iaf_verified=true`
  + certifications to Supabase and renders on `tstr.directory/company/[slug]`.
- Credit counter logs usage; monthly cap enforced.
