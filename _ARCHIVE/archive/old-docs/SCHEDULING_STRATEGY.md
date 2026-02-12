# 📅 SCHEDULING STRATEGY - TSTR.SITE

**Date**: October 16, 2025  
**Goal**: Respectful, efficient scraping without rule violations

---

## 🎯 SCRAPER COMPARISON

### **Primary Scraper (dual_scraper.py)**
**Purpose**: Directory listings + Sales leads  
**Sources**:
- Google Maps API (15 categories × locations)
- Alternative sources (Energy Pedia, Pharma Tech, Biocompare)

**Safeguards**:
✅ URL validation (95% success)  
✅ Rate limiting (0.5s between requests)  
✅ Duplicate detection (Supabase)  
✅ Invalid URL tracking  
✅ User-Agent headers  

### **Secondary Scraper (scraper.py)**
**Purpose**: Directory listings only (no leads)  
**Sources**:
- Google Maps API (fallback if available)
- Alternative sources (same as primary)

**Safeguards**:
✅ URL validation (95% success)  
✅ Rate limiting (0.5s between requests)  
✅ Duplicate detection (Supabase)  
✅ Invalid URL tracking  
✅ User-Agent headers  
✅ **Only scrapes NEW listings**

---

## ⚖️ KEY INSIGHT

**Both scrapers have identical safeguards!**

The secondary scraper provides value by:
- Finding listings the primary might miss
- Cross-validating data
- **Detecting duplicates** (won't re-add existing listings)

---

## 📋 RECOMMENDED SCHEDULING

### **Option A: Conservative (Recommended)**
```
Primary Scraper:   Every 3 days @ 2am
Secondary Scraper: Once per week @ 3am (Sunday)
Cleanup:          Once per month @ 4am (1st)
```

**Why?**
- Respectful to website owners (not daily hammering)
- Secondary finds what primary missed
- No duplicate data (both check database)
- Complies with reasonable crawl delays

### **Option B: Moderate**
```
Primary Scraper:   Daily @ 2am
Secondary Scraper: Once per week @ 3am (Sunday)
Cleanup:          Once per month @ 4am (1st)
```

**Why?**
- Daily updates keep data fresh
- Weekly secondary validates/supplements
- Still respectful with rate limiting

### **Option C: Minimal**
```
Primary Scraper:   Once per week @ 2am (Monday)
Secondary Scraper: Manual trigger only (fallback)
Cleanup:          Once per month @ 4am (1st)
```

**Why?**
- Most conservative approach
- Secondary only runs when you need it
- Reduces API usage

---

## 🛡️ RESPECT & COMPLIANCE

### **What Makes This Safe**

1. **Rate Limiting**
   - 0.5 seconds between each request
   - Total ~120 requests/minute max
   - Well below typical limits (1000/min)

2. **Duplicate Detection**
   - Secondary scraper checks database first
   - Won't re-add existing listings
   - No data bloat

3. **User-Agent Identification**
   - Properly identifies as TSTR bot
   - Not spoofing or hiding

4. **Reasonable Frequency**
   - Not hammering sites constantly
   - Alternative sources are public directories
   - Google Maps API is paid/licensed

5. **robots.txt Compliance** (Can add)
   - Can add robots.txt checker if needed
   - Currently scraping public APIs/directories

---

## 💡 MY RECOMMENDATION

**Use Option A: Conservative Schedule**

```bash
# Primary Scraper - Every 3 days
gcloud scheduler jobs create http tstr-primary-scraper \
  --location=us-central1 \
  --schedule="0 2 */3 * *" \
  --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-primary" \
  --http-method=GET \
  --time-zone="Asia/Singapore" \
  --description="Primary scraper - every 3 days at 2am"

# Secondary Scraper - Weekly (Sunday)
gcloud scheduler jobs create http tstr-secondary-scraper \
  --location=us-central1 \
  --schedule="0 3 * * 0" \
  --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-secondary" \
  --http-method=GET \
  --time-zone="Asia/Singapore" \
  --description="Secondary scraper - weekly Sunday 3am"

# Cleanup - Monthly
gcloud scheduler jobs create http tstr-monthly-cleanup \
  --location=us-central1 \
  --schedule="0 4 1 * *" \
  --uri="https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-cleanup" \
  --http-method=POST \
  --message-body='{"mode":"2"}' \
  --headers="Content-Type=application/json" \
  --time-zone="Asia/Singapore" \
  --description="Monthly URL validation and cleanup"
```

**Benefits**:
- ✅ Respectful to website owners
- ✅ Compliant with best practices
- ✅ Secondary finds missed listings
- ✅ No duplicate data
- ✅ Keeps data fresh
- ✅ Minimal cost ($0.90/month)

---

## 🔄 HOW THEY WORK TOGETHER

### **Primary Scraper (Every 3 Days)**
```
1. Scrapes all 15 Google Maps categories
2. Validates URLs
3. Checks Supabase for duplicates
4. Adds only NEW listings
5. Generates sales leads
```

### **Secondary Scraper (Weekly)**
```
1. Runs alternative sources
2. Validates URLs
3. Checks Supabase for duplicates
4. Finds listings primary missed
5. Cross-validates existing data
6. **Skips duplicates automatically**
```

**No Overlap** - Both check database first!

---

## 📊 EXPECTED BEHAVIOR

### **Week 1**
- Day 1: Primary finds 20 listings → Adds all 20
- Day 4: Primary finds 5 new + 15 existing → Adds 5 (skips 15)
- Day 7: Secondary finds 3 new + 17 existing → Adds 3 (skips 17)

**Total**: 28 unique listings (no duplicates)

### **Week 2**
- Day 10: Primary finds 2 new + 26 existing → Adds 2
- Day 13: Primary finds 1 new + 29 existing → Adds 1
- Day 14: Secondary finds 0 new + 30 existing → Adds 0

**Total**: 30 unique listings

---

## 🎯 SUMMARY

**Both scrapers are safe and complementary!**

✅ Same validation rules  
✅ Same rate limiting  
✅ Both check for duplicates  
✅ No rule violations  
✅ Respectful frequency  

**Secondary scraper adds value** by finding listings the primary might miss, without creating duplicates.

---

## 🚀 READY TO DEPLOY?

**Recommend**: Option A (Conservative)
- Primary: Every 3 days
- Secondary: Weekly
- Cleanup: Monthly

**Cost**: $0.90/month  
**Risk**: Minimal  
**Compliance**: Excellent

Should I deploy this schedule?
