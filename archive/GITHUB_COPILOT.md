# TSTR.site - GitHub Copilot CLI Project Context

## Agent Identity
**Name**: GitHub Copilot CLI  
**Account**: albertus@albertusangkuw.com  
**Environment**: PowerShell 7 (Windows)  
**Strengths**: Terminal automation, DevOps, CLI workflows, PowerShell scripting, multi-tool orchestration

---

## Project Overview
Global niche directory platform for Tests and Testing Services & Products serving specialized, high-margin industries.

**Target Industries**:
- Oil & Gas Testing
- Pharmaceutical Testing
- Biochemistry & Genetics Testing
- Satellite & Aerospace Testing
- High-Tech & Silicon Chip Manufacturing
- Defense & Military Testing
- Other underserved specialized testing sectors (to be researched)

**Core Value Proposition**: Connect specialized testing service providers with high-value industrial clients in underserved niche markets through automated directory population, SEO-optimized landing pages, and global-to-local geographic hierarchy.

**Geographic Strategy**: Global directory structure drilling down through regional → country → city levels. Localized sites will be established and mirrored after initial profitability is achieved.

---

## Tech Stack

### Frontend (Astro + React)
- **Framework**: Astro 5.x (static site generation)
- **UI**: React 18 + Tailwind CSS
- **Hosting**: Cloudflare Pages (free tier)
- **Location**: `web/tstr-frontend/`
- **Entry Point**: `src/pages/index.astro`

### Backend (Python + Supabase)
- **Database**: Supabase (PostgreSQL)
- **Automation**: Python 3.11 scrapers
- **Location**: `web/tstr-automation/`
- **Key Scripts**:
  - `dual_scraper.py` - **Primary scraper** (listings + lead generation data)
  - `scraper.py` - **Listings scraper** (directory listings only)
  - `auto_updater.py` - Scheduled data updates
  - `test_supabase.py` - Database connection testing

### Infrastructure
- **Version Control**: Git (local, not yet remote)
- **CI/CD**: GitHub Actions (planned)
- **Package Managers**: npm (frontend), pip (backend)

---

## Directory Structure
```
TSTR.site/
├── web/
│   ├── tstr-frontend/          # Astro website (Global directory)
│   │   ├── src/
│   │   │   ├── pages/          # Routes (geographic hierarchy)
│   │   │   │   ├── index.astro              # Global homepage
│   │   │   │   ├── [region]/               # Regional pages
│   │   │   │   ├── [country]/              # Country pages
│   │   │   │   └── [city]/                 # City pages
│   │   │   ├── components/     # React components
│   │   │   └── layouts/        # Page templates
│   │   ├── public/             # Static assets
│   │   ├── .env                # Supabase keys
│   │   └── astro.config.mjs    # Astro config
│   │
│   └── tstr-automation/        # Python automation
│       ├── dual_scraper.py     # PRIMARY: Listings + leads scraper
│       ├── scraper.py          # Listings scraper (directory only)
│       ├── auto_updater.py     # Scheduler
│       ├── config.json         # Industry targets & sources
│       ├── requirements.txt    # Python deps
│       └── SUPABASE_*.sql      # Database schema (global hierarchy)
│
├── management/                 # Project docs
│   ├── reference/              # Credentials & guides
│   ├── tasks/                  # Task tracking
│   └── agents/                 # Agent-specific files
│
├── .env.github-copilot         # Copilot environment
├── GITHUB_COPILOT.md          # This file
├── GEMINI.md                   # Gemini agent context
└── handoff_core.md             # Multi-agent handoff log
```

---

## GitHub Copilot Usage Strategy

### Primary Responsibilities
Use GitHub Copilot CLI for **automation-heavy, terminal-centric tasks**:

1. **DevOps & Deployment**
   - Git operations (commit, branch, merge)
   - CI/CD pipeline setup (GitHub Actions)
   - Environment configuration
   - Server deployment scripts

