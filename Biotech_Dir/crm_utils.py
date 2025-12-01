#!/usr/bin/env python3
"""
CRM Utility Functions for Testing Lab Outreach
Usage: python3 crm_utils.py <command> [args]
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

DB_PATH = os.path.expanduser("~/memory/db/tstr.db")

def get_db():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

# ============================================
# QUERY FUNCTIONS (Read Operations)
# ============================================

def get_providers_by_status(status: str = 'unclaimed') -> List[Dict]:
    """
    Get all providers with a specific status.
    
    Args:
        status: 'unclaimed', 'contacted', 'claimed', 'verified', 'sponsor'
    
    Returns:
        List of provider dicts
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, website, category, status, tier, created_at
        FROM providers
        WHERE status = ?
        ORDER BY created_at DESC
    ''', (status,))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row[0],
            'name': row[1],
            'website': row[2],
            'category': row[3],
            'status': row[4],
            'tier': row[5],
            'created_at': row[6]
        })
    
    conn.close()
    return results

def get_next_actions(days_ahead: int = 7) -> List[Dict]:
    """
    Get all providers that need follow-up in the next N days.
    
    Args:
        days_ahead: Look ahead this many days
    
    Returns:
        List of actions due
    """
    conn = get_db()
    cursor = conn.cursor()
    
    today = datetime.now().date()
    future_date = today + timedelta(days=days_ahead)
    
    cursor.execute('''
        SELECT 
            ol.id,
            ol.provider_id,
            p.name,
            p.website,
            ol.action_type,
            ol.next_action_date,
            ol.email_sequence_number
        FROM outreach_log ol
        JOIN providers p ON ol.provider_id = p.id
        WHERE ol.next_action_date BETWEEN ? AND ?
        ORDER BY ol.next_action_date ASC
    ''', (today.isoformat(), future_date.isoformat()))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'log_id': row[0],
            'provider_id': row[1],
            'provider_name': row[2],
            'website': row[3],
            'last_action': row[4],
            'next_action_date': row[5],
            'sequence_number': row[6]
        })
    
    conn.close()
    return results

def get_outreach_history(provider_id: int) -> List[Dict]:
    """
    Get full outreach history for a specific provider.
    
    Args:
        provider_id: Provider ID
    
    Returns:
        List of outreach events
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            id,
            action_type,
            content_summary,
            sentiment,
            email_sequence_number,
            timestamp
        FROM outreach_log
        WHERE provider_id = ?
        ORDER BY timestamp DESC
    ''', (provider_id,))
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'id': row[0],
            'action_type': row[1],
            'summary': row[2],
            'sentiment': row[3],
            'sequence': row[4],
            'timestamp': row[5]
        })
    
    conn.close()
    return results

def get_funnel_stats() -> Dict:
    """
    Get conversion funnel statistics.
    
    Returns:
        Dict with counts by status and tier
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Counts by status
    cursor.execute('''
        SELECT status, COUNT(*) as count
        FROM providers
        GROUP BY status
    ''')
    status_counts = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Counts by tier
    cursor.execute('''
        SELECT tier, COUNT(*) as count
        FROM providers
        GROUP BY tier
    ''')
    tier_counts = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Revenue calculation
    revenue = (
        tier_counts.get('fast_track', 0) * 50 +
        tier_counts.get('partner', 0) * 250
    )
    
    conn.close()
    
    return {
        'by_status': status_counts,
        'by_tier': tier_counts,
        'total_revenue': revenue,
        'total_providers': sum(status_counts.values())
    }

# ============================================
# ACTION FUNCTIONS (Write Operations)
# ============================================

def log_outreach(
    provider_id: int,
    action_type: str,
    content_summary: str,
    sentiment: Optional[str] = None,
    sequence_number: int = 1,
    days_until_next: int = 3
) -> int:
    """
    Log an outreach action (email sent, reply received, etc.)
    
    Args:
        provider_id: Provider ID
        action_type: 'email_sent', 'reply_received', 'bounced', 'invoice_sent'
        content_summary: One-line summary of what happened
        sentiment: 'positive', 'negative', 'neutral', 'bounced'
        sequence_number: Which email in the sequence (1-4)
        days_until_next: Schedule next follow-up in N days
    
    Returns:
        Log entry ID
    """
    conn = get_db()
    cursor = conn.cursor()
    
    next_action_date = (datetime.now() + timedelta(days=days_until_next)).date()
    
    cursor.execute('''
        INSERT INTO outreach_log (
            provider_id,
            action_type,
            content_summary,
            sentiment,
            email_sequence_number,
            next_action_date
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', (provider_id, action_type, content_summary, sentiment, sequence_number, next_action_date.isoformat()))
    
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return log_id

def update_provider_status(provider_id: int, new_status: str) -> None:
    """
    Update provider status in the funnel.
    
    Args:
        provider_id: Provider ID
        new_status: 'unclaimed', 'contacted', 'claimed', 'verified', 'sponsor'
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE providers
        SET status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (new_status, provider_id))
    
    conn.commit()
    conn.close()

