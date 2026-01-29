#!/usr/bin/env python3
"""
A2LA Materials Testing Scraper
Extracts ISO/IEC 17025 accredited materials testing laboratories from A2LA directory
"""

import re
import logging
from typing import Dict, List
from bs4 import BeautifulSoup
from urllib.parse import urlencode

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_scraper import BaseNicheScraper

logger = logging.getLogger(__name__)


class A2LAMaterialsScraper(BaseNicheScraper):
    """
    Scraper for Materials Testing laboratories from A2LA Directory

    Custom Fields Extracted:
    - material_types: Metals, Polymers, Composites, Nanomaterials, Ceramics
    - test_procedures: Tensile Testing, Fatigue Testing, Corrosion Testing, Hardness Testing, Failure Analysis
    - instrumentation: Text description of equipment/instruments
    - industry_sectors: Aerospace, Automotive, Semiconductor, Medical Device
    - custom_test_dev: Boolean for custom test development capability
    - rd_capabilities: Text description of R&D capabilities
    - project_lead_time: Same Day, 1-3 Days, 1 Week, 2-4 Weeks, 1+ Month
    """

    def __init__(self):
        super().__init__(
            category_slug='materials-testing',
            source_name='A2LA Directory',
            rate_limit_seconds=2.0
        )

        self.base_search_url = 'https://customer.a2la.org/index.cfm'

        # Keyword mapping for material types
        self.material_type_keywords = {
            'Metals': [
                'metal', 'steel', 'aluminum', 'alloy', 'copper', 'titanium',
                'iron', 'brass', 'bronze', 'stainless', 'metallurgy', 'metallographic'
            ],
            'Polymers': [
                'polymer', 'plastic', 'elastomer', 'rubber', 'resin',
                'thermoplastic', 'thermoset', 'composite polymer', 'pvc', 'polyethylene'
            ],
            'Composites': [
                'composite', 'fiber reinforced', 'carbon fiber', 'fiberglass',
                'laminate', 'frp', 'cfrp', 'gfrp', 'sandwich structure'
            ],
            'Nanomaterials': [
                'nanomaterial', 'nanoparticle', 'nanotechnology', 'nano-',
                'graphene', 'carbon nanotube', 'quantum dot', 'nanocomposite'
            ],
            'Ceramics': [
                'ceramic', 'glass', 'refractory', 'porcelain', 'oxide',
                'carbide', 'nitride', 'silicate', 'clay'
            ]
        }

        # Test procedure keywords
        self.test_procedure_keywords = {
            'Tensile Testing': [
                'tensile', 'tension test', 'ultimate strength', 'yield strength',
                'elongation', 'astm e8', 'astm d638', 'pull test'
            ],
            'Fatigue Testing': [
                'fatigue', 'cyclic', 'endurance test', 'stress cycle',
                'fatigue life', 'fatigue crack', 's-n curve', 'astm e466'
            ],
            'Corrosion Testing': [
                'corrosion', 'salt spray', 'electrochemical', 'rust',
                'oxidation', 'astm b117', 'astm g48', 'pitting', 'crevice corrosion'
            ],
            'Hardness Testing': [
                'hardness', 'rockwell', 'brinell', 'vickers', 'knoop',
                'shore', 'durometer', 'astm e18', 'astm d2240', 'indentation'
            ],
            'Failure Analysis': [
                'failure analysis', 'root cause', 'fractography', 'sem analysis',
                'failure investigation', 'defect analysis', 'metallography'
            ]
        }

        # Industry sector keywords
        self.industry_sector_keywords = {
            'Aerospace': [
                'aerospace', 'aviation', 'aircraft', 'space', 'aeronautical',
                'nadcap', 'as9100', 'mil-spec', 'aerospace materials'
            ],
            'Automotive': [
                'automotive', 'automobile', 'vehicle', 'iatf 16949',
                'automotive components', 'car', 'truck', 'aiag'
            ],
            'Semiconductor': [
                'semiconductor', 'microelectronics', 'chip', 'wafer',
                'integrated circuit', 'cleanroom', 'pcb', 'electronic assembly'
            ],
            'Medical Device': [
                'medical device', 'biomedical', 'implant', 'surgical',
                'fda', 'iso 13485', 'medical grade', 'biocompatibility'
            ]
        }

        # Custom test development keywords
        self.custom_test_keywords = [
            'custom test', 'test development', 'r&d', 'research and development',
            'method development', 'custom method', 'test protocol development',
            'bespoke testing', 'specialized testing', 'proprietary test'
        ]

        # R&D capability keywords
        self.rd_keywords = [
            'research', 'development', 'innovation', 'prototype',
            'consulting', 'engineering support', 'technical consulting',
            'material characterization', 'material selection'
        ]

        # Lead time patterns
        self.lead_time_patterns = {
            'Same Day': r'same\s+day|24\s*hour|rush|emergency|immediate',
            '1-3 Days': r'1-3\s+days?|2-3\s+days?|within\s+72\s+hours?',
            '1 Week': r'1\s+week|one\s+week|5-7\s+days?|within\s+a\s+week',
            '2-4 Weeks': r'2-4\s+weeks?|2\s+to\s+4\s+weeks?|standard\s+turnaround',
            '1+ Month': r'1\+?\s+months?|4-6\s+weeks?|extended\s+turnaround'
        }

        # Program IDs for materials testing (ISO/IEC 17025)
        self.materials_program_ids = [
            '23',  # Construction Materials Field of Testing
            '60',  # Mechanical Field of Testing
            '14',  # Chemical Field of Testing
            '65',  # Nondestructive Field of Testing
        ]

    def get_listing_urls(self) -> List[str]:
        """
        Get list of lab detail URLs

        Note: A2LA directory uses AJAX/JavaScript for search results, making it difficult
        to scrape dynamically. Using a seed list of known materials testing labs
        found via web search and A2LA directory.

        Future enhancement: Implement Selenium/Playwright for JS-rendered content
        """
        # Load PIDs from external file (64 labs collected via research)
        seed_pids_file = os.path.join(os.path.dirname(__file__), 'a2la', 'a2la_pids_final.txt')

        seed_lab_pids = []
        if os.path.exists(seed_pids_file):
            with open(seed_pids_file, 'r') as f:
                seed_lab_pids = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(seed_lab_pids)} PIDs from {seed_pids_file}")
        else:
            # Fallback to hardcoded seed list
            logger.warning(f"Seed file not found: {seed_pids_file}")
            seed_lab_pids = [
                '37384671-0AE3-4471-BAAD-D1EF6BA0B2A0',  # ICS Laboratories, Inc. - Mechanical Testing
            ]

        listing_urls = []
        for lab_pid in seed_lab_pids:
            url = f"https://customer.a2la.org/index.cfm?event=directory.detail&labPID={lab_pid}"
            listing_urls.append(url)

        logger.info(f"Using {len(listing_urls)} seed lab URLs")
        logger.info("Note: A2LA uses AJAX for directory search. Additional labs require Selenium/Playwright.")
        return listing_urls

    def _search_by_keyword(self, keyword: str) -> List[str]:
        """
        Execute search for specific keyword and extract result URLs

        Args:
            keyword: Search term

        Returns:
            List of lab detail URLs
        """
        # Build search URL (using GET parameters based on form structure)
        search_params = {
            'event': 'directory.index',
            'keyword': keyword,
        }

        search_url = f"{self.base_search_url}?{urlencode(search_params)}"

        try:
            # Fetch search results page
            soup = self.fetch_page(search_url)
            if not soup:
                logger.warning(f"Failed to fetch search results for: {keyword}")
                return []

            # Extract lab detail URLs from results table
            # Results are in table with cert numbers linking to detail pages
            urls = []

            # Look for links to lab details (pattern: ?event=directory.detail&labid=XXXX)
            detail_links = soup.find_all('a', href=re.compile(r'event=directory\.detail'))

            for link in detail_links:
                href = link.get('href', '')

                # Construct full URL if relative
                if href.startswith('?'):
                    full_url = f"{self.base_search_url}{href}"
                elif not href.startswith('http'):
                    full_url = f"https://customer.a2la.org/{href}"
                else:
                    full_url = href

                urls.append(full_url)

            logger.info(f"  Found {len(urls)} labs for keyword: {keyword}")
            return urls

        except Exception as e:
            logger.error(f"Error searching for '{keyword}': {e}")
            return []

    def extract_standard_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract standard listing fields from A2LA lab detail page

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

        # Extract organization name from structured field
        org_name_field = soup.find('label', string=re.compile(r'Organization Name:', re.I))
        if org_name_field:
            org_name_p = org_name_field.find_next('p', class_='form-control-static')
            if org_name_p:
                fields['business_name'] = org_name_p.get_text(strip=True)

        # Extract website from structured field
        web_field = soup.find('label', string=re.compile(r'Web:', re.I))
        if web_field:
            web_link = web_field.find_next('a', href=True)
            if web_link:
                fields['website'] = web_link.get('href', '').strip()

        # Extract address from structured field
        address_field = soup.find('label', string=re.compile(r'Address:', re.I))
        if address_field:
            address_link = address_field.find_next('a', href=re.compile(r'google.com/maps'))
            if address_link:
                # Address is in the link text (multi-line)
                address_parts = []
                for content in address_link.stripped_strings:
                    if 'fa-map-marker' not in content:  # Skip icon text
                        address_parts.append(content)
                if address_parts:
                    fields['address'] = ', '.join(address_parts)

        # Extract contact information
        contact_field = soup.find('label', string=re.compile(r'Contact\(s\):', re.I))
        if contact_field:
            contact_div = contact_field.find_next('div')
            if contact_div:
                contact_text = contact_div.get_text()

                # Extract email
                email_match = re.search(r'email:?\s*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})', contact_text, re.I)
                if email_match:
                    fields['email'] = email_match.group(1).strip()

                # Extract phone
                phone_match = re.search(r'phone:?\s*([\d\s\-\(\)]+)', contact_text, re.I)
                if phone_match:
                    fields['phone'] = phone_match.group(1).strip()

        # Extract description from accreditation information
        description_parts = []

        # Get all accreditation sections (certificates)
        cert_headers = soup.find_all('h4', string=re.compile(r'^\d+\.\d+:'))
        for cert_header in cert_headers:
            cert_text = cert_header.get_text(strip=True)
            description_parts.append(cert_text)

        # Get standard versions and expiration
        standard_texts = soup.find_all(string=re.compile(r'Standard Version|ISO/IEC|Expiration', re.I))
        for text in standard_texts:
            parent = text.find_parent(['div', 'p'])
            if parent:
                desc_text = parent.get_text(strip=True)
                if len(desc_text) > 20 and desc_text not in description_parts:
                    description_parts.append(desc_text)

        if description_parts:
            fields['description'] = '. '.join(description_parts[:3])[:1000]  # Limit to 1000 chars

        # Parse location using location_parser
        if fields['address']:
            fields['location_id'] = self.location_parser.parse_and_link(
                address=fields['address'],
                latitude=fields['latitude'],
                longitude=fields['longitude']
            )

        return fields

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract Materials Testing specific custom fields

        Args:
            soup: BeautifulSoup parsed HTML
            url: Source URL

        Returns:
            Dict with custom field values
        """
        # Get full page text for keyword matching
        page_text = soup.get_text().lower()

        custom_fields = {}

        # 1. Extract material_types
        material_types = []
        for material_type, keywords in self.material_type_keywords.items():
            if any(kw in page_text for kw in keywords):
                material_types.append(material_type)

        if material_types:
            custom_fields['material_types'] = material_types

        # 2. Extract test_procedures
        test_procedures = []
        for procedure, keywords in self.test_procedure_keywords.items():
            if any(kw in page_text for kw in keywords):
                test_procedures.append(procedure)

        if test_procedures:
            custom_fields['test_procedures'] = test_procedures

        # 3. Extract instrumentation (look for equipment mentions)
        instrumentation_text = []

        # Look for sections mentioning equipment or instrumentation
        equipment_keywords = [
            'equipment', 'instrument', 'machine', 'testing equipment',
            'sem', 'xrf', 'xrd', 'ftir', 'universal testing machine',
            'hardness tester', 'microscope', 'spectrometer'
        ]

        # Find sentences containing equipment keywords
        sentences = re.split(r'[.!?]\s+', soup.get_text())
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(kw in sentence_lower for kw in equipment_keywords):
                instrumentation_text.append(sentence.strip())

        if instrumentation_text:
            # Combine and limit to 500 chars
            custom_fields['instrumentation'] = ' '.join(instrumentation_text[:3])[:500]

        # 4. Extract industry_sectors
        industry_sectors = []
        for sector, keywords in self.industry_sector_keywords.items():
            if any(kw in page_text for kw in keywords):
                industry_sectors.append(sector)

        if industry_sectors:
            custom_fields['industry_sectors'] = industry_sectors

        # 5. Check for custom_test_dev (boolean)
        custom_fields['custom_test_dev'] = any(
            kw in page_text for kw in self.custom_test_keywords
        )

        # 6. Extract rd_capabilities (text description)
        rd_text = []

        # Find sentences with R&D keywords
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(kw in sentence_lower for kw in self.rd_keywords):
                rd_text.append(sentence.strip())

        if rd_text:
            # Combine and limit to 500 chars
            custom_fields['rd_capabilities'] = ' '.join(rd_text[:3])[:500]

        # 7. Extract project_lead_time
        # Try to find lead time mentions
        lead_time_found = None

        for lead_time, pattern in self.lead_time_patterns.items():
            if re.search(pattern, page_text, re.IGNORECASE):
                lead_time_found = lead_time
                break  # Use first match (usually most prominent)

        if lead_time_found:
            custom_fields['project_lead_time'] = [lead_time_found]

        return custom_fields


def main():
    """Test the A2LA Materials Testing scraper"""
    import argparse

    parser = argparse.ArgumentParser(description='A2LA Materials Testing Scraper')
    parser.add_argument('--limit', type=int, help='Limit number of listings to scrape')
    parser.add_argument('--dry-run', action='store_true', help='Parse but don\'t save to database')

    args = parser.parse_args()

    scraper = A2LAMaterialsScraper()
    scraper.run(limit=args.limit, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
