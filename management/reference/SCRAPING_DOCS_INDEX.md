# Scraping Documentation Index

**Last Updated**: 2025-12-02 20:00 UTC
**Purpose**: Guide to all scraping-related documentation
**Recent Updates**:
- Added deployment strategy section (local vs OCI based on resource requirements)
- Added dashboard monitoring section with script details and source mapping

---

## 📚 Documents Overview

### For AI Agents Building Scrapers

#### **`Agents_Guide_to_Scraper_Best_Practise.txt`** ⭐ PRIMARY
**Location**: Project root  
**Audience**: AI agents (CASCADE, Claude Code, Gemini, etc.)  
**Purpose**: Development principles for creating new scrapers

**Key Topics**:
- ✅ Ethical scraping (robots.txt, GDPR compliance)
- ✅ Anti-blocking measures (throttling, user-agents, stealth)
- ✅ Cost optimization (indirect extraction, token efficiency)
- ✅ Technical strategies (CSS selectors, XPath, headless browsers)
- ✅ LLM collaboration patterns (prompt engineering)
- ✅ Dynamic content handling (internal APIs, JavaScript)

**When to Use**: 
- Building a new scraper from scratch
- Modifying existing scraper logic
- Debugging anti-blocking issues
- Optimizing scraper performance

---

### For Users Running Existing Scrapers

#### **`web/tstr-automation/SCRAPING_EXECUTION_GUIDE.md`**
**Location**: tstr-automation folder  
**Audience**: User (Albert)  
**Purpose**: Step-by-step operational guide

**Key Topics**:
- ✅ How to run `dual_scraper.py`
- ✅ Upload directory listings to site
- ✅ Generate outreach emails
- ✅ Send outreach campaigns
- ✅ Expected results and metrics
- ✅ Troubleshooting common issues
- ✅ Scaling strategy

**When to Use**:
- Running the scraper to get new data
- Uploading listings to the site
- Starting a new outreach campaign
- Checking expected results

---

## 🔄 Document Relationships

```
Agents_Guide_to_Scraper_Best_Practise.txt
    ↓ (Guides development of)
dual_scraper.py, scraper.py
    ↓ (Execution documented in)
SCRAPING_EXECUTION_GUIDE.md
    ↓ (Produces)
tstr_directory_import.csv, tstr_sales_leads.csv
    ↓ (Used for)
Site population & Outreach campaigns
```

---

## 🎯 Quick Decision Tree

**Question: What do you need to do?**

### Build/Modify a Scraper?
→ Read: `Agents_Guide_to_Scraper_Best_Practise.txt`  
→ Agent: CASCADE, Claude Code, or Gemini  
→ Follow: Ethical guidelines, anti-blocking measures  
→ Output: Python scraper code

### Run Existing Scraper?
→ Read: `web/tstr-automation/SCRAPING_EXECUTION_GUIDE.md`  
→ Execute: `python dual_scraper.py`  
→ Follow: Step-by-step instructions  
→ Output: CSV files for import

### Debug Scraper Issues?
→ Check: `Agents_Guide_to_Scraper_Best_Practise.txt` (principles)  
→ Verify: robots.txt compliance, rate limiting, user-agents  
→ Test: With agent help using development principles  
→ Fix: Code in `dual_scraper.py` or `scraper.py`

### Scale Scraping Operations?
→ Read: Both documents  
→ Optimize: Using best practices from guide  
→ Execute: Using execution guide workflow  
→ Monitor: Response rates and data quality

---

## 📂 Scraper Files Reference

### Active Scrapers

**`web/tstr-automation/dual_scraper.py`** - PRIMARY
- Purpose: Scrape directory listings + extract sales leads
- Output: 2 CSV files (listings + contacts)
- Status: ✅ Production-ready
- Deployment: Local execution (heavy processing)

**`web/tstr-automation/scraper.py`** - SECONDARY
- Purpose: Directory listings only (no lead extraction)
- Output: 1 CSV file (listings)
- Status: ✅ Backup option
- Deployment: Local execution (heavy processing)

**OCI Scrapers** (Oracle Cloud Infrastructure)
- Instance: 84.8.139.90 (Oracle Linux 9)
- Status: ✅ ACTIVE (daily 2:00 AM GMT schedule)
- Purpose: Lightweight scraping operations
- Deployment: OCI (when resources allow)
- Note: Heavy-duty scrapers (browser automation) run locally due to OCI RAM limitations

### Support Scripts

**`web/tstr-automation/auto_updater.py`**
- Purpose: Schedule automated scraping runs
- Status: Available but not configured

**`web/tstr-automation/generate_outreach.py`**
- Purpose: Generate personalized outreach emails from leads
- Input: `tstr_sales_leads.csv`
- Output: `outreach_emails_[timestamp].txt`

### Data Files

**`web/tstr-automation/tstr_directory_import.csv`**
- Source: Output from scrapers
- Contains: Company listings for site import
- Current: 134 listings (20 imported to Supabase)