2. **Build & Test Automation**
   - Running build processes (`npm run build`)
   - Test execution (`npm test`, `pytest`)
   - Linting and formatting (`eslint`, `prettier`)
   - Dependency management (`npm install`, `pip install`)

3. **Data Processing & Scripting**
   - Batch file operations
   - CSV/JSON data transformations
   - Log analysis and parsing
   - PowerShell automation scripts

4. **Multi-Tool Orchestration**
   - Chaining commands across tools
   - Parallel process management
   - Interactive CLI tool navigation
   - Database migrations and seeding

5. **Development Workflow**
   - Hot reload management (`npm run dev`)
   - Database connection testing
   - API endpoint testing
   - Environment variable management

### Delegate to Other Agents
- **Complex Architecture** → Claude Code (architectural decisions, refactoring)
- **Simple Code Gen** → Gemini (boilerplate, utilities, documentation)
- **Deep Debugging** → Claude Code (intricate bugs, integration issues)

---

## Development Principles

1. **Command-Line First**: Leverage PowerShell 7 features (&&, ||, parallel operations)
2. **Automation Over Manual**: Script repetitive tasks, use tool chains
3. **Test-Driven Workflow**: Build → Test → Commit → Deploy cycle
4. **Parallel Execution**: Use async operations when possible
5. **Version Control Discipline**: Commit working checkpoints frequently
6. **Cost Optimization**: Use free tier limits wisely (Supabase, Google Maps API)

---

## Key Commands

### Frontend Development
```powershell
# Start dev server
cd web\tstr-frontend && npm run dev

# Build for production
cd web\tstr-frontend && npm run build

# Preview production build
cd web\tstr-frontend && npm run preview

# Install dependencies
cd web\tstr-frontend && npm install
```

### Backend/Automation
```powershell
# Test Supabase connection
cd web\tstr-automation && python test_supabase.py

# Run PRIMARY scraper (listings + lead generation data)
cd web\tstr-automation && python dual_scraper.py

# Run listings-only scraper (directory population)
cd web\tstr-automation && python scraper.py

# Install Python dependencies
cd web\tstr-automation && pip install -r requirements.txt
```

### Database Operations
```powershell
# Connect to Supabase CLI (if installed)
cd web\tstr-frontend && npx supabase login

# Run migrations
cd web\tstr-frontend && npx supabase db push

# Seed database (manual - execute SQL files)
# Use Supabase dashboard SQL editor
```

### Git Operations
```powershell
# Status check and diff in one command
git --no-pager status && git --no-pager diff

# Stage, commit, and push
git add . && git commit -m "feat: description" && git push

# Create and checkout new branch
git checkout -b feature/new-feature
```

---

## Environment Configuration

### File: `.env.github-copilot`
Personal environment file for GitHub Copilot agent. Contains:
- Supabase credentials
- Google Maps API key
- Agent metadata (ID, session timestamps)

**Security**: Never commit `.env*` files to version control.

### Loading Environment
```powershell
# PowerShell 7
Get-Content .env.github-copilot | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process')
    }
}
```

---

## Current Project Status

### Completed ✅
- Frontend: Astro site scaffolded, Supabase integration configured
- Backend: Python scrapers operational
  - **PRIMARY**: `dual_scraper.py` (listings + lead generation data)
  - **SECONDARY**: `scraper.py` (listings only)
- Database: Supabase schema defined, RLS policies set
- Automation: Dual-mode scraping with cost-effective fallback strategy

### In Progress 🚧
- Frontend UI development (industry-specific listing pages, advanced search)
- Data population (specialized testing labs scraping, CSV imports)
- SEO optimization (geographic hierarchy + industry landing pages)
- Industry research for additional underserved testing sectors

### Planned 📋
- GitHub Actions CI/CD pipeline
- Automated weekly scraping schedule (primary scraper for listings + leads)
- Payment integration (manual → PayPal → Stripe for premium listings)
- Cloudflare Pages deployment
- Lead outreach automation (email/contact captured listings)
- Localized site mirroring strategy (post-profitability)

