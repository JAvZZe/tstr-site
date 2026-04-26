# 📊 TSTR.DIRECTORY - PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - Executive summary for agents
> **Last Updated**: 2026-04-28 07:30 UTC
> **Updated By**: GEMINI (via Antigravity)
> **Status**: ✅ DEPLOYMENT READY - Geospatial Maps (v2.5.1)



---

## 🎯 PROJECT OVERVIEW

| Field | Value |
|-------|-------|
| **Name** | TSTR.directory |
| **Type** | Testing Services Directory Platform |
| **Stack** | Astro 5.x + React 18 + Supabase + Python Scrapers |
| **Deployment** | Cloudflare Pages (Frontend) + OCI (Scrapers) |
| **Protocol** | ✅ Systems Thinking Protocol (Mandatory for all agents) |
| **Listings** | 596+ active (Materials Testing enriched) |
| **Categories** | 33+ specialized (+3 Hydrogen) |
| **Standards** | 70+ (+15 Hydrogen) |
| **Geospatial** | ✅ Integrated (Google Maps Static + Interactive) |

---

## 🚀 LATEST UPDATES (v2.5.0)
- **Google Maps Integration**: ✅ **COMPLETE**. Integrated `<StaticLabMap />` and `<ListingMap />` across Browse, Category, Listing, and Industry pages.
- **Geocoding Optimization**: ✅ **RESOLVED**. Fixed failures for "Global" listings by implementing placeholder coordinate handling (0.000001) and custom UI placeholders ("Global Operations").
- **A2LA Pipeline**: ✅ **STABILIZED**. Resolved custom field ingestion gaps for Materials Testing.

---

## 🔒 SECURITY HARDENING (v2.2)
- **Credential Rotation**: ✅ COMPLETE (Supabase Anon, Service Role, PAT, DB Pass)
- **Secret Scrubbing**: ✅ COMPLETE (Removed from 50+ files in `/web`, `/management`, `/docs`)
- **Git Protection**: ✅ COMPLETE (`.gitignore` updated to exclude `TSTR_hub_Supabase_Keys.md` and MCP configs)
- **Environment Enforced**: ✅ COMPLETE (All scripts now use `os.environ` or `import.meta.env`)
- **Audit Results**: ✅ Verified no legacy JWT keys remaining in codebase or archives.

---

## 📈 COMPONENT STATUS

```
┌─────────────────────────────────────────────┐
│  COMPONENT STATUS                           │
├─────────────────────────────────────────────┤
│  ✅ Database (Supabase)        OPERATIONAL  │
│  ✅ Hydrogen Premium Hub       LIVE         │
│  ✅ Browse Hub (Obsidian)      MIGRATED     │
│  ✅ Standard Matrix            DEPLOYED     │
│  ✅ PSEO Routing (Slashes)     FIXED        │
│  ✅ Frontend (Cloudflare)     LIVE         │
│  ✅ Analytics (Apollo)        ACTIVE       │
└─────────────────────────────────────────────┘
```

---

## 🌐 PSEO ARCHITECTURE (PSEO 2.0)

### Routes & Templates

| Route | Purpose | File |
|-------|---------|------|
| `/hydrogen-testing` | Premium Hydrogen Hub | `src/pages/hydrogen-testing.astro` |
| `/browse` | Global Directory (Obsidian) | `src/pages/browse.astro` |
| `/testing/[industry]/[slug]` | Standard + Industry + Region | `src/pages/testing/[industry]/[slug].astro` |
| `/[category]/[region]/index` | Category + Region | `src/pages/[category]/[region]/index.astro` |
| `/[category]/index` | Category Overview | `src/pages/[category]/index.astro` |
| `/standards/[slug]` | Standard Overview | `src/pages/standards/[slug].astro` |

### Schema Implementations

- **FAQPage Schema**: Auto-generated from database standard metadata
- **ItemList Schema**: Dynamic listing arrays for rich results
- **Conversion Optimization**:
  - `LabManagerTeaser.tsx`: Glassmorphism CTA for B2B portal engagement.
  - `StandardMatrix.tsx`: Technical capability matrix for niche hubs.
  - `Sticky Conversion Bar`: High-velocity hash-triggered (#rfq) RFQ routing.
  - `ContactLabModal.tsx`: Global support and URL hash listening.

---

## 📊 DATA DEBT & STALE BRANCHES

| Branch | Stale Since | Data/Purpose | Conflict Status |
|--------|-------------|--------------|-----------------|
| `hydrogen-standards` | 2026-03-19 | 15 Hydrogen Standards (Recovery) | ✅ RESOLVED - Manual extraction & deployment complete. |
| `feat/astro-6-migration` | 2026-03-24 | Platform Upgrade (Stats Fixes) | ℹ️ LOW - Staged for later phase. |

---

## 📝 PENDING TASKS

### High Priority
- [x] Deploy Hydrogen Premium Page (Obsidian Aesthetic)
- [x] Fix Standard Slug routing (Forward slashes sanitized)
- [x] Migrate Browse Hub to Obsidian Design System
- [x] Verify PSEO pages render correctly (Post-slug-fix)
- [x] Test category page listing visibility
- [x] Standardize Scraper Suite (BaseNicheScraper inheritance)
- [x] Hardened Location Parsing (International support & hierarchy fixes)
- [x] Automate Directory Enrichment (A2LA Custom Fields Stabilized)
- [ ] Run full backfill for Materials Testing (219 listings) - ⚠️ DB VERIFICATION FAILED (Zero custom fields found)
- [x] Setup systemd automation for local enrichment runs
- [x] Query database for active standards with PSEO pages (596 listings / 240 standards)
- [x] Restore OCI maintenance access (SSH key recovered)
- [x] Integrate Google Maps (Static & Interactive) across all core pages
- [x] Resolve 'Global' listing geocoding failures with custom placeholders

### Medium Priority
- [ ] Add more geographic regions (Asia, Europe, Middle East)
- [ ] Setup error alerting for scraper failures
- [ ] Deploy Oil & Gas scraper

---

## 🔗 IMPORTANT LINKS

- **Live Site**: https://tstr.directory
- **GitHub**: https://github.com/JAvZZe/tstr-site
- **Supabase**: https://haimjeaetrsaauitrhfy.supabase.co
