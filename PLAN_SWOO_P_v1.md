# TSTR Scraper Toolset — Improved Build Plan (v2, 2026-08-31)

## Context
- Current stack: BS4 scripts + DDG enrichment + LinkedIn (Playwright CDP) + CSV outreach generator.  
- Proven this session: BAML extracts typed fields from LLM output (free tier, $0); `crawl4ai → BAML → LabListing` works on real sources (TÜV SÜD, Intertek).  
- Goal: reusable scraper toolset + agent for **(1) lead generation** and **(2) industry‑news collection** serving our audiences and adjacent industries (energy, hydrogen, aerospace, pharma, environmental).

## How the best scrapers are built (research summary)
| Category | What they provide | Our self‑hosted substitute (OCI free tier) |
|----------|-------------------|--------------------------------------------|
| **Managed proxy / unblocking** | Residential/ISP pools, CAPTCHA solve, fingerprint rotation | Polite rate‑limit + UA rotation + OCI egress IP; fallback to vetted free proxy list only after 3 consecutive 429/403 responses. |
| **Fetch → Parse → Extract → Store → Monitor** | Queue, retries, autoscaling, schema validation, drift alerts | `crawl4ai` (JS) / `trafilatura` (article) / BS4 (simple) → BAML‑validated extraction → Supabase upsert → lightweight health‑check cron + alert on HTTP error rate >5% or schema‑validation failures >2%. |
| **Actor / agent model** | Reusable scrapers, scheduler, dataset store | Python agent reading a *job spec* (URLs + extractor type) → fetch/parse → BAML extract → dedupe → Supabase → log. Scheduler = OCI cron (or Cloud Scheduler if we outgrow free VM). |
| **LLM‑native parsing** | markdown/markdown‑fit, schema extraction, graph‑of‑nodes | Keep `crawl4ai` for JS rendering; use BAML for deterministic, typed extraction (preferred over LLM‑only strategies for cost & verifiability). |
| **Observability** | Logging, metrics, dashboards | Structured JSON logs to OCI Logging; Prometheus exporter (optional) for request latency, LLM token usage, extraction success rate. |

## Core Design Principles (first‑principles)
1. **Separation of concerns** – fetch/parse, extraction, storage, orchestration are independent modules with clear contracts (input/output types).  
2. **Fail‑fast validation** – BAML schema validation occurs immediately after extraction; malformed rows are rejected before storage (root‑cause fix for “garbage‑in” bugs).  
3. **Politeness & compliance** – configurable delay, UA rotation, respect `robots.txt`, log each request URL; leads start as `unverified` and require manual confirmation before outreach (GDPR/CAN‑SPAM).  
4. **Cost awareness** – LLM calls are capped per run; free‑tier default; alert if paid tokens exceed $0.01/run.  
5. **Observability & verifiability** – every pipeline step emits a JSON event; CI includes schema‑invariant test and a synthetic‑data smoke test.  
6. **Incremental delivery** – each phase yields a shippable artifact with defined acceptance criteria.  
7. **Extensibility** – source registry table drives what to crawl, extractor to use, and cadence; adding a new source requires only a DB row.

## Layer‑by‑Layer Specification

### Layer A – Fetch & Parse
- **Primary fetcher:** `crawl4ai` (JS rendering → markdown). Configurable: `wait_for: "networkidle"`, `timeout: 30s`.  
- **Fallback parser:** `trafilatura` for plain‑article/about pages (faster, lower token usage).  
- **Deterministic fallback:** BS4+lxml for known static sources (e.g., CSV indexes, sitemaps).  
- **Politeness middleware:**  
  - Per‑domain delay: base 2s + jitter 0‑3s (exponential backoff on 429/403).  
  - UA pool: rotate among 10 common desktop/mobile strings.  
  - OCI egress IP: use the VM’s public IP; if blocked >3 times in 5 min, enable free‑proxy list (e.g., `proxy‑scrape`) with same UA rotation.  
  - `robots.txt` check via `reppy`; skip disallowed paths.  
- **Observability:** each fetch emits `{timestamp, url, status_code, latency_ms, proxy_used, ua, attempt}`.

