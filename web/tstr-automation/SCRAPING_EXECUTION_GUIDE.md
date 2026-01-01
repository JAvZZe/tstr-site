# 🚀 DUAL-PURPOSE SCRAPING EXECUTION GUIDE

## What You're About to Do

**Two outputs from one scraping session:**
1. **Directory Listings** → Populate your website (100+ companies)
2. **Sales Leads** → Decision-makers to contact (20-50 qualified leads)

---

## Step 1: Run the Dual Scraper (10 minutes)

```bash
cd C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation
python dual_scraper.py
```

### What It Does:
1. Scrapes Google Maps for testing labs (company data)
2. Visits each company website
3. Extracts decision-maker contacts (names, emails, LinkedIn)
4. Generates TWO CSV files

### Expected Output:
```
Directory Listings: 50-100 companies
Sales Leads Found: 20-50 contacts
Files created:
  1. tstr_directory_import.csv
  2. tstr_sales_leads.csv
```

**Time:** ~10 minutes (API calls + website scraping)

---

## Step 2: Upload Directory Listings (5 minutes)

1. Go to: https://tstr.directory/wp-admin
2. Login: `user` / `TstrAdmin2025Secure`
3. Navigate: **Directorist > Import/Export**
4. Upload: `tstr_directory_import.csv`
5. Map fields (should auto-detect)
6. Click **Import**

**Result:** 50-100 testing labs now live on your site!

---

## Step 3: Generate Personalized Outreach Emails (2 minutes)

```bash
python generate_outreach.py
```

### What It Does:
- Reads `tstr_sales_leads.csv`
- Filters for contacts with emails
- Generates personalized email templates
- Prioritizes high-confidence leads

### Output File:
`outreach_emails_[timestamp].txt`

Contains:
- **HIGH PRIORITY:** Contacts with name + email (send first)
- **MEDIUM PRIORITY:** Contacts with email only (follow-up)
- Pre-written emails ready to copy-paste
- LinkedIn messages included

---

## Step 4: Start Outreach (30 minutes/day)

### Day 1: Send 10 Emails
1. Open: `outreach_emails_[timestamp].txt`
2. Copy first 10 HIGH PRIORITY emails
3. Paste into Gmail (one at a time)
4. Personalize first line if possible
5. Send

### Track Responses:
Update `tstr_sales_leads.csv`:
- **outreach_status**: "Email Sent" → "Responded" → "Interested" → "Converted"
- **notes**: Add any feedback or follow-up needed

### Day 2-7: Send 10 More Daily
- Maintain consistent daily outreach
- Follow up after 3 days if no response
- Connect on LinkedIn simultaneously

**Target:** 10 emails/day = 70/week = 7-14 interested prospects

---

## Understanding the Data Quality

### Sales Leads Confidence Levels:

**HIGH Confidence:**
- Has contact name AND email
- Title/role identified
- Often has LinkedIn profile
- **Action:** Send immediately, highest priority

**MEDIUM Confidence:**
- Has email but generic contact
- Or has name but no email
- **Action:** Send but expect lower response rate

**What We DON'T Capture:**
- Generic emails (info@, contact@, support@)
- Non-decision makers
- Incomplete data

---

## Expected Results

### From 100 Directory Listings:
- **40-60** will have scrapeable websites
- **20-40** will yield some contact info
- **10-20** will be high-confidence leads

### From 50 Emails Sent:
- **10-15** will open (20-30% open rate)
- **3-5** will respond (5-10% response rate)
- **1-2** will convert to paying customers (2-4% conversion)

**Math:** 50 emails → 2 customers @ £50/month = **£100 MRR**

---

## Pro Tips for Higher Response Rates

### Email Best Practices:
1. **Send between 9am-11am** (highest open rates)
2. **Tuesday-Thursday** (best days)
3. **Personalize first line** (mention their specific service)
4. **Keep it short** (under 100 words)
5. **One clear CTA** (reply YES)

### LinkedIn Strategy:
1. Connect with decision-makers
2. Wait 2-3 days after email
3. Send personalized message referencing email
4. **Don't pitch immediately** - build relationship first

### Follow-Up Sequence:
- **Day 0:** Initial email
- **Day 3:** Gentle follow-up ("Just checking if you saw this")
- **Day 7:** Final follow-up with urgency ("Last 5 spots available")
- **Day 10:** LinkedIn connection

---

## Troubleshooting

**Q: Scraper is slow?**
A: Normal! Each company takes 2-5 seconds. 50 companies = 5-10 minutes.

**Q: Not finding many contacts?**
A: Some industries have better website contact info than others. 20-40% success rate is normal.

**Q: Emails bouncing?**
A: Scrapped emails aren't always current. 10-20% bounce rate is expected.

**Q: Low response rate?**
A: B2B average is 5-10%. You're doing well if you hit that.

**Q: Want more leads?**
A: Run scraper again with different locations or categories.

---

## Scaling Strategy

### Week 1: Test & Learn
- Run scraper once
- Send 50 emails
- Track response rate
- Refine messaging

### Week 2-3: Scale Up
- Run scraper 2x/week (different regions)
- Send 100 emails/week
- A/B test subject lines
- Target: 5-10 interested prospects

### Month 2: Automate
- Schedule weekly scraping
- Build email sequences
- Use CRM for tracking
- Target: 20-30 new customers

---

## Integration with Revenue Strategy

### Immediate Revenue (Week 1-2):
**Source:** Email outreach to scraped contacts
**Target:** 2-3 customers @ £50/month = £100-150 MRR

### Medium-term Revenue (Month 1-2):
**Source:** Organic traffic to directory
**Target:** 10-15 customers @ £50/month = £500-750 MRR

### Long-term Revenue (Month 3+):
**Source:** Lead generation + subscriptions
**Target:** £3,000-5,000/month combined

---

## Ready to Execute?

### Checklist:
- [ ] WordPress URLs fixed (https://tstr.directory working)
- [ ] Python installed and dependencies ready
- [ ] Google Maps API key active
- [ ] Gmail ready for sending emails
- [ ] 30 minutes blocked for first outreach session

### Execute Now:
```bash
cd C:\Users\alber\OneDrive\Documents\.WORK\tstr-automation
python dual_scraper.py
```

**Then:**
1. Upload directory CSV to WordPress
2. Generate outreach emails
3. Send first 10 emails TODAY

---

**Your first customer is ONE email away. Let's get started! 🚀**
