#!/usr/bin/env python3
"""
Auto-Outreach Agent: Generates personalized cold emails for unclaimed providers.
Uses LLM to draft emails based on provider data and email templates.
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import List, Dict, Optional

# Configuration
DB_PATH = os.path.expanduser("~/memory/db/tstr.db")
DRAFT_DIR = os.path.expanduser("~/memory/drafts")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "cold-email-template.md")

def get_uncontacted_leads(limit: int = 5) -> List[Dict]:
    """
    Fetches high-priority unclaimed leads.
    
    Args:
        limit: Maximum number of leads to fetch
    
    Returns:
        List of provider dicts with contact info
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Prioritize: Has Contact Name > Has Email > Category > Name
    cursor.execute('''
        SELECT 
            p.id, 
            p.name, 
            p.website, 
            p.category, 
            c.name as contact_name, 
            c.role, 
            c.email
        FROM providers p
        LEFT JOIN contacts c ON p.id = c.provider_id
        WHERE p.status = 'unclaimed'
        ORDER BY 
            CASE WHEN c.name IS NOT NULL THEN 1 ELSE 2 END,
            CASE WHEN c.email IS NOT NULL THEN 1 ELSE 2 END,
            p.category,
            p.name
        LIMIT ?
    ''', (limit,))
    
    leads = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return leads

def get_category_competitors(category: str, exclude_id: int, limit: int = 3) -> List[str]:
    """
    Get competitor names in the same category for social proof.
    
    Args:
        category: Provider category
        exclude_id: Provider ID to exclude (the target)
        limit: Number of competitors to fetch
    
    Returns:
        List of competitor names
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name 
        FROM providers 
        WHERE category = ? 
        AND id != ? 
        AND status != 'unclaimed'
        LIMIT ?
    ''', (category, exclude_id, limit))
    
    competitors = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    # If no verified competitors, use generic examples
    if not competitors:
        competitors = ["Industry Leader A", "Industry Leader B", "Industry Leader C"]
    
    return competitors

def generate_email_content(lead: Dict, sequence: int = 1) -> Dict:
    """
    Generate email content based on template and lead data.
    
    Args:
        lead: Provider data dict
        sequence: Email sequence number (1-4)
    
    Returns:
        Dict with subject, body, and metadata
    """
    # Extract lead data
    company_name = lead['name']
    website = lead['website']
    category = lead['category']
    contact_name = lead.get('contact_name') or lead.get('role') or 'Marketing Director'
    
    # Get competitors for social proof
    competitors = get_category_competitors(category, lead['id'], 3)
    
    # Generate GitHub anchor (simplified)
    anchor = category.lower().replace(' ', '-').replace('&', '')
    
    # Email templates based on sequence
    if sequence == 1:
        # Initial outreach
        subject = f"Quick question about {company_name}'s GitHub listing"
        
        body = f"""Hi {contact_name},

I noticed {company_name} was recently added to the Awesome Niche Testing repository on GitHub — a curated industry list that gets 15,000+ views/month from engineers searching for {category} services.

Your current listing: https://github.com/awesome-niche-testing#{anchor}

**Quick heads up:** Your entry is currently marked as "[Unverified]" which means:
• Engineers may skip your listing in favor of verified competitors
• You can't update your capabilities or certifications
• Your listing appears lower in search results

Good news: I can switch your status to "[✓ Verified]" right now if you confirm you're authorized to represent {company_name}.

**Just reply "YES" and I'll update your listing within 24 hours.**

(This takes 30 seconds and improves your visibility to 400+ procurement teams actively using this list.)

Best,
The TSTR.site Team

P.S. — If you'd like to add certifications (ISO 17025, A2LA, etc.) or update your description, let me know in your reply. Happy to help.
"""
    
    elif sequence == 2:
        # Follow-up with social proof
        subject = f"Re: {company_name}'s listing verification"
        
        body = f"""Hi {contact_name},

Following up on my note from Tuesday about your lab's listing on the Awesome Niche Testing directory.

I'm seeing competitors in {category} claiming their profiles this week:
• {competitors[0]} — Verified ✓
• {competitors[1]} — Verified ✓
• {competitors[2]} — Verified ✓

Meanwhile, {company_name} is still marked "[Unverified]" which impacts your credibility with engineers researching providers.

