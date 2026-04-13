# TSTR.DIRECTORY - IMPLEMENTATION PROJECT PLAN

## 🏗️ Phase: Niche Localization & Trust Architecture

### 📄 Reference Document
- **Architecture Strategy**: [tstr-architecture-plan.md](./tstr-architecture-plan.md)

### 🎯 Objective
Transition the directory to a dynamic SSR-based PSEO system with a 3-tier trust funnel and parent/branch group hierarchy.

---

## 🛠️ TASK BOARD

### Phase 1: Database Refinement (Supabase)
- [x] **Task 1.1**: RLS lockdown on `listing_capabilities.verified` column. (Migration created)
- [x] **Task 1.2**: Revoke permissive UPDATE policies from standard users. (Migration created)
- [x] **Task 1.3**: Create Postgres View/RPC for Parent Group branch aggregation. (Migration created)
- **Assigned Agent**: `opencode`

### Phase 2: Frontend Architecture (Astro & Cloudflare)
- [x] **Task 2.1**: Implement dynamic SSR routing for `/[category]/[standard]/[region]`. (Page structure created)
- [x] **Task 2.2**: Implement `/group/[slug]` and `/company/[slug]` routes. (Pages created)
- [x] **Task 2.3**: Configure Edge Cache-Control headers for all dynamic PSEO routes. (Headers injected)
- **Assigned Agent**: `omg-executor`

### Phase 3: UI Development (React/Tailwind)
- [x] **Task 3.1**: Build "Compliance Matrix" component.
- [x] **Task 3.2**: Build "Branch Locator" map component for Group pages.
- [x] **Task 3.3**: Integrate Tier 3 "TSTR Verified" badges.
- **Assigned Agent**: `ask-gemini`

### Phase 4: Automation Updates (Python)
- [x] **Task 4.1**: Update scrapers to detect and link parent conglomerate brands.
- [x] **Task 4.2**: Populate `parent_listing_id` for existing branch listings.
- **Assigned Agent**: `qwen`

---

## ✅ VALIDATION CHECKLIST
- [ ] RLS Security: Update on `verified` fails for standard users.
- [ ] PSEO: Dynamic routes resolve correctly at the edge.
- [ ] Caching: `s-maxage` headers present in network responses.
- [ ] Hierarchy: Group pages correctly list all local physical branches.

## ⚙️ Phase 5: Maintenance & Optimization

- [x] **Task 5.1**: Remove duplicate info in Gemini.md.
- [x] **Task 5.2**: Add tools repository link to Gemini.md instead of clogging it up.
- [x] **Task 5.3**: Note that MuninnDB is part of the AI memory in Gemini.md files.
- [x] **Task 5.4**: Add link/name of Skills folders to Gemini.md files.
- [x] **Task 5.5**: Update scrapers to monitor and keep listing info up to date.
- [x] **Task 5.6**: Create live listing counter in Supabase and replace static site numbers.
