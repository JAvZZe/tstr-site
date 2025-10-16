# TSTR.site - Gemini CLI Project Context

## Project Overview
Global niche directory platform for Tests and Testing Services & Products serving specialized, high-margin industries.

**Target Industries**: Oil & Gas, Pharmaceutical, Biochemistry, Genetics, Satellite, High-Tech Manufacturing, Defense, and other underserved specialized testing sectors.

**Geographic Scope**: Global directory with hierarchical drill-down (Global → Region → Country → City).

## Tech Stack & Deployment
- **Frontend**: Astro + React (`web/tstr-frontend/`)
- **Backend/Automation**: Python scrapers (`web/tstr-automation/`)
- **Database**: Supabase (PostgreSQL)
- **Hosting**: Netlify (connected to GitHub)
- **GitHub Repo**: `https://github.com/JAvZZe/tstr-site.git`

## Deployment & Automation Workflow
1.  **Code Push**: All changes are pushed to the `main` branch on GitHub.
2.  **Netlify Build**: Netlify automatically detects the push, builds the frontend, and deploys it.
    - **Base directory**: `web/tstr-frontend`
    - **Build command**: `npm run build`
    - **Publish directory**: `web/tstr-frontend/dist`
3.  **Scraper Execution**: A cloud scheduler runs the Python scrapers automatically every 3 days.
4.  **Database Update**: Scrapers add new listings to the Supabase `listings` table.
5.  **Live Site Update**: A Supabase Webhook triggers a new Netlify build whenever the `listings` table is updated, ensuring new data appears on the live site automatically.

## Key Files
- **Frontend entry**: `web/tstr-frontend/src/pages/index.astro`
- **PRIMARY scraper**: `web/tstr-automation/dual_scraper.py`
- **Deployment Plan**: `DEPLOY_NOW.md`
- **Supabase Schema**: `web/tstr-automation/SUPABASE_*.sql`
- **Frontend Environment**: `web/tstr-frontend/.env` (stores public Supabase keys)

## Development Principles
1. **MVP-first**: Ship quick, iterate based on feedback.
2. **Systematic testing**: One feature at a time with checkpoints.
3. **Git commits**: Every working checkpoint for easy rollback.
4. **Pareto focus**: 80/20 rule - focus on high-impact features.
5. **Cost optimization**: Use cheapest effective tool.

## Current Status
- **Frontend**: Ready for first deployment to Netlify.
- **Backend**: Python scrapers are operational.
- **Database**: Supabase schema is defined and ready.
- **Automation**: Auto-update workflow (Supabase Webhook -> Netlify Build Hook) is designed and ready for implementation post-deployment.

## Common Tasks
```bash
# Frontend development
cd web/tstr-frontend && npm run dev

# Run PRIMARY scraper (listings + leads)
cd web/tstr-automation && python dual_scraper.py

# Deploy Frontend (after committing to git)
git push origin main
```

## Important Notes
- API keys in `.env` files must never be committed to Git.
- The `.gitignore` file is configured to prevent this.
- Follow existing code style and test incrementally.