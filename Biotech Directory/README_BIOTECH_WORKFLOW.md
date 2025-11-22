# Biotech Outreach Workflow - Quick Reference

**Location**: `/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/Biotech Directory`

**Database**: `~/memory/db/tstr.db` (shared, outside this folder)  
**Drafts**: `~/memory/drafts/` (shared, outside this folder)

---

## Files in This Directory

### Scripts (Executable)
- `crm_utils.py` - CRM management CLI
- `dashboard.py` - Visual pipeline dashboard
- `auto_outreach.py` - Email generator
- `ingest_providers.py` - Import labs from README
- `dashboard.sh` - Shell dashboard (requires sqlite3)

### Data Sources
- `awesome-biotech-niche-testing-README.md` - Public directory (for GitHub)
- `private_leads.csv` - Private contact database (imported)
- `BIOTECH_LISTINGS_SUMMARY.md` - Analysis of 108 pharma/biotech labs

### Documentation
- `cold-email-template.md` - 4-email sequence templates
- `awesome-testing-SPONSORSHIP.md` - Pricing tiers ($50/$250)
- `awesome-testing-CONTRIBUTING.md` - Submission guidelines

### Development Files
- `query_biotech.py` - Database query helper
- `query_biotech.sql` - SQL queries

---

## Quick Start (From This Directory)

### View Dashboard
```bash
cd "/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/Biotech Directory"
python3 dashboard.py
```

### List Unclaimed Providers
```bash
python3 crm_utils.py list
```

### Generate Email Drafts
```bash
# Preview single email
python3 auto_outreach.py preview <provider_id> 1

# Generate 5 emails
python3 auto_outreach.py generate 5 1
```

### Track Outreach Activity
```bash
# Log email sent
python3 crm_utils.py log <provider_id> 1

# View provider history
python3 crm_utils.py history <provider_id>

# See next actions
python3 crm_utils.py next
```

---

## Current Database Status

**Total**: 34 testing laboratories
- Original (from awesome-biotech README): 14 labs
- Private leads (from CSV): 20 labs

**Contacts**: 21 providers have email addresses

**Pipeline**:
- Drafted: 6 (emails ready to send)
- Contacted: 1 (sent, waiting for reply)
- Unclaimed: 27 (need action)

**Revenue**: $0 (all on free tier)

---

## Email Sequence Strategy

### Email #1 (Initial Outreach)
**Subject**: "Quick question about {Company}'s GitHub listing"  
**Hook**: Loss aversion (unverified = lower ranking)  
**CTA**: Reply "YES" to verify  
**Send when**: Provider is unclaimed

### Email #2 (Follow-up - Day 3)
**Subject**: "Re: {Company}'s listing verification"  
**Hook**: Social proof (competitors verified)  
**CTA**: Reply "YES"  
**Send when**: No response to Email #1

### Email #3 (Value-Add - Day 7)
**Subject**: "Last call: {Company} profile (+ analytics offer)"  
**Hook**: Free analytics + removal threat  
**CTA**: Reply "YES"  
**Send when**: No response to Email #2

### Email #4 (Breakup - Day 14)
**Subject**: "Removing {Company} from directory?"  
**Hook**: Final chance before permanent removal  
**CTA**: Reply "KEEP IT"  
**Send when**: No response to Email #3

---

## Revenue Tiers

### Free Tier (Current: 34)
- Listed on awesome-niche-testing GitHub
- Marked as [Unverified]
- Basic description

### Fast Track ($50 one-time)
- [✓ Verified] badge
- Priority placement in category
- Top of search results
- Updated within 48 hours

### Lab Partner ($250/month)
- All Fast Track benefits
- Company logo displayed
- Bold listing with 200-word description
- Monthly analytics reports
- Direct booking link

---

## Conversion Funnel

```
Unclaimed (27)
    ↓ Send Email #1
Contacted (1)
    ↓ Reply "YES"
Claimed (0)
    ↓ Pitch Fast Track
Verified (0)
    ↓ Upsell Lab Partner
Sponsor (0)
```

**Target Conversion Rates**:
- Email → Reply: 10-15%
- Claimed → Fast Track: 15-20%
- Fast Track → Lab Partner: 5-10%

**Revenue Projection** (21 providers with emails):
- Replies: ~3 (15%)
- Fast Track: ~1 ($50)
- Lab Partner: ~0 (need more volume)

---

## Daily Workflow

### Morning (5 minutes)
```bash
cd "/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/Biotech Directory"

# Check dashboard
python3 dashboard.py

# Check next actions
python3 crm_utils.py next
```

### When Reply Received
```bash
# Positive reply ("YES")
python3 << 'EOF'
import sqlite3, os
conn = sqlite3.connect(os.path.expanduser("~/memory/db/tstr.db"))
cursor = conn.cursor()
cursor.execute("UPDATE providers SET status = 'claimed' WHERE id = ?", (PROVIDER_ID,))
cursor.execute("INSERT INTO outreach_log (provider_id, action_type, content_summary, sentiment) VALUES (?, ?, ?, ?)", 
               (PROVIDER_ID, 'reply_received', 'Replied YES to verification', 'positive'))
conn.commit()
conn.close()
EOF

# Then send verification confirmation + Fast Track upsell
python3 auto_outreach.py preview PROVIDER_ID 5  # (if we add upsell email template)
```

