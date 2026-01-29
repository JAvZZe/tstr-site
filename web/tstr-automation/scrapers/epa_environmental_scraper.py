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


class EPAScraper:
    """
    Simple scraper for EPA approved environmental testing labs
    """

    def __init__(self):
        self.base_url = "https://www.epa.gov"
        self.source_url = "https://www.epa.gov/emc/epa-approved-test-labs-and-third-party-certifiers-table"
        self.category_slug = "environmental-testing"

        # Initialize Supabase client
        import os
        from supabase import create_client

        load_dotenv = __import__("dotenv").load_dotenv
        load_dotenv()

        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")

        self.supabase = create_client(supabase_url, supabase_key)

        # Get category_id
        result = (
            self.supabase.from_("categories")
            .select("id")
            .eq("slug", self.category_slug)
            .single()
            .execute()
        )
        self.category_id = result.data["id"]

        # Set up session
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def scrape_labs(self) -> List[Dict]:
        """
        Scrape lab data from EPA page
        """
        logger.info("Scraping EPA approved environmental testing labs...")

        try:
            response = self.session.get(self.source_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            labs = []

            # Find the table with lab data
            table = soup.find("table")
            if not table:
                logger.error("No table found on EPA page")
                return labs

            # Skip header row
            rows = table.find_all("tr")[1:]

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

                    # Test lab and third party flags
                    is_test_lab = cells[4].get_text(strip=True).lower() == "yes"
                    is_third_party = cells[5].get_text(strip=True).lower() == "yes"

                    # Approval expiration
                    expires = cells[6].get_text(strip=True) if len(cells) > 6 else ""

                    # Only include test labs
                    if not is_test_lab:
                        continue

                    lab_data = {
                        "company_name": company_name,
                        "website": website,
                        "address": address,
                        "contact_name": contact_name,
                        "contact_email": contact_email,
                        "contact_phone": contact_phone,
                        "is_third_party": is_third_party,
                        "approval_expires": expires,
                        "source_url": self.source_url,
                    }

                    labs.append(lab_data)
                    logger.info(f"Found lab: {company_name}")

                except Exception as e:
                    logger.error(f"Error parsing row: {e}")
                    continue

            logger.info(f"Successfully scraped {len(labs)} labs from EPA")
            return labs

        except Exception as e:
            logger.error(f"Error scraping EPA page: {e}")
            return []

    def save_to_database(self, labs: List[Dict]) -> int:
        """
        Save labs to database
        """
        saved_count = 0

        for lab in labs:
            try:
                # Check if lab already exists
                existing = (
                    self.supabase.from_("listings")
                    .select("id")
                    .eq("business_name", lab["company_name"])
                    .execute()
                )

                if existing.data:
                    logger.info(f"Lab already exists: {lab['company_name']}")
                    continue

                # Create listing data
                listing_data = {
                    "business_name": lab["company_name"],
                    "description": f"EPA approved environmental testing laboratory. Approval expires: {lab['approval_expires']}",
                    "address": lab["address"],
                    "phone": lab["contact_phone"],
                    "email": lab["contact_email"],
                    "website": lab["website"],
                    "category_id": self.category_id,
                    "source_script": "epa_environmental_scraper.py",
                    "script_location": "web/tstr-automation/scrapers/",
                    "status": "active",
                }

                # Insert listing
                result = self.supabase.from_("listings").insert(listing_data).execute()

                if result.data:
                    listing_id = result.data[0]["id"]
                    saved_count += 1

                    # Add custom fields
                    custom_fields = {
                        "compliance_standards": ["EPA"],
                        "field_lab_services": [
                            "Lab Only"
                        ],  # EPA approved labs are typically lab-based
                        "test_types": [
                            "Air Quality",
                            "Emissions Testing",
                        ],  # Based on EPA EMC focus
                    }

                    for field_name, field_value in custom_fields.items():
                        if field_value:
                            self.supabase.from_("custom_fields").insert(
                                {
                                    "listing_id": listing_id,
                                    "field_name": field_name,
                                    "field_value": field_value,
                                }
                            ).execute()

                    logger.info(f"Saved lab: {lab['company_name']}")

            except Exception as e:
                logger.error(f"Error saving lab {lab['company_name']}: {e}")
                continue

        return saved_count


def main():
    """Main function"""
    scraper = EPAScraper()
    labs = scraper.scrape_labs()

    if labs:
        saved = scraper.save_to_database(labs)
        print(f"Successfully scraped {len(labs)} labs and saved {saved} new listings")
    else:
        print("No labs found")


if __name__ == "__main__":
    main()
