#!/usr/bin/env python3
"""
Contract Laboratory Oil & Gas Testing Scraper
Extracts petroleum testing laboratories from Contract Laboratory directory
Source: https://www.contractlaboratory.com/directory/laboratories/by-industry.cfm?i=45
"""

import re
import logging
from typing import Dict, List, Optional
from bs4 import BeautifulSoup

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_scraper import BaseNicheScraper

logger = logging.getLogger(__name__)


class ContractLabOilGasScraper(BaseNicheScraper):
    """
    Scraper for petroleum testing laboratories from Contract Laboratory directory

    Source: 170 petroleum testing labs across 15 pages
    URL pattern: /directory/laboratories/by-industry.cfm?i=45/page/[n]/?_sort=featured_vendor__desc

    Custom Fields Extracted:
    - testing_types: Petroleum Testing, Chemical Analysis, NDT Inspection, etc.
    - real_time_analytics: Boolean for real-time monitoring capabilities
    - equipment_brands: Text description of equipment used
    - coverage_type: Onshore, Offshore, or Both
    - certifications: API, ISO 17025, ASME, etc.
    - rapid_deployment: Boolean for 24/7 emergency services
    - recent_projects: Text description of recent work
    """

    def __init__(self):
        super().__init__(
            category_slug='oil-gas-testing',
            source_name='Contract Laboratory Directory',
            rate_limit_seconds=2.0
        )

        self.base_url = 'https://www.contractlaboratory.com'
        self.directory_url = f'{self.base_url}/directory/laboratories/by-industry.cfm?i=45'

        # Keyword mapping for testing types
        self.testing_type_keywords = {
            'Petroleum Testing': [
                'petroleum', 'crude oil', 'fuel', 'gasoline', 'diesel',
                'octane', 'cetane', 'distillation'
            ],
            'Chemical Analysis': [
                'chemical analysis', 'composition', 'chromatography', 'spectroscopy',
                'elemental analysis', 'gcms', 'lcms'
            ],
            'NDT Inspection': [
                'ndt', 'non-destructive', 'ultrasonic', 'radiographic',
                'magnetic particle', 'eddy current', 'visual inspection'
            ],
            'Pipeline Inspection': [
                'pipeline inspection', 'in-line inspection', 'pig inspection',
                'pipeline integrity', 'corrosion inspection'
            ],
            'Pressure Testing': [
                'pressure test', 'hydrostatic', 'pressure vessel',
                'pneumatic test', 'leak detection'
            ]
        }

        # Certification patterns
        self.certification_patterns = {
            'API': r'\bAPI[\s-]?\d*\b',
            'ISO 17025': r'\bISO[\s-]?17025\b',
            'ASME': r'\bASME\b',
            'ISO 9001': r'\bISO[\s-]?9001\b',
            'ASTM': r'\bASTM\b'
        }

        # Equipment brand keywords
        self.equipment_brands = [
            'agilent', 'perkinelmer', 'thermo fisher', 'shimadzu',
            'waters', 'bruker', 'varian'
        ]

    def get_listing_urls(self) -> List[str]:
        """
        Scrape pagination from Contract Laboratory directory

        Returns list of individual lab profile URLs
        Total: ~170 labs across 15 pages (12 per page)
        """
        listing_urls = []

        # Scrape all 15 pages
        for page_num in range(1, 16):  # Pages 1-15
            if page_num == 1:
                page_url = self.directory_url
            else:
                page_url = f'{self.directory_url}/page/{page_num}/?_sort=featured_vendor__desc'

            logger.info(f"Fetching page {page_num}: {page_url}")

            try:
                response = self.session.get(page_url, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all lab cards with class "hp-vendor--view-block"
                lab_cards = soup.find_all('div', class_='hp-vendor--view-block')

                for card in lab_cards:
                    # Find the profile link
                    link_elem = card.find('a', href=True)
                    if link_elem:
                        profile_url = link_elem['href']
                        # Convert relative URL to absolute
                        if profile_url.startswith('/'):
                            profile_url = f'{self.base_url}{profile_url}'
                        listing_urls.append(profile_url)

                logger.info(f"Found {len(lab_cards)} labs on page {page_num}")

                # Rate limiting
                self._rate_limit(self.base_url)

            except Exception as e:
                logger.error(f"Error fetching page {page_num}: {e}")
                continue

        logger.info(f"Total labs found: {len(listing_urls)}")
        return listing_urls

    def extract_standard_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract standard listing fields from Contract Laboratory profile page

        Args:
            soup: BeautifulSoup parsed HTML
            url: Source URL

        Returns:
            Dict with standard fields
        """
        fields = {
            'business_name': '',
            'description': '',
            'address': '',
            'location_id': None,
            'phone': '',
            'email': '',
            'website': '',
            'latitude': None,
            'longitude': None
        }

        # Extract company name from h1 or title
        name_elem = soup.find('h1')
        if name_elem:
            fields['business_name'] = name_elem.get_text(strip=True)
        else:
            # Fallback: try meta title or page title
            title_elem = soup.find('title')
            if title_elem:
                # Clean up title (remove " - Contract Laboratory")
                title_text = title_elem.get_text(strip=True)
                fields['business_name'] = title_text.split(' - ')[0].strip()

        # Extract address from structured data or contact section
        # Contract Laboratory typically has address in schema.org markup or visible text
        page_text = soup.get_text()

        # Try to find address with common US/international patterns
        # Pattern 1: "123 Main St, City, State ZIP, Country"
        address_patterns = [
            r'(\d+[^,]+,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?)',  # US: 123 St, City, ST 12345
            r'([A-Z][^,\n]+,\s*[A-Z][a-z\s]+,\s*[A-Z]{2,3}\s+\d[\w\s-]+)',  # Intl: St, City, Country Code
        ]

        for pattern in address_patterns:
            address_match = re.search(pattern, page_text)
            if address_match:
                fields['address'] = address_match.group(1).strip()
                break

        # If no structured address found, look for location text near labels
        if not fields['address']:
            # Look for text after "Address:", "Location:", etc.
            location_section = re.search(r'(?:Address|Location):\s*([^\n]+(?:\n[^\n]+){0,2})', page_text, re.IGNORECASE)
            if location_section:
                fields['address'] = location_section.group(1).strip()

        # Extract phone (various formats)
        phone_patterns = [
            r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US: (123) 456-7890
            r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # Intl: +1-234-567-8900
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, page_text)
            if phone_match:
                fields['phone'] = phone_match.group(0).strip()
                break

        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', page_text)
        if email_match:
            fields['email'] = email_match.group(0)

        # Extract website
        # Look for links that are NOT contractlaboratory.com
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href.startswith('http') and 'contractlaboratory.com' not in href.lower():
                # Likely the lab's own website
                fields['website'] = href
                break

        # Extract description from "About" or "Services" section
        # Contract Laboratory profiles usually have a description paragraph
        description_keywords = ['about', 'services', 'capabilities', 'testing', 'laboratory']
        for heading in soup.find_all(['h2', 'h3', 'h4', 'strong', 'b']):
            heading_text = heading.get_text(strip=True).lower()
            if any(kw in heading_text for kw in description_keywords):
                # Get following paragraph or div
                next_elem = heading.find_next(['p', 'div'])
                if next_elem:
                    desc_text = next_elem.get_text(strip=True)
                    if len(desc_text) > 50:
                        fields['description'] = desc_text[:1000]  # Limit to 1000 chars
                        break

        # Fallback: first substantial paragraph
        if not fields['description']:
            for p in soup.find_all('p'):
                text = p.get_text(strip=True)
                if len(text) > 100:
                    fields['description'] = text[:1000]
                    break

        # Use location_parser to get location_id
        if fields['address']:
            fields['location_id'] = self.location_parser.parse_and_link(
                address=fields['address'],
                latitude=fields['latitude'],
                longitude=fields['longitude']
            )

        return fields

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract Oil & Gas specific custom fields

        Args:
            soup: BeautifulSoup parsed HTML
            url: Source URL

        Returns:
            Dict with custom field values
        """
        # Get full page text for keyword matching
        page_text = soup.get_text().lower()

        custom_fields = {}

        # 1. Extract testing_types
        testing_types = []
        for test_type, keywords in self.testing_type_keywords.items():
            if any(kw in page_text for kw in keywords):
                testing_types.append(test_type)

        if testing_types:
            custom_fields['testing_types'] = testing_types

        # 2. Check for real_time_analytics
        real_time_keywords = [
            'real-time', 'real time', 'live monitoring', 'remote monitoring',
            'online monitoring', 'continuous monitoring'
        ]
        custom_fields['real_time_analytics'] = any(kw in page_text for kw in real_time_keywords)

        # 3. Extract equipment_brands
        found_brands = []
        for brand in self.equipment_brands:
            if brand.lower() in page_text:
                found_brands.append(brand.title())

        if found_brands:
            custom_fields['equipment_brands'] = ', '.join(found_brands)

        # 4. Determine coverage_type (onshore, offshore, both)
        has_offshore = any(kw in page_text for kw in ['offshore', 'subsea', 'deepwater', 'platform'])
        has_onshore = any(kw in page_text for kw in ['onshore', 'land', 'pipeline', 'field'])

        coverage = []
        if has_offshore:
            coverage.append('Offshore')
        if has_onshore:
            coverage.append('Onshore')
        if has_offshore and has_onshore:
            coverage = ['Both']

        if coverage:
            custom_fields['coverage_type'] = coverage

        # 5. Extract certifications
        certifications = []
        for cert_name, pattern in self.certification_patterns.items():
            if re.search(pattern, page_text, re.IGNORECASE):
                certifications.append(cert_name)

        if certifications:
            custom_fields['certifications'] = certifications

        # 6. Check for rapid_deployment capability
        rapid_keywords = [
            'rapid', '24/7', '24-7', 'emergency', 'immediate response',
            'quick response', 'expedited', 'fast deployment'
        ]
        custom_fields['rapid_deployment'] = any(kw in page_text for kw in rapid_keywords)

        # 7. Extract recent_projects (if mentioned)
        # Look for section headers about projects, clients, or experience
        recent_projects = None
        for heading in soup.find_all(['h2', 'h3', 'h4', 'strong']):
            heading_text = heading.get_text(strip=True).lower()
            if any(kw in heading_text for kw in ['project', 'client', 'experience', 'recent work']):
                # Get text from following sibling
                next_elem = heading.find_next_sibling(['p', 'ul', 'div'])
                if next_elem:
                    project_text = next_elem.get_text(strip=True)
                    if len(project_text) > 50:
                        recent_projects = project_text[:500]  # Limit to 500 chars
                        break

        if recent_projects:
            custom_fields['recent_projects'] = recent_projects

        return custom_fields


def main():
    """Run the Contract Laboratory Oil & Gas scraper"""
    import argparse

    parser = argparse.ArgumentParser(description='Contract Laboratory Oil & Gas Testing Scraper')
    parser.add_argument('--limit', type=int, help='Limit number of listings to scrape')
    parser.add_argument('--dry-run', action='store_true', help='Parse but don\'t save to database')

    args = parser.parse_args()

    scraper = ContractLabOilGasScraper()
    scraper.run(limit=args.limit, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
