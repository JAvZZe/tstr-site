#!/usr/bin/env python3
"""
TNI LAMS Environmental Testing Scraper
Extracts NELAP accredited environmental laboratories from TNI LAMS database
Data source: https://lams.nelac-institute.org/search
"""

import re
import logging
import time
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import requests

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_scraper import BaseNicheScraper

logger = logging.getLogger(__name__)


class TNIEnvironmentalScraper(BaseNicheScraper):
    """
    Scraper for Environmental Testing labs from TNI LAMS (NELAP database)

    Custom Fields Extracted:
    - test_types: Water Quality, Soil Testing, Air Quality, Noise, Asbestos
    - field_lab_services: Field Only, Lab Only, Both
    - esg_reporting: Boolean for ESG/sustainability reporting capabilities
    - sampling_equipment: Text description of sampling equipment/methods
    - compliance_standards: NELAC, ISO 14001, EPA standards
    - monitoring_tech: Monitoring technologies and methods
    - custom_programs: Boolean for custom/tailored testing programs
    """

    # US states to scrape (all 50 states + DC)
    US_STATES = [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "District of Columbia",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    ]

    def __init__(self, dry_run=False):
        super().__init__(
            category_slug="environmental-testing",
            source_name="TNI LAMS (NELAP)",
            rate_limit_seconds=3.0,  # Respectful rate limiting for government site
            dry_run=dry_run,
        )

        self.base_url = "https://lams.nelac-institute.org"
        self.search_url = f"{self.base_url}/search"

        # Matrix type to test type mapping
        self.matrix_mapping = {
            "air": "Air Quality",
            "drinking water": "Water Quality",
            "drinking_water": "Water Quality",
            "non-potable water": "Water Quality",
            "non_potable_water": "Water Quality",
            "water": "Water Quality",
            "solids/chemical": "Soil Testing",
            "solids": "Soil Testing",
            "soil": "Soil Testing",
            "tissue": "Soil Testing",  # Often grouped with solids
            "biological": "Soil Testing",
        }

        # Keywords for ESG reporting detection
        self.esg_keywords = [
            "esg",
            "environmental social governance",
            "sustainability",
            "environmental reporting",
            "carbon footprint",
            "ghg",
            "greenhouse gas",
            "climate",
            "csrd",
            "gri",
            "sasb",
        ]

        # Keywords for custom programs
        self.custom_program_keywords = [
            "custom",
            "tailored",
            "specialized",
            "bespoke",
            "customized",
            "flexible",
            "client-specific",
        ]

        # Accreditation bodies (for reference)
        self.accreditation_bodies = [
            "A2LA",
            "ANSI-ANAB",
            "PJLA",
            "L-A-B",
            "AIHA-LAP, LLC",
        ]

        # Lab data cache: {tni_code: lab_data}
        self.labs_cache = []

    def _get_form_viewstate(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Extract ASP.NET ViewState and EventValidation for form submission

        Args:
            soup: BeautifulSoup of search page

        Returns:
            Dict with __VIEWSTATE, __VIEWSTATEGENERATOR, __EVENTVALIDATION
        """
        form_data = {}

        viewstate = soup.find("input", {"name": "__VIEWSTATE"})
        if viewstate:
            form_data["__VIEWSTATE"] = viewstate.get("value", "")

        viewstate_gen = soup.find("input", {"name": "__VIEWSTATEGENERATOR"})
        if viewstate_gen:
            form_data["__VIEWSTATEGENERATOR"] = viewstate_gen.get("value", "")

        event_validation = soup.find("input", {"name": "__EVENTVALIDATION"})
        if event_validation:
            form_data["__EVENTVALIDATION"] = event_validation.get("value", "")

        return form_data

    def search_labs_by_state(
        self, state: str, limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Search for labs in a specific state

        Args:
            state: US state name (e.g., 'Texas', 'California')
            limit: Optional limit on number of results

        Returns:
            List of lab data dictionaries
        """
        logger.info(f"Searching for labs in {state}...")

        try:
            # First, fetch the search page to get ViewState
            response = self.session.get(self.search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract form data
            form_data = self._get_form_viewstate(soup)

            # Build search request
            # Note: This is a best-effort implementation based on typical ASP.NET patterns
            # May need adjustment after testing against live site
            form_data.update(
                {
                    "ctl00$MainContent$rcbState": state,
                    "ctl00$MainContent$rcbState_ClientState": "",
                    "ctl00$MainContent$rcbActive": "Yes",
                    "ctl00$MainContent$RadButton1": "Search",
                    "__EVENTTARGET": "",
                    "__EVENTARGUMENT": "",
                }
            )

            # Submit search
            time.sleep(self.rate_limit_seconds)
            search_response = self.session.post(
                self.search_url,
                data=form_data,
                headers={
                    "Referer": self.search_url,
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
            search_response.raise_for_status()

            # Parse results
            results_soup = BeautifulSoup(search_response.content, "html.parser")
            labs = self._parse_search_results(results_soup, state)

            if limit:
                labs = labs[:limit]

            logger.info(f"Found {len(labs)} labs in {state}")
            return labs

        except Exception as e:
            logger.error(f"Error searching labs in {state}: {e}")
            return []

    def _parse_search_results(self, soup: BeautifulSoup, state: str) -> List[Dict]:
        """
        Parse lab results from search results page (Telerik RadGrid format)

        Args:
            soup: BeautifulSoup of results page
            state: State being searched

        Returns:
            List of lab data dictionaries
        """
        labs = []

        # Find the RadGrid table with class 'rgMasterTable'
        results_table = soup.find("table", class_="rgMasterTable")

        if not results_table:
            logger.warning(f"No RadGrid results table found for {state}")
            return labs

        # Parse tbody rows (skip header and filter rows)
        tbody = results_table.find("tbody")
        if not tbody:
            logger.warning(f"No tbody found in results table for {state}")
            return labs

        rows = tbody.find_all("tr", class_=re.compile(r"rgRow|rgAltRow"))

        for row in rows:
            cells = row.find_all("td", class_="Radtext")

            if len(cells) < 4:
                continue

            # Extract lab data from table columns
            # Columns: Name (0), City (1), State (2), TNI Lab Code (3)
            business_name = cells[0].get_text(strip=True)
            city = cells[1].get_text(strip=True)
            state_name = cells[2].get_text(strip=True)
            tni_code = cells[3].get_text(strip=True)

            # Skip empty rows
            if not business_name or business_name == "&nbsp;":
                continue

            # Build address from city and state
            address = f"{city}, {state_name}" if city and state_name else ""

            lab_data = {
                "business_name": business_name,
                "tni_code": tni_code,
                "city": city,
                "state": state_name,
                "address": address,
                "accreditation_body": "",  # Not in basic results, need detail page
                "source_url": self.search_url,
                "matrix": "",  # Not in basic results, need detail page
                "methods": "",  # Not in basic results, need detail page
                "detail_url": "",  # TNI LAMS doesn't provide individual detail pages
            }

            labs.append(lab_data)

        return labs

    def get_listing_urls(self) -> List[str]:
        """
        Get list of lab detail URLs to scrape

        Note: TNI LAMS doesn't provide individual detail pages,
        so we return a placeholder list and process from cache instead

        Returns:
            List of placeholder URLs (one per lab)
        """
        if not self.labs_cache:
            # Search states to populate cache
            all_labs = []
            for state in self.US_STATES:  # Search all configured states
                labs = self.search_labs_by_state(state)  # No limit per state
                all_labs.extend(labs)
                time.sleep(self.rate_limit_seconds)

            self.labs_cache = all_labs

        # Return unique placeholder URLs for each lab (use TNI code as identifier)
        return [f"{self.search_url}#{lab['tni_code']}" for lab in self.labs_cache]

    def extract_standard_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract standard listing fields from lab data

        Args:
            soup: BeautifulSoup parsed HTML (may be None for cached data)
            url: Source URL (contains TNI code after #)

        Returns:
            Dict with standard fields
        """
        # Extract TNI code from URL fragment
        tni_code = url.split("#")[-1] if "#" in url else None

        # Find lab data in cache by TNI code
        lab_data = None
        if tni_code:
            for lab in self.labs_cache:
                if lab.get("tni_code") == tni_code:
                    lab_data = lab
                    break

        fields = {
            "business_name": "",
            "description": "",
            "address": "",
            "location_id": None,
            "phone": "",
            "email": "",
            "website": "",
            "latitude": None,
            "longitude": None,
        }

        # Use cached data
        if lab_data:
            fields["business_name"] = lab_data.get("business_name", "")
            fields["address"] = lab_data.get("address", "")

            # Build description from available data
            desc_parts = []
            desc_parts.append(f"NELAP accredited environmental laboratory")
            if lab_data.get("accreditation_body"):
                desc_parts.append(f"accredited by {lab_data['accreditation_body']}")
            if lab_data.get("tni_code"):
                desc_parts.append(f"(TNI Code: {lab_data['tni_code']})")
            if lab_data.get("matrix"):
                desc_parts.append(f"Testing capabilities: {lab_data['matrix']}")
            fields["description"] = ". ".join(desc_parts)

        # Use location_parser to get location_id (skip in dry run)
        if fields["address"] and self.location_parser:
            fields["location_id"] = self.location_parser.parse_and_link(
                address=fields["address"],
                latitude=fields["latitude"],
                longitude=fields["longitude"],
                fallback_country="United States",  # All TNI LAMS labs are in USA
            )

        return fields

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract Environmental Testing specific custom fields

        Args:
            soup: BeautifulSoup parsed HTML (may be None for cached data)
            url: Source URL (contains TNI code after #)

        Returns:
            Dict with custom field values
        """
        # Extract TNI code from URL fragment
        tni_code = url.split("#")[-1] if "#" in url else None

        # Find lab data in cache by TNI code
        lab_data = None
        if tni_code:
            for lab in self.labs_cache:
                if lab.get("tni_code") == tni_code:
                    lab_data = lab
                    break

        # Use business name for keyword matching
        page_text = ""
        if lab_data:
            page_text = f"{lab_data.get('business_name', '')} {lab_data.get('city', '')} {lab_data.get('state', '')}".lower()

        custom_fields = {}

        # 1. Extract test_types from matrix field
        test_types = set()

        if lab_data and lab_data.get("matrix"):
            # Matrix already mapped to test types
            for test_type in lab_data["matrix"].split(";"):
                if test_type.strip():
                    test_types.add(test_type.strip())

        # Also check page text for matrix keywords
        for matrix_key, test_type in self.matrix_mapping.items():
            if matrix_key in page_text:
                test_types.add(test_type)

        # Additional test types based on keywords
        if any(kw in page_text for kw in ["noise", "sound", "acoustic"]):
            test_types.add("Noise")
        if any(kw in page_text for kw in ["asbestos", "acm", "plm"]):
            test_types.add("Asbestos")

        if test_types:
            custom_fields["test_types"] = list(test_types)

        # 2. Determine field_lab_services
        has_field = any(
            kw in page_text for kw in ["field", "on-site", "mobile", "sampling"]
        )
        has_lab = any(
            kw in page_text for kw in ["laboratory", "lab testing", "lab analysis"]
        )

        if has_field and has_lab:
            custom_fields["field_lab_services"] = ["Both"]
        elif has_field:
            custom_fields["field_lab_services"] = ["Field Only"]
        elif has_lab:
            custom_fields["field_lab_services"] = ["Lab Only"]
        else:
            # Default to Lab Only for NELAP accredited facilities
            custom_fields["field_lab_services"] = ["Lab Only"]

        # 3. Check for esg_reporting
        custom_fields["esg_reporting"] = any(
            kw in page_text for kw in self.esg_keywords
        )

        # 4. Extract sampling_equipment from methods/scope
        sampling_equipment = []

        if lab_data and lab_data.get("methods"):
            sampling_equipment.append(lab_data["methods"])

        # Look for equipment keywords
        equipment_keywords = [
            "sampler",
            "probe",
            "monitor",
            "analyzer",
            "meter",
            "sensor",
            "detector",
            "pump",
            "impinger",
        ]

        # Find sentences containing equipment keywords
        sentences = page_text.split(".")
        for sentence in sentences:
            if any(kw in sentence for kw in equipment_keywords) and len(sentence) < 200:
                sampling_equipment.append(sentence.strip())

        if sampling_equipment:
            custom_fields["sampling_equipment"] = "; ".join(
                sampling_equipment[:3]
            )  # Limit to 3 items

        # 5. Extract compliance_standards
        standards = set(["NELAC"])  # Always include NELAC for TNI labs

        # Check for ISO 14001
        if re.search(r"\biso[\s-]?14001\b", page_text, re.IGNORECASE):
            standards.add("ISO 14001")

        # Check for EPA
        if any(kw in page_text for kw in ["epa", "environmental protection agency"]):
            standards.add("EPA")

        # Check for other standards
        if re.search(r"\biso[\s-]?17025\b", page_text, re.IGNORECASE):
            standards.add("ISO 17025")

        if "ansi" in page_text:
            standards.add("ANSI")

        if "a2la" in page_text:
            standards.add("A2LA")

        custom_fields["compliance_standards"] = list(standards)

        # 6. Extract monitoring_tech
        monitoring_tech = []

        # Common monitoring technologies
        tech_keywords = {
            "GC-MS": ["gc-ms", "gcms", "gas chromatography mass spectrometry"],
            "ICP-MS": ["icp-ms", "icpms", "inductively coupled plasma"],
            "HPLC": ["hplc", "high performance liquid chromatography"],
            "XRF": ["xrf", "x-ray fluorescence"],
            "PCR": ["pcr", "polymerase chain reaction"],
            "UV-Vis": ["uv-vis", "spectrophotometry"],
            "Ion Chromatography": ["ion chromatography", "ic"],
            "TOC Analysis": ["toc", "total organic carbon"],
        }

        for tech, keywords in tech_keywords.items():
            if any(kw in page_text for kw in keywords):
                monitoring_tech.append(tech)

        if monitoring_tech:
            custom_fields["monitoring_tech"] = ", ".join(monitoring_tech)

        # 7. Check for custom_programs
        custom_fields["custom_programs"] = any(
            kw in page_text for kw in self.custom_program_keywords
        )

        return custom_fields

    def scrape_listing(self, url: str) -> bool:
        """
        Override base scraper to skip fetching since we use cached data

        Args:
            url: URL of listing (contains TNI code after #)

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Processing: {url}")

        try:
            # Extract standard fields from cache
            standard_fields = self.extract_standard_fields(None, url)

            # Extract custom fields from cache
            custom_fields = self.extract_custom_fields(None, url)

            # Save to database
            listing_id = self.save_listing(standard_fields, custom_fields, url)

            if listing_id:
                self.stats["listings_scraped"] += 1
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error processing listing {url}: {e}")
            self.stats["listings_failed"] += 1
            return False


def main():
    """Test the TNI Environmental scraper"""
    import argparse

    parser = argparse.ArgumentParser(
        description="TNI LAMS Environmental Testing Scraper"
    )
    parser.add_argument("--limit", type=int, help="Limit number of listings to scrape")
    parser.add_argument(
        "--dry-run", action="store_true", help="Parse but don't save to database"
    )
    parser.add_argument(
        "--states", type=int, default=5, help="Number of states to search (default: 5)"
    )

    args = parser.parse_args()

    # Override state limit for testing
    if args.states:
        TNIEnvironmentalScraper.US_STATES = TNIEnvironmentalScraper.US_STATES[
            : args.states
        ]

    scraper = TNIEnvironmentalScraper(dry_run=args.dry_run)
    scraper.run(limit=args.limit, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
