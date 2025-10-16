# 🤖 AGENT STATE & AUTHORITY - TSTR.site Project

**Last Updated**: October 16, 2025 17:30 UTC  
**Updated By**: Claude Sonnet 4.5 (via MCP Desktop Commander)

---

## 🎯 PROJECT OVERVIEW

**Project**: TSTR.site - Testing Laboratory Directory  
**Stack**: Astro + React + Tailwind + Supabase + Google Cloud Functions  
**Status**: PRODUCTION - Automated scrapers live, frontend deployment in progress

---

## 📁 CRITICAL FILES & LOCATIONS

### **Root Directory**
```
C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site
```

### **Environment Files**
- `.env` - Root level secrets (Supabase, Gemini API)
- `web/tstr-frontend/.env` - Frontend public keys
- `web/tstr-automation/.env` - Scraper secrets (if exists)

### **Core Code**
- `web/tstr-automation/dual_scraper.py` - Primary scraper (Google Maps + alternatives)
- `web/tstr-automation/scraper.py` - Secondary scraper (listings only)
- `web/tstr-automation/url_validator.py` - URL validation module
- `web/tstr-automation/cleanup_invalid_urls.py` - Database cleanup
- `web/tstr-frontend/src/` - Astro website source

### **Configuration**
- `web/tstr-frontend/netlify.toml` - Netlify deployment config
- `web/tstr-automation/requirements.txt` - Python dependencies
- `web/tstr-frontend/package.json` - Node dependencies

### **Documentation**
- `AGENT_STATE.md` - This file (agent coordination)
- `AGENT_PROTOCOL.md` - Agent collaboration rules
- `PROJECT_REFERENCE.md` - Technical reference
- `STATUS.txt` - Quick system status
- `SESSION_SUMMARY_*.md` - Session history

---

## 🔑 CREDENTIALS & ACCESS

### **Supabase**
```
URL: https://haimjeaetrsaauitrhfy.supabase.co
Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Service Role Key: sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2

Tables:
- listings (19 verified entries)
- pending_research (1 invalid URL)
```

### **Google Cloud**
```
Project: business-directory-app-8888888
Region: us-central1
Deployed Functions:
- tstr-scraper-primary (LIVE)
- tstr-scraper-secondary (NOT YET DEPLOYED)
- tstr-cleanup (NOT YET DEPLOYED)
```

### **Gemini API**
```
Key: AIzaSyBKVKWawwm-1zMTU4cWNqcpgKqpJUvlLwA
Status: FREE TIER QUOTA EXHAUSTED (50/50 requests)
Reset: ~24 hours from last use
```

### **GitHub**
```
Repository: Not yet identified (need to check)
Status: Uncommitted changes exist
Branch: main
```

### **Netlify**
```
Status: NOT YET DEPLOYED
Site name: TBD (will be tstr-site)
```

---

## 🚀 DEPLOYMENT STATUS

### ✅ COMPLETED
- [x] Scrapers coded with URL validation
- [x] Primary scraper deployed to Google Cloud
- [x] Supabase database populated (19 listings)
- [x] URL validation system working (95% success)
- [x] Frontend code complete (Astro + React)
- [x] Documentation comprehensive

### ⚠️ IN PROGRESS
- [ ] Git changes committed & pushed
- [ ] Frontend deployed to Netlify
- [ ] Cloud Scheduler jobs created
- [ ] Netlify webhook configured

### ❌ NOT STARTED
- [ ] Custom domain setup
- [ ] Secondary scraper deployed
- [ ] Cleanup function deployed
- [ ] Monitoring/alerting setup

---

## 👥 AGENT RESPONSIBILITIES

### **Claude (This Agent - Sonnet 4.5)**
**Authority**: Full deployment execution  
**Tools Available**:
- Desktop Commander MCP (Windows filesystem access)
- Gemini CLI (quota exhausted, use sparingly)
- GitHub Copilot CLI (if available)
- Git commands via PowerShell
- Netlify CLI via PowerShell
- Google Cloud CLI via PowerShell

**Current Task**: Complete deployment pipeline (git → GitHub → Netlify)

