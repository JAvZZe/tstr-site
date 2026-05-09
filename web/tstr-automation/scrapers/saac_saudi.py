#!/usr/bin/env python3
# ruff: noqa: E402
"""
SAC (Saudi Accreditation Center) Scraper
Standardized to use BaseNicheScraper architecture.
Extracts accredited labs in Saudi Arabia.
Source: https://saac.gov.sa/en/accredited-cabs/
"""

import os
import sys
import logging
import re
import time
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_scraper import BaseNicheScraper

logger = logging.getLogger(__name__)


class SACSaudiScraper(BaseNicheScraper):
    """
    Scraper for Saudi accredited labs from SAAC
    """

    def __init__(self, dry_run: bool = False):
        super().__init__(
            category_slug="materials-testing", 
            source_name="SAC Saudi Arabia",
            rate_limit_seconds=3.0,
            dry_run=dry_run
        )
        self.base_url = "https://saac.gov.sa"
        self.directory_url = "https://saac.gov.sa/en/accredited-cabs/"

    def get_listing_urls(self, limit: Optional[int] = None) -> List[str]:
        """
        Use Playwright to crawl the dynamic table and extract detail URLs
        """
        listing_urls = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()

            logger.info(f"Fetching SAC directory: {self.directory_url}")
            try:
                page.goto(self.directory_url, wait_until="load", timeout=120000)
                # Wait for the table to populate
                page.wait_for_selector("table", timeout=60000)
                time.sleep(10) # Extra buffer for AJAX

                # Scrape current page
                content = page.content()
                soup = BeautifulSoup(content, "html.parser")
                
                rows = soup.find_all("tr")[1:] # Skip header
                for row in rows:
                    if limit and len(listing_urls) >= limit:
                        break
                        
                    cols = row.find_all("td")
                    if not cols:
                        continue
                    
                    # Look for the 'Show' button/link
                    show_btn = cols[-1].find("a")
                    if show_btn:
                        href = show_btn.get("href", "")
                        if "appid=" in href:
                            if not href.startswith("http"):
                                href = f"{self.base_url}{href}"
                            listing_urls.append(href)
                
                logger.info(f"Found {len(listing_urls)} labs on the first page")

            except Exception as e:
                logger.error(f"Error fetching SAC directory: {e}")
            
            browser.close()
            
        return listing_urls

    def scrape_listing(self, url: str) -> bool:
        """
        Scrape rich detail page for a Saudi lab
        """
        logger.info(f"Scraping detail page: {url}")
        
        # Detail pages seem to be dynamic too
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                time.sleep(3)
                
                content = page.content()
                soup = BeautifulSoup(content, "html.parser")
                
                # Extract fields
                # Typically data is in a table or definition list
                name_elem = soup.find("h2") or soup.find("h1")
                name = name_elem.get_text(strip=True) if name_elem else "Unknown Lab"
                
                standard_fields = {
                    "business_name": name,
                    "description": f"SAC Accredited Laboratory in Saudi Arabia. {name}",
                    "website": url,
                    "phone": "",
                    "email": "",
                    "address": "Saudi Arabia" # Default
                }

                # Extract address from the rich table if present
                # Highlights showed: | Kingdom of Saudi Arabia | 13213 - 2190 Riyadh... |
                address_row = soup.find("td", string=re.compile(r"Riyadh|Jeddah|Dammam|Saudi", re.I))
                if address_row:
                    addr = address_row.get_text(strip=True)
                    standard_fields["address"] = addr
                    if self.location_parser:
                        standard_fields["location_id"] = self.location_parser.parse_and_link(addr)

                # Extract custom fields
                custom_fields = {}
                cert_match = re.search(r"appid=([^&]+)", url)
                if cert_match:
                    custom_fields["cert_number"] = cert_match.group(1)
                
                custom_fields["accreditation_body"] = "SAC"
                
                # Try to extract more from table
                tables = soup.find_all("table")
                if tables:
                    # Look for classification or specification
                    text = tables[0].get_text()
                    if "ISO" in text:
                        custom_fields["test_procedures"] = "ISO/IEC 17025"

                self.save_listing(standard_fields, custom_fields, url)
                browser.close()
                return True
                
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
                browser.close()
                return False

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        return {}


def main():
    import argparse
    parser = argparse.ArgumentParser(description='SAC Saudi Arabia Scraper')
    parser.add_argument('--limit', type=int, default=5, help='Limit labs')
    parser.add_argument('--dry-run', action='store_true', help='Dry run')
    args = parser.parse_args()

    scraper = SACSaudiScraper(dry_run=args.dry_run)
    scraper.run(limit=args.limit)

if __name__ == "__main__":
    main()