### End of Day (2 minutes)
```bash
# Log any emails sent today
python3 crm_utils.py log <provider_id> <sequence_number>

# Check updated stats
python3 crm_utils.py stats
```

---

## Add New Leads

### From CSV
```bash
# 1. Create CSV with columns: name,website,category,contact_name,contact_role,contact_email
# 2. Run import
python3 << 'EOF'
import sqlite3, csv, os
db_path = os.path.expanduser('~/memory/db/tstr.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()

with open('new_leads.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute('INSERT OR IGNORE INTO providers (name, website, category, status) VALUES (?, ?, ?, ?)', 
                    (row['name'], row['website'], row['category'], 'unclaimed'))
        cur.execute('SELECT id FROM providers WHERE website = ?', (row['website'],))
        pid = cur.fetchone()[0]
        cur.execute('INSERT OR IGNORE INTO contacts (provider_id, name, role, email) VALUES (?, ?, ?, ?)',
                    (pid, row['contact_name'], row['contact_role'], row['contact_email']))

conn.commit()
print('Import complete')
EOF
```

### Manual Entry
```bash
python3 << 'EOF'
import sqlite3, os
conn = sqlite3.connect(os.path.expanduser("~/memory/db/tstr.db"))
cursor = conn.cursor()

# Add provider
cursor.execute('''
    INSERT INTO providers (name, website, category, status, tier)
    VALUES (?, ?, ?, ?, ?)
''', ("Lab Name", "https://labwebsite.com", "Biotech", "unclaimed", "free"))
provider_id = cursor.lastrowid

# Add contact
cursor.execute('''
    INSERT INTO contacts (provider_id, name, role, email)
    VALUES (?, ?, ?, ?)
''', (provider_id, "Jane Doe", "Marketing Director", "jane@labwebsite.com"))

conn.commit()
conn.close()
print(f"Added provider ID: {provider_id}")
EOF
```

---

## Troubleshooting

### Scripts Not Working?
**Problem**: Python not found  
**Fix**: Use `python3` instead of `python`

**Problem**: Database not found  
**Fix**: Database is at `~/memory/db/tstr.db` (absolute path, works from anywhere)

**Problem**: No email drafts generated  
**Fix**: Providers need contacts added first. Check: `python3 crm_utils.py list`

### Email Bounces
```bash
# Mark as bounced
python3 << 'EOF'
import sqlite3, os
conn = sqlite3.connect(os.path.expanduser("~/memory/db/tstr.db"))
cursor = conn.cursor()
cursor.execute("UPDATE providers SET status = 'bounced' WHERE id = ?", (PROVIDER_ID,))
cursor.execute("INSERT INTO outreach_log (provider_id, action_type, content_summary, sentiment) VALUES (?, ?, ?, ?)", 
               (PROVIDER_ID, 'email_bounced', 'Email bounced - invalid address', 'bounced'))
conn.commit()
conn.close()
EOF
```

---

## File Structure Map

```
Biotech Directory/
├── Scripts
│   ├── crm_utils.py              # CRM management
│   ├── dashboard.py              # Visual dashboard
│   ├── auto_outreach.py          # Email generator
│   └── ingest_providers.py       # Data import
│
├── Data
│   ├── awesome-biotech-niche-testing-README.md  # Public list
│   ├── private_leads.csv                        # Private contacts
│   └── BIOTECH_LISTINGS_SUMMARY.md              # Analysis
│
├── Documentation
│   ├── cold-email-template.md                   # Email sequences
│   ├── awesome-testing-SPONSORSHIP.md           # Pricing
│   └── awesome-testing-CONTRIBUTING.md          # Guidelines
│
└── This File
    └── README_BIOTECH_WORKFLOW.md               # You are here

External (Shared):
├── ~/memory/db/tstr.db           # CRM database (34 providers)
└── ~/memory/drafts/              # Generated email drafts (6 files)
```

---

## Next Steps

**Immediate** (Today):
1. Review 6 generated email drafts in `~/memory/drafts/`
2. Send first batch (5-10 emails)
3. Log sent emails with `crm_utils.py log`

**This Week**:
1. Generate remaining email drafts (`auto_outreach.py generate 15 1`)
2. Send all initial outreach (sequence #1)
3. Track replies and update statuses

**Next Week**:
1. Send follow-ups (sequence #2) to non-responders
2. Handle positive replies (verification + Fast Track pitch)
3. Monitor conversion rates in dashboard

---

## Support & Resources

**Database Location**: `~/memory/db/tstr.db`  
**Drafts Location**: `~/memory/drafts/`  
**Main Project**: `../` (TSTR.site main directory)

**Key Learning**: All scripts use absolute paths to shared database, so they work from any directory.

---

**Last Updated**: 2025-11-21  
**Status**: Production-ready with 34 labs, 21 contacts, 6 drafts generated
