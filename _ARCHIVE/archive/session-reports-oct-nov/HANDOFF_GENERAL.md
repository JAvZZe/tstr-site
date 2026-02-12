# General Handoff Notes - TSTR.site

**Last Updated**: 2025-11-22
**From**: Claude Sonnet 4.5
**To**: Any future agent

---

## Recent Completion: Analytics System v2.1.0

### What Was Built
1. **Click Tracking System**
   - Internal redirect endpoint: `/api/out?url=X&listing=Y`
   - Security: Database validation prevents open redirect attacks
   - SEO: Internal links preserve PageRank
   - Performance: Async logging (non-blocking)

2. **Analytics Dashboard**
   - URL: https://tstr.site/admin/analytics
   - Features: Metrics, charts, top listings, recent activity, CSV export
   - Database functions: `get_top_clicked_listings()`, `get_click_stats()`
   - RLS policies: Anonymous INSERT, Authenticated SELECT

3. **Documentation**
   - `ANALYTICS_SYSTEM.md` - Comprehensive guide (architecture, security, queries, roadmap)

### Critical Fixes Applied
- ✅ Removed broken Cloudflare edge auth checks (caused 500 errors)
- ✅ Listing detail pages now work (defaulting to 'free' tier)
- ✅ Analytics dashboard accessible (no auth required for now)

### Commits
- `507cee3` - Initial redirect system
- `2b8dc91` - Analytics dashboard
- `f4ffc7e` - Database functions
- `353d094` - Auth fixes + documentation

---

## Key Learnings (Recorded in Global DB)

### Learning #119: Cloudflare Edge Auth Incompatibility
**Tag**: `TSTR.site`, `cloudflare`, `astro`, `supabase`, `auth`
**Issue**: SSR auth checks using `supabase.auth.getUser()` fail on Cloudflare Pages edge runtime
**Solution**: Use client-side auth OR remove SSR auth entirely
**Confidence**: 5/5

### Learning #120: Analytics Dashboard Pattern
**Tag**: `TSTR.site`, `analytics`, `supabase`, `performance`
**Pattern**: Use database RPC functions for aggregation instead of client-side processing
**Example**: `get_top_clicked_listings()` returns pre-aggregated data
**Confidence**: 5/5

### Learning #121: Internal Redirect Pattern
**Tag**: `TSTR.site`, `seo`, `analytics`, `security`
**Pattern**: `/api/out` validates URLs against database before redirect
**Benefits**: Prevents open redirect, preserves SEO, enables analytics
**Confidence**: 5/5

### Learning #122: Documentation Best Practice
**Tag**: `TSTR.site`, `documentation`, `continuity`
**Pattern**: Complex features need dedicated .md files with architecture, security, examples, roadmap
**Why**: Prevents knowledge loss across sessions
**Confidence**: 5/5

### Learning #123: Auth Scope Creep
**Tag**: `TSTR.site`, `auth`, `scope-creep`, `deployment`
**Gotcha**: Don't implement auth checks for features without auth system
**Result**: Causes 500 errors, blocks users
**Solution**: Default to public/free, add TODO, implement when auth is ready
**Confidence**: 5/5

---

## Current State

### Production (LIVE)
- URL: https://tstr.site
- Listings: 163 active
- Click tracking: ✅ Working
- Analytics dashboard: ✅ Accessible at /admin/analytics
- Auth system: ❌ Not implemented (TODO)

### Database (Supabase)
- URL: https://haimjeaetrsaauitrhfy.supabase.co
- Tables: listings, categories, locations, clicks, custom_fields, etc.
- Functions: `get_top_clicked_listings()`, `get_click_stats()`
- Views: `potential_dead_links`
- RLS: Enabled on clicks table
- MCP Server: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`
  - Server: @supabase/mcp-server-supabase@latest
  - Project Ref: haimjeaetrsaauitrhfy
  - Access Token: sbp_e290bc7ea1ba64ae4b0be38134b7b4a67ca24e04
  - Mode: Read-only

### Scrapers (OCI)
- Instance: 84.8.139.90 (Oracle Linux 9)
- Status: ACTIVE
- Schedule: Daily 2:00 AM GMT (`0 2 * * *`)
- Last run: 2025-10-27 (108 listings, 64 contacts)

---

## Next Priorities

### P0 (Critical - Security)
- [ ] Implement authentication system for admin routes
- [ ] Add rate limiting to `/api/out` (prevent click spam)
- [ ] Add bot detection (filter crawlers from analytics)

### P1 (High Value)
- [ ] Dead link detection (monitor clicks → 404s)
- [ ] Email alerts for high-performing listings
- [ ] Click-through rate (CTR) by category/region

### P2 (Enhancements)
- [ ] A/B testing framework
- [ ] Geographic click heatmap
- [ ] Device breakdown (mobile vs desktop)

---

## Common Patterns

### Reading Project Context
```bash
./bootstrap.sh TSTR.site  # Loads project-specific learnings
```

**Note**: The bootstrap script file is `Link_to_bootstrap_agent.sh` in the project root. Always run bootstrap at the start of every session.

```bash
cat .ai-session.md         # Latest session notes
cat ANALYTICS_SYSTEM.md    # Analytics documentation
cat TSTR.md                # Primary project guide
```

### Database Operations
```bash
# Query Supabase
cd web/tstr-frontend
npm run db:query