### Layer B – Structured Extract (BAML)
| Extractor | Target | Fields (BAML class) | Validation notes |
|-----------|--------|---------------------|------------------|
| `ExtractLabListing` | Lab/company overview pages | `name, website, location, accreditation[], services[], contact_email, phone` | Existing; moved to repo, unit‑tested with sample HTML. |
| `ExtractNewsArticle` | News/article pages | `title, source, published_date (ISO), summary, topics[], related_industry[], url` | Date parsed with `dateparser`; fallback to `null` if unparsable → row rejected. |
| `ExtractLead` | Lead‑gen pages (company directories, press releases, event sites) | `company, contact_name, role, email, linkedin_url, signal, intent_score (0‑1), source_url` | Email format regex; `intent_score` derived from keyword match (e.g., “new lab”, “expansion”, “hiring”). |
| **Common** | All | `_raw_html (truncated to 2 KB for debugging), extraction_timestamp` | Stored in Supabase `raw_extract` column for audit. |
| **Error handling** | If BAML returns validation error → emit `extraction_failed` event, skip row, increment error metric. |

*All extractors live in `src/extractors/` with a factory `get_extractor(job_type)` returning a Pydantic‑compatible BAML model.*

### Layer C – Agent Orchestration
- **Job spec JSON** (saved in `jobs/` or Supabase `scrape_jobs` table):
  ```json
  {
    "job_id": "news_tuvsud_2026_08",
    "type": "news",
    "sources": ["https://www.tuvsud.com/en/news", "https://www.intertek.com/news/"],
    "extractor": "ExtractNewsArticle",
    "cadence": "6h",
    "enabled": true
  }
  ```
- **Agent flow (Python script `run_job.py`):**  
  1. Load job spec.  
  2. For each source URL: fetch → parse → extract → validate.  
  3. Dedupe using a composite key: `(source_url, title)` for news; `(company, email)` for leads; `(name, website)` for labs. Dedupe logic lives in `src/dedupe.py` (Supabase upsert with `ON CONFLICT DO NOTHING`).  
  4. Upsert rows to appropriate Supabase table (`industry_news`, `sales_leads`, `lab_listings`).  
  5. Emit summary event: `{job_id, processed, inserted, skipped, errors, latency_s, llm_tokens_used}`.  
  6. If `errors > 0` or `llm_tokens_used > free_tier_threshold`, raise alert via OCI Monitoring (email/webhook).  
- **Scheduler:** OCI cron entry (free VM) runs `run_job.py` every 15 min; reads enabled jobs from `scrape_jobs`.  
- **Logging:** Structured JSON to stdout → captured by OCI Logging; retained 30 days.  
- **Metrics:** Simple Prometheus exporter (`/metrics`) exposing: `scrape_jobs_total`, `scrape_success`, `scrape_errors`, `llm_token_consumption`.  

## Cross‑cutting Practices
- **`ARCHITECTURE.md`** – one‑page doc describing invariants: (a) every extractor returns a BAML model; (b) all external network calls go through `fetch_wrapper`; (c) storage layer only accepts validated models.  
- **CI schema‑invariant check** – GitHub Actions workflow:  
  1. Run unit tests for each extractor against a fixture set.  
  2. Run the agent on a *synthetic* job (local HTML server) and assert output conforms to BAML schema (using `jsonschema`).  
  3. Fail build on any validation error or >5% extraction failure rate.  
