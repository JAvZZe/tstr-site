#!/usr/bin/env python3
"""
Oil & Gas Testing Scraper using Playwright (bypasses Cloudflare)
Scrapes Contract Laboratory petroleum testing directory
"""

import os
import sys
import time
import re
import logging
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def generate_slug(name):
    """Generate URL-safe slug from business name"""
    if not name:
        return ''
    # Convert to lowercase, remove special chars, replace spaces with hyphens
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s]+', '-', slug)
    slug = slug.strip('-')
    return slug or 'unnamed'


def scrape_contract_laboratory(dry_run=False, limit=None):
    """
    Scrape petroleum testing labs from Contract Laboratory using Playwright

    Args:
        dry_run: If True, parse but don't save to database
        limit: Max number of listings to scrape (for testing)

    Returns:
        List of scraped listing dictionaries
    """

    # Initialize Supabase
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not supabase_url or not supabase_key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")

    supabase = create_client(supabase_url, supabase_key)

    # Get category ID for oil-gas-testing
    category_result = supabase.table('categories').select('id').eq('slug', 'oil-gas-testing').execute()
    if not category_result.data:
        raise ValueError("Category 'oil-gas-testing' not found in database")
    category_id = category_result.data[0]['id']
    logger.info(f"Category ID: {category_id}")

    listings = []
    base_url = 'https://www.contractlaboratory.com'
    directory_url = f'{base_url}/directory/laboratories/by-industry.cfm?i=45'

    with sync_playwright() as p:
        # Launch browser (headless=True for production, False for debugging)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()

        # Scrape paginated directory
        for page_num in range(1, 16):  # 15 pages total
            if limit and len(listings) >= limit:
                break

            if page_num == 1:
                url = directory_url
            else:
                url = f'{directory_url}/page/{page_num}/?_sort=featured_vendor__desc'

            logger.info(f"Fetching page {page_num}: {url}")

            try:
                # Navigate to page
                page.goto(url, wait_until='networkidle', timeout=30000)
                time.sleep(2)  # Give time for JS to render

                # Get page HTML
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')

                # Find lab cards - try multiple selectors
                lab_cards = soup.find_all('div', class_='hp-vendor--view-block')
                if not lab_cards:
                    # Try alternative selector
                    lab_cards = soup.find_all('div', class_=lambda x: x and 'vendor' in x.lower())

                logger.info(f"Found {len(lab_cards)} labs on page {page_num}")

                for card in lab_cards:
                    if limit and len(listings) >= limit:
                        break

                    try:
                        # Extract basic info from card
                        name_elem = card.find('h3') or card.find('h2') or card.find('a')
                        if not name_elem:
                            continue

                        business_name = name_elem.get_text(strip=True)

                        # Extract profile link
                        link = card.find('a', href=True)
                        profile_url = None
                        if link:
                            profile_url = link['href']
                            if profile_url.startswith('/'):
                                profile_url = f'{base_url}{profile_url}'

                        # Extract address from card
                        address_text = card.get_text()
                        # Simple address extraction (can be improved)
                        address = None
                        for line in address_text.split('\n'):
                            line = line.strip()
                            if ',' in line and len(line) > 10:
                                address = line
                                break

                        listing = {
                            'business_name': business_name,
                            'slug': generate_slug(business_name),
                            'address': address,
                            'website': profile_url,
                            'category_id': category_id,
                            'location_id': 'aac4019b-7e93-4aec-ba55-150103da7d6f',  # Global location (default)
                            'status': 'pending',
                            'verified': False,
                            'claimed': False
                        }

                        listings.append(listing)
                        logger.info(f"Scraped: {business_name}")

                    except Exception as e:
                        logger.error(f"Error extracting lab from card: {e}")
                        continue

                # Rate limiting
                time.sleep(2)

            except Exception as e:
                logger.error(f"Error fetching page {page_num}: {e}")
                continue

        browser.close()

    logger.info(f"\n{'='*70}")
    logger.info(f"SCRAPING COMPLETE")
    logger.info(f"Total listings scraped: {len(listings)}")
    logger.info(f"{'='*70}\n")

    # Save to database if not dry run
    if not dry_run and listings:
        logger.info("Saving to Supabase...")
        saved_count = 0
        duplicate_count = 0

        for listing in listings:
            try:
                # Check for duplicates
                existing = supabase.table('listings')\
                    .select('id')\
                    .eq('business_name', listing['business_name'])\
                    .execute()

                if existing.data:
                    logger.info(f"Duplicate skipped: {listing['business_name']}")
                    duplicate_count += 1
                    continue

                # Insert listing
                result = supabase.table('listings').insert(listing).execute()
                saved_count += 1
                logger.info(f"Saved: {listing['business_name']}")

            except Exception as e:
                logger.error(f"Error saving {listing['business_name']}: {e}")

        logger.info(f"\nSaved: {saved_count}, Duplicates: {duplicate_count}")

    return listings


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Oil & Gas Testing Scraper (Playwright)')
    parser.add_argument('--dry-run', action='store_true', help='Parse but don\'t save to database')
    parser.add_argument('--limit', type=int, help='Limit number of listings to scrape')

    args = parser.parse_args()

    scrape_contract_laboratory(dry_run=args.dry_run, limit=args.limit)
