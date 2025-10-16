# TSTR.site - Gemini CLI Project Context

## Project Overview
Global niche directory platform for Tests and Testing Services & Products serving specialized, high-margin industries.

**Target Industries**: Oil & Gas, Pharmaceutical, Biochemistry, Genetics, Satellite, High-Tech Manufacturing, Defense, and other underserved specialized testing sectors.

**Geographic Scope**: Global directory with hierarchical drill-down (Global → Region → Country → City). Localized sites will be established post-profitability.

## Tech Stack
- **Frontend**: Astro + React (tstr-frontend/)
- **Backend/Automation**: Python scrapers + Supabase (tstr-automation/)
- **Database**: Supabase (PostgreSQL)

## Directory Structure
```
TSTR.site/
├── web/
│   ├── tstr-frontend/          # Astro website (Global directory)
│   │   ├── src/
│   │   │   ├── pages/          # Geographic hierarchy routes
│   │   ├── public/
│   │   └── astro.config.mjs
│   └── tstr-automation/        # Python automation
│       ├── dual_scraper.py     # PRIMARY: Listings + leads
│       ├── scraper.py          # SECONDARY: Listings only
│       ├── auto_updater.py     # Scheduler
│       └── generate_outreach.py
```

## Key Files
- **Frontend entry**: tstr-frontend/src/pages/index.astro
- **PRIMARY scraper**: tstr-automation/dual_scraper.py (listings + leads)
- **Listings scraper**: tstr-automation/scraper.py (directory only)
- **Supabase setup**: tstr-automation/SUPABASE_*.sql
- **Environment**: tstr-frontend/.env (Supabase keys)

## Gemini CLI Usage Strategy
Use Gemini for token-efficient tasks:
- Simple code generation (boilerplate, utilities)
- File editing and refactoring
- Documentation generation
- SQL query writing
- CSV/data processing scripts

Reserve Claude Code for:
- Complex architecture decisions
- Multi-file refactoring
- Debugging intricate issues
- Integration work

## Development Principles
1. **MVP-first**: Ship quick, iterate based on feedback
2. **Systematic testing**: One feature at a time with checkpoints
3. **Git commits**: Every working checkpoint for easy rollback
4. **Pareto focus**: 80/20 rule - focus on high-impact features
5. **Cost optimization**: Use cheapest effective tool (Gemini < Claude Code)

## Current Status
- Frontend: Astro site deployed
- Backend: Python scrapers operational
  - **PRIMARY**: dual_scraper.py (listings + lead data)
  - **SECONDARY**: scraper.py (listings only)
- Database: Supabase configured
- Automation: Auto-updater running

## Common Tasks
```bash
# Frontend development
cd web/tstr-frontend && npm run dev

# Run PRIMARY scraper (listings + leads)
cd web/tstr-automation && python dual_scraper.py

# Run listings scraper (directory only)
cd web/tstr-automation && python scraper.py

# Test Supabase connection
cd web/tstr-automation && python test_supabase.py
```

## Important Notes
- API keys in .env files - never commit
- Follow existing code style
- Test incrementally
- Document breaking changes
