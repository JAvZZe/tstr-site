# TSTR.DIRECTORY Automation Setup Guide

## Quick Start (5 minutes)

### 1. Install Python Dependencies
```bash
cd C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation
pip install -r requirements.txt
```

### 2. Run the Scraper
```bash
python scraper.py
```

This will generate: `tstr_labs_bulk_import.csv`

### 3. Upload to WordPress
1. Go to: http://34.100.223.247/wp-admin
2. Login: `user` / `TstrAdmin2025Secure`
3. Navigate to: **Directorist > Import/Export**
4. Upload the CSV file
5. Map fields if prompted
6. Click Import

---

## Google Maps API Usage

Your API Key: `AIzaSyAJfCW_X3fJerYy6fXwUR7T11QkKTLFUzM`

**Free Tier Limits:**
- $200 credit per month
- ~28,000 Places API requests free
- Each scraping session uses ~10-50 API calls

**Cost Control:**
- Script includes rate limiting (0.5s between requests)
- Runs ~8 searches = ~16 API calls per execution
- Well within free limits

---

## Expanding Your Data Collection

### Option A: More Google Maps Searches
Edit `scraper.py` line 140, add more locations:
```python
searches = [
    ('Oil & Gas Testing', 'Dubai UAE'),
    ('Pharmaceutical Testing', 'Mumbai India'),
    ('Biotech Testing', 'Shanghai China'),
    # Add 50+ more...
]
```

### Option B: Industry Directory Scraping
The script has templates for scraping specific industry directories.
Add URLs in the `scrape_industry_directories()` function.

**Target Directories:**
- Energy-pedia.com (Oil & Gas)
- Pharmaceutical-technology.com (Pharma)
- Biocompare.com (Biotech)
- ISO 17025 accredited lab directories

### Option C: Manual CSV Creation
Create CSV with these columns:
```
listing_title, listing_content, listing_category, listing_location, 
address, phone, email, website, listing_img, latitude, longitude
```

---

## Automated Scheduled Scraping

### Windows Task Scheduler Setup:
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Weekly (every Sunday 2am)
4. Action: Start Program
   - Program: `python`
   - Arguments: `C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation\scraper.py`
5. Save

This keeps your directory automatically updated weekly.

---

## SEO Landing Page Generation

Once you have 100+ listings, create location + category pages:
- "Oil & Gas Testing Houston"
- "Pharma Testing New Jersey"
- "Biotech Labs Singapore"

WordPress will auto-generate these from your listings.

---

## Monetisation Setup (Bank Transfer)

### Configure Payment Page:
1. Go to: **Directorist > Settings > Monetization**
2. Enable Monetization: Yes
3. Active Gateways: Check "Bank Transfer"
4. Bank Details:
   ```
   Bank: [Your Bank Name]
   Account Name: TSTR Site Ltd
   Account Number: [Your Account]
   Sort Code: [Your Sort Code]
   Reference: Invoice Number
   ```

### Create Pricing Plans:
1. **Basic Listing**: Free (to attract listings)
2. **Featured Listing**: £50/month (homepage visibility)
3. **Premium Package**: £200/month (top ranking + badge + priority support)

### Lead Capture Forms:
Already installed: Contact Form 7

Create forms for:
- "Request Quote" (captures: name, email, service needed, budget, timeline)
- "Claim Listing" (allows businesses to claim their profile)

---

## Next Steps Checklist

- [ ] Run scraper to get first 50-100 listings
- [ ] Upload CSV to WordPress
- [ ] Check listings display correctly
- [ ] Create 3 pricing plans
- [ ] Set up bank transfer details
- [ ] Test submission process
- [ ] Create lead capture form
- [ ] Add to Google Search Console
- [ ] Submit sitemap
- [ ] Start outreach to labs for paid upgrades

---

## Support & Troubleshooting

**Scraper not working?**
- Check internet connection
- Verify API key is active
- Check Google Cloud console for API errors

**CSV import failing?**
- Check field mapping in Directorist
- Ensure CSV is UTF-8 encoded
- Remove any special characters from company names

**Can't login to WordPress?**
- URL: http://34.100.223.247/wp-admin
- Username: `user`
- Password: `TstrAdmin2025Secure`

---

## Performance Notes

Current setup (all free tier):
- ✅ VM: e2-micro (free)
- ✅ Static IP: Free while attached
- ✅ 30GB storage: Free
- ✅ Google Maps API: $200/month credit
- ✅ All plugins: Free versions

**Estimated capacity:** 10,000+ listings before needing upgrades.
