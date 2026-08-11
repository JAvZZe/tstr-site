# BAML Spike + Open-Source Scraper Tooling Review (2026-08-11)

## 1. BAML spike — RESULT: ✅ WORKS (proven, $0 cost)

**Goal:** test BAML (BoundaryML) for structured extraction of lab-listing fields, to judge
if it should replace/adopt in the scraper.

**Setup:** throwaway venv in `web/tstr-automation/_baml_spike/`
- `baml-cli 0.225.0`, SDK import `baml_py`, generated client `baml_client/`.
- Defined `class LabListing` + `function ExtractLabListing(raw_page_text) -> LabListing`
  mirroring the scraper schema (business_name, website, email, phone, address,
  testing_types[], certifications[], description).
- Provider: **OpenRouter free tier** (`nvidia/nemotron-3-super-120b-a12b:free` —
  `google/gemma-4-31b-it:free` and `meta-llama/llama-3.1-8b-instruct:free` were 429/404
  on the shared free pool; nemotron-3-super was reachable).

**Evidence (real run, Element.com homepage):**
```
business_name: "Element"
testing_types: [Aerospace, Connected Technologies, Construction & Infrastructure, Defense, Energy, Environmental]
certifications: [Nadcap Approved, US NRTL, Canadian SCC, IECEE CB Scheme, FCC, ISED, ...]
description: "Element provides testing, inspection, and certification services across ..."
```
Typed, validated output. BAML built the prompt, called OpenRouter, parsed+validated JSON
into the Pydantic model. website/email/phone/address were `null` only because the homepage
is a JS nav page (no contact details in raw HTML) — a contact/about page would fill them.

**Verdict:** BAML delivers on its promise — strict, type-safe LLM output with retries,
no hand-rolled JSON parsing. But the *current* scraper extracts via BeautifulSoup (no LLM),
so BAML's value is for a **future AI-enrichment path**, not the live extractor. The existing
`enrich_listings.py` does DDG search only (no LLM). BAML fits there.

**Recommendation:** Adopt BAML *only* for the AI-enrichment step (extract structured fields
from lab pages / classify testing types / certs), behind a feature flag. Keep BS4 as the
primary extractor (cheaper, deterministic, no LLM dependency). Do NOT rewrite the existing
scraper in BAML.

## 2. Open-source scraper tooling — what's available & worth adopting

Live GitHub stats (2026-08-11), all active (not archived):

| Tool | ★ | License | Lang | Best for | Fit for TSTR |
|------|---|---------|------|----------|--------------|
| **crawl4ai** | 78k | Apache-2.0 | Py | LLM-ready scraping, markdown/structured output, JS rendering | **High** — drop-in upgrade for AI enrichment |
| **browser-use** | 109k | MIT | Py | Browser agent (clicks, navigates) | Medium — only if JS-heavy sites need interaction |
| **trafilatura** | 6.6k | Apache-2.0 | Py | Main-content / article extraction, metadata | **High** — clean text from lab "about" pages |
| **crawlee** | 25k | Apache-2.0 | TS/JS | Robust crawler, anti-bot, Python port exists | Medium — if we scale to many sources |
| **scrapy** | 64k | BSD-3 | Py | Classic large-scale crawling | Low — overkill vs current BS4 scripts |
| **markitdown** (MS) | 173k | MIT | Py | Docs/PDF→Markdown | Low-Med — only for PDF datasheets |
| **maxun** | 17k | AGPL-3.0 | TS | No-code point-extract | Low (AGPL, no-code — not for our agent stack) |
| **newspaper** | 15k | MIT | Py | News article parse | Low (news-specific) |
| **playwright** | — | Apache-2.0 | Py/TS | Headless browser engine | **Infra** — underpinning for JS rendering |

**Recommended stack for the "better scraper toolset" rebuild:**
1. **crawl4ai** (primary) — renders JS, outputs clean markdown, built for LLM ingestion.
   Pairs perfectly with BAML: crawl4ai → markdown → BAML → typed LabListing.
2. **trafilatura** (secondary) — main-content extraction for directory/about pages where
   crawl4ai is heavy.
3. **Playwright** (infra) — only if a source needs real browser interaction; browser-use
   on top if agentic navigation is needed.
4. Keep **BS4** for the simple, stable sources (cheap, deterministic).
5. **BAML** for the structured-LLM layer (proven above).

## 3. Future useful things to build (roadmap)

**Scraper toolset / agent rebuild:**
- [ ] Pilot `crawl4ai` on 3–5 representative lab sources; compare extraction quality vs BS4.
- [ ] Wire `crawl4ai → BAML.ExtractLabListing` for AI enrichment (replaces DDG-only `enrich_listings.py`).
- [ ] Add `trafilatura` for about-page main-content extraction.
- [ ] Build a **scraper agent** (agentic): given a source URL, pick extractor (BS4/crawl4ai/
  trafilatura), validate against schema, retry on failure, log to Supabase.
- [ ] Centralize validation: reuse `url_validator.py` + add schema/field validation (the
  ABIOMED `; jfraile` junk would be caught by a strict parser).
- [ ] Dedupe/merge pipeline: better parent-company detection (`detect_parent` exists, weak).
- [ ] Cost guardrails: cap LLM calls per run; use free tier (OpenRouter) for enrichment.

**General AI-system improvements (from the BAML talk's practices, applicable to TSTR):**
- [ ] A tiny stable `architecture.md` (not just CLAUDE.md) that every agent/model reads —
      invariants that won't change for months.
- [ ] CI invariants: a CLI check that scraper output conforms to the listing schema before
      merge (catch malformed rows early — root-cause fix for Fix 1 class of bugs).
- [ ] A/B-test agent prompts: measure tool-call count / error rate per scraper variant.
- [ ] Keep the continuity system (checkpoints/learnings) — already in place.

## 4. Notes / caveats
- Free-tier LLM models rotate (the `:free` slugs change availability). Pin a paid fallback
  or check `/api/v1/models` before runs.
- BAML spike lives in `_baml_spike/` (NOT committed to the scraper). Re-run:
  `cd _baml_spike && . .venv/bin/activate && baml generate --from baml_src && python run_spike.py`
- The shared OpenRouter free pool rate-limits hard (429); for production use a paid key or
  BYOK to accumulate limits.