# Run migration
supabase migration up

# Check analytics
psql -c "SELECT * FROM get_top_clicked_listings(10);"
```

### Deployment
```bash
git add -A
git commit -m "feat: description"
git push origin main
# Triggers: GitHub Actions → Cloudflare Pages
```

### Recording Learnings
```python
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state"
python3 << 'PYEOF'
from db_utils import add_learning
add_learning(
    "Your learning here",
    "pattern",  # or "gotcha", "optimization", "security"
    confidence=5,
    tags=["TSTR.site", "relevant", "tags"]
)
PYEOF
```

---

## Files Changed This Session

### New Files
- `ANALYTICS_SYSTEM.md` - Complete analytics documentation
- `supabase/migrations/20251122000003_create_clicks_table.sql`
- `supabase/migrations/20251122000004_create_analytics_functions.sql`
- `web/tstr-frontend/src/pages/admin/analytics.astro`
- `web/tstr-frontend/src/pages/admin/analytics/export.ts`
- `web/tstr-frontend/src/pages/api/out.ts`
- `web/tstr-frontend/src/lib/redirect.ts`

### Modified Files
- `web/tstr-frontend/src/pages/listing/[slug].astro` (removed auth)
- `web/tstr-frontend/src/pages/[category]/[region]/index.astro` (redirect links)
- `web/tstr-frontend/src/pages/browse.astro` (redirect links)
- `web/tstr-frontend/src/pages/browse/[country].astro` (redirect links)
- `web/tstr-frontend/src/pages/browse/city/[city].astro` (redirect links)
- `web/tstr-frontend/src/pages/standards/iso-19880-3.astro` (redirect links)

---

## Troubleshooting Guide

### Analytics Dashboard Not Loading
1. Check Cloudflare deployment status
2. Check browser console for errors
3. Verify Supabase connection (check logs)
4. Check RLS policies allow SELECT

### Redirects Not Working
1. Check `/api/out.ts` endpoint logs
2. Verify listing_id exists in database
3. Verify URL matches listing.website exactly
4. Check clicks table for logged data

### 500 Errors on Pages
1. Check for SSR auth checks (remove if no auth system)
2. Check Cloudflare edge compatibility
3. Check Supabase queries (validate schema)
4. Check environment variables

---

## Query Global Learnings

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state"
python3 << 'PYEOF'
from db_utils import query_learnings

# TSTR.site specific
learnings = query_learnings(tags=["TSTR.site"])
print(f"Found {len(learnings)} TSTR.site learnings")

# Analytics related
learnings = query_learnings(tags=["analytics"])
for l in learnings:
    print(f"- {l['content'][:100]}")
PYEOF
```

---

## Status Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Frontend | ✅ LIVE | tstr.site (Cloudflare Pages) |
| Database | ✅ LIVE | Supabase (free tier) |
| Scrapers | ✅ ACTIVE | OCI (daily 2AM GMT) |
| Click Tracking | ✅ LIVE | /api/out endpoint |
| Analytics | ✅ LIVE | /admin/analytics (public) |
| Auth System | ❌ TODO | Not implemented |
| Rate Limiting | ❌ TODO | Not implemented |
| Bot Detection | ❌ TODO | Not implemented |

---

**Remember**:
- Always run `./bootstrap.sh TSTR.site` at session start
- Record learnings after discoveries (builds institutional knowledge)
- Check ANALYTICS_SYSTEM.md for analytics questions
- Default to client-side auth (Cloudflare edge incompatible with SSR auth)
- Test locally before deploying (npm run dev)

---

**Last Session**: 2025-11-22 (Analytics v2.1.0)
**Next Agent**: Continue with P0 priorities (auth, rate limiting, bot detection)
