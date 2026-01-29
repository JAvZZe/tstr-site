#!/usr/bin/env python3
"""
Debug script to inspect Contract Laboratory HTML structure
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def debug_contract_laboratory():
    """Fetch and inspect first page HTML"""

    base_url = 'https://www.contractlaboratory.com'
    directory_url = f'{base_url}/directory/laboratories/by-industry.cfm?i=45'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        print(f"Fetching: {directory_url}")
        page.goto(directory_url, wait_until='networkidle', timeout=30000)
        time.sleep(2)

        # Save raw HTML
        html = page.content()
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Saved raw HTML to debug_page.html")

        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Try multiple selectors
        print("\n" + "="*70)
        print("TESTING SELECTORS")
        print("="*70)

        # Test 1: Original selector
        cards1 = soup.find_all('div', class_='hp-vendor--view-block')
        print(f"\n1. div.hp-vendor--view-block: {len(cards1)} found")

        # Test 2: Any div with 'vendor' in class
        cards2 = soup.find_all('div', class_=lambda x: x and 'vendor' in x.lower())
        print(f"2. div[class*='vendor']: {len(cards2)} found")

        # Test 3: Look for lab names directly
        h3_tags = soup.find_all('h3')
        print(f"3. <h3> tags: {len(h3_tags)} found")
        if h3_tags:
            print(f"   First 3: {[h3.get_text(strip=True)[:50] for h3 in h3_tags[:3]]}")

        # Test 4: Look for links
        links = soup.find_all('a', href=True)
        print(f"4. <a href> tags: {len(links)} found")

        # Test 5: Inspect first card if found
        if cards1:
            print("\n" + "="*70)
            print("FIRST CARD INSPECTION (hp-vendor--view-block)")
            print("="*70)
            card = cards1[0]

            print("\nCard HTML structure:")
            print(card.prettify()[:1000])

            print("\n\nExtracting data from first card:")

            # Try to find name
            name_elem = card.find('h3') or card.find('h2') or card.find('a')
            print(f"Name element: {name_elem}")
            if name_elem:
                print(f"Name text: {name_elem.get_text(strip=True)}")

            # Try to find link
            link = card.find('a', href=True)
            print(f"Link element: {link}")
            if link:
                print(f"Link href: {link.get('href')}")

            # Show full text
            print(f"\nFull card text:\n{card.get_text()[:500]}")

        elif cards2:
            print("\n" + "="*70)
            print("FIRST CARD INSPECTION (div with 'vendor' class)")
            print("="*70)
            card = cards2[0]
            print(card.prettify()[:1000])

        else:
            print("\n⚠️  No cards found with any selector!")
            print("\nSaving full page HTML for manual inspection...")

        browser.close()

        print("\n" + "="*70)
        print("✓ Debug complete. Check debug_page.html for full source")
        print("="*70)

if __name__ == "__main__":
    debug_contract_laboratory()
