# 🚀 TSTR.SITE - QUICK START GUIDE

**Status**: 🟢 LIVE | **Updated**: Oct 16, 2025

---

## ⚡ QUICK COMMANDS

### Run Scrapers (Production)
```bash
cd "C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site\web\tstr-automation"

# Primary scraper (directory + leads)
python dual_scraper.py

# Secondary scraper (listings only)
python scraper.py
```

**✅ URL validation happens automatically**

### Check Database Health
```bash
# Review & clean invalid URLs
python cleanup_invalid_urls.py 3  # Report only
python cleanup_invalid_urls.py 2  # Move to research
```

---

## 📊 CURRENT STATUS

### Production Database
```
✅ Listings:        19 (all verified URLs)
📋 Pending Research: 1 (needs URL fix)
✅ Success Rate:    94.7%
🟢 Status:          OPERATIONAL
```

### Features Live
- ✅ Automatic URL validation
- ✅ Invalid URL handling
- ✅ Duplicate detection
- ✅ Smart error reporting
- ✅ CSV exports (verified only)

---

## 📁 KEY FILES

### Production Code
```
web/tstr-automation/
├── dual_scraper.py          (Primary - directory + leads)
├── scraper.py               (Secondary - listings only)
├── url_validator.py         (Validation engine)
├── cleanup_invalid_urls.py  (Database cleanup)
└── .env                     (Credentials - DO NOT COMMIT)
```

### Configuration
```
├── config.json              (Scraper targets)
└── .env                     (API keys & DB credentials)
```

### Generated Reports
```
├── tstr_directory_import.csv     (✅ verified listings)
├── tstr_sales_leads.csv          (from dual_scraper)
├── invalid_urls_report.csv       (⚠️ needs review)
```

---

## 🎯 COMMON TASKS

### 1. Add New Listings
```bash
# Edit config.json to add new search terms
python dual_scraper.py

# Output: tstr_directory_import.csv (auto-validated)
```

### 2. Check for Invalid URLs
```bash
python cleanup_invalid_urls.py 3

# Review: invalid_listings_[timestamp].csv
```

### 3. Data Sync to Supabase
```
Option A: Direct Insert (Automated)
- Scrapers write directly to Supabase
- No CSV upload needed
- Updates appear immediately on Astro site

Option B: Manual CSV Upload (if needed)
- Use Supabase dashboard SQL editor
- Import CSV to listings table
```

### 4. Review Research Queue
```sql
-- In Supabase SQL Editor
SELECT business_name, website, validation_error 
FROM pending_research 
WHERE status = 'pending_research';
```

---

## 🔧 TROUBLESHOOTING

### Scraper Won't Run
```bash
# Check Python
python --version  # Should be 3.8+

# Install dependencies
pip install requests beautifulsoup4 python-dotenv supabase

# Check .env file exists
ls .env
```

### URLs Failing Validation
```bash
# Test connectivity
python -c "from url_validator import validate_url_simple; print(validate_url_simple('https://google.com'))"

# Should output: True
```

### Database Connection Failed
```bash
# Check .env credentials
cat .env | grep SUPABASE

# Should see:
# SUPABASE_URL=https://...
# SUPABASE_KEY=...
```

---

## 📚 DOCUMENTATION

### Full Documentation
- `URL_VALIDATION_LIVE.md` - Production status & features
- `URL_VALIDATION_INTEGRATION.md` - Technical integration details
- `handoff_core.md` - Complete project history

### Quick Reference
- Scrapers validate URLs automatically ✅
- Invalid URLs go to `pending_research` table 📋
- Only verified URLs exported to CSV 🎯
- Check reports folder for details 📊

---

## 🎓 FOR NEW TEAM MEMBERS

### First Time Setup
1. Clone/download project
2. Install Python 3.8+
3. Install dependencies: `pip install -r requirements.txt`
4. Get `.env` file from secure location
5. Test: `python -c "from url_validator import validate_url_simple; print('OK')"`

### Daily Workflow
1. Run scraper: `python dual_scraper.py`
2. Review output CSV
3. Import to WordPress
4. Done! (validation automatic)

---

## 🆘 SUPPORT

### Self-Help
1. Check `URL_VALIDATION_LIVE.md` (troubleshooting section)
2. Review error messages in terminal
3. Check `invalid_urls_report.csv` for details

### Common Issues
- **High invalid rate**: Check network connection
- **Slow validation**: Normal for first run (no cache)
- **Import fails**: Check CSV format in WordPress

---

## ✅ SUCCESS CHECKLIST

Before going live with new data:
- [ ] Run scraper successfully
- [ ] Check `tstr_directory_import.csv` exists
- [ ] Review `invalid_urls_report.csv`
- [ ] Verify success rate >85%
- [ ] Test import in WordPress staging
- [ ] Deploy to production

---

## 🎉 QUICK WINS

### What Just Works™
✅ URL validation (automatic)  
✅ Duplicate detection (automatic)  
✅ Error handling (automatic)  
✅ CSV generation (automatic)  
✅ Invalid URL preservation (automatic)

### What You Control
- Scraper targets (config.json)
- When to run scrapers
- Import timing
- Research queue priority

---

**🟢 SYSTEM STATUS: OPERATIONAL**  
**Last Check**: Oct 16, 2025  
**Next Action**: Run scrapers as needed