---

## Testing Strategy

### Frontend Testing
```powershell
# Manual browser testing
npm run dev
# Navigate to http://localhost:4321

# Build verification
npm run build && npm run preview
```

### Backend Testing
```powershell
# Database connection
python test_supabase.py

# PRIMARY scraper dry run (listings + leads)
python dual_scraper.py  # Modify config.json to limit results during testing

# Listings-only scraper test
python scraper.py  # Modify script to limit API calls during testing

# Configuration validation
python -c "import json; print(json.load(open('config.json')))"
```

### Integration Testing
```powershell
# Full workflow test (primary scraper + build)
cd web\tstr-automation && python dual_scraper.py && `
cd ..\tstr-frontend && npm run build
```

---

## Common Workflows

### 1. Feature Development Cycle
```powershell
# Create feature branch
git checkout -b feature/new-listing-form

# Start dev server (async)
cd web\tstr-frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"

# Make changes, test, commit
git add . && git commit -m "feat: add listing submission form"

# Merge to main
git checkout main && git merge feature/new-listing-form
```

### 2. Data Refresh Workflow (Industry-Specific Scraping)
```powershell
# Run PRIMARY scraper (listings + leads for sales)
cd web\tstr-automation
python dual_scraper.py

# Verify scraped data (CSV or JSON)
Get-Content -Path "output.csv" -Head 10

# Check geographic distribution
Import-Csv output.csv | Group-Object location | Select-Object Name, Count

# Check lead data (contact info for outreach)
Import-Csv output.csv | Where-Object { $_.email -or $_.phone } | Measure-Object

# Import to Supabase (manual via dashboard or script)
```

### 3. Deployment Workflow
```powershell
# Build frontend
cd web\tstr-frontend
npm run build

# Deploy to Cloudflare Pages (push to repo triggers auto-deploy)
git add dist && git commit -m "build: production build" && git push origin main
```

---

## PowerShell 7 Optimization Tips

### Parallel Operations
```powershell
# Install dependencies in parallel
$frontendJob = Start-Job { cd web\tstr-frontend; npm install }
$backendJob = Start-Job { cd web\tstr-automation; pip install -r requirements.txt }
Wait-Job $frontendJob, $backendJob
Receive-Job $frontendJob, $backendJob
```

### Command Chaining
```powershell
# Build and test in one line
npm run build && npm run test || Write-Error "Build/test failed"
```

### Interactive Tool Navigation
```powershell
# Use async PowerShell for interactive CLIs
# Example: Supabase CLI login
Start-Process powershell -NoNewWindow -ArgumentList "-Command", "npx supabase login"
```

---

## API Rate Limits & Cost Control

### Google Maps API (Free Tier)
- **Monthly Credit**: $200 (~28,000 Places API requests)
- **Per Request Cost**: ~$0.007
- **Scraper Usage**: ~10-50 API calls per session
- **Rate Limiting**: 0.5s delay between requests (built into scraper)

### Supabase (Free Tier)
- **Database**: 500MB storage
- **Bandwidth**: 2GB/month
- **Rows**: Unlimited
- **Auth**: 50k monthly active users

### Monitoring
```powershell
# Check Google Cloud API usage
# Visit: https://console.cloud.google.com/apis/dashboard

# Check Supabase usage
# Visit: https://app.supabase.com/project/_/settings/billing
```

---

## Troubleshooting

### Build Failures
```powershell
# Clear cache and reinstall
cd web\tstr-frontend
Remove-Item -Recurse -Force node_modules, package-lock.json
npm install
npm run build
```

### Scraper Issues
```powershell
# Verify Python environment
python --version  # Should be 3.11+
pip list | Select-String "requests|beautifulsoup4|supabase"

