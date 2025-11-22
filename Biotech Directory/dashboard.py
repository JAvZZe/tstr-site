#!/usr/bin/env python3
"""
TSTR.site Provider Database Dashboard
Shows pipeline statistics and funnel metrics
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.expanduser("~/memory/db/tstr.db")

def print_box(title, data, headers=None):
    """Print data in a nice box format"""
    if not data:
        print(f"No data for {title}")
        return
    
    # Calculate column widths
    if headers:
        widths = [len(str(h)) for h in headers]
    else:
        widths = [len(str(data[0][i])) for i in range(len(data[0]))]
    
    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    # Print header
    if headers:
        header_str = " │ ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))
        separator = "─┼─".join("─" * w for w in widths)
        print(f"┌─{separator}─┐")
        print(f"│ {header_str} │")
        print(f"├─{separator}─┤")
    else:
        separator = "─┼─".join("─" * w for w in widths)
        print(f"┌─{separator}─┐")
    
    # Print rows
    for row in data:
        row_str = " │ ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
        print(f"│ {row_str} │")
    
    print(f"└─{separator}─┘")

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clear screen
    os.system('clear')
    
    print("=" * 60)
    print("   TSTR.site | PROVIDER DATABASE DASHBOARD")
    print("=" * 60)
    print()
    
    # Total Leads
    cursor.execute("SELECT COUNT(*) FROM providers")
    total = cursor.fetchone()[0]
    print_box("TOTAL LEADS", [[total]], headers=["Count"])
    print()
    
    # Breakdown by Category
    print("--- Breakdown by Category ---")
    cursor.execute('''
        SELECT category, COUNT(*) as count 
        FROM providers 
        GROUP BY category 
        ORDER BY count DESC
    ''')
    categories = cursor.fetchall()
    print_box("Categories", categories, headers=["Category", "Count"])
    print()
    
    # Pipeline Status (The Funnel)
    print("--- Pipeline Status (The Funnel) ---")
    cursor.execute('''
        SELECT status, tier, COUNT(*) as count 
        FROM providers 
        GROUP BY status, tier 
        ORDER BY 
            CASE tier 
                WHEN 'partner' THEN 1 
                WHEN 'fast_track' THEN 2 
                WHEN 'free' THEN 3 
                ELSE 4 
            END,
            CASE status 
                WHEN 'sponsor' THEN 1 
                WHEN 'verified' THEN 2 
                WHEN 'claimed' THEN 3 
                WHEN 'contacted' THEN 4 
                WHEN 'unclaimed' THEN 5 
                ELSE 6 
            END
    ''')
    pipeline = cursor.fetchall()
    print_box("Pipeline", pipeline, headers=["Status", "Tier", "Count"])
    print()
    
    # Revenue Summary
    print("--- Revenue Summary ---")
    cursor.execute('''
        SELECT 
            tier,
            COUNT(*) as count,
            CASE 
                WHEN tier = 'fast_track' THEN COUNT(*) * 50
                WHEN tier = 'partner' THEN COUNT(*) * 250
                ELSE 0
            END as revenue
        FROM providers
        GROUP BY tier
    ''')
    revenue_data = cursor.fetchall()
    print_box("Revenue", revenue_data, headers=["Tier", "Count", "Revenue ($)"])
    
    # Calculate total revenue
    cursor.execute('''
        SELECT 
            SUM(CASE 
                WHEN tier = 'fast_track' THEN 50
                WHEN tier = 'partner' THEN 250
                ELSE 0
            END) as total_revenue
        FROM providers
    ''')
    total_revenue = cursor.fetchone()[0] or 0
    print(f"\n💰 Total Revenue: ${total_revenue:,}")
    print()
    
    # Recent Activity
    print("--- Recent Activity (Last 5 Actions) ---")
    cursor.execute('''
        SELECT 
            p.name,
            ol.action_type,
            ol.sentiment,
            datetime(ol.timestamp) as time
        FROM outreach_log ol
        JOIN providers p ON ol.provider_id = p.id
        ORDER BY ol.timestamp DESC
        LIMIT 5
    ''')
    recent = cursor.fetchall()
    if recent:
        print_box("Recent Actions", recent, headers=["Provider", "Action", "Sentiment", "Timestamp"])
    else:
        print("No activity logged yet.")
    print()
    
    # Next Actions Due
    print("--- Next Actions Due (Next 7 Days) ---")
    cursor.execute('''
        SELECT 
            p.name,
            ol.next_action_date,
            ol.email_sequence_number,
            ol.action_type
        FROM outreach_log ol
        JOIN providers p ON ol.provider_id = p.id
        WHERE ol.next_action_date >= date('now')
        AND ol.next_action_date <= date('now', '+7 days')
        ORDER BY ol.next_action_date ASC
    ''')
    next_actions = cursor.fetchall()
    if next_actions:
        print_box("Upcoming", next_actions, headers=["Provider", "Due Date", "Email #", "Last Action"])
    else:
        print("No pending actions in the next 7 days.")
    print()
    
    # Conversion Rates
    print("--- Conversion Metrics ---")
    cursor.execute('''
        SELECT 
            CAST(SUM(CASE WHEN status != 'unclaimed' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as contacted_rate,
            CAST(SUM(CASE WHEN status IN ('claimed', 'verified', 'sponsor') THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as claimed_rate,
            CAST(SUM(CASE WHEN status IN ('verified', 'sponsor') THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as verified_rate,
            CAST(SUM(CASE WHEN tier != 'free' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as paid_rate
        FROM providers
    ''')
    metrics = cursor.fetchone()
    
    print(f"📊 Contacted Rate:  {metrics[0]:.1f}%")
    print(f"📊 Claimed Rate:    {metrics[1]:.1f}%")
    print(f"📊 Verified Rate:   {metrics[2]:.1f}%")
    print(f"📊 Paid Tier Rate:  {metrics[3]:.1f}%")
    print()
    
    conn.close()
    
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

if __name__ == '__main__':
    main()
