# 📊 TSTR.DIRECTORY - PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - Executive summary for agents
> **Last Updated**: 2026-08-28 10:16 UTC
> **Updated By**: Hermes Agent
> **Status**: ⚠️ IAF VERIFICATION IN PROGRESS - Pricing-page UI done; backend client is a STUB (# TODO: Implement actual API call in iaf_api_client.py), no API key wired, Basic 499 plan not purchased. See pending tasks.

---

## 🌍 GEOGRAPHIC EXPANSION (PHASE 6)
- [x] **Phase 1: Europe (EA)**: ✅ Scaled (54+ labs via ScopeMatch.eu).
- [x] **Phase 2: Middle East (ARAC)**: ✅ Scaled (25+ labs via GAC & Manual Seeding).
- [ ] **Phase 3: Asia-Pacific (APAC)**: ⚠️ NATA Blocked (Bot protection); redirected to IAF API path.

### 🛡️ GLOBAL VERIFICATION (IAF)
- [ ] **Strategy**: Integrate [IAF CertSearch API](./docs/active/IAF_API_INTEGRATION_PLAN.md) for global verification.
- [ ] **Cost**: ~$499/year for Basic (150 company verifications).
- [ ] **Next**: User registration and API key generation.

---

## 🎯 PROJECT OVERVIEW

| Field | Value |
|-------|-------|
| **Name** | TSTR.directory |
| **Type** | Testing Services Directory Platform |
| **Stack** | Astro 5.x + React 18 + Supabase + Python Scrapers |
| **Deployment** | Cloudflare Pages (Frontend) + OCI (Scrapers) |
| **Listings** | 784 active (Verified on Homepage) |
| **Categories** | 33+ specialized (+3 Hydrogen) |
| **Geospatial** | ✅ Integrated (Google Maps Static + Interactive) |

---

## 🚀 LATEST UPDATES (v2.6.4)
- **Security Hardening**: ✅ **LOCAL FIXES APPLIED + 2026-08-10 REPO REDACTION SWEEP**. Tracked docs/configs and git-ignored credential stores (`docs/credentials/*`, `TSTR_hub_Supabase_Keys.md`, `secret_alerts.json`, `.gitnexus/lbug`) had plaintext secrets redacted; a commit-gating secret scanner now exists (`scripts/secret_scan.py` + `scripts/pre-commit.hook`, see `agents/tstr-secret-scanner.md`). Live debug routes (`/api/debug-env`, `/api/debug-full`) return 404 in production (gated behind `PUBLIC_DEBUG_ENDPOINTS`). ⚠️ **KEY ROTATION STILL PENDING**: 19 GitHub secret-scanning alerts remain OPEN (secrets still in git history + runtimes). Per `CREDENTIAL_ROTATION_RUNBOOK.md`, rotate every exposed credential, then update Cloudflare/OCI/GitHub/local `.env` before alerts can close. `ai-search.ts:8,55` still uses the service-role key — code fix outstanding.
- **Saudi Energy Hub**: ✅ **SEEDED**. Manually enriched top-tier labs (GCC Lab, Al-Hoty, ETLCO).
- **ShellCheck gate**: ✅ **ADDED**. `scripts/shellcheck-changed.sh` lints changed `.sh` at warning severity (excludes `_ARCHIVE/`), wired into `scripts/pre-commit.hook` (shell stage) and `.github/workflows/ci.yml`. Fixed 4 real warnings in active scripts (unquoted `cd` + dead vars). Pre-existing `-S info` hits (unquoted `$DATABASE_URL` in `tests/*.sh`) logged but not enforced.
- **International Scaling**: ✅ **COMPLETE**. Deployed ScopeMatch.eu (Europe) and GAC (Middle East) scrapers. 
- **OAuth Fix**: ✅ **RESOLVED**. Implemented cookie-based state preservation for LinkedIn redirects.
- **Search Experience**: ✅ **IMPROVED**. Added premium floating search button and header search link (v2.6.2).

---

## 📝 PENDING TASKS

### High Priority
- [ ] Register for IAF CertSearch API (User Action required).
- [ ] Implement `iaf_verify_client.py` for global certification checks.
- [x] Standardize Scraper Suite (BaseNicheScraper inheritance).
- [x] Hardened Location Parsing (International support & hierarchy fixes).

### Medium Priority
- [x] Build **Saudi Energy Testing Hub** PSEO landing page.
- [ ] Setup error alerting for scraper failures.
- [ ] Deploy Europe-specific PSEO landing pages.

### Low Priority
- [x] **Fix 1 — invalid URL**: SCANNED 792 live listings (read-only, 2026-08-10).
  - **Confirmed malformed (safe to fix):** `ABIOMED HIGIENE` → `https://abiomed-hygiene.com ; jfraile` (stray `;`+junk). Fix: `update listings set website='https://abiomed-hygiene.com' where business_name='ABIOMED HIGIENE';` (needs a valid write credential — on-disk keys are stale post-rotation; anon PATCH is RLS-blocked).
  - **Full dead-link re-scan attempt (blocked by environment):** an automated HEAD/GET scan from this dev box was unreliable — it flagged ~40 "dead" URLs, but most were false positives: live orgs (3M, SABS, SASO, Waygate/Baker Hughes, MACAW) returned `URLError` only because **this VM's outbound network can't reach them**; others were bot-403/soft-404 on Element/Eurofins deep pages, plus a `UnicodeEncodeError` script bug on a TÜV non-ASCII URL. A trustworthy dead-link scan must run from the **OCI scraper box** (clean outbound) or a neutral network. Action: re-run `cleanup_invalid_urls.py` (or a URL re-validation) on OCI, then apply fixes there.
  - 23 listings have empty website (not "invalid") — left as-is.
- [x] **Fix 2 — wire a free analytics provider**: DONE. Consent-gated loader + cookie banner live; Cloudflare Web Analytics confirmed active on `tstr.directory` (beacon present). Guide: `docs/active/ANALYTICS_SETUP_GUIDE.md`.

---

## 🔗 IMPORTANT LINKS

- **Live Site**: https://tstr.directory
- **GitHub**: https://github.com/JAvZZe/tstr-site
- **Supabase**: https://haimjeaetrsaauitrhfy.supabase.co