# Test PRIMARY scraper configuration
python -c "import json; config = json.load(open('config.json')); print('Industries:', len(config.get('searches', [])))"

# Test API key
python -c "import os; print(os.getenv('GOOGLE_MAPS_API_KEY', 'NOT SET'))"
```

### Database Connection
```powershell
# Test Supabase connection
cd web\tstr-automation
python test_supabase.py

# Verify .env file
Get-Content ..\..\tstr-frontend\.env
```

---

## Multi-Agent Collaboration

### Handoff Protocol
1. **Before Starting**: Read `handoff_core.md` for latest project state
2. **During Work**: Log significant decisions and blockers
3. **On Completion**: Update handoff log with timestamped summary
4. **File Attribution**: New files → append agent ID, existing files → log entry only

### Communication Flow
- **No Direct Agent-to-Agent Communication**
- **Human or automation routes instructions between agents**
- **Shared context via `handoff_core.md`**

### When to Hand Off
- **Context/Token Exhaustion**: Update handoff before limits reached
- **Task Completion**: Log completion status and next steps
- **Blockers**: Document issue for human or specialist agent

---

## Security & Best Practices

### Secrets Management
- **Never commit** `.env` files or API keys
- Use `.env.github-copilot` for local development
- Rotate keys if accidentally exposed

### Code Quality
- Follow existing code style (no comments unless necessary)
- Use ecosystem tools (linters, formatters)
- Test incrementally, commit working states

### Git Hygiene
```powershell
# Check for sensitive files before commit
git --no-pager diff --staged | Select-String "API_KEY|SECRET|PASSWORD"

# Add to .gitignore if needed
".env*" | Out-File -Append .gitignore
```

---

## Resource Links

### Documentation
- **Astro Docs**: https://docs.astro.build
- **Supabase Docs**: https://supabase.com/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **PowerShell 7**: https://learn.microsoft.com/powershell

### Project-Specific
- **Architecture**: `web/tstr-automation/ARCHITECTURE.md`
- **Supabase Setup**: `web/tstr-automation/SUPABASE_SETUP.sql`
- **Frontend Guide**: `management/reference/TSTR.SITE FRONTEND BUILD - COMPLETE BEGINNER'S GUIDE`

---

## Next Actions (Prioritized)

1. **Initialize Git Repository** (if not done)
   ```powershell
   git init
   git add .
   git commit -m "chore: initial commit"
   ```

2. **Set Up GitHub Actions CI/CD**
   - Create `.github/workflows/deploy.yml`
   - Configure Cloudflare Pages deployment

3. **Populate Database**
   - Run `dual_scraper.py` for initial data
   - Verify data in Supabase dashboard

4. **Frontend Development**
   - Build listing detail pages
   - Implement search/filter functionality
   - Create submission form

5. **SEO Optimization**
   - Generate location + category landing pages
   - Set up sitemap.xml
   - Configure meta tags

---

## Notes
- **MVP-First Philosophy**: Ship quick, iterate based on feedback
- **High-Margin Focus**: Target underserved specialized testing industries with high buyer intent
- **Cost-Conscious**: Maximize free tier usage before scaling
- **Pareto Principle**: Focus on 20% of features that deliver 80% of value
- **Global-to-Local Strategy**: Build global directory first, localize after profitability
- **Systematic Testing**: One feature at a time with checkpoints

## Revenue Model
- **Free Tier**: Basic directory listings (attract critical mass)
- **Featured Listings**: Premium placement for testing labs ($50-200/month)
- **Lead Generation**: Qualified inquiry forwarding + direct contact leads to testing services
- **Outreach Services**: Sell captured lead data (emails/contacts) from PRIMARY scraper
- **Localized Sites**: Geographic-specific domains (post-profitability expansion)

---

**Last Updated**: 2025-10-14  
**Agent**: GitHub Copilot CLI (albertus@albertusangkuw.com)  
**Status**: Active Development  
**Business Model**: Global B2B niche directory for specialized testing services