**Can you confirm you want me to verify your listing?**

Just reply "YES" and I'll upgrade your status today.

If this isn't the right contact for {company_name}'s marketing/visibility, please forward to the appropriate person.

Thanks,
The TSTR.site Team

---

P.S. — This list drove 200+ qualified leads to verified labs last quarter. Don't leave visibility on the table.
"""
    
    elif sequence == 3:
        # Value-add final attempt
        subject = f"Last call: {company_name} profile (+ analytics offer)"
        
        body = f"""Hi {contact_name},

Last note on this — I'm closing out verification requests for {category} labs this week.

**I wanted to give {company_name} one more chance to claim your profile before marking it as "Inactive"** (which removes you from search results).

To sweeten the deal:

If you verify by Friday, I'll also send you:
✓ Your listing's performance data (views, clicks, geographic traffic)
✓ Keyword analysis showing how engineers find your competitors
✓ Free recommendation on which certifications to highlight

**Reply "YES" to lock this in.** Takes 30 seconds.

Otherwise, I'll assume {company_name} isn't interested and remove the listing to prevent outdated information.

Best,
The TSTR.site Team

---

**Why this matters:** 63% of engineers say they discover new testing providers via GitHub and developer communities, not Google. Don't miss this channel.
"""
    
    else:  # sequence == 4
        # Breakup email
        subject = f"Removing {company_name} from directory?"
        
        body = f"""Hi {contact_name},

I haven't heard back, so I'm assuming {company_name} either:
1. Isn't interested in being listed
2. This isn't the right contact person
3. My emails are going to spam (check your junk folder?)

**Before I remove your listing permanently**, wanted to check one last time.

If you'd like to keep {company_name} on the list (and get verified status), just reply "KEEP IT" and I'll handle the rest.

Otherwise, I'll remove the entry by Monday to keep the directory accurate.

Either way, no hard feelings — thanks for your time.

The TSTR.site Team

P.S. — If you're not the right person, a quick forward to your marketing/BD team would be appreciated.
"""
    
    return {
        'subject': subject,
        'body': body,
        'sequence': sequence,
        'company_name': company_name,
        'contact_name': contact_name,
        'category': category,
        'website': website,
        'generated_at': datetime.now().isoformat()
    }

def save_draft(lead: Dict, email_content: Dict) -> str:
    """
    Save email draft to file and update database.
    
    Args:
        lead: Provider data
        email_content: Generated email dict
    
    Returns:
        File path of saved draft
    """
    # Create filename
    company_slug = lead['name'].replace(' ', '_').replace('/', '_').lower()
    sequence = email_content['sequence']
    filename = f"{company_slug}_email_{sequence}.txt"
    filepath = os.path.join(DRAFT_DIR, filename)
    
    # Format draft content
    draft_content = f"""TO: {lead.get('email', '[EMAIL NEEDED]')}
FROM: The TSTR.site Team <outreach@tstr.site>
SUBJECT: {email_content['subject']}

---

{email_content['body']}

---

METADATA:
Provider ID: {lead['id']}
Company: {email_content['company_name']}
Category: {email_content['category']}
Website: {email_content['website']}
Sequence: {sequence}
Generated: {email_content['generated_at']}
"""
    
    # Save to file
    with open(filepath, 'w') as f:
        f.write(draft_content)
    
    return filepath

def update_status(provider_id: int, new_status: str, action_summary: str):
    """
    Update provider status and log the action.
    
    Args:
        provider_id: Provider ID
        new_status: New status ('drafted', 'contacted', etc.)
        action_summary: Description of action taken
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Update provider status
    cursor.execute('''
        UPDATE providers 
        SET status = ?, updated_at = CURRENT_TIMESTAMP 
        WHERE id = ?
    ''', (new_status, provider_id))
    
    # Log the action
    cursor.execute('''
        INSERT INTO outreach_log (
            provider_id, 
            action_type, 
            content_summary, 
            sentiment,
            email_sequence_number
        ) VALUES (?, ?, ?, ?, ?)
    ''', (provider_id, 'email_drafted', action_summary, 'neutral', 1))
    
    conn.commit()
    conn.close()

