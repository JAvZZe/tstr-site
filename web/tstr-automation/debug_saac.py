from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def scrape_saac():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Fetching SAAC page...")
        page.goto("https://saac.gov.sa/en/accredited-cabs/", wait_until="networkidle")
        time.sleep(5) # Wait for table load
        
        content = page.content()
        soup = BeautifulSoup(content, "html.parser")
        
        # Find table rows
        rows = soup.find_all("tr")
        print(f"Found {len(rows)} rows")
        
        for row in rows[1:5]: # Header + first 4
            cols = row.find_all("td")
            if cols:
                name = cols[1].get_text(strip=True)
                show_btn = cols[-1]
                link = show_btn.find("a")
                href = link.get("href") if link else "No link"
                print(f"Lab: {name} | Link: {href}")
        
        browser.close()

if __name__ == "__main__":
    scrape_saac()
