# 📊 TSTR.SITE - CENTRALIZED PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - All agents update this document
> **Last Updated**: 2025-12-21 13:45 UTC
> **Updated By**: opencode
> **Status**: ✅ PRODUCTION - Live at https://tstr.site
> **Reference**: See `docs/REFERENCE_STATUS.md` for history and details.

---

## 🎯 PROJECT OVERVIEW
**Name**: TSTR.SITE
**Type**: Testers & Testing Services Directory Platform
**Stack**: Astro 5.14.4 + React 18.3.1 + Supabase + Python Scrapers
**Deployment**: OCI (Scrapers) + Cloudflare Pages (Frontend)
**Status**: ✅ LIVE - 191 listings

---

## 📈 CURRENT STATUS DASHBOARD

```
┌─────────────────────────────────────────────┐
│  COMPONENT STATUS                           │
├─────────────────────────────────────────────┤
│  ✅ Database (Supabase)        OPERATIONAL  │
│  ✅ URL Validation             LIVE         │
│  ✅ Click Tracking             DEPLOYED ✨  │
│  ✅ OCI Scrapers               DEPLOYED     │
│  ✅ Local Heavy Scrapers       ACTIVE       │
│  ✅ Frontend (Cloudflare)      LIVE         │
└─────────────────────────────────────────────┘

Listings:         191 verified
Data Quality:     95%+ (URL validation active)
Automation:       100% (cron daily 2 AM GMT)
Cost/Month:       $0.00 (Oracle Always Free Tier)
OCI Uptime:       15 days continuous
Last Scrape:      November 10, 2025 02:31 UTC
```

---

## 🛠️ DEPLOYED INFRASTRUCTURE

### **Dashboard Enhancements**
- **Scraper Monitoring**: https://tstr.site/admin/dashboard (Real-time status)
- **Project Organization**: ✅ CLEAN (Archive cleanup complete)

### **Oracle Cloud Infrastructure (OCI)**
- **Instance**: 84.8.139.90 (Oracle Linux 9, Python 3.9.21)
- **Status**: ✅ OPERATIONAL (Free Tier)
- **Scrapers**: `run_scraper.py` (Daily 2 AM GMT)
- **SSH Access**: ✅ VERIFIED (Key: `/media/al/69AD-FC41/AI_PROJECTS_ARCHIVE/Oracle_Cloud_Machines/avz_Oracle_Linux_9_pvt_ssh-key-2025-10-25.key`)
- **Last Run**: December 20, 2025 02:29 UTC (106 listings, 66 contacts)

### **Database (Supabase)**
- **URL**: https://haimjeaetrsaauitrhfy.supabase.co
- **Tables**: `listings`, `custom_fields`, `pending_research`, `clicks`
- **Status**: ✅ OPERATIONAL

### **Frontend (Cloudflare Pages)**
- **URL**: https://tstr.site
- **Stack**: Astro 5.16.6 + React 18.3.1 + Tailwind CSS
- **Features**: Category filters, Click tracking, Admin dashboard, LinkedIn OAuth
- **Status**: ✅ LIVE (Upgraded to latest secure versions)

---

## 📝 PENDING TASKS

### **High Priority**
- [x] **Claim Button Visibility Enhancement**: Make claim buttons visible to all users on unclaimed listings (Lead Magnet Strategy) ✅ COMPLETED
- [x] **OCI SSH Access Fix**: Located correct SSH key path and verified scraper functionality ✅ COMPLETED
- [x] **Environmental Testing Expansion**: ✅ COMPLETED - Expanded to 200+ listings across 5 subcategories (Air Quality, Water Quality, Soil Testing, Noise/Vibration, ESG/Sustainability). Subcategory pages live, scraper operational with API key resolved.
- [ ] **Oil & Gas Scraper**: Deploy locally (Already local)

### **Medium Priority**
- [ ] Add more geographic regions (Asia, Europe, Middle East)
- [ ] Create admin dashboard for monitoring scraper health
- [ ] Setup error alerting (email/Slack for scraper failures)

### **Authentication & Rights Management** ✅ COMPLETE
- [x] LinkedIn OAuth UI & Database Schema
- [x] Domain Verification Logic & Claim API
- [x] Account Dashboard & Owner Dashboard
- [x] **Subscription Management**: `/account/subscription` created

---

## 🚨 KNOWN ISSUES

