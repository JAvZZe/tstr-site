# 📊 TSTR.SITE - CENTRALIZED PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** - All agents update this document
> **Last Updated**: 2025-12-03 14:00 UTC
> **Updated By**: JAvZZe
> **Status**: ✅ PRODUCTION - Live at https://tstr.site
> **Reference**: See `docs/REFERENCE_STATUS.md` for history and details.

---

## 🎯 PROJECT OVERVIEW
**Name**: TSTR.SITE
**Type**: Testing Laboratory Directory Platform
**Stack**: Astro 5.14.4 + React 18.3.1 + Supabase + Python Scrapers
**Deployment**: OCI (Scrapers) + Cloudflare Pages (Frontend)
**Status**: ✅ LIVE - 163 listings

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

Listings:         163 verified
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

### **Database (Supabase)**
- **URL**: https://haimjeaetrsaauitrhfy.supabase.co
- **Tables**: `listings`, `custom_fields`, `pending_research`, `clicks`
- **Status**: ✅ OPERATIONAL

### **Frontend (Cloudflare Pages)**
- **URL**: https://tstr.site
- **Features**: Category filters, Click tracking, Admin dashboard, LinkedIn OAuth
- **Status**: ✅ LIVE

---

## 📝 PENDING TASKS

### **High Priority**
- [ ] Expand Environmental Testing (currently 14 listings)
- [ ] **Oil & Gas Scraper**: Complete OCI deployment (Currently Local)

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

---

## 📊 VERSION HISTORY (LATEST)

### **v2.3.3** - December 2, 2025 (CURRENT)
- ✅ **Listing Ownership Features Complete** - All claim functionality fully operational
- ✅ Claim buttons on individual listing pages for authenticated users
- ✅ Domain verification logic for automatic ownership approval
- ✅ "My Listings" section in account dashboard with full management
- ✅ Verified owners can access full contact information (phone/email)
- ✅ Owner badges and status indicators on listing pages
- ✅ Corporate domain verification model (80% automation)
- 🔄 **Cloudflare Pages Deployment Issue** - Account page CSS changes pending deployment
- 🔄 Need to update LinkedIn app redirect URIs
- ✅ Completed: Oil & Gas scraper deployed locally

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
