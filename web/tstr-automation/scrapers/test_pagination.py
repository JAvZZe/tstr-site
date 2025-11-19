#!/usr/bin/env python3
"""
Test if pagination actually changes content or shows same results
"""
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def test_pagination():
    base_url = 'https://www.contractlaboratory.com'
    directory_url = f'{base_url}/directory/laboratories/by-industry.cfm?i=45'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Headless for automation
        page = browser.new_page()

        # Page 1
        print("="*70)
        print("PAGE 1")
        print("="*70)
        page.goto(directory_url, wait_until='networkidle')
        time.sleep(3)

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        labs = soup.find_all('article', class_='hp-vendor--view-block')

        page1_names = []
        for lab in labs:
            name = lab.find('h4', class_='hp-vendor__name')
            if name:
                link = name.find('a')
                if link:
                    page1_names.append(link.get_text(strip=True))

        print(f"Found {len(page1_names)} labs:")
        for name in page1_names[:5]:
            print(f"  - {name}")

        # Try clicking next button
        print("\n" + "="*70)
        print("CLICKING NEXT PAGE BUTTON")
        print("="*70)

        # Look for pagination next button
        try:
            next_button = page.locator('a.page-link:has-text("›")').first
            if next_button:
                print("Found next button, clicking...")
                next_button.click()
                time.sleep(5)

                html2 = page.content()
                soup2 = BeautifulSoup(html2, 'html.parser')
                labs2 = soup2.find_all('article', class_='hp-vendor--view-block')

                page2_names = []
                for lab in labs2:
                    name = lab.find('h4', class_='hp-vendor__name')
                    if name:
                        link = name.find('a')
                        if link:
                            page2_names.append(link.get_text(strip=True))

                print(f"Found {len(page2_names)} labs:")
                for name in page2_names[:5]:
                    print(f"  - {name}")

                # Compare
                print("\n" + "="*70)
                print("COMPARISON")
                print("="*70)
                if page1_names == page2_names:
                    print("❌ SAME RESULTS - Pagination not working!")
                else:
                    print("✅ DIFFERENT RESULTS - Pagination works!")
                    print(f"Page 1 unique: {set(page1_names) - set(page2_names)}")
                    print(f"Page 2 unique: {set(page2_names) - set(page1_names)}")
        except Exception as e:
            print(f"Error clicking next: {e}")

        browser.close()

if __name__ == "__main__":
    test_pagination()
