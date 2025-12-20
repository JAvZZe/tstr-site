# TSTR.site Oracle Cloud Infrastructure Deployment Summary
**Date Generated**: 2025-11-08
**Based On**: Session notes from 2025-10-27 deployment

## CRITICAL OCI DEPLOYMENT STATUS

### Status: ✅ OPERATIONAL - Scrapers deployed and running on Oracle Cloud

---

## Oracle Cloud Instance Details

### Server Information
- **IP Address**: 84.8.139.90
- **OS**: Oracle Linux 9 (6.12.0-103.40.4.2.el9uek.x86_64)
- **Python Version**: 3.9.21
- **SSH User**: `opc`
- **SSH Key**: Located at `/media/al/AvZ WD White My Passport/PROJECTS/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key`
- **Cost**: FREE (Always Free Tier - 4 OCPU Ampere instance, 24GB RAM)

### Quick SSH Access
```bash
ssh -i "/media/al/AvZ WD White My Passport/PROJECTS/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key" opc@84.8.139.90
cd ~/tstr-scraper
```

---

## Deployed Scraper Files

### Location on OCI Instance
```
~/tstr-scraper/
├── dual_scraper.py              # Main scraper (fixed v2 - 729 lines)
├── run_scraper.py               # Orchestration script
├── upload_final.py              # Working Supabase upload
├── url_validator.py             # Website validation module
├── config.json                  # Source configuration (BBB, BIVDA, Biocompare)
├── .env                         # CONFIGURED with real Supabase credentials
├── test_supabase.py            # Connection verification script
├── check_schema.py             # Database schema inspector
├── dual_scraper_broken.py      # Backup of original (broken)
├── tstr_directory_import.csv   # Last scrape results (108 listings)
├── sales_contacts.csv          # 64 extracted contacts
├── invalid_urls.csv            # 17 failed URLs
└── scraper.log                 # Execution logs
```

---

## Scraper Execution Commands

### Run Full Scraper
```bash
cd ~/tstr-scraper
python3 run_scraper.py  # Full scrape (all sources)
```

### Just Upload CSV to Supabase
```bash
python3 upload_final.py
```

### Test Connection
```bash
python3 test_supabase.py          # Test connection + count listings
python3 check_schema.py           # View table structure
```

### View Logs
```bash
tail -50 scraper.log              # Last 50 lines of execution log
```

---

## Latest Production Results (2025-10-27)

**Source**: BIVDA (British In Vitro Diagnostics Association)
- **URL**: https://www.bivda.org.uk/about-bivda/find-a-member/
- **Companies Scraped**: 108 biopharma/biotech testing companies
- **Sales Contacts Extracted**: 64 decision-maker contacts
- **Upload Success Rate**: 100% (all 108 listings in Supabase)
- **Total Database Listings**: 127 (up from 19)

**Output Files Generated**:
1. `tstr_directory_import.csv` (109 lines including header)
2. `sales_contacts.csv` (64 contacts)
3. `invalid_urls.csv` (17 failed URLs)

---

## Supabase Database Connection

### Credentials (CONFIGURED ON OCI INSTANCE)
```bash
SUPABASE_URL=https://haimjeaetrsaauitrhfy.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2
```

### Database Details
- **Project ID**: `haimjeaetrsaauitrhfy`
- **Project URL**: https://haimjeaetrsaauitrhfy.supabase.co
- **Direct Dashboard**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy

### Listings Table Structure
```sql
Key columns:
- id (uuid, primary key)
- business_name (text, required)
- slug (text, required, URL-friendly)
- category_id (uuid, foreign key to categories)
- location_id (uuid, foreign key to locations)
- description, website, phone, address
- latitude, longitude (float, optional)
- status ('active'), plan_type ('free')
```

### Available Categories
- Oil & Gas Testing
- Biopharma & Life Sciences Testing ✅ (currently used)
- Environmental Testing
- Materials Testing

### Available Locations
- Global, North America, Europe, Asia
- United States, United Kingdom ✅ (currently used)
- Singapore, Houston, San Francisco, New York

---

## Scraper Configuration

### Sources Configured (config.json)
1. **BIVDA** - British In Vitro Diagnostics Association (✅ WORKING - 108 results)
2. **BBB** - Better Business Bureau (configured, 0 results found - needs investigation)
3. **Biocompare** - Life science research directory (configured, not yet run)

