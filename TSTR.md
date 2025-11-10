# TSTR.md - AI Agent Context for TSTR.site Project

> **Purpose**: Instructions for AI agents (Claude, Gemini, etc.) working on TSTR.site
> **Last Updated**: 2025-11-09
> **Read This**: Every new session, before making changes

---

## Project Overview

**TSTR.site** - Global niche directory for Testing Services & Products serving specialized, high-margin industries (Oil & Gas, Environmental, Materials Testing, Pharmaceuticals, etc.).

**Business Model**: B2B directory + lead generation for testing laboratories seeking clients in specialized sectors.

**Status**: Production - 127 listings deployed, scrapers active on OCI, frontend needs rebuild

---

## Architecture

### Current Stack

**Frontend** (Not deployed yet):
- Astro 5.14.4 + React 18.3.1 + Tailwind CSS
- Location: `web/tstr-frontend/`
- Target: Cloudflare Pages (free tier)
- Status: Built but not deployed

**Scrapers** (ACTIVE in production):
- Python 3.9.21 on Oracle Linux 9
- Location: OCI instance 84.8.139.90 at `~/tstr-scraper/`
- Scheduler: Cron `0 2 * * *` (2 AM GMT daily)
- Status: ✅ Working (last run 2025-10-27: 108 listings, 64 contacts)
- Cost: FREE (Oracle Always Free Tier)

**Database**:
- Supabase PostgreSQL (free tier)
- URL: https://haimjeaetrsaauitrhfy.supabase.co
- Tables: `listings` (main), `custom_fields` (JSON), `pending_research`
- Status: ✅ Operational

**Deployment Flow**:
```
OCI Cron (daily 2AM)
    ↓
Python scrapers run (A2LA, TNI, Rigzone, etc.)
    ↓
Parse data → validate → deduplicate
    ↓
Insert to Supabase listings table
    ↓
Frontend queries Supabase (when deployed)
```

---

## Key File Locations

### Project Root
- `TSTR.md` - This file (agent instructions)
- `PROJECT_STATUS.md` - Deployment status, infrastructure details
- `README.md` - User-facing project overview
- `.ai-session.md` - Session notes and learnings
- `GEMINI.md` - Gemini CLI agent context
- `HANDOFF_TO_CLAUDE.md` - Latest handoff (from Gemini)

### Frontend
```
web/tstr-frontend/
├── src/
│   ├── pages/index.astro       # Homepage
│   ├── components/             # React components
│   └── layouts/
├── .env                        # Supabase keys (GITIGNORED)
├── package.json
└── astro.config.mjs
```

### Scrapers (Active on OCI)
```
web/tstr-automation/
├── scrapers/
│   ├── a2la_materials.py       # A2LA accredited labs (complex auth)
│   ├── tni_environmental.py    # TNI environmental labs
│   └── rigzone_oil_gas.py      # Oil & Gas testing
├── base_scraper.py             # Shared scraper utilities
├── location_parser.py          # Geographic data extraction
├── requirements.txt
└── *.sql                       # Database schemas
```

### OCI Scraper Deployment
- **Instance IP**: 84.8.139.90
- **OS**: Oracle Linux 9, Python 3.9.21
- **Path**: `~/tstr-scraper/` on OCI instance
- **SSH Key**: `/media/al/AvZ White 1TB WD MyPassport/PROJECTS/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key`
- **Access**: `ssh -i "<key_path>" opc@84.8.139.90`

---

## Development Principles

### User Profile
- **Non-technical, AuDHD**: Terse, factual communication. No fluff.
- **Methodologies**: OODA Loop, Pareto Principle (80/20), First Principles Thinking, Game Theory, Root Cause Analysis
- **Testing**: Always test before deploying. MVP approach. Iterate fast.

### Code Standards
1. **MVP-first**: Ship quickly, iterate based on feedback
2. **Test systematically**: One feature at a time with checkpoints
3. **Git discipline**: Commit every working checkpoint for easy rollback
4. **Pareto focus**: 80/20 rule - focus on high-impact features first
5. **Cost optimization**: Use cheapest effective tool (Oracle Free Tier, Supabase Free Tier, Cloudflare Free Tier)

### Common Patterns

**Scraper Development**:
- Base all scrapers on `base_scraper.py` (shared utilities)
- Handle authentication complexity (A2LA uses Touchstone SAML2)
- Parse locations with `location_parser.py` (handles "City, State" and "City, Country")
- Validate before inserting (check duplicates, validate required fields)
- Log everything for debugging

**Database Operations**:
- Use Supabase CLI: `~/.local/bin/supabase`
- Local dev: `supabase status`, `supabase db remote psql`
- Query: `supabase db remote psql -c "SELECT COUNT(*) FROM listings;"`
- Schema changes: Create SQL migration files

**Frontend Development**:
- Use `npm run dev` for local testing
- Build with `npm run build` (requires `.env` with Supabase keys)
- Deploy via Cloudflare Pages (connected to GitHub `main` branch)

---

## Current Priorities

### P0 - Critical
1. **Fix GitHub workflow failure**: Workflow "Keep Supabase Active" failed due to uncommitted changes
   - Commit changes in `GEMINI.md` and `PROJECT_STATUS.md`
   - Update `web/tstr-automation/.gitignore` to exclude report files (*.md, *.txt, *.csv, *.sql in automation folder)
   - Re-evaluate untracked Python files in scrapers/

2. **Frontend deployment**: Build and deploy Astro frontend to Cloudflare Pages
   - Ensure `.env` has correct Supabase keys
   - Test locally first
   - Deploy via GitHub push

