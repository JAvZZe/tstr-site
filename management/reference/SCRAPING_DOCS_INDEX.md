# Scraping Documentation Index

**Last Updated**: 2025-10-15 18:23 UTC  
**Purpose**: Guide to all scraping-related documentation

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

**`web/tstr-automation/scraper.py`** - SECONDARY
- Purpose: Directory listings only (no lead extraction)
- Output: 1 CSV file (listings)
- Status: ✅ Backup option

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
