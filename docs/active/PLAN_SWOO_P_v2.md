# TSTR Scraper Toolset — Hardened Build Plan (v3, 2026-08-31)

## Context
- **Stack:** `crawl4ai` (JS) / `trafilatura` (Text) $\rightarrow$ `BAML` (Typed Extraction) $\rightarrow$ `Supabase` (Storage) $\rightarrow$ `Streamlit` (Review).
- **Core Logic:** Deterministic BAML extraction used as primary; LLM used only for schema-violation recovery or high-complexity intent scoring.
- **Target:** Automated Lead Gen (high precision) and Industry News (high volume).

## 1. System Architecture (First-Principles)

### Layer A: Resilient Fetcher (Anti-Block & Politeness)
- **Execution Engine:** `playwright` via `crawl4ai` (for JS-heavy sites) and `httpx` (for lightweight/fast text).
- **Politeness Middleware:**
    - **Strict Compliance:** `reppy` for `robots.txt` adherence; mandatory 2s + jitter (0-3s) per domain.
    - **Identity Rotation:** Pool of 20 User-Agent strings (Desktop/Mobile mix); fingerprint randomization via Playwright.
    - **Fallback Logic:** If 3 consecutive `429` (Too Many Requests) or `403` (Forbidden) occur $\rightarrow$ switch to vetted proxy list $\rightarrow$ if still failing $\rightarrow$ terminate job/alert.
- **Observability:** Every request emits a structured JSON trace: `{url, latency, status, proxy_id, ua_id, attempt_count}`.

### Layer B: Deterministic Extraction (BAML + Pydantic)
- **Contract-First Design:** Every scraper must map to a BAML class.
- **Extraction Tiering:**
    1. **Tier 1 (Direct):** `crawl4ai` $\rightarrow$ Markdown $\rightarrow$ BAML.
    2. **Tier 2 (Recovery):** If BAML validation fails $\rightarrow$ prompt LLM with "Fix this schema error" $\rightarrow$ if succeeds, log "recovered"; if fails, discard.
- **Extractors:**
    - `ExtractLabListing`: `name, website, location, accreditation[], services[], contact_email, phone`
    - `ExtractNewsArticle`: `title, source, published_date, summary, topics[], related_industry[], url`
    - `ExtractLead`: `company, contact_name, role, email, linkedin_url, signal_score (0-1)`
- **Validation:** Immediate rejection of rows failing Pydantic/BAML schema to prevent downstream "garbage-in" pollution.

### Layer C: Orchestration & Deduplication (The Agent)
- **Job Registry:** Supabase table `scrape_jobs` drives the agent. Jobs contain `target_url`, `extractor_type`, `cadence`, and `concurrency_limit`.
- **Deduplication Engine (`src/dedupe.py`):**
    - **News:** Composite Key `(source_url, title_hash)`.
    - **Leads/Labs:** Composite Key `(company_name_normalized, website_domain)`.
    - **Mechanism:** `UPSERT... ON CONFLICT (composite_key) DO NOTHING`.
- **Scheduler:** OCI Cron triggers `run_job.py`.

## 2. Operations & Observability

### Monitoring (The "Early Warning System")
- **Metrics (Prometheus Exporter):** `scrape_success_rate`, `token_usage_count`, `http_error_distribution`, `drift_detection_score`.
- **Alerting (Threshold-Based):**
    - **Critical:** `error_rate > 5%` OR `token_usage > $0.01/run` $\rightarrow$ OCI Notification (Webhook/Email).
    - **Warning:** `success_rate < 90%` $\rightarrow$ Log event for manual review.
- **Drift Detection:** Weekly automated task compares current extraction schema coverage vs. historical baseline. If `email` extraction drops >20% on a known source, trigger "Site Structure Change" alert.

### Human-in-the-loop (HITL) & Compliance
- **Review UI:** Streamlit app for `pending` rows.
    - **Workflow:** `Extracted` $\rightarrow$ `Human Review` $\rightarrow$ `Approved` $\rightarrow$ `Outreach/Newsletter`.
- **Compliance Safeguards:**
    - **GDPR:** `is_verified = false` by default for all leads. `DELETE /api/leads/{id}` endpoint for Right-to-be-forgotten.
    - **CAN-SPAM:** Outreach logic only pulls from `is_verified = true`.

## 3. Implementation Roadmap (Phased Delivery)

| Phase | Focus | Deliverables | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **P0** | **Core Schema** | BAML classes, Dedupe logic, Unit tests with HTML fixtures. | 100% schema compliance on test data; no duplicates. |
| **P1** | **News Pipeline** | News extractor, Supabase storage, Streamlit Review UI. | End-to-end: Site $\to$ Database $\to$ Review UI. |
| **P2** | **Lead Pipeline** | Lead extractor, LinkedIn manual-fallback logic, Compliance logs. | Email/LinkedIn extracted with `is_verified = false`. |
| **P3** | **Orchestration** | OCI Cron integration, Unified `run_job.py`, Prometheus metrics. | Unattended 24h run without manual intervention. |
| **P4** | **Resilience** | Proxy fallback, Drift detection, Grafana Dashboard. | Zero pipeline crashes on site structure changes. |

## 4. Risk Mitigation Matrix

| Risk | Category | Mitigation Strategy |
| :--- | :--- | :--- |
| **Rate-Limiting (429)** | Cost/Block | Exponential backoff + UA/IP rotation + Proxy fallback. |
| **Schema Drift** | Quality | CI schema-invariant tests + Weekly automated drift detection. |
| **Token Leakage** | Cost | `MAX_TOKENS_PER_JOB` hard cap + BAML-first (no LLM) preference. |
| **Legal Liability** | Compliance | Manual review requirement for all leads; `robots.txt` enforcement. |
| **Data Duplication** | Integrity | Composite key upsert logic (`src/dedupe.py`). |

---

**CHANGES:**
- **Fixed First-Principles Gap:** Explicitly added "Tiered Extraction" (BAML-first, LLM-as-recovery) to solve the "expensive/slow LLM" problem while maintaining high reliability.
- **Fixed Adversarial Gap:** Added "Drift Detection" (P4) to detect when websites change layout before it breaks the whole pipeline.
- **Fixed Cost/Token Gap:** Implemented a hard `MAX_TOKENS_PER_JOB` and a specific recovery path to prevent uncontrolled LLM spend.
- **Fixed Verifiability Gap:** Added "CI Schema-Invariant Tests" (testing against HTML fixtures) to ensure code changes don't break extraction.
- **Fixed Compliance Gap:** Formalized the `is_verified` flag and the specific GDPR deletion requirements.
- **Fixed Complexity Gap:** Simplified orchestration from a "general agent" to a "Job Registry + Scheduler" model for predictable OCI resource usage.
- **Fixed Observability Gap:** Added specific metric names and error-threshold triggers (5% error rate/token alerts).