**`web/tstr-automation/tstr_sales_leads.csv`**
- Source: Output from `dual_scraper.py`
- Contains: Decision-maker contacts for outreach
- Fields: Name, email, title, LinkedIn, company

---

## 🚀 Deployment Strategy

### Current State (2025-11-22)
- **Heavy-duty scrapers** (Playwright, Selenium, browser automation): Run locally on development machines
- **Lightweight scrapers** (simple HTTP requests, HTML parsing): Deployed to OCI when resources allow
- **Local Automation**: Ready with 40GB RAM available for automated execution
- **Reason**: OCI has low RAM allocation, insufficient for browser automation tools
- **Future**: Migrate lightweight scrapers to OCI cron jobs when Oracle upgrades free tier resources

### Resource Requirements
- **Local advantages**: Unlimited RAM, full control, browser automation capability
- **OCI limitations**: Resource-constrained, cannot handle memory-intensive operations
- **Decision criteria**: Use local for any scraper requiring >1GB RAM or JavaScript rendering

---

## 📊 Monitoring & Dashboard

### **Scraper Dashboard** ⭐ NEW
**Location**: https://tstr.directory/admin/dashboard
**Purpose**: Real-time monitoring of all scraper operations

**Features**:
- ✅ Live scraper status (OCI and Local)
- ✅ Script details and file locations
- ✅ Source mapping (which script handles each category)
- ✅ Performance metrics by category
- ✅ Recent activity and system health
- ✅ Failed URL validation alerts

**When to Use**:
- Monitor scraper health and performance
- Identify which script handles specific categories
- Troubleshoot scraper issues
- View automation status and schedules

---

## 🛡️ Compliance & Best Practices

### Always Follow (from Best Practice Guide)

1. **Check robots.txt** before scraping any domain
2. **Implement rate limiting** (random delays between requests)
3. **Rotate user-agents** (mimic different browsers)
4. **Respect GDPR** (no PII of EU citizens)
5. **Avoid honeypots** (don't interact with hidden elements)
6. **Use indirect extraction** (reusable functions over API calls)
7. **Handle errors gracefully** (retry logic, fallbacks)

### Never Do

1. ❌ Ignore robots.txt disallow rules
2. ❌ Send requests at uniform intervals
3. ❌ Use outdated or suspicious user-agents
4. ❌ Scrape behind authentication without permission
5. ❌ Store or republish copyrighted content
6. ❌ Overload servers (DoS-like behavior)
7. ❌ Scrape personal data without consent

---

## 📊 Metrics & Success Criteria

### Data Quality Expectations
- **Directory listings**: 50-100 companies per scrape run
- **Contact success rate**: 20-40% of companies yield contacts
- **High-confidence leads**: 10-20 per 100 listings
- **Email accuracy**: 80-90% valid emails

### Performance Benchmarks
- **Speed**: 2-5 seconds per company
- **Success rate**: 70-80% successful scrapes
- **Bounce rate**: 10-20% expected for emails
- **Response rate**: 5-10% for B2B outreach

### Business Impact
- **Week 1**: 50 emails → 2-3 customers @ £50/month
- **Month 1**: 200 emails → 10-15 customers @ £500-750 MRR
- **Month 3**: Scale to £3,000-5,000/month combined revenue

---

## 🔧 For AI Agents: Integration Guidelines

### When Building New Scrapers

**Read First**:
1. `Agents_Guide_to_Scraper_Best_Practise.txt` (ALL sections)
2. Existing scrapers (`dual_scraper.py`) for patterns
3. `requirements.txt` for approved libraries

**Follow**:
1. Output structured data (JSON/CSV with Pydantic schema)
2. Use Python (Requests, BeautifulSoup, Selenium/Playwright)
3. Implement all stealth measures (delays, user-agents, etc.)
4. Check robots.txt programmatically
5. Include error handling and retry logic

**Avoid**:
1. Making continuous LLM API calls for parsing (use indirect extraction)
2. Aggressive scraping patterns
3. Hardcoded delays (use randomization)
4. Storing raw HTML (extract and discard)

---

## 📖 Version Control

**Best Practice Guide**: 
- Created: User-provided (pre-CASCADE session)
- Location: Root (will move to management/reference)
- Status: ✅ Active reference

**Execution Guide**:
- Created: Previous session (Gemini)
- Location: tstr-automation folder
- Status: ✅ Active operational doc

**This Index**:
- Created: 2025-10-15 by CASCADE
- Location: management/reference/
- Purpose: Connect the two documents

---

## 🎯 Quick Links

| Need | Document | Location |
|------|----------|----------|
| Build scraper | Best Practice Guide | Root folder |
| Run scraper | Execution Guide | tstr-automation/ |
| Check compliance | Best Practice Guide → Part 2 | Root folder |
| Generate emails | Execution Guide → Step 3 | tstr-automation/ |
| Debug issues | Both documents | Multiple |
| Scale operations | Execution Guide → Scaling | tstr-automation/ |

---

**Both documents are essential and complementary. Keep them both active.**
