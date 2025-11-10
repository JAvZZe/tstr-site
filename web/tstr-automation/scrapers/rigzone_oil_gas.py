#!/usr/bin/env python3
"""
Rigzone Oil & Gas Testing Scraper
Extracts testing laboratories and inspection services from Rigzone directory
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


class RigzoneOilGasScraper(BaseNicheScraper):
    """
    Scraper for Oil & Gas testing and inspection companies from Rigzone

    Custom Fields Extracted:
    - testing_types: Well Logging, Production Testing, Flow Assurance, etc.
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
            source_name='Rigzone Directory',
            rate_limit_seconds=2.0
        )

        # Keyword mapping for testing types
        self.testing_type_keywords = {
            'Well Logging': [
                'well logging', 'wireline', 'formation evaluation',
                'downhole logging', 'electric logging'
            ],
            'Production Testing': [
                'production testing', 'well testing', 'flow testing',
                'well performance', 'productivity testing'
            ],
            'Flow Assurance': [
                'flow assurance', 'multiphase', 'pipeline flow',
                'flow measurement', 'hydraulic analysis'
            ],
            'Pressure Testing': [
                'pressure test', 'hydrostatic', 'pressure vessel',
                'pneumatic test', 'leak detection', 'hydro-test'
            ],
            'NDT Inspection': [
                'ndt', 'non-destructive', 'ultrasonic', 'radiographic',
                'magnetic particle', 'eddy current', 'visual inspection'
            ],
            'Pipeline Inspection': [
                'pipeline inspection', 'in-line inspection', 'pig inspection',
                'pipeline integrity', 'corrosion inspection'
            ]
        }

        # Certification patterns
        self.certification_patterns = {
            'API': r'\bAPI[\s-]?\d*\b',
            'ISO 17025': r'\bISO[\s-]?17025\b',
            'ASME': r'\bASME\b',
            'ISO 9001': r'\bISO[\s-]?9001\b',
            'NACE': r'\bNACE\b'
        }

        # Equipment brand keywords
        self.equipment_brands = [
            'schlumberger', 'halliburton', 'weatherford', 'baker hughes',
            'oceaneering', 'technip', 'subsea 7', 'aker solutions'
        ]

    def get_listing_urls(self) -> List[str]:
        """
        Return list of company URLs to scrape

        For initial implementation, using known testing/inspection companies
        Future: Implement search/pagination to discover more
        """
        # Seed list from web search results
        seed_urls = [
            'https://www.rigzone.com/directory/company/20421/3iInternationalInspectingInc/',
            'https://www.rigzone.com/directory/company/3395/AlphaPipelineIntegrityServices/',
            'https://www.rigzone.com/directory/company/11110/QualityProcessServicesLLC/',
            'https://www.rigzone.com/directory/company/21603/PROMETRICEngineeringandInspectionServices/',
            'https://www.rigzone.com/directory/company/3563/CECOPipelineServicesCompanyInc/',
        ]

        logger.info(f"Using {len(seed_urls)} seed URLs for testing")
        return seed_urls

    def extract_standard_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract standard listing fields from Rigzone company profile

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

        # Extract company name from h1 or page header
        name_elem = soup.find('h1')
        if name_elem:
            fields['business_name'] = name_elem.get_text(strip=True)

        # Extract address (usually in a paragraph or contact section)
        # Pattern: "Address Line, City, State Zip"
        address_text = soup.get_text()
        address_match = re.search(r'(\d+[^,]+,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5})', address_text)
        if address_match:
            fields['address'] = address_match.group(1).strip()

        # Extract phone numbers (look for patterns like 281-334-5865)
        phone_match = re.search(r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', address_text)
        if phone_match:
            fields['phone'] = phone_match.group(1)

        # Extract website
        website_link = soup.find('a', href=re.compile(r'^http'))
        if website_link:
            href = website_link.get('href', '')
            # Skip Rigzone's own links
            if 'rigzone.com' not in href.lower():
                fields['website'] = href

        # Extract description (paragraph about company services)
        # Look for paragraphs containing service descriptions
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            # Description paragraphs are usually longer and contain service keywords
            if len(text) > 100 and any(kw in text.lower() for kw in ['service', 'testing', 'inspection', 'consulting']):
                fields['description'] = text
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
    """Test the Rigzone Oil & Gas scraper"""
    import argparse

    parser = argparse.ArgumentParser(description='Rigzone Oil & Gas Testing Scraper')
    parser.add_argument('--limit', type=int, help='Limit number of listings to scrape')
    parser.add_argument('--dry-run', action='store_true', help='Parse but don\'t save to database')

    args = parser.parse_args()

    scraper = RigzoneOilGasScraper()
    scraper.run(limit=args.limit, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
