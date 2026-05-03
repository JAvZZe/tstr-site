# 📊 TSTR.DIRECTORY - PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - Executive summary for agents
> **Last Updated**: 2026-05-03 20:09 UTC
> **Updated By**: JAvZZe
> **Status**: ✅ INTERNATIONAL SCALE ACTIVE - Europe & Middle East (v2.6.0)

---

## 🌍 GEOGRAPHIC EXPANSION (PHASE 6)
- [x] **Phase 1: Europe (EA)**: ✅ Scaled (54+ high-fidelity labs via ScopeMatch.eu).
- [x] **Phase 2: Middle East (ARAC)**: ✅ Scaled (14+ labs via GAC).
- [ ] **Phase 3: Asia-Pacific (APAC)**: ⚠️ NATA Blocked (Bot protection); redirected to IAF API path.

### 🛡️ GLOBAL VERIFICATION (IAF)
- [ ] **Strategy**: Integrate [IAF CertSearch API](./docs/active/IAF_API_INTEGRATION_PLAN.md) for cross-border verification.
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
| **Listings** | 781 active (Verified on Homepage) |
| **Categories** | 33+ specialized (+3 Hydrogen) |
| **Geospatial** | ✅ Integrated (Google Maps Static + Interactive) |

---

## 🚀 LATEST UPDATES (v2.6.0)
- **International Scaling**: ✅ **COMPLETE**. Deployed ScopeMatch.eu (Europe) and GAC (Middle East) scrapers. 
- **OAuth Fix**: ✅ **RESOLVED**. Implemented cookie-based state preservation for LinkedIn redirects.
- **Data Integrity**: ✅ **VERIFIED**. Materials Testing enrichment successful (105/219 listings).

---

## 📝 PENDING TASKS

### High Priority
- [ ] Register for IAF CertSearch API (User Action required).
- [ ] Implement `iaf_verify_client.py` for global certification checks.
- [x] Standardize Scraper Suite (BaseNicheScraper inheritance).
- [x] Hardened Location Parsing (International support & hierarchy fixes).
- [ ] Complete Materials Testing backfill (~114 international listings via IAF API).

### Medium Priority
- [ ] Setup error alerting for scraper failures.
- [ ] Deploy Europe-specific PSEO landing pages.
- [ ] Build Saudi-specific energy testing hub.

---

## 🔗 IMPORTANT LINKS

- **Live Site**: https://tstr.directory
- **GitHub**: https://github.com/JAvZZe/tstr-site
- **Supabase**: https://haimjeaetrsaauitrhfy.supabase.co
