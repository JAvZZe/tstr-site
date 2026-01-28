"""
Email Outreach Generator
Reads sales_leads.csv and generates personalized outreach emails
"""

import csv
import os
from datetime import datetime

def generate_personalized_email(contact):
    """
    Generate personalized email based on contact info
    """
    company = contact['company_name']
    name = contact['contact_name']
    category = contact['category']
    
    # Personalize first line based on what we know
    if name:
        greeting = f"Hi {name.split()[0]},"
    else:
        greeting = "Hi there,"
    
    # Customize value prop based on category
    value_props = {
        'Oil & Gas Testing': 'oil & gas pipeline integrity and materials testing',
        'Pharmaceutical Testing': 'pharmaceutical stability and analytical testing',
        'Biotech Testing': 'biotech analytical and characterization services',
        'Environmental Testing': 'environmental compliance and contamination analysis',
        'Materials Testing': 'materials characterization and failure analysis'
    }
    
    value_prop = value_props.get(category, 'specialized testing services')
    
    email_body = f"""Subject: {company} - Featured Listing on New Testing Labs Directory

{greeting}

I'm launching TSTR.directory, a specialist directory exclusively for high-value testing laboratories serving {value_prop}.

I came across {company} and was impressed by your expertise in {category.lower()}. You'd be perfect for our Featured section at launch.

Would you like a FREE 3-month Featured listing? (Worth £150)

This includes:
• Homepage prominent placement
• Priority in search results  
• Full company profile with photos
• Direct lead forwarding from clients

Only 20 launch spots available. Interested?

Reply "YES" and I'll set it up today.

Best regards,
Your name
TSTR.directory
https://tstr.directory"""

    return email_body

def generate_linkedin_message(contact):
    """
    Generate short LinkedIn connection message
    """
    company = contact['company_name']
    name = contact['contact_name'].split()[0] if contact['contact_name'] else "there"
    
    message = f"""Hi {name},

I'm building TSTR.directory - a specialist directory for testing laboratories.

{company} would be perfect for our featured launch section. Would love to offer you a complimentary 3-month premium listing.

Interested in a quick chat?"""

    return message

def main():
    """
    Generate outreach emails from scraped contacts
    """
    input_file = 'tstr_sales_leads.csv'
    output_file = f'outreach_emails_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run dual_scraper.py first.")
        return
    
    print("="*70)
    print("EMAIL OUTREACH GENERATOR")
    print("="*70)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        contacts = list(reader)
    
    # Filter for high-confidence contacts with email
    high_confidence = [c for c in contacts if c['email'] and c['confidence'] == 'high']
    medium_confidence = [c for c in contacts if c['email'] and c['confidence'] == 'medium']
    
    print(f"\nTotal leads: {len(contacts)}")
    print(f"High confidence with email: {len(high_confidence)}")
    print(f"Medium confidence with email: {len(medium_confidence)}")
    
    # Generate emails
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("TSTR.DIRECTORY - OUTREACH EMAILS\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        # High confidence contacts first
        if high_confidence:
            f.write("\n" + "="*70 + "\n")
            f.write("HIGH PRIORITY CONTACTS (Send First)\n")
            f.write("="*70 + "\n\n")
            
            for idx, contact in enumerate(high_confidence, 1):
                f.write(f"\n--- EMAIL #{idx} ---\n")
                f.write(f"To: {contact['email']}\n")
                f.write(f"Company: {contact['company_name']}\n")
                f.write(f"LinkedIn: {contact['linkedin_url']}\n")
                f.write("\n" + "-"*70 + "\n\n")
                f.write(generate_personalized_email(contact))
                f.write("\n\n" + "-"*70 + "\n")
                
                if contact['linkedin_url']:
                    f.write("\nLINKEDIN MESSAGE:\n")
                    f.write(generate_linkedin_message(contact))
                    f.write("\n" + "-"*70 + "\n\n")
        
        # Medium confidence contacts
        if medium_confidence:
            f.write("\n" + "="*70 + "\n")
            f.write("MEDIUM PRIORITY CONTACTS (Follow-up)\n")
            f.write("="*70 + "\n\n")
            
            for idx, contact in enumerate(medium_confidence[:20], 1):  # Limit to 20
                f.write(f"\n--- EMAIL #{idx} ---\n")
                f.write(f"To: {contact['email']}\n")
                f.write(f"Company: {contact['company_name']}\n")
                f.write("\n" + "-"*70 + "\n\n")
                f.write(generate_personalized_email(contact))
                f.write("\n\n" + "-"*70 + "\n\n")
    
    print(f"\n✓ Generated: {output_file}")
    print("\nNext steps:")
    print("  1. Review generated emails")
    print("  2. Copy-paste into your email client")
    print("  3. Send 10 emails per day (avoid spam filters)")
    print("  4. Track responses in sales_leads.csv")
    print("="*70)

if __name__ == "__main__":
    main()
