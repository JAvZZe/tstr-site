#!/usr/bin/env python3
"""
EPA Approved Environmental Testing Labs Scraper
Extracts EPA approved environmental testing laboratories from EPA EMC directory
Data source: https://www.epa.gov/emc/epa-approved-test-labs-and-third-party-certifiers-table
"""

import re
import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EPALabsScraper:
    """
    Simple scraper for EPA approved environmental testing laboratories
    """

    def __init__(self):
        self.base_url = "https://www.epa.gov"
        self.source_url = "https://www.epa.gov/emc/epa-approved-test-labs-and-third-party-certifiers-table"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )

    def scrape_labs(self) -> List[Dict]:
        """
        Scrape EPA approved labs from the table

        Returns:
            List of lab data dictionaries
        """
        logger.info("Scraping EPA approved environmental testing labs...")

        try:
            response = self.session.get(self.source_url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find the table with lab information
            table = soup.find("table")
            if not table:
                logger.error("No table found on EPA page")
                return []

            labs = []
            rows = table.find_all("tr")[1:]  # Skip header row

            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 6:
                    continue

                try:
                    # Extract data from table cells
                    company_name = cells[0].get_text(strip=True)

                    # Handle website link
                    website_cell = cells[1]
                    website = ""
                    if website_cell.find("a"):
                        website = website_cell.find("a")["href"]
                        if not website.startswith("http"):
                            website = urljoin(self.base_url, website)

                    # Address
                    address = cells[2].get_text(strip=True)

                    # Contact info
                    contact_cell = cells[3]
                    contact_name = ""
                    contact_email = ""
                    contact_phone = ""

                    # Parse contact info
                    contact_text = contact_cell.get_text(separator="\n", strip=True)
                    contact_lines = contact_text.split("\n")

                    for line in contact_lines:
                        line = line.strip()
                        if "@" in line and not contact_email:
                            # Extract email
                            email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", line)
                            if email_match:
                                contact_email = email_match.group()
                        elif re.search(r"\(\d{3}\)", line) or re.search(
                            r"\d{3}-\d{3}", line
                        ):
                            # Phone number
                            contact_phone = line
                        elif line and not contact_name:
                            # Name
                            contact_name = line

                    # Test Lab and Third Party flags
                    is_test_lab = cells[4].get_text(strip=True).lower() == "yes"
                    is_third_party = cells[5].get_text(strip=True).lower() == "yes"

                    # Approval expiration
                    expires = cells[6].get_text(strip=True) if len(cells) > 6 else ""

                    # Only include test labs (not just third party certifiers)
                    if not is_test_lab:
                        continue

                    lab_data = {
                        "business_name": company_name,
                        "website": website,
                        "address": address,
                        "contact_name": contact_name,
                        "contact_email": contact_email,
                        "contact_phone": contact_phone,
                        "is_test_lab": is_test_lab,
                        "is_third_party": is_third_party,
                        "approval_expires": expires,
                        "source_url": self.source_url,
                        "accreditation_body": "EPA Approved",
                        "description": f"EPA approved environmental testing laboratory. Expires: {expires}",
                        "category_slug": "environmental-testing",
                    }

                    labs.append(lab_data)
                    logger.info(f"Extracted: {company_name}")

                except Exception as e:
                    logger.error(f"Error parsing row: {e}")
                    continue

            logger.info(f"Successfully extracted {len(labs)} EPA approved labs")
            return labs

        except Exception as e:
            logger.error(f"Error scraping EPA labs: {e}")
            return []


def main():
    """Test the EPA scraper"""
    scraper = EPALabsScraper()
    labs = scraper.scrape_labs()

    print(f"\nFound {len(labs)} EPA approved environmental testing labs:")
    print("-" * 80)

    for i, lab in enumerate(labs[:10], 1):  # Show first 10
        print(f"{i}. {lab['business_name']}")
        print(f"   Address: {lab['address']}")
        print(f"   Website: {lab['website']}")
        print(f"   Contact: {lab['contact_name']} - {lab['contact_email']}")
        print(f"   Expires: {lab['approval_expires']}")
        print()

    if len(labs) > 10:
        print(f"... and {len(labs) - 10} more labs")


if __name__ == "__main__":
    main()
