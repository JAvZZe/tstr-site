# 📊 TSTR.DIRECTORY - PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - Executive summary for agents
> **Last Updated**: 2026-04-16 18:33 UTC
> **Updated By**: JAvZZe
> **Status**: ✅ PRODUCTION - Live at <https://tstr.directory>

---

## 🎯 PROJECT OVERVIEW

| Field | Value |
|-------|-------|
| **Name** | TSTR.directory |
| **Type** | Testing Services Directory Platform |
| **Stack** | Astro 5.x + React 18 + Supabase + Python Scrapers |
| **Deployment** | Cloudflare Pages (Frontend) + OCI (Scrapers) |
| **Listings** | 579+ active |
| **Categories** | 30+ specialized |
| **Standards** | 55+ |

---

## 📈 COMPONENT STATUS

```
┌─────────────────────────────────────────────┐
│  COMPONENT STATUS                           │
├─────────────────────────────────────────────┤
│  ✅ Database (Supabase)        OPERATIONAL  │
│  ✅ URL Validation             LIVE         │
│  ✅ Click Tracking             DEPLOYED     │
│  ✅ OCI Scrapers              DEPLOYED     │
│  ✅ Local Heavy Scrapers      ACTIVE       │
│  ✅ Frontend (Cloudflare)     LIVE         │
│  ✅ Analytics (Apollo)        ACTIVE       │
└─────────────────────────────────────────────┘

Cost/Month:       $0.00 (Oracle Always Free Tier)
Automation:       100% (cron daily 2 AM GMT)
```

---

## 🌐 PSEO ARCHITECTURE (PSEO 2.0)

### Routes & Templates

| Route | Purpose | File |
|-------|---------|------|
| `/testing/[industry]/[slug]` | Standard + Industry + Region | `src/pages/testing/[industry]/[slug].astro` |
| `/[category]/[region]/index` | Category + Region | `src/pages/[category]/[region]/index.astro` |
| `/[category]/index` | Category Overview | `src/pages/[category]/index.astro` |
| `/standards/[slug]` | Standard Overview | `src/pages/standards/[slug].astro` |

### Schema Implementations

- **FAQPage Schema**: Auto-generated from database standard metadata
- **ItemList Schema**: Dynamic listing arrays for rich results
- **Organization Schema**: Homepage and category pages

### PSEO Infrastructure

- **IndexNow Integration**: `src/lib/indexnow.ts`
  - Notifies Bing, Yandex on listing updates
  - URL matrix generation per listing
- **Edge Caching**: `Cache-Control: s-maxage=86400, stale-while-revalidate=3600`

### URL Matrix Pattern

Each listing generates URLs for:
- `/company/[slug]` - Main profile
- `/[category]/[region]/[slug]` - Category + Region permutations
- `/testing/[industry]/[standard]-[region]/[slug]` - PSEO pages

### Standards with PSEO Pages

Query database to identify active standards with linked listings:
- Core NDT: iso-17025, asme-section-iii, api-510/570/653
- Hydrogen: iso-19880-1, iec-62282-3-100
- Aerospace: mil-std-810h, ams-2644
- [Full list in database - query needed]

### Known PSEO Issues

1. **Category pages showing empty** - Listings may not be linked to `listing_categories`
2. **Testing industry pages empty** - Requires `listing_capabilities` + `listing_categories` linkage
3. **URL slug generation** - Standards need proper slugs (verified for iso-ts-15916-2026)

---

## 💳 PAYMENT SYSTEM

- ✅ **PayPal LIVE** - Professional ($295/mo), Premium ($795/mo)
- ✅ **Manual Payments** - EFT, Bitcoin
- ✅ **Webhook Processing** - Production active

---

## 📧 EMAIL SYSTEM

- ✅ **Shared Service**: `src/services/email.ts`
- ✅ **Subdomains**: Via Cloudflare (e.g., `mg.tstr.directory`)
- ✅ **Resend Integration**: Claim verification, payment notifications

---

## 🛠️ DEPLOYED INFRASTRUCTURE

### Database (Supabase)
- **URL**: https://haimjeaetrsaauitrhfy.supabase.co
- **Tables**: `listings`, `listing_categories`, `listing_capabilities`, `standards`, `clicks`, `leads_rfq`
- **Status**: ✅ OPERATIONAL

### Oracle Cloud (OCI)
- **Instance**: 84.8.139.90 (Oracle Linux 9)
- **Scrapers**: Daily 2 AM GMT
- **Status**: ✅ OPERATIONAL (Free Tier)

### Frontend (Cloudflare Pages)
- **URL**: https://tstr.directory
- **Stack**: Astro 5.x + React 18 + Tailwind CSS
- **Status**: ✅ LIVE

---

## 🚨 KNOWN ISSUES

1. **Category pages showing empty** - Investigate `listing_categories` linkage
2. **Apollo Tracking** - Not verified working (needs test)
3. **PSEO pages empty** - May need `listing_capabilities` data

### Fixed Issues

- ✅ Search API Location Filter (2026-04-15)
- ✅ PayPal Subscription Flow (2026-01-16)
- ✅ Account Dashboard UI (2026-01-02)
- ✅ JSON-LD Parsing Error (2026-01-01)

---

## 📝 PENDING TASKS

### High Priority
- [ ] Verify PSEO pages render correctly
- [ ] Test category page listing visibility
- [ ] Query database for active standards with PSEO pages

### Medium Priority
- [ ] Add more geographic regions (Asia, Europe, Middle East)
- [ ] Setup error alerting for scraper failures
- [ ] Deploy Oil & Gas scraper

### Phase 3 (Future)
- [ ] Team management for multi-user listing access
- [ ] Advanced verification methods
- [ ] API access for integrations

---

## 🔗 IMPORTANT LINKS

- **Live Site**: https://tstr.directory
- **GitHub**: https://github.com/JAvZZe/tstr-site
- **Supabase**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
- **OCI SSH**: `ssh -i /tmp/oci-key.pem opc@84.8.139.90`

---

## 📚 DOCUMENTATION STRUCTURE

| Document | Purpose |
|----------|---------|
| `PROJECT_STATUS.md` | This file - Executive summary |
| `docs/VERSION_HISTORY.md` | Full changelog archive (v2.3.5+) |
| `docs/CURRENT_WORK.md` | Active sprints, agent assignments |
| `docs/REFERENCE_STATUS.md` | Historical versions pre-v2.3.5 |
| `docs/MAINTENANCE_LOG.md` | Security/linting updates |

---

## 🤖 AGENT UTILIZATION

- **Claude Sonnet 4.5**: Complex reasoning, architecture
- **Gemini 2.5 Pro**: Continuation, medium complexity (FREE)
- **Gemini Flash**: Quick tasks, PSEO optimization (FREE)
- **Qwen3-Coder**: Bulk operations, cost-effective ($0.45/1M input)