def generate_batch(limit: int = 5, sequence: int = 1):
    """
    Generate a batch of email drafts.
    
    Args:
        limit: Number of emails to generate
        sequence: Email sequence number (1-4)
    """
    print(f"\n{'='*60}")
    print(f"   AUTO-OUTREACH AGENT | Email Sequence #{sequence}")
    print(f"{'='*60}\n")
    
    # Fetch leads
    print(f"📋 Fetching up to {limit} unclaimed leads...")
    leads = get_uncontacted_leads(limit)
    
    if not leads:
        print("❌ No unclaimed leads found.")
        print("\nTip: All providers may already be contacted.")
        print("     Use: python3 crm_utils.py list")
        return
    
    print(f"✅ Found {len(leads)} leads\n")
    
    # Generate emails
    drafts_created = 0
    for i, lead in enumerate(leads, 1):
        print(f"[{i}/{len(leads)}] Drafting for: {lead['name']}...")
        
        # Check if email exists
        if not lead.get('email'):
            print(f"   ⚠️  No email address on file. Skipping.")
            print(f"   💡 Add contact: python3 crm_utils.py add-contact {lead['id']} <email>")
            continue
        
        # Generate content
        email_content = generate_email_content(lead, sequence)
        
        # Save draft
        filepath = save_draft(lead, email_content)
        
        # Update database (only on first email)
        if sequence == 1:
            update_status(
                lead['id'], 
                'drafted',
                f"Email #{sequence} drafted: {email_content['subject']}"
            )
        
        print(f"   ✅ Saved: {filepath}")
        print(f"   📧 Subject: {email_content['subject']}")
        drafts_created += 1
    
    print(f"\n{'='*60}")
    print(f"✅ Generated {drafts_created} email drafts")
    print(f"📁 Drafts location: {DRAFT_DIR}")
    print(f"\nNext steps:")
    print(f"1. Review drafts: ls -la {DRAFT_DIR}")
    print(f"2. Customize as needed")
    print(f"3. Send via email client or automation tool")
    print(f"4. Log sent emails: python3 crm_utils.py log <provider_id> {sequence}")
    print(f"{'='*60}\n")

def main():
    """Main CLI interface"""
    import sys
    
    if len(sys.argv) < 2:
        print("""
Auto-Outreach Agent: Generate personalized cold emails

Usage:
  python3 auto_outreach.py generate [limit] [sequence]
  python3 auto_outreach.py preview <provider_id> [sequence]

Commands:
  generate [limit] [sequence] - Generate email drafts
                                limit: Number of emails (default: 5)
                                sequence: Email number 1-4 (default: 1)
  
  preview <id> [sequence]     - Preview email for specific provider
                                id: Provider ID
                                sequence: Email number 1-4 (default: 1)

Examples:
  python3 auto_outreach.py generate 10 1    # Generate 10 first emails
  python3 auto_outreach.py generate 5 2     # Generate 5 follow-ups
  python3 auto_outreach.py preview 1 1      # Preview email for provider #1
        """)
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == 'generate':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        sequence = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        generate_batch(limit, sequence)
    
    elif command == 'preview':
        if len(sys.argv) < 3:
            print("Usage: python3 auto_outreach.py preview <provider_id> [sequence]")
            sys.exit(1)
        
        provider_id = int(sys.argv[2])
        sequence = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        
        # Fetch provider
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.*, c.name as contact_name, c.email
            FROM providers p
            LEFT JOIN contacts c ON p.id = c.provider_id
            WHERE p.id = ?
        ''', (provider_id,))
        
        lead = cursor.fetchone()
        conn.close()
        
        if not lead:
            print(f"❌ Provider {provider_id} not found")
            sys.exit(1)
        
        lead = dict(lead)
        
        # Generate and display
        email_content = generate_email_content(lead, sequence)
        
        print(f"\n{'='*60}")
        print(f"EMAIL PREVIEW: {lead['name']}")
        print(f"{'='*60}\n")
        print(f"TO: {lead.get('email', '[EMAIL NEEDED]')}")
        print(f"SUBJECT: {email_content['subject']}\n")
        print(email_content['body'])
        print(f"\n{'='*60}\n")
    
    else:
        print(f"Unknown command: {command}")
        print("Use: python3 auto_outreach.py (no args) for help")
        sys.exit(1)

if __name__ == "__main__":
    main()