### **Current**
1. **Biotech & Oil/Gas Categories**: Not yet deployed (0 listings). Plan: Deploy scrapers.
2. **Invalid URLs**: 17 URLs failed validation. Action: Manual research.
3. **Custom Fields**: Missing specialized data. Fix: Enhance extraction logic.
4. **Submit Page**: ✅ FIXED - Replaced Footer component import with inline HTML. Prerenders successfully now.

### **Security & Database Fixes** ✅ COMPLETE
1. **RLS Policy Fixes**: ✅ Successfully corrected column name issues in Row Level Security policies
2. **Migration Applied**: `20251203000001_fix_rls_policies_column_names.sql` deployed and version-controlled
3. **Hybrid Fix Approach**: ✅ Supabase agent applied immediate fixes + version-controlled migrations completed

---

## 📊 VERSION HISTORY (LATEST)

### **v2.3.12** - December 21, 2025 (CURRENT)
- 🔧 **Bootstrap System Fixes**: Corrected outdated file paths and symlinks
  - Fixed /home/al/AI_PROJECTS_SPACE/ paths to /media/al/AI_DATA/AI_PROJECTS_SPACE/
  - Recreated broken bootstrap.sh and Link_to_bootstrap_agent.sh symlinks
  - Updated documentation to reflect current directory structure
- 🔍 **SEO Optimization**: Enhanced homepage search engine optimization
  - Added dynamic meta description with listing count
  - Implemented Open Graph tags for social sharing
  - Added structured data (JSON-LD) for search engines
  - Included relevant keywords for testing services
- 📋 **Documentation Updates**: Synchronized project status across all docs
  - Updated TSTR.md and START_HERE.md with current live status
  - Fixed GitHub workflow blocking by committing all changes
  - Maintained single source of truth in PROJECT_STATUS.md

### **v2.3.8** - December 16, 2025
- 🔒 **Security Hardening Deployed**: All 12 functions now have secure search_path=pg_catalog, public (verified via SQL query)
- 🛡️ **View Security Fixed**: potential_dead_links view set to security_invoker
- 📊 **Performance Monitoring**: pg_stat_statements extension enabled for query analysis
- ✅ **Vulnerability Resolved**: Eliminated function shadowing attack vector

### **v2.3.7** - December 16, 2025
- 🔒 **Critical Security Fix**: Removed SUPABASE_SERVICE_ROLE_KEY from frontend .env to prevent client-side exposure
- 📊 **Observability Enhancement**: Created migration to enable pg_stat_statements extension for performance monitoring
- 📋 **Manual Deployment**: Created MANUAL_MIGRATION_DEPLOYMENT.md due to CLI sync issues
- ✅ **Security Verification**: Confirmed no schema errors and proper key isolation between frontend/backend

### **v2.3.6** - December 4, 2025
- 📋 **Claim Button Visibility Project Plan**: Comprehensive plan created for making claim buttons visible to all users as lead magnets
- 🎯 **First Principles Strategy**: Adopted "Lead Magnet" approach - claim buttons drive user registrations and verified listings
- 🛠️ **Implementation Roadmap**: 5-phase plan covering browse page buttons, auth routing, login redirects, and testing

### **v2.3.5** - December 3, 2025
- ✅ **System Health Verification Complete** - Phase 1 verification passed (93/100 health score)
- ✅ **Listing Count Updated** - Corrected from 163 to 191 verified listings
- ✅ **Build Process Verified** - Frontend builds successfully with Cloudflare adapter
- ✅ **Site Functionality Confirmed** - All core features operational (browse, search, categories)
- ✅ **Admin Dashboard Active** - Scraper monitoring and analytics accessible
- 🔄 **Supabase API Keys** - Legacy keys disabled; need new publishable/secret keys for build prerendering
- 🔄 **Database Count Verification** - Dashboard shows 0 listings (query bug); site shows 191
- ✅ **Infrastructure Operational** - OCI scrapers active, Cloudflare Pages live

*(See `docs/REFERENCE_STATUS.md` for older versions)*

---

## 💰 COST BREAKDOWN (SUMMARY)
**Total**: $0.00/mo (Oracle Free Tier + Supabase Free + Cloudflare Free)
**Domain**: ~$12/year

---

## 🔗 IMPORTANT LINKS
- **Live Site**: https://tstr.site
- **GitHub**: https://github.com/JAvZZe/tstr-site
- **Supabase**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
- **OCI SSH**: `ssh -i /tmp/oci-key.pem opc@84.8.139.90`