### P1 - High
3. **Expand scraper coverage**: Add more testing categories and regions
4. **Monitoring**: Setup error alerting for OCI scraper failures
5. **Admin dashboard**: Create simple dashboard to monitor scraper runs and data quality

### P2 - Medium
6. **Revenue features**: Lead generation, contact exports, premium listings
7. **SEO optimization**: Meta tags, sitemap, structured data
8. **Analytics**: Track user behavior, popular categories

---

## Common Commands

### OCI Scraper Management
```bash
# SSH to OCI instance
ssh -i "/media/al/AvZ White 1TB WD MyPassport/PROJECTS/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key" opc@84.8.139.90

# Check cron schedule
ssh opc@84.8.139.90 "crontab -l"

# View scraper logs
ssh opc@84.8.139.90 "tail -100 ~/tstr-scraper/scraper.log"

# Run scraper manually
ssh opc@84.8.139.90 "cd ~/tstr-scraper && python3 main_scraper.py"
```

### Local Development
```bash
# Frontend dev server
cd web/tstr-frontend && npm run dev

# Build frontend
cd web/tstr-frontend && npm run build

# Test scraper locally (requires .env with Supabase keys)
cd web/tstr-automation
python3 scrapers/tni_environmental.py

# Database query
~/.local/bin/supabase db remote psql -c "SELECT COUNT(*) FROM listings;"
```

### Git Workflow
```bash
# Standard flow
git status
git add <files>
git commit -m "description"
git push origin main  # Triggers Cloudflare auto-deploy (when configured)

# Check GitHub Actions
gh run list
gh run view <run-id>
```

---

## Key Learnings (Add to .ai-session.md)

### Scrapers
- **A2LA authentication**: Complex Touchstone SAML2, requires session cookies
- **CSV encoding**: Use `encoding='utf-8-sig'` to handle BOM
- **Oracle Linux**: Python 3.9.21 (not 3.11+), use compatible packages
- **Cron gotcha**: Needs absolute paths or explicit PATH

### Database
- **Supabase free tier**: 500MB limit, 50K rows
- **Custom fields**: Use JSONB column for flexible schema
- **RLS policies**: Required for frontend access, set up per table

### Deployment
- **Google Cloud**: OVERDUE and unavailable - all moved to OCI
- **OCI Always Free**: Perfect for scrapers, no expiry
- **Cloudflare Pages**: Auto-deploy from GitHub, free tier generous
- **Cost target**: <$1/day total (currently $0 on free tiers)

---

## Troubleshooting

### Scraper Issues
1. Check OCI logs: `ssh opc@84.8.139.90 "tail -100 ~/tstr-scraper/scraper.log"`
2. Verify cron is running: `ssh opc@84.8.139.90 "crontab -l"`
3. Test scraper manually on OCI: `ssh opc@84.8.139.90 "cd ~/tstr-scraper && python3 main_scraper.py"`
4. Check Supabase for new data: `supabase db remote psql -c "SELECT * FROM listings ORDER BY created_at DESC LIMIT 10;"`

### Frontend Issues
1. Verify `.env` exists in `web/tstr-frontend/` with correct Supabase keys
2. Test build locally: `cd web/tstr-frontend && npm run build`
3. Check Cloudflare Pages deployment logs in dashboard
4. Verify GitHub Actions workflow succeeded: `gh run list`

### Database Issues
1. Test connection: `~/.local/bin/supabase status`
2. Check RLS policies: `supabase db remote psql -c "\d+ listings"`
3. Verify data: `supabase db remote psql -c "SELECT COUNT(*) FROM listings;"`

---

## File Retention Policy

**Root-level files (keep only current)**:
- `TSTR.md` - Agent instructions (this file)
- `PROJECT_STATUS.md` - Deployment status
- `README.md` - Project overview
- `.ai-session.md` - Session notes
- `GEMINI.md`, `HANDOFF_TO_CLAUDE.md` - Agent handoffs (archive after resolution)
- Config files: `.gitignore`, `netlify.toml`, `package.json`

**Archive to `archive/old-docs/`**:
- Historical handoff files
- Old deployment summaries
- Outdated documentation
- Meta-system scaffolding (AGENT_*.md, CASCADE.md, etc.)

**Move to `docs/`**:
- Technical deep-dives (still relevant)
- Architecture diagrams
- Domain knowledge references

**Auto-generated reports** (in `web/tstr-automation/`):
- Format: `REPORT_NAME_YYYYMMDD.md`
- Archive anything >30 days old to `archive/reports/YYYY-MM/`
- Examples: `DEPLOYMENT_REPORT_20251109.md`

**Rule**: If README doesn't mention it, question if it belongs in root.

---

## Next Session Checklist

When starting a new session:
1. ✅ Read `START_HERE.md` for orientation (if first time)
2. ✅ Read `.ai-session.md` for latest context
3. ✅ Check `HANDOFF_TO_CLAUDE.md` (or latest handoff file)
4. ✅ Review `PROJECT_STATUS.md` for deployment status
5. ✅ Run `git status` to check for uncommitted changes
6. ✅ Check OCI scraper status: `ssh opc@84.8.139.90 "tail -20 ~/tstr-scraper/scraper.log"`
7. ✅ Update `.ai-session.md` with new session details
8. ✅ Add learnings to `.ai-session.md` as you discover them

---

## References

- **GitHub Repo**: https://github.com/JAvZZe/tstr-site.git
- **Live Site**: https://tstr.site (when deployed)
- **Supabase Dashboard**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
- **Cloudflare Pages**: (To be configured)
- **Technical Docs**: See `docs/` folder

---

**Remember**: First Principles. OODA Loop. Test before deploy. No theater, working code only.