### Google Maps API
- **Status**: DISABLED (intentionally left blank)
- **Reason**: Cost concerns - $7/1000 requests for Places API
- **Strategy**: Using free industry association directories instead
- **Can Enable**: Later after cost/benefit analysis

---

## Critical Issues & Notes

### ⚠️ Unresolved Issue: Supabase Dashboard Login
**Problem**: Cannot log into Supabase web UI from Windows machine
**Accounts Tried**: 
- JAvZZe GitHub sign-in
- tstr.site1@gmail.com
- avztest8@gmail.com

**API Access**: ✅ Working (API keys functional)
**Impact**: Low (can manage via API, but UI would be helpful for schema changes)
**Next Step**: Check Windows browsers for active session/saved credentials

---

## Automation & Scheduling

### Cron Job Template (Ready to Deploy)
```bash
# Add to Oracle instance crontab (crontab -e):
0 2 * * * cd /home/opc/tstr-scraper && python3 run_scraper.py >> scraper.log 2>&1
```

**Schedule**: Daily at 2:00 AM UTC
**Status**: NOT YET CONFIGURED - manual runs only

---

## File Transfer Commands

### Upload to OCI Instance
```bash
scp -i "/media/al/AvZ WD White My Passport/PROJECTS/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key" LOCAL_FILE opc@84.8.139.90:~/tstr-scraper/
```

### Download from OCI Instance
```bash
scp -i "/media/al/AvZ WD White My Passport/PROJECTS/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key" opc@84.8.139.90:~/tstr-scraper/FILE ./
```

---

## Missing OCI Configuration Components

⚠️ **NO OCI CLI CONFIG FOUND** - `/home/al/.oci/config` does NOT EXIST

### What Would Be Needed for OCI CLI:
1. OCI Compartment ID
2. OCI Region (currently using 84.8.139.90 - need to identify actual region)
3. OCI Tenancy ID
4. OCI User ID
5. OCI API Key pair

### Current Access Method
- SSH-based access only (no OCI CLI configured)
- Direct management via Oracle Cloud console

---

## Scheduler Status

### Current Setup: NONE
**Options Available**:
1. **Cron job on OCI instance** (recommended)
2. **OCI Scheduler** (would need OCI CLI configuration)
3. **GitHub Actions** (alternative)
4. **Cloudflare Cron** (alternative)

### Recommended Next Step
Set up cron job on OCI instance (simplest, most reliable)

---

## CRITICAL NEXT STEPS

### Priority 1: ✅ IMMEDIATE - Configure Scheduler
```bash
ssh opc@84.8.139.90
crontab -e
# Add: 0 2 * * * cd /home/opc/tstr-scraper && python3 run_scraper.py >> scraper.log 2>&1
```

### Priority 2: Find Supabase Dashboard Login
- Check Windows browsers for active session
- Document which email owns project
- Add to password manager

### Priority 3: Verify Live Site
- Visit https://tstr.site
- Confirm 127 listings display
- Check "Biopharma & Life Sciences Testing" category
- Test search functionality

### Priority 4: Set Up Monitoring
- Monitor first automated run
- Set up email alerts for failures
- Create dashboard for execution history

### Priority 5: Expand Data Sources
- Investigate why BBB returned 0 results
- Deploy Biocompare scraper
- Research Oil & Gas testing sources

---

## Cost Summary

| Component | Cost | Status |
|-----------|------|--------|
| Oracle Cloud Instance | FREE | Always Free Tier |
| Database (Supabase) | ~$1/mo | Current usage |
| Frontend (Cloudflare Pages) | FREE | Static hosting |
| **TOTAL** | **~$1/month** | ✅ Sustainable |

---

## Documentation Files

### On Local Machine
- `/media/al/AI_DATA/AI_PROJECTS_SPACE/TSTR_ORACLE_SCRAPER_STATUS.md` - Status (last updated 2025-10-28)
- `/media/al/AI_DATA/AI_PROJECTS_SPACE/TSTR_ORACLE_SCRAPER_NOTES.md` - Technical notes
- `/media/al/AI_DATA/AI_PROJECTS_SPACE/TSTR_CREDENTIALS_MASTER.md` - Full credentials reference
- `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/HANDOFF_2025-10-27.md` - Detailed handoff doc

### On OCI Instance
- `~/tstr-scraper/scraper.log` - Execution logs
- `~/tstr-scraper/config.json` - Source configuration

---

**Report Generated**: 2025-11-08
**Source Documents Reviewed**: 12 files
**Confidence Level**: HIGH (based on recent session documentation)