- **A/B‑test prompts** – For experimental LLM‑based extraction (e.g., using `crawl4ai`'s LLM strategy), we toggle via env var `USE_LLM_EXTRACTION=true`. Metrics compare token usage and error rate against BAML baseline.  
- **Cost guardrail** – `MAX_LLM_TOKENS_PER_JOB = 5000` (≈ $0.0015 on free tier). Agent aborts if exceeded; alert sent.  
- **Human‑in‑the‑loop review** – Supabase tables include a `review_status` column (`pending`, `approved`, `rejected`). A simple internal Streamlit app (`apps/review_ui.py`) shows pending rows; only `approved` rows are exported to outreach or newsletter pipelines.  
- **Compliance checklist** (applied per job):  
  - **robots.txt** respected (fetch_wrapper).  
  - **Rate‑limit** ≤ 1 request/2 s per domain (configurable).  
  - **Lead data**: flag `is_verified = false` until manual confirmation; outreach script filters `is_verified = true`.  
  - **GDPR**: store only lawfully obtained data; provide deletion endpoint (`/api/leads/{id}`) for right‑to‑be‑forgotten.  
  - **CAN‑SPAM/POPIA**: outreach includes unsubscribe link, physical address, and honest subject lines.  
- **Source registry** – Supabase table `scrape_sources`:  
  ```sql
  CREATE TABLE scrape_sources (
    id UUID PRIMARY KEY,
    domain TEXT NOT NULL,
    extractor_type TEXT NOT NULL,
    cadence_interval INTERVAL NOT NULL,
    owner TEXT,
    active BOOLEAN DEFAULT TRUE,
    notes TEXT
  );
  ```
  Agent queries this table at start if no explicit job spec is provided, enabling dynamic job generation.  
- **Dedupe/merge** – Implemented in `src/dedupe.py` with pluggable strategies; early investment (P0) prevents silent duplication at scale.  
- **Content reuse pipeline** – Approved news rows feed a nightly LangChain job that drafts a newsletter snippet; output stored in `content_drafts` for editorial review before publishing to blog/email.  

## Build Phases (incremental, shippable)

| Phase | Duration | Deliverables | Acceptance Criteria |
|-------|----------|--------------|----------------------|
| **P0 – Harden extraction & dedupe** | 2 days | • Move `ExtractLabListing` BAML to `src/extractors/`.<br>• Implement `ExtractNewsArticle` & `ExtractLead` BAML classes.<br>• Write unit tests (≥ 80 % coverage) with HTML fixtures.<br>• Create `src/dedupe.py` with upsert logic.<br>• Add Supabase upsert helpers (` upsert_lab`, `upsert_news`, `upsert_lead`).<br>• Update `ARCHITECTURE.md`. | All extractors pass validation on fixtures; dedupe prevents duplicate rows on repeated runs; CI schema test passes. |
| **P1 – News collector** | 3 days | • Build `jobs/news_job.yaml` with 5 seed RSS/sites.<br>• Agent reads job spec, runs fetch→extract→dedupe→store.<br>• Streamlit review UI (`apps/review_ui.py`) shows pending news.<br>• Simple newsletter draft generator (LangChain) creates markdown snippet per approved article.<br>• Add Prometheus metrics for news pipeline. | Agent inserts ≥ 5 distinct news items per run; review UI displays correct fields; newsletter snippet contains title, source, summary; no duplicate inserts across runs. |
| **P2 – Lead‑gen pipeline** | 4 days | • Populate `scrape_sources` table with target industry directories (e.g., Kompass, ThomasNet, regional lab associations).<br>• Agent runs lead job, extracts `ExtractLead`, writes to `sales_leads` with `is_verified=false`.<br>• Outreach script (`generate_outreach.py`) modified to join on `is_verified=true` and add unsubscribe footer.<br>• Review UI extended for lead verification.<br>• Add compliance log table (`scrape_compliance_log`). | Leads extracted with non‑null email and company; deduplication works; outreach only sends to verified leads; compliance log records each scrape request (URL, timestamp, GDPR basis). |
| **P3 – Agent wrapper & orchestration** | 3 days | • Unified `run_job.py` that loads job spec from CLI arg *or* `scrape_jobs` table.<br>• OCI cron entry (`*/15 * * * * /usr/bin/python3 /opt/tstr/run_job.py`).<br>• Centralised logging struct (`structlog`) → OCI Logging.<br>• Health‑check endpoint (`/health`) returning 200 if last job succeeded < 1 h ago.<br>• Alert rule: if `errors > 0` **or** `llm_tokens_used > 4000` → send OCI Notification (email). | Agent runs unattended for 24 h, processes all enabled jobs, logs JSON, respects politeness delays, triggers alerts only on defined thresholds. |
| **P4 – Anti‑block, monitoring & observability** | Ongoing (2 days initial) | • Implement `robots.txt` checker & delay wrapper.<br>• Free‑proxy list fallback with health‑check.<br>• Drift detection: weekly job that samples 10 random pages per source, compares extraction field presence; alerts if drop > 20 %.<br>• Dashboard (Grafana OCI) visualizing requests/min, token usage, success rate.<br>• Update cost guardrail to dynamic based on remaining free‑tier quota (via OCI Usage API). | No 429/429 responses after politeness + proxy fallback; drift alert triggers only on genuine site changes; dashboard shows < 5 % error rate; token usage stays within free‑tier limits. |

## Risks & Mitigations (applied throughout)
| Risk | Impact | Mitigation (built into plan) |
|------|--------|------------------------------|
| Free LLM rate‑limit (429) | Pipeline stall, missed data | Guardrail + paid‑fallback flag (`USE_PAID_LLM=true`) with OCI Notification when approached; keep BAML as primary (zero‑cost). |
| LinkedIn ToS friction | Legal risk, blocked IP | Keep LinkedIn scraper manual/opt‑in (`scrape_linkedin_local.py`) and exclude from automated agent; document in compliance checklist. |
| OCI free‑tier VM CPU/memory limits | Slow crawls, timeouts | Use lightweight fetchers (crawl4ai with limited concurrency 2); monitor CPU via Prometheus; if sustained > 80 % scale to paid shape or add job queue (OCI Functions). |
| Data quality degradation (site changes) | Bad leads/news | Drift detection job (P4) + schema‑invariant CI; human review step before publishing/outreach. |
| Legal compliance (GDPR, CAN‑SPAM) | Fines, reputation loss | Explicit compliance checks per job; leads start unverified; opt‑out link in all outreach; deletion API. |
| Operational overhead (manual review) | Bottleneck | Review UI limits to ≤ 50 pending rows per batch; automated scoring (`intent_score`) prioritises high‑value leads for faster review. |

## Evidence (this session)
- BAML spike: `SCRAPER_BAML_SPIKE_AND_TOOLING.md` (commit `544eb28`).  
- crawl4ai pilot: rendered TÜV SÜD + Intertek → typed BAML output (ran live).  
- Throwaway venvs `_baml_spike/`, `_crawl4ai_venv/` are git‑ignored.  

---  

## CHANGES:
- Added explicit **politeness middleware**, UA rotation, and `robots.txt` respect to Layer A.  
- Introduced **Source Registry** table and dynamic job generation to replace hardcoded source lists.  
- Inserted **human‑in‑the‑loop review** workflow with `review_status` and Streamlit UI for both news and leads.  
- Formalised **compliance checklist** (GDPR, CAN‑SPAM/POPIA) and added verification flag for leads.  
- Expanded **observability**: structured JSON logs, Prometheus metrics, health‑check endpoint, alert rules on errors/token usage.  
- Specified **deduplication/merge** component early (P0) with pluggable strategies and Supabase upsert logic.  
- Detailed **cost guardrail** with token caps, free‑tier defaults, and alerts when thresholds approached.  
- Added **drift detection** and **proxy fallback** mechanisms in Phase P4 for anti‑block resilience.  
- Clarified **CI schema‑invariant check** steps (unit tests, synthetic job run, jsonschema validation).  
- Provided **acceptance criteria** per phase to ensure shippable, testable increments.  
- Updated **architecture documentation** (`ARCHITECTURE.md`) and cross‑cutting practices section.  
- Refined **risk/mitigation** table to directly map identified risks to concrete plan elements.  
- Included **content reuse pipeline** (news → newsletter draft) to satisfy the second stated use case.  
- Improved **layer definitions** with concrete field lists, validation notes, and error handling paths.  
- Added **metrics & dashboard** guidance for operational visibility.  
- Ensured **self‑contained** plan: all tables, scripts, and config references are described inline.  
- Removed ambiguous language, added verification steps, and aligned every element with the seven critique checks.