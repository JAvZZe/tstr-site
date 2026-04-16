# 📋 CURRENT WORK - TSTR.directory

> **Active sprints and agent assignments** - Updated: 2026-04-16

---

## 🎯 Active Sprint: PSEO 2.0 Optimization

### Owner
**Agent**: Gemini Flash (in Antigravity session)

### Goals
1. Optimize PSEO (Programmatic SEO) architecture
2. Complete PSEO page refinement and testing
3. Data enrichment for standards
4. Verify E2E conversion flow

---

## ✅ Completed (Antigravity)

### v2.9.17 - PSEO 2.0 Conversion Optimization Overhaul
- **Industry Hubs**: Dark mode "Obsidian" theme with Indigo/Emerald accents
- **Dynamic FAQ**: Auto-generated from database standard metadata
- **Deep-Linking**: `#rfq` hash-triggered modal with `?standard=...` params
- **Sticky CTA**: Mobile/desktop conversion bars
- **IndexNow**: SEO ping integration via `lib/indexnow.ts`

### Design System
| Token | Value |
|-------|-------|
| Background | `#050505` |
| Primary | Indigo `#4F46E5` |
| Secondary | Emerald `#10B981` |
| Card BG | `rgba(17, 17, 17, 0.7)` with `backdrop-filter: blur(12px)` |
| Border | `rgba(255, 255, 255, 0.05)` |

---

## 📋 Pending Work (from Antigravity Handoff)

### 1. Listing Page Refinement
- [ ] **Lab Manager Portal Teaser**: Refactor "Claim Listing" block into high-value dashboard teaser
- [ ] **Animations**: Add fade-up CSS transitions for listing cards and capabilities grid
- [ ] **Data Enrichment**: Backfill `description_long` for top 25 standards in `standards` table

### 2. SEO & Automation
- [ ] **IndexNow Trigger**: Implement admin UI trigger or script to auto-call IndexNow API on standard updates
- [ ] **Schema Audit**: Verify rich results for dynamic FAQs via Search Console URL Inspection

### 3. Verification
- [ ] **E2E Flow Test**: Full funnel `Industry Page -> Listing Page + #rfq -> Pre-filled Modal -> Submission`

---

## 🔄 Pending Handoffs

| From | To | Topic | Status |
|------|----|-------|--------|
| Antigravity | Gemini Flash | PSEO continuation | In Progress |
| opencode | Gemini Flash | Documentation split complete | Done |

---

## 📝 Immediate Next Steps

1. **Verify PSEO pages** - Test `/testing/ndt-testing-inspection/iso-17025-in-global`
2. **Query active standards**:
   ```sql
   SELECT s.slug, s.code, COUNT(lc.listing_id) as listing_count
   FROM standards s
   JOIN listing_capabilities lc ON lc.standard_id = s.id
   GROUP BY s.id, s.slug, s.code
   HAVING COUNT(lc.listing_id) > 0
   ```
3. **Investigate empty category pages** - Check `listing_categories` linkage
4. **Document active PSEO pages** - Which standards have listings

---

## 📊 Sprint Metrics

| Metric | Value |
|--------|-------|
| Listings | 579+ active |
| Categories | 30+ specialized |
| Standards | 55+ |
| Last PSEO Update | 2026-04-16 |

---

## 🔗 Related Documents

- `PROJECT_STATUS.md` - Executive summary
- `docs/VERSION_HISTORY.md` - Full changelog archive
- `HANDOFF_PSEO_OVERHAUL_PARTIAL.md` - Antigravity handoff details
