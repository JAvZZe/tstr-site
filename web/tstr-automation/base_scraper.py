#!/usr/bin/env python3
"""
Base Scraper for tstr.directory Niche-Specific Intelligence Collection
Abstract base class providing common functionality for all niche scrapers
"""

import os
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from supabase import create_client
from dotenv import load_dotenv

from location_parser import LocationParser
from url_validator import URLValidator

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BaseNicheScraper(ABC):
    """
    Abstract base class for niche-specific scrapers

    Provides:
    - Standard field extraction (name, address, website, etc.)
    - Location parsing via libpostal
    - URL validation
    - Rate limiting
    - robots.txt compliance
    - Database operations (insert/update listings)
    - Duplicate detection

    Subclasses must implement:
    - extract_custom_fields(): Extract niche-specific data
    - get_listing_urls(): Return list of URLs to scrape
    """

    def __init__(
        self,
        category_slug: str,
        source_name: str,
        rate_limit_seconds: float = 2.0,
        user_agent: Optional[str] = None,
        dry_run: bool = False,
    ):
        """
        Initialize base scraper

        Args:
            category_slug: Category slug in database (e.g., 'oil-gas-testing')
            source_name: Name of data source (e.g., 'Rigzone Directory')
            rate_limit_seconds: Seconds to wait between requests (default 2.0)
            user_agent: Custom user agent string (optional)
        """
        self.category_slug = category_slug
        self.source_name = source_name
        self.rate_limit_seconds = rate_limit_seconds
        self.dry_run = dry_run
        self.dry_data = [] if dry_run else None

        if not dry_run:
            # Initialize Supabase client
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_ANON_KEY") or os.getenv(
                "SUPABASE_SERVICE_ROLE_KEY"
            )

            if not supabase_url or not supabase_key:
                raise ValueError(
                    "Missing SUPABASE_URL or SUPABASE_ANON_KEY/SUPABASE_SERVICE_ROLE_KEY"
                )

            self.supabase = create_client(supabase_url, supabase_key)

            # Get category_id from database
            self.category_id = self._get_category_id()

            # Load custom fields for this category
            self.custom_fields = self._load_custom_fields()

            # Initialize location parser
            self.location_parser = LocationParser(self.supabase)
        else:
            self.supabase = None
            self.category_id = None
            self.custom_fields = []
            self.location_parser = None

        # Initialize utility components
        if not dry_run:
            self.location_parser = LocationParser(self.supabase)
        self.url_validator = URLValidator()

        # Initialize requests session with headers
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": user_agent or self._get_default_user_agent()}
        )

        # Rate limiting tracker: {domain: last_request_time}
        self.last_request_times = {}

        # robots.txt cache: {domain: RobotFileParser}
        self.robots_cache = {}

        # Statistics
        self.stats = {
            "listings_scraped": 0,
            "listings_saved": 0,
            "listings_skipped_duplicate": 0,
            "listings_failed": 0,
            "custom_fields_populated": 0,
            "rate_limit_delays": 0,
            "robots_blocked": 0,
        }

    def _get_category_id(self) -> str:
        """Get category UUID from database by slug"""
        try:
            result = (
                self.supabase.from_("categories")
                .select("id")
                .eq("slug", self.category_slug)
                .single()
                .execute()
            )

            if not result.data:
                raise ValueError(
                    f"Category '{self.category_slug}' not found in database"
                )

            return result.data["id"]

        except Exception as e:
            logger.error(f"Failed to get category_id for '{self.category_slug}': {e}")
            raise

    def _load_custom_fields(self) -> Dict[str, Dict]:
        """
        Load custom field definitions for this category

        Returns:
            Dict mapping field_name to field definition {id, label, field_type, options, ...}
        """
        try:
            result = (
                self.supabase.from_("custom_fields")
                .select("*")
                .eq("category_id", self.category_id)
                .execute()
            )

            custom_fields = {}
            for field in result.data:
                custom_fields[field["field_name"]] = field

            logger.info(
                f"Loaded {len(custom_fields)} custom fields for category '{self.category_slug}'"
            )
            return custom_fields

        except Exception as e:
            logger.error(f"Failed to load custom fields: {e}")
            return {}

    def _get_default_user_agent(self) -> str:
        """Return default User-Agent string"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

    def check_robots_allowed(self, url: str) -> bool:
        """
        Check if URL is allowed by robots.txt

        Args:
            url: URL to check

        Returns:
            True if allowed, False if disallowed
        """
        parsed = urlparse(url)
        domain = parsed.netloc
        robots_url = f"{parsed.scheme}://{domain}/robots.txt"

        # Check cache first
        if domain not in self.robots_cache:
            rp = RobotFileParser()
            rp.set_url(robots_url)

            try:
                rp.read()
                self.robots_cache[domain] = rp
            except Exception as e:
                logger.warning(f"Failed to fetch robots.txt from {domain}: {e}")
                # Assume allowed if can't fetch robots.txt
                return True

        rp = self.robots_cache[domain]

        # Check if our user agent can fetch this URL
        user_agent = self.session.headers.get("User-Agent", "*")
        allowed = rp.can_fetch(user_agent, url)

        if not allowed:
            logger.warning(f"URL blocked by robots.txt: {url}")
            self.stats["robots_blocked"] += 1

        return allowed

    def respect_rate_limit(self, url: str):
        """
        Enforce rate limiting per domain

        Args:
            url: URL being accessed (used to determine domain)
        """
        domain = urlparse(url).netloc

        if domain in self.last_request_times:
            elapsed = time.time() - self.last_request_times[domain]
            if elapsed < self.rate_limit_seconds:
                sleep_time = self.rate_limit_seconds - elapsed
                logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s for {domain}")
                time.sleep(sleep_time)
                self.stats["rate_limit_delays"] += 1

        self.last_request_times[domain] = time.time()

    def fetch_page(self, url: str, max_retries: int = 3) -> Optional[BeautifulSoup]:
        """
        Fetch and parse HTML page with retry logic

        Args:
            url: URL to fetch
            max_retries: Number of retry attempts

        Returns:
            BeautifulSoup object or None if failed
        """
        # Check robots.txt
        if not self.check_robots_allowed(url):
            return None

        # Respect rate limiting
        self.respect_rate_limit(url)

        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")
                return soup

            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"Attempt {attempt + 1}/{max_retries} failed for {url}: {e}"
                )

                if attempt < max_retries - 1:
                    # Exponential backoff
                    sleep_time = 2**attempt
                    time.sleep(sleep_time)
                else:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                    return None

    def extract_standard_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract standard listing fields common to all niches

        Subclasses can override to customize extraction logic

        Args:
            soup: BeautifulSoup parsed HTML
            url: Source URL

        Returns:
            Dict with standard fields: {
                'business_name': str,
                'description': str,
                'address': str,
                'location_id': UUID | None,
                'phone': str,
                'email': str,
                'website': str,
                'latitude': float | None,
                'longitude': float | None
            }
        """
        # Default implementation - subclasses should override with source-specific selectors
        logger.warning(
            "Using default extract_standard_fields - subclass should override this method"
        )

        return {
            "business_name": "",
            "description": "",
            "address": "",
            "location_id": None,
            "phone": "",
            "email": "",
            "website": url,
            "latitude": None,
            "longitude": None,
        }

    @abstractmethod
    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """
        Extract niche-specific custom fields

        Must be implemented by subclass

        Args:
            soup: BeautifulSoup parsed HTML
            url: Source URL

        Returns:
            Dict mapping field_name to value: {
                'field_name': value,  # Must match custom_fields.field_name
                ...
            }
        """
        raise NotImplementedError("Subclass must implement extract_custom_fields()")

    @abstractmethod
    def get_listing_urls(self) -> List[str]:
        """
        Get list of listing URLs to scrape

        Must be implemented by subclass

        Returns:
            List of URLs to scrape
        """
        raise NotImplementedError("Subclass must implement get_listing_urls()")

    def is_duplicate(
        self,
        website: str,
        phone: Optional[str] = None,
        business_name: Optional[str] = None,
    ) -> bool:
        """
        Check if listing already exists in database

        Args:
            website: Website URL
            phone: Phone number (optional additional check)
            business_name: Business name (fallback for sources without websites)

        Returns:
            True if duplicate exists, False otherwise
        """
        try:
            # Check by website URL (primary key for duplicates) - only if website is provided
            if website and website.strip():
                query = (
                    self.supabase.from_("listings")
                    .select("id")
                    .eq("website", website)
                    .eq("category_id", self.category_id)
                )
                result = query.execute()

                if result.data:
                    return True

            # Check by phone if provided
            if phone and phone.strip():
                query = (
                    self.supabase.from_("listings")
                    .select("id")
                    .eq("phone", phone)
                    .eq("category_id", self.category_id)
                )
                result = query.execute()

                if result.data:
                    return True

            # Fallback: Check by business name for sources without website/phone
            if business_name and business_name.strip():
                query = (
                    self.supabase.from_("listings")
                    .select("id")
                    .eq("business_name", business_name)
                    .eq("category_id", self.category_id)
                )
                result = query.execute()

                if result.data:
                    return True

            return False

        except Exception as e:
            logger.error(f"Error checking duplicate: {e}")
            return False

    def save_listing(
        self, standard_fields: Dict, custom_fields: Dict, source_url: str
    ) -> Optional[str]:
        """
        Save listing to database (listings + custom field values)

        Args:
            standard_fields: Standard listing data
            custom_fields: Niche-specific custom field data
            source_url: URL where data was scraped from

        Returns:
            listing_id (UUID) if successful, None otherwise
        """
        try:
            # Check for duplicates
            if self.is_duplicate(
                standard_fields.get("website", ""),
                standard_fields.get("phone"),
                standard_fields.get("business_name"),
            ):
                logger.info(
                    f"Skipping duplicate listing: {standard_fields.get('business_name', 'Unknown')}"
                )
                self.stats["listings_skipped_duplicate"] += 1
                return None

            # Generate slug from business name
            business_name = standard_fields.get("business_name", "")
            if business_name:
                # Create URL-safe slug
                import re

                slug = re.sub(r"[^a-z0-9]+", "-", business_name.lower()).strip("-")
                # Truncate if too long
                slug = slug[:100] if len(slug) > 100 else slug
            else:
                slug = "listing"

            # Prepare listing data
            listing_data = {
                "business_name": business_name,
                "slug": slug,
                "description": standard_fields.get("description", ""),
                "category_id": self.category_id,
                "location_id": standard_fields.get("location_id"),
                "address": standard_fields.get("address", ""),
                "phone": standard_fields.get("phone", ""),
                "email": standard_fields.get("email", ""),
                "website": standard_fields.get("website", ""),
                "latitude": standard_fields.get("latitude"),
                "longitude": standard_fields.get("longitude"),
                "status": "active",
            }

            # Insert listing
            result = self.supabase.from_("listings").insert(listing_data).execute()

            if not result.data:
                logger.error("Failed to insert listing - no data returned")
                return None

            listing_id = result.data[0]["id"]
            logger.info(
                f"✓ Saved listing: {standard_fields.get('business_name', 'Unknown')} (ID: {listing_id[:8]}...)"
            )

            # Save custom field values
            self._save_custom_field_values(listing_id, custom_fields)

            self.stats["listings_saved"] += 1
            return listing_id

        except Exception as e:
            logger.error(f"Failed to save listing: {e}")
            self.stats["listings_failed"] += 1
            return None

    def _save_custom_field_values(self, listing_id: str, custom_fields: Dict):
        """
        Save custom field values to listing_custom_field_values table

        Args:
            listing_id: UUID of the listing
            custom_fields: Dict mapping field_name to value
        """
        if not custom_fields:
            return

        try:
            values_to_insert = []

            for field_name, field_value in custom_fields.items():
                # Skip empty values
                if field_value is None or field_value == "" or field_value == []:
                    continue

                # Get custom_field_id
                if field_name not in self.custom_fields:
                    logger.warning(f"Unknown custom field: {field_name}")
                    continue

                custom_field_id = self.custom_fields[field_name]["id"]

                # Convert value to appropriate format based on field_type
                field_type = self.custom_fields[field_name]["field_type"]

                if field_type in ["multi_select", "select"]:
                    # Store as JSON array
                    if isinstance(field_value, list):
                        field_value_json = field_value
                    else:
                        field_value_json = [field_value]
                elif field_type == "boolean":
                    field_value_json = bool(field_value)
                else:
                    # Text, number, date, url, email, phone
                    field_value_json = str(field_value)

                values_to_insert.append(
                    {
                        "listing_id": listing_id,
                        "custom_field_id": custom_field_id,
                        "value": field_value_json,
                    }
                )

                self.stats["custom_fields_populated"] += 1

            if values_to_insert:
                self.supabase.from_("listing_custom_fields").insert(
                    values_to_insert
                ).execute()
                logger.info(f"  Saved {len(values_to_insert)} custom field values")

        except Exception as e:
            logger.error(f"Failed to save custom field values: {e}")

    def scrape_listing(self, url: str) -> bool:
        """
        Scrape single listing and save to database

        Args:
            url: URL of listing page

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Scraping: {url}")

        try:
            # Fetch page
            soup = self.fetch_page(url)
            if not soup:
                self.stats["listings_failed"] += 1
                return False

            # Extract standard fields
            standard_fields = self.extract_standard_fields(soup, url)

            # Extract custom fields
            custom_fields = self.extract_custom_fields(soup, url)

            # Save to database
            listing_id = self.save_listing(standard_fields, custom_fields, url)

            if listing_id:
                self.stats["listings_scraped"] += 1
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Error scraping listing {url}: {e}")
            self.stats["listings_failed"] += 1
            return False

    def run(self, limit: Optional[int] = None, dry_run: bool = False):
        """
        Main scraping workflow

        Args:
            limit: Limit number of listings to scrape (for testing)
            dry_run: Fetch and parse but don't save to database
        """
        logger.info("=" * 70)
        logger.info(f"Starting scraper: {self.__class__.__name__}")
        logger.info(f"Category: {self.category_slug}")
        logger.info(f"Source: {self.source_name}")
        logger.info("=" * 70)

        if dry_run:
            logger.info("DRY RUN MODE - No database writes")
            dry_run_data = []

        # Get listing URLs
        listing_urls = self.get_listing_urls()
        logger.info(f"Found {len(listing_urls)} listings to scrape")

        if limit:
            listing_urls = listing_urls[:limit]
            logger.info(f"Limiting to {limit} listings")

        # Scrape each listing
        for idx, url in enumerate(listing_urls, 1):
            logger.info(f"\n[{idx}/{len(listing_urls)}] Processing listing...")

            if dry_run:
                # Extract data but don't save
                soup = self.fetch_page(url)
                if soup:
                    logger.info("  Successfully fetched")
                    # Extract fields
                    standard_fields = self.extract_standard_fields(soup, url)
                    custom_fields = self.extract_custom_fields(soup, url)
                    # Combine
                    listing_data = {**standard_fields, **custom_fields}
                    dry_run_data.append(listing_data)
                else:
                    # If no soup (e.g., for cached data), try to extract from URL or skip
                    logger.info("  Using cached data")
                    standard_fields = self.extract_standard_fields(None, url)
                    custom_fields = self.extract_custom_fields(None, url)
                    listing_data = {**standard_fields, **custom_fields}
                    dry_run_data.append(listing_data)
            else:
                self.scrape_listing(url)

        # Write to CSV in dry run
        if dry_run and dry_run_data:
            self._write_dry_run_csv(dry_run_data)

        # Print summary
        self._print_summary()

    def _write_dry_run_csv(self, data: List[Dict]):
        """Write dry run data to CSV file"""
        import csv
        import os

        if not data:
            return

        # Create output directory if needed
        output_dir = "scraped_data"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"{output_dir}/{self.category_slug}_dry_run.csv"

        # Get all unique keys
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())

        fieldnames = sorted(all_keys)

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

        logger.info(f"Dry run data written to {filename} ({len(data)} records)")

    def _print_summary(self):
        """Print scraping statistics"""
        logger.info("\n" + "=" * 70)
        logger.info("SCRAPING COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Listings scraped: {self.stats['listings_scraped']}")
        logger.info(f"Listings saved: {self.stats['listings_saved']}")
        logger.info(f"Duplicates skipped: {self.stats['listings_skipped_duplicate']}")
        logger.info(f"Failed: {self.stats['listings_failed']}")
        logger.info(f"Custom fields populated: {self.stats['custom_fields_populated']}")
        logger.info(f"Rate limit delays: {self.stats['rate_limit_delays']}")
        logger.info(f"URLs blocked by robots.txt: {self.stats['robots_blocked']}")

        # Location parser stats
        if self.location_parser:
            location_stats = self.location_parser.get_stats()
            logger.info(
                f"\nLocation parser cache hit rate: {location_stats['cache_hit_rate']:.1%}"
            )
            logger.info(f"New locations created: {location_stats['created_locations']}")

    def get_stats(self) -> Dict:
        """Return scraping statistics"""
        return self.stats
