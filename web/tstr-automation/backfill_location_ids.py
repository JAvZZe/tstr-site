#!/usr/bin/env python3
"""
Backfill location_id for existing TSTR.site listings using libpostal
Parses formatted_address to extract city, country, then links to locations table
"""

import os
import sys
from postal.parser import parse_address
from supabase import create_client
import logging
from typing import Optional, Dict, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LocationBackfiller:
    def __init__(self):
        # Initialize Supabase client
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

        if not supabase_url or not supabase_key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

        self.supabase = create_client(supabase_url, supabase_key)

        # Cache for location lookups
        self.location_cache = {}
        self._load_existing_locations()

    def _load_existing_locations(self):
        """Load all existing locations into cache"""
        logging.info("Loading existing locations from database...")

        result = self.supabase.from_('locations').select('*').execute()

        for loc in result.data:
            # Cache by name for quick lookup
            cache_key = f"{loc['name']}:{loc['level']}"
            self.location_cache[cache_key] = loc

        logging.info(f"Loaded {len(result.data)} existing locations")

    def parse_address_components(self, formatted_address: str) -> Dict[str, str]:
        """
        Use libpostal to parse address into components

        Example input: "123 Main St, Houston, TX 77001, United States"
        Example output: {
            'city': 'Houston',
            'state': 'TX',
            'country': 'United States',
            'postcode': '77001'
        }
        """
        if not formatted_address:
            return {}

        try:
            # libpostal returns list of (value, label) tuples
            parsed = parse_address(formatted_address)

            components = {}
            for value, label in parsed:
                components[label] = value

            return components

        except Exception as e:
            logging.error(f"Failed to parse address '{formatted_address}': {e}")
            return {}

    def find_or_create_location(self, city: Optional[str], country: str, state: Optional[str] = None) -> Optional[str]:
        """
        Find existing location or create new entry in locations table
        Returns location_id (UUID) or None

        Strategy:
        1. Find country in locations table (or create)
        2. Find city under that country (or create)
        3. Return city location_id
        """
        if not country:
            return None

        # Normalize country name
        country = country.strip()

        # Check cache first
        country_key = f"{country}:country"

        if country_key not in self.location_cache:
            # Try to find country in database
            result = self.supabase.from_('locations').select('*').eq('name', country).eq('level', 'country').execute()

            if result.data:
                country_loc = result.data[0]
            else:
                # Create new country
                logging.info(f"Creating new country: {country}")

                # First, get or create region (simplified: just link to Global)
                global_loc = self.supabase.from_('locations').select('id').eq('slug', 'global').single().execute()
                global_id = global_loc.data['id']

                # Create country slug
                country_slug = country.lower().replace(' ', '-')

                new_country = self.supabase.from_('locations').insert({
                    'name': country,
                    'slug': country_slug,
                    'level': 'country',
                    'parent_id': global_id
                }).execute()

                country_loc = new_country.data[0]

            self.location_cache[country_key] = country_loc

        country_loc = self.location_cache[country_key]

        # If city provided, find or create city
        if city:
            city = city.strip()
            city_key = f"{city}:city"

            if city_key not in self.location_cache:
                # Try to find city
                result = self.supabase.from_('locations').select('*').eq('name', city).eq('level', 'city').execute()

                # Filter to cities under this country (might be multiple cities with same name)
                city_loc = None
                for loc in result.data:
                    # Check if parent is our country (or parent's parent for state hierarchy)
                    if loc['parent_id'] == country_loc['id']:
                        city_loc = loc
                        break

                if not city_loc:
                    # Create new city
                    logging.info(f"Creating new city: {city}, {country}")

                    city_slug = city.lower().replace(' ', '-')

                    new_city = self.supabase.from_('locations').insert({
                        'name': city,
                        'slug': city_slug,
                        'level': 'city',
                        'parent_id': country_loc['id']
                    }).execute()

                    city_loc = new_city.data[0]

                self.location_cache[city_key] = city_loc

            return self.location_cache[city_key]['id']

        # No city, return country location_id
        return country_loc['id']

    def backfill_listing(self, listing: Dict) -> bool:
        """
        Process single listing: parse address, find/create location, update location_id
        Returns True if successful
        """
        listing_id = listing['id']
        business_name = listing['business_name']
        address = listing.get('address')

        if not address:
            logging.warning(f"No address for listing {business_name} (ID: {listing_id})")
            return False

        # Parse address components
        components = self.parse_address_components(address)

        if not components:
            logging.warning(f"Failed to parse address for {business_name}: {address}")
            return False

        # Extract city and country
        city = components.get('city') or components.get('suburb')
        country = components.get('country')
        state = components.get('state')

        if not country:
            logging.warning(f"No country found in address for {business_name}: {address}")
            return False

        # Find or create location
        location_id = self.find_or_create_location(city, country, state)

        if not location_id:
            logging.error(f"Failed to get location_id for {business_name}")
            return False

        # Update listing with location_id
        try:
            self.supabase.from_('listings').update({
                'location_id': location_id
            }).eq('id', listing_id).execute()

            logging.info(f"✓ Updated {business_name} → {city or country} (location_id: {location_id[:8]}...)")
            return True

        except Exception as e:
            logging.error(f"Failed to update listing {listing_id}: {e}")
            return False

    def run_backfill(self, limit: Optional[int] = None, dry_run: bool = False):
        """
        Main backfill process

        Args:
            limit: Process only N listings (for testing)
            dry_run: Parse and log, but don't update database
        """
        logging.info("Starting location backfill...")

        # Get listings without location_id
        query = self.supabase.from_('listings').select('*').eq('status', 'active').is_('location_id', 'null')

        if limit:
            query = query.limit(limit)

        result = query.execute()
        listings = result.data

        logging.info(f"Found {len(listings)} listings to process")

        if dry_run:
            logging.info("DRY RUN MODE - No database updates")

        stats = {
            'total': len(listings),
            'success': 0,
            'failed': 0
        }

        for idx, listing in enumerate(listings, 1):
            logging.info(f"\n[{idx}/{len(listings)}] Processing: {listing['business_name']}")

            if dry_run:
                # Just parse and show results
                components = self.parse_address_components(listing.get('address', ''))
                logging.info(f"  Parsed components: {components}")
            else:
                # Actually update
                success = self.backfill_listing(listing)
                if success:
                    stats['success'] += 1
                else:
                    stats['failed'] += 1

        # Summary
        logging.info("\n" + "=" * 60)
        logging.info("BACKFILL COMPLETE")
        logging.info("=" * 60)
        logging.info(f"Total listings: {stats['total']}")
        logging.info(f"Successfully updated: {stats['success']}")
        logging.info(f"Failed: {stats['failed']}")
        logging.info(f"Success rate: {(stats['success']/stats['total']*100):.1f}%")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Backfill location_id for TSTR.site listings')
    parser.add_argument('--limit', type=int, help='Process only N listings (for testing)')
    parser.add_argument('--dry-run', action='store_true', help='Parse addresses but don\'t update database')

    args = parser.parse_args()

    try:
        backfiller = LocationBackfiller()
        backfiller.run_backfill(limit=args.limit, dry_run=args.dry_run)
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)
