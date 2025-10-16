# TSTR.site - Global Testing Laboratory Directory

**Status**: 🟡 Site Live, API Configuration Needed  
**URL**: https://tstr.site  
**Repository**: https://github.com/JAvZZe/tstr-site.git  
**Last Updated**: 2025-10-15 17:00 UTC

---

## 🎯 Quick Start for New Agents

### 1. Read This First
- **`handoff_core.md`** - Current system state, blockers, next actions
- **`CASCADE.md`** - CASCADE agent capabilities (if you're CASCADE)
- **`GEMINI.md`** - Gemini agent capabilities (if you're Gemini)

### 2. Current Priority
**P0**: Fix site API error by updating Cloudflare environment variables with new Supabase keys

### 3. Project Structure
```
web/
├── tstr-frontend/     # Astro site (deployed to Cloudflare)
└── tstr-automation/   # Python scrapers & automation
```

---

## 📚 Documentation Index

### Agent Coordination
- **`handoff_core.md`** - ⭐ PRIMARY handoff document
  - Current system state
  - Active blockers
  - Priority actions
  - Agent roster and handoff protocols
  - Session logs

### Agent Profiles
- **`CASCADE.md`** - CASCADE (Windsurf) capabilities
- **`GEMINI.md`** - Gemini CLI capabilities
- **`TOOLS_REFERENCE.md`** - All tools, plugins, and integrations

### Agent Identity & Coordination
- **`management/agents/AGENT_IDENTIFICATION_GUIDE.md`** - ⭐ How agents identify themselves
- **`.env.cascade`** - CASCADE agent config and session tracking
- **`management/agents/CASCADE_IDENTITY.md`** - Current CASCADE session details
- **`management/agents/AGENT_TEMPLATE.md`** - Template for new agents

### Technical Documentation
- **`DEPLOYMENT_VERIFICATION.md`** - Deployment status (Oct 14)
- **`FINAL_STEP_ADD_CUSTOM_DOMAIN.md`** - DNS configuration
- **`FAST_TRACK_DEPLOYMENT.md`** - Quick deployment reference

### Database
- **`web/tstr-automation/SUPABASE_*.sql`** - Database schema
- **`web/tstr-automation/ARCHITECTURE.md`** - Database design

### Scraping & Automation
- **`Agents_Guide_to_Scraper_Best_Practise.txt`** - ⭐ AI agent development principles
- **`web/tstr-automation/SCRAPING_EXECUTION_GUIDE.md`** - Operational guide for running scrapers
- **`web/tstr-automation/dual_scraper.py`** - Main scraper (listings + leads)

---

## 🚀 Tech Stack

**Frontend**:
- Astro 5.14.4
- React 18.3.1
- Tailwind CSS 3.4.1
- Deployed on Cloudflare Pages

**Backend**:
- Python 3.14
- Supabase (PostgreSQL)
- Python automation scripts

**Hosting & Services**:
- GitHub (version control, CI/CD trigger)
- Cloudflare Pages (hosting, CDN, SSL)
- Supabase (database, auth, API)

---

## ✅ What's Working

1. **Site Live**: https://tstr.site (DNS, SSL, CDN)
2. **GitHub**: Push/pull working, auto-deploy configured
3. **Database**: Schema created, 20 listings imported
4. **Python**: All dependencies installed
5. **API Keys**: New working keys retrieved from Supabase

---

## ⚠️ Current Blockers

### P0 - CRITICAL
**Frontend API Error**: "Invalid API key" on live site
- **Cause**: Cloudflare using old/missing Supabase keys
- **Solution**: Update Cloudflare environment variables
- **Keys Ready**: 
  - `PUBLIC_SUPABASE_URL`: https://haimjeaetrsaauitrhfy.supabase.co
  - `PUBLIC_SUPABASE_ANON_KEY`: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO
- **Action Required**: User must update via Cloudflare dashboard

### P1 - HIGH
**Incomplete Data**: 114 of 134 listings not imported
- **Cause**: Location name mismatch (CSV has "New Jersey", DB has city-level)
- **Decision Needed**: MVP with 20 listings or fix locations?

---

## 🎯 Next Actions

### Immediate (User)
1. Open Cloudflare dashboard: https://dash.cloudflare.com/.../tstr-site/settings/environment-variables
2. Add/update environment variables (see handoff_core.md for values)
3. Redeploy Cloudflare Pages
4. Verify site loads without errors

### Then (Agent)
1. Test site functionality with 20 listings
2. Verify categories and search work
3. Decide on remaining data import strategy
4. Plan MVP launch

---

## 🔐 Credentials

**Locations**:
- Root `.env`: Gemini API key, Supabase service role key
- `web/tstr-frontend/.env`: Supabase frontend keys (GITIGNORED)
- All credentials documented in `handoff_core.md`

**Never commit .env files to git**

---

## 🛠️ Common Commands

### Frontend Development
```powershell
cd web\tstr-frontend
npm run dev          # Start dev server (http://localhost:4321)
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Operations
```powershell
cd web\tstr-automation
python import_to_supabase.py    # Import listings
python test_supabase.py         # Test DB connection
python dual_scraper.py          # Scrape new listings
```

### Git Workflow
```powershell
git status                      # Check status
git add .                       # Stage all changes
git commit -m "description"     # Commit
git push origin main            # Push (triggers auto-deploy)
```

---

## 📞 Support & Contact

**Project Owner**: Albert (non-technical, AuDHD)
- Prefers direct, factual communication
- Lean MVP approach, quick iteration
- Systematic testing with checkpoints

**Agent Coordination**: See `handoff_core.md`

---

## 📁 Folder Structure

```
TSTR.site/
├── web/
│   ├── tstr-frontend/          # Astro frontend
│   │   ├── src/                # Source code
│   │   │   ├── pages/          # Routes
│   │   │   ├── components/     # React components
│   │   │   └── layouts/        # Page layouts
│   │   ├── public/             # Static assets
│   │   ├── dist/               # Built files (deployed)
│   │   └── .env                # Frontend config (GITIGNORED)
│   └── tstr-automation/        # Python backend
│       ├── dual_scraper.py     # PRIMARY scraper (listings + leads)
│       ├── scraper.py          # Listings only scraper
│       ├── import_to_supabase.py  # Data import
│       ├── test_supabase.py    # DB connection test
│       ├── tstr_directory_import.csv  # 134 listings ready
│       ├── SUPABASE_*.sql      # Database schema (7 files)
│       └── requirements.txt    # Python dependencies
├── management/                 # Project management
│   ├── agents/                 # Agent-specific configs
│   ├── tasks/                  # Task tracking
│   ├── project_docs/           # Project documentation
│   └── reference/              # Reference materials
├── archive/                    # Old/deprecated files
├── handoff_core.md            # ⭐ PRIMARY HANDOFF DOCUMENT
├── CASCADE.md                 # CASCADE agent profile
├── GEMINI.md                  # Gemini agent profile
├── TOOLS_REFERENCE.md         # Tools & plugins reference
├── README.md                  # This file
├── DEPLOYMENT_VERIFICATION.md # Deployment status
├── .env                       # Root environment variables
└── package.json               # Wrangler dependency
```

---

## 🔄 Version

- **Project**: v0.1 (MVP phase)
- **Documentation**: v2.0 (Comprehensive agent coordination)
- **Last Session**: 2025-10-15 15:00-17:00 UTC
- **Active Agent**: CASCADE (Windsurf)
- **Session Status**: Pending user action (Cloudflare env vars)

---

## 📖 Quick Reference

| Document | Purpose | Read When |
|----------|---------|-----------|
| `handoff_core.md` | System state & coordination | Every session start |
| `CASCADE.md` | Agent capabilities | First time as CASCADE |
| `TOOLS_REFERENCE.md` | Tools & plugins | Need to use a tool |
| `DEPLOYMENT_VERIFICATION.md` | Deployment details | Deployment issues |
| `GEMINI.md` | Gemini capabilities | Handing off to Gemini |

---

**For current status, always start with `handoff_core.md`**