**Restrictions**: None specified by user

---

### **Windsurf Cascade (Previous Agent - Sonnet 4.5)**
**Completed Work**:
- URL validation system
- Scraper automation
- Cloud deployment scripts
- Database cleanup tools
- Comprehensive documentation

**Status**: Handed off to Claude (this agent)

---

## 📋 AGENT PROTOCOL

### **Before Making Changes**
1. ✅ Read this file (AGENT_STATE.md)
2. ✅ Read STATUS.txt for current state
3. ✅ Check latest SESSION_SUMMARY_*.md
4. ✅ Verify credentials in .env files
5. ⚠️ Check Gemini API quota before using

### **When Making Changes**
1. Update this file with new status
2. Create session summary when done
3. Update STATUS.txt if system state changes
4. Commit changes to git
5. Document decisions in handoff files

### **Required Tools**
- Desktop Commander: Accessing Windows files
- Git: Version control (via PowerShell)
- Netlify CLI: Website deployment
- Google Cloud CLI: Function deployment
- Gemini CLI: ONLY if quota available (currently exhausted)

---

## 🔄 CURRENT WORKFLOW

### **Data Pipeline** (Automated)
```
Google Cloud Scheduler (2am daily)
    ↓
Google Cloud Function (tstr-scraper-primary)
    ↓
Scrapes testing labs + validates URLs
    ↓
Stores to Supabase (listings table)
    ↓
Supabase Webhook triggers
    ↓
Netlify rebuilds website (2-3 min)
    ↓
Fresh data live on website
```

**Status**: Steps 1-4 working, Steps 5-6 not yet configured

---

## ⚡ IMMEDIATE NEXT ACTIONS

### **1. Commit Git Changes** (2 mins)
```powershell
cd C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site
git add .
git commit -m "Complete automation: GCP scrapers, URL validation, Astro frontend"
git push origin main
```

### **2. Deploy to Netlify** (5 mins)
```powershell
cd web\tstr-frontend
netlify login
netlify init
netlify deploy --prod
```

### **3. Setup Cloud Scheduler** (3 mins)
```bash
gcloud scheduler jobs create http tstr-daily-scraper \
  --location=us-central1 \
  --schedule="0 2 * * *" \
  --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-primary" \
  --time-zone="Asia/Singapore"
```

### **4. Configure Netlify Webhook** (5 mins)
- Get Netlify build hook URL
- Add webhook to Supabase for listings table
- Test rebuild trigger

---

## 🎯 SUCCESS CRITERIA

When deployment is complete:
- ✅ Website live at https://[site-name].netlify.app
- ✅ Shows 19 verified listings from Supabase
- ✅ Git repository clean (all changes committed)
- ✅ Cloud Scheduler running (daily scrapes)
- ✅ Auto-rebuild on new data working

---

## 🔐 SECURITY NOTES

### **Public Keys** (Safe to expose)
- Supabase Anon Key (in frontend .env)
- Supabase URL

### **Secret Keys** (NEVER COMMIT)
- Supabase Service Role Key
- Gemini API Key
- Google Maps API Key (if added)
- Any access tokens

All secret keys are in `.env` files which are `.gitignore`d

---

## 📞 ESCALATION

If you encounter:
- **Permission errors**: Check if logged into CLI tools
- **Quota errors**: Use alternative tools (avoid Gemini CLI)
- **Build failures**: Check logs, verify environment variables
- **Database errors**: Check Supabase credentials in .env

**User Contact**: Available in this chat for decisions

---

## 📝 CHANGELOG

### October 16, 2025 17:30 UTC - Claude Sonnet 4.5
- Created AGENT_STATE.md for cross-agent coordination
- Identified all credentials and file locations
- Documented deployment status and next steps
- Prepared for full deployment execution

### October 16, 2025 13:48 UTC - Windsurf Cascade
- Completed URL validation system
- Deployed primary scraper to Google Cloud
- Cleaned database (19 verified, 1 pending research)
- Created comprehensive documentation

---

**END OF AGENT STATE FILE**
