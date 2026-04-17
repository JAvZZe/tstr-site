# 📊 TSTR.DIRECTORY - PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - Executive summary for agents
> **Last Updated**: 2026-04-17 11:30 UTC
> **Updated By**: Antigravity (AI Agent)
> **Status**: ✅ PRODUCTION - Live at <https://tstr.directory> (Hydrogen Premium Hub Deployed)

---

## 🎯 PROJECT OVERVIEW

| Field | Value |
|-------|-------|
| **Name** | TSTR.directory |
| **Type** | Testing Services Directory Platform |
| **Stack** | Astro 5.x + React 18 + Supabase + Python Scrapers |
| **Deployment** | Cloudflare Pages (Frontend) + OCI (Scrapers) |
| **Protocol** | ✅ Cleanup & Archiving (Mandatory for all agents) |
| **Listings** | 596+ active |
| **Categories** | 33+ specialized (+3 Hydrogen) |
| **Standards** | 70+ (+15 Hydrogen) |

---

## 📈 COMPONENT STATUS

```
┌─────────────────────────────────────────────┐
│  COMPONENT STATUS                           │
├─────────────────────────────────────────────┤
│  ✅ Database (Supabase)        OPERATIONAL  │
│  ✅ Hydrogen Premium Hub       LIVE         │
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
- [ ] Verify PSEO pages render correctly (Post-slug-fix)
- [ ] Test category page listing visibility
- [ ] Query database for active standards with PSEO pages

### Medium Priority
- [ ] Add more geographic regions (Asia, Europe, Middle East)
- [ ] Setup error alerting for scraper failures
- [ ] Deploy Oil & Gas scraper

---

## 🔗 IMPORTANT LINKS

- **Live Site**: https://tstr.directory
- **GitHub**: https://github.com/JAvZZe/tstr-site
- **Supabase**: https://haimjeaetrsaauitrhfy.supabase.co