def update_provider_tier(provider_id: int, new_tier: str) -> None:
    """
    Update provider tier (revenue level).
    
    Args:
        provider_id: Provider ID
        new_tier: 'free', 'fast_track', 'partner'
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE providers
        SET tier = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (new_tier, provider_id))
    
    conn.commit()
    conn.close()

def add_contact(
    provider_id: int,
    name: str,
    email: str,
    role: Optional[str] = None,
    linkedin_url: Optional[str] = None
) -> int:
    """
    Add a contact person for a provider.
    
    Args:
        provider_id: Provider ID
        name: Contact person's name
        email: Contact email
        role: Job title (e.g., 'Marketing Director')
        linkedin_url: LinkedIn profile URL
    
    Returns:
        Contact ID
    """
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO contacts (provider_id, name, email, role, linkedin_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (provider_id, name, email, role, linkedin_url))
    
    contact_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return contact_id

# ============================================
# CLI COMMANDS
# ============================================

def cmd_list_unclaimed():
    """List all unclaimed providers (ready for outreach)"""
    providers = get_providers_by_status('unclaimed')
    
    print(f"\n=== UNCLAIMED PROVIDERS ({len(providers)}) ===\n")
    
    for p in providers:
        print(f"ID: {p['id']}")
        print(f"Name: {p['name']}")
        print(f"Category: {p['category']}")
        print(f"Website: {p['website']}")
        print("-" * 60)

def cmd_next_actions():
    """Show providers that need follow-up soon"""
    actions = get_next_actions(days_ahead=7)
    
    print(f"\n=== NEXT ACTIONS (Next 7 Days) ===\n")
    
    if not actions:
        print("No pending actions. Good job!")
        return
    
    for a in actions:
        print(f"📅 {a['next_action_date']} - {a['provider_name']}")
        print(f"   Last Action: {a['last_action']} (Email #{a['sequence_number']})")
        print(f"   Provider ID: {a['provider_id']}")
        print()

def cmd_stats():
    """Show funnel statistics"""
    stats = get_funnel_stats()
    
    print("\n=== FUNNEL STATISTICS ===\n")
    
    print("📊 By Status:")
    for status, count in stats['by_status'].items():
        print(f"   {status:15} : {count:3} providers")
    
    print("\n💰 By Tier:")
    for tier, count in stats['by_tier'].items():
        print(f"   {tier:15} : {count:3} providers")
    
    print(f"\n💵 Total Revenue: ${stats['total_revenue']:,}")
    print(f"📈 Total Providers: {stats['total_providers']}")

def cmd_log_email(provider_id: int, sequence: int = 1):
    """Log that an email was sent"""
    log_id = log_outreach(
        provider_id=provider_id,
        action_type='email_sent',
        content_summary=f'Sent email #{sequence} (verification request)',
        sequence_number=sequence,
        days_until_next=3
    )
    
    update_provider_status(provider_id, 'contacted')
    
    print(f"✅ Logged email #{sequence} to provider {provider_id}")
    print(f"   Next follow-up scheduled in 3 days")
    print(f"   Log ID: {log_id}")

def cmd_history(provider_id: int):
    """Show outreach history for a provider"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, website, status, tier FROM providers WHERE id = ?', (provider_id,))
    provider = cursor.fetchone()
    
    if not provider:
        print(f"❌ Provider {provider_id} not found")
        return
    
    print(f"\n=== OUTREACH HISTORY: {provider[0]} ===")
    print(f"Website: {provider[1]}")
    print(f"Status: {provider[2]} | Tier: {provider[3]}\n")
    
    history = get_outreach_history(provider_id)
    
    if not history:
        print("No outreach history yet.")
        return
    
    for event in history:
        print(f"📅 {event['timestamp']}")
        print(f"   Action: {event['action_type']} (Email #{event['sequence']})")
        print(f"   Summary: {event['summary']}")
        if event['sentiment']:
            print(f"   Sentiment: {event['sentiment']}")
        print()
    
    conn.close()

# ============================================
# MAIN CLI
# ============================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("""
CRM Utility Commands:

  python3 crm_utils.py list           - List all unclaimed providers
  python3 crm_utils.py next           - Show next actions due
  python3 crm_utils.py stats          - Show funnel statistics
  python3 crm_utils.py log <id> [seq] - Log email sent to provider
  python3 crm_utils.py history <id>   - Show provider outreach history

Examples:
  python3 crm_utils.py list
  python3 crm_utils.py log 1 1        # Log email #1 to provider ID 1
  python3 crm_utils.py history 1      # Show history for provider ID 1
        """)
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        cmd_list_unclaimed()
    elif command == 'next':
        cmd_next_actions()
    elif command == 'stats':
        cmd_stats()
    elif command == 'log':
        if len(sys.argv) < 3:
            print("Usage: python3 crm_utils.py log <provider_id> [sequence_number]")
            sys.exit(1)
        provider_id = int(sys.argv[2])
        sequence = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        cmd_log_email(provider_id, sequence)
    elif command == 'history':
        if len(sys.argv) < 3:
            print("Usage: python3 crm_utils.py history <provider_id>")
            sys.exit(1)
        provider_id = int(sys.argv[2])
        cmd_history(provider_id)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
