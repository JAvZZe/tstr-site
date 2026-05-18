# 📊 TSTR.DIRECTORY - PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - Executive summary for agents
> **Last Updated**: 2026-05-18 17:38 UTC
> **Updated By**: JAvZZe
> **Status**: 🛡️ SECURITY HARDENING IN PROGRESS - Local CodeQL fixes applied (v2.6.4)

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
- **Security Hardening**: ✅ **LOCAL FIXES APPLIED**. Removed a hardcoded instrumentation API key from tracked code, sanitized API error responses, disabled local Flask debug defaults, tightened workflow permissions, added exact host checks, reduced sensitive logging, and ignored raw GitHub alert exports. Credential rotation/provider verification remains a separate dashboard task.
- **Saudi Energy Hub**: ✅ **SEEDED**. Manually enriched top-tier labs (GCC Lab, Al-Hoty, ETLCO).
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
- [ ] Build **Saudi Energy Testing Hub** PSEO landing page.
- [ ] Setup error alerting for scraper failures.
- [ ] Deploy Europe-specific PSEO landing pages.

---

## 🔗 IMPORTANT LINKS

- **Live Site**: https://tstr.directory
- **GitHub**: https://github.com/JAvZZe/tstr-site
- **Supabase**: https://haimjeaetrsaauitrhfy.supabase.co
