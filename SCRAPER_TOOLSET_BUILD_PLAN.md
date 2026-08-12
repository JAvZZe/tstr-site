# TSTR Scraper Toolset — Build Plan (v1, 2026-08-11)

## Context
Current scraper = BS4 scripts + a DDG-only enrichment step + LinkedIn (Playwright CDP) + outreach
CSV generator. Proven this session:
- **BAML** extracts typed lab fields from LLM output (free tier, $0).
- **crawl4ai** renders JS + outputs markdown; pipeline `crawl4ai → BAML → LabListing` works
  on real sources (TÜV SÜD, Intertek).
Goal: build a **reusable scraper toolset + agent** for (1) **lead gen** and (2) **industry-news
collection** for our audiences + related industries.

## How the best commercial/OS scrapers are built (research summary)
**Commercial (Bright Data, Zyte, Oxylabs, Apify, ScrapingBee, ZenRows):** managed proxy pools
(residential/ISP), anti-bot (CAPTCHA solve, fingerprint rotation), unblocking APIs, scheduling,
"scrape API" (send URL → get markdown/json). Apify = actor model (reusable scrapers) + scheduler
+ dataset store. All charge per GB/request; we avoid cost by self-hosting on OCI (free tier).

**Open-source patterns that matter:**
- **crawl4ai** (78k★) — LLM-native: markdown/markdown-fit, schema extraction, JS render.
- **ScrapeGraphAI** (29k★) — graph of LLM "nodes" for natural-language scrape specs.
- **browser-use / Portia** — agentic browser (plan → act → observe). Good for JS-heavy/click-through.
- **markitdown** (173k★, MS) — docs/PDF → Markdown (for datasheets, reports).
- **trafilatura** — main-content extraction (lighter than crawl4ai for article pages).
- **Apify SDK / crawlee** — robust queue, retries, autoscaling (TS; Python port exists).
- **Key architecture:** fetch layer (proxy/rotate) → parse layer (BS4/trafilatura/crawl4ai) →
  **schema-validated extract** (BAML/Pydantic) → **store** (Supabase) → **monitor** (alert on
  drift/block). Commercial adds the proxy + unblocking; we substitute with polite rate-limiting
  + OCI IP + fallback to LLM extraction.

## What we will build — "TSTR Scrape Agent" (3 layers)

### Layer A — Fetch & Parse (reuse, don't rewrite)
- `crawl4ai` = primary (JS + markdown). `trafilatura` = fallback for article/about pages.
- `BS4` kept for simple stable sources (cheap, deterministic).
- Proxy: start with **polite direct + rotate UA + 2–5s delay**; add OCI egress / free proxy list
  only if blocked. Avoid paid proxies initially (cost target ~$0).

### Layer B — Structured Extract (BAML, proven)
- `ExtractLabListing` (exists) for lab/company pages → typed `LabListing`.
- NEW `ExtractNewsArticle` (BAML class) for news: title, source, date, summary, topics[],
  related_industry[].
- NEW `ExtractLead` for lead-gen: company, contact_name, role, email, linkedin, signal
  (e.g. "new lab opened"), intent_score.
- All outputs schema-validated → **catches malformed rows at the edge** (root-cause fix for
  Fix-1 class bugs like `ABIOMED ; jfraile`).

### Layer C — Agent orchestration (new)
- A **scraper agent** (Python, runs on OCI cron): given a *job spec* (source URL(s) + target
  type: lab | news | lead), it: picks extractor → crawls → BAML-extracts → validates →
  deduplicates (reuse `detect_parent`/dedupe) → writes to Supabase → logs result.
- **Lead-gen job:** scan target industries/sources → `ExtractLead` → push to `sales_leads`
  table → feed existing `generate_outreach.py`.
- **News job:** monitor RSS + lab/standards sites → `ExtractNewsArticle` → `industry_news`
  table → later used for content (blog/newsletter) for our audiences + adjacent industries
  (energy, hydrogen, aerospace, pharma, environmental).

### Cross-cutting (from the BAML talk's practices)
- **`architecture.md`** — tiny stable invariants every agent reads.
- **CI schema-invariant check** — pre-merge test that scraper output conforms to the BAML
  class; blocks malformed rows.
- **A/B-test prompts** — measure error rate / tool-calls per extractor variant.
- **Cost guardrail** — cap LLM calls/run; free-tier default; alert if paid used.

## Build phases (incremental, each shippable)
1. **P0 — Harden extract** (1–2 days): move `ExtractLabListing` BAML into the scraper repo
   (not throwaway); add `ExtractNewsArticle` + `ExtractLead`; write Supabase upsert helpers.
2. **P1 — News collector** (2–3 days): RSS + 5 seed sites → `industry_news`; manual review UI
   later. Lowest risk, immediate content value.
3. **P2 — Lead-gen pipeline** (3–5 days): target-source list → `ExtractLead` → `sales_leads` →
   wire to `generate_outreach.py`. Reuse `conglomerates.py` for parent mapping.
4. **P3 — Agent wrapper** (3–5 days): job-spec JSON → orchestrator → Supabase + logs; OCI cron.
5. **P4 — Anti-block + monitoring** (ongoing): proxy/rotate if needed; drift alerts; CI
   schema check; dedupe/merge improvements.

## What else should we consider (beyond the 2 asks)
- **Dedupe/merge** is the silent killer at scale — invest early (P0/P3).
- **Source registry**: a table of "sources → extractor → cadence → owner" so the agent knows
  what to crawl and how (replaces hardcoded scripts).
- **Human-in-the-loop review**: news/leads need a review queue before publish/outreach
  (avoid spamming wrong contacts — reputation risk).
- **Compliance**: scraping ToS + GDPR for lead emails; keep leads flagged "unverified"
  until confirmed. Outreach must be CAN-SPAM/POPIA-compliant (you're ZA-based).
- **Content reuse**: news → blog/LLM newsletter for audiences + adjacent industries (energy,
  hydrogen, aerospace, pharma, environmental) — this is the 2nd stated use, high leverage.
- **Reuse crawl4ai's `ExtractStrategy`/schema mode** to skip hand-writing BAML if faster, but
  BAML gives typed clients + tests (preferred).

## Risks / caveats
- Free LLM pool rate-limits hard (proven: 429 on gemma/llama-free). Pin a paid fallback or BYOK
  for production news/lead runs.
- LinkedIn scraping is ToS-fragile — keep `scrape_linkedin_local.py` manual/opt-in only.
- OCI free tier = 1 VM; heavy crawling may need the always-free shape limits.

## Evidence (this session)
- BAML spike: `SCRAPER_BAML_SPIKE_AND_TOOLING.md` (committed `544eb28`).
- crawl4ai pilot: rendered TÜV SÜD + Intertek → typed BAML output (ran live).
- Throwaway venvs `_baml_spike/`, `_crawl4ai_venv/` are gitignored.
