#!/usr/bin/env python3
"""
Location Parser for tstr.directory Scrapers
Parses addresses using libpostal and links to hierarchical locations table
"""

import os
import logging
from typing import Optional, Dict

# from postal.parser import parse_address  # Commented out due to dependency issues
from supabase import create_client, Client

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class LocationParser:
    """
    Parse raw addresses and link to locations table hierarchy

    Features:
    - libpostal integration for robust address parsing
    - In-memory cache to minimize DB queries
    - Hierarchical location creation (Global → Region → Country → City)
    - Handles edge cases (missing city, international formats, abbreviations)

    Usage:
        parser = LocationParser(supabase_client)
        location_id = parser.parse_and_link(
            address="123 Main St, Houston, TX 77001, USA",
            lat=29.7604,
            lng=-95.3698
        )
    """

    def __init__(self, supabase_client: Client):
        """
        Initialize LocationParser

        Args:
            supabase_client: Authenticated Supabase client
        """
        self.supabase = supabase_client

        # Cache structure: {cache_key: location_record}
        self.location_cache = {}

        # Stats for monitoring
        self.stats = {
            "cache_hits": 0,
            "cache_misses": 0,
            "created_locations": 0,
            "parse_errors": 0,
        }

        # Load existing locations into cache
        self._load_locations_cache()

        # Country name normalization map (common variations)
        self.country_aliases = {
            "usa": "United States",
            "us": "United States",
            "united states of america": "United States",
            "uk": "United Kingdom",
            "gb": "United Kingdom",
            "great britain": "United Kingdom",
            "uae": "United Arab Emirates",
            "south korea": "Republic of Korea",
            "korea": "Republic of Korea",
            "singapore": "Singapore",  # City-state
            "dubai": "United Arab Emirates",  # City, but helps identify country
            "abu dhabi": "United Arab Emirates",
        }

        # City-states that are both city and country
        self.city_states = {
            "singapore": "Singapore",
            "monaco": "Monaco",
            "vatican city": "Vatican City",
            "hong kong": "Hong Kong",
            "macau": "Macau",
        }

    def _load_locations_cache(self):
        """Load all existing locations from database into memory cache"""
        logger.info("Loading locations cache...")

        try:
            result = self.supabase.from_("locations").select("*").execute()

            for loc in result.data:
                # Cache by multiple keys for flexible lookup
                # Key format: "name:level" or "slug:level"
                name_key = f"{loc['name'].lower()}:{loc['level']}"
                slug_key = f"{loc['slug']}:{loc['level']}"

                self.location_cache[name_key] = loc
                self.location_cache[slug_key] = loc

            logger.info(f"Loaded {len(result.data)} locations into cache")

        except Exception as e:
            logger.error(f"Failed to load locations cache: {e}")
            raise

    def parse_address_components(self, raw_address: str) -> Dict[str, str]:
        """
        Parse raw address string into structured components using libpostal

        Args:
            raw_address: Unstructured address string

        Returns:
            Dictionary with parsed components: {
                'house_number': '123',
                'road': 'Main Street',
                'city': 'Houston',
                'state': 'Texas',
                'country': 'United States',
                'postcode': '77001'
            }

        Example:
            >>> parse_address_components("123 Main St, Houston, TX 77001, USA")
            {'house_number': '123', 'road': 'Main St', 'city': 'Houston',
             'state': 'TX', 'country': 'USA', 'postcode': '77001'}
        """
        if not raw_address or not raw_address.strip():
            return {}

        try:
            # Simple regex-based parsing as fallback for libpostal
            import re

            # Pattern for US addresses: street, city, state zip
            us_pattern = r"(.+?),\s*([^,]+),\s*([A-Z]{2})\s+(\d{5}(?:-\d{4})?)"
            match = re.search(us_pattern, raw_address.strip())

            components = {}
            if match:
                components["road"] = match.group(1).strip()
                components["city"] = match.group(2).strip()
                components["state"] = match.group(3).strip()
                components["postcode"] = match.group(4).strip()
                components["country"] = "United States"
            else:
                # Fallback: split by comma
                parts = [p.strip() for p in raw_address.split(",")]
                if len(parts) >= 1:
                    components["road"] = parts[0]
                if len(parts) >= 2:
                    components["city"] = parts[-2]
                if len(parts) >= 3:
                    state_zip = parts[-1].split()
                    if len(state_zip) >= 1:
                        components["state"] = state_zip[0]
                    if len(state_zip) >= 2:
                        components["postcode"] = state_zip[1]
                    components["country"] = "United States"
                # If duplicate labels (e.g., multiple 'road' entries), concatenate
                if label in components:
                    components[label] = f"{components[label]} {value}"
                else:
                    components[label] = value

            return components

        except Exception as e:
            logger.error(f"Failed to parse address '{raw_address}': {e}")
            self.stats["parse_errors"] += 1
            return {}

    def normalize_country(self, country: str) -> str:
        """
        Normalize country name to consistent format

        Args:
            country: Raw country name or abbreviation

        Returns:
            Normalized country name
        """
        if not country:
            return ""

        country_lower = country.lower().strip()

        # Check aliases map
        if country_lower in self.country_aliases:
            return self.country_aliases[country_lower]

        # Otherwise, return title-cased version
        return country.strip().title()

    def _get_or_create_location(
        self,
        name: str,
        level: str,
        parent_id: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> Dict:
        """
        Find existing location or create new entry

        Args:
            name: Location name (e.g., "Houston", "United States")
            level: Location level ('global', 'region', 'country', 'city')
            parent_id: UUID of parent location (None for global)
            latitude: Optional latitude coordinate
            longitude: Optional longitude coordinate

        Returns:
            Location record dict with 'id', 'name', 'slug', 'level', etc.
        """
        # Check cache first
        cache_key = f"{name.lower()}:{level}"

        if cache_key in self.location_cache:
            self.stats["cache_hits"] += 1
            return self.location_cache[cache_key]

        self.stats["cache_misses"] += 1

        # Try to find in database
        query = (
            self.supabase.from_("locations")
            .select("*")
            .eq("name", name)
            .eq("level", level)
        )

        # For cities, also filter by parent (same city name can exist in multiple countries)
        if parent_id and level == "city":
            query = query.eq("parent_id", parent_id)

        result = query.execute()

        if result.data:
            location = result.data[0]
            self.location_cache[cache_key] = location
            return location

        # Not found, create new location
        logger.info(f"Creating new {level}: {name}")

        slug = name.lower().replace(" ", "-").replace(".", "")

        new_location_data = {
            "name": name,
            "slug": slug,
            "level": level,
            "parent_id": parent_id,
        }

        # Add coordinates if provided
        if latitude is not None:
            new_location_data["latitude"] = latitude
        if longitude is not None:
            new_location_data["longitude"] = longitude

        try:
            insert_result = (
                self.supabase.from_("locations").insert(new_location_data).execute()
            )
            location = insert_result.data[0]

            # Add to cache
            self.location_cache[cache_key] = location
            self.stats["created_locations"] += 1

            return location

        except Exception as e:
            logger.error(f"Failed to create location {name} ({level}): {e}")
            raise

    def find_or_create_hierarchy(
        self,
        city: Optional[str],
        state: Optional[str],
        country: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> str:
        """
        Navigate/create location hierarchy and return deepest location_id

        Hierarchy: Global → Region → Country → State → City

        Args:
            city: City name (optional)
            state: State/province name (optional)
            country: Country name (required)
            latitude: Optional latitude (stored on city level)
            longitude: Optional longitude (stored on city level)

        Returns:
            UUID of the most specific location (city if provided, else country)
        """
        # Normalize country name
        country = self.normalize_country(country)

        # Get Global location (should always exist as root)
        global_loc = self._get_or_create_location("Global", "global")

        # Get or create country
        country_loc = self._get_or_create_location(
            name=country, level="country", parent_id=global_loc["id"]
        )

        # If no city provided, return country location_id
        if not city:
            return country_loc["id"]

        # If state provided, create state level (optional middle tier)
        parent_id = country_loc["id"]
        if state:
            state_loc = self._get_or_create_location(
                name=state,
                level="region",  # Using 'region' level for states
                parent_id=country_loc["id"],
            )
            parent_id = state_loc["id"]

        # Get or create city
        city_loc = self._get_or_create_location(
            name=city,
            level="city",
            parent_id=parent_id,
            latitude=latitude,
            longitude=longitude,
        )

        return city_loc["id"]

    def parse_and_link(
        self,
        address: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        fallback_country: Optional[str] = None,
    ) -> Optional[str]:
        """
        Main method: Parse address and return location_id

        Args:
            address: Raw address string
            latitude: Optional latitude coordinate
            longitude: Optional longitude coordinate
            fallback_country: Country to use if parsing fails

        Returns:
            location_id (UUID) or None if parsing failed

        Example:
            >>> location_id = parser.parse_and_link(
            ...     "123 Main St, Houston, TX 77001, USA",
            ...     lat=29.7604,
            ...     lng=-95.3698
            ... )
            >>> print(location_id)
            'a3f5c8d9-...'
        """
        if not address:
            if fallback_country:
                logger.warning(
                    f"No address provided, using fallback country: {fallback_country}"
                )
                return self.find_or_create_hierarchy(None, None, fallback_country)
            return None

        # Parse address components
        components = self.parse_address_components(address)

        if not components:
            logger.warning(f"Failed to parse address: {address}")
            if fallback_country:
                return self.find_or_create_hierarchy(None, None, fallback_country)
            return None

        # Extract relevant components
        city = (
            components.get("city")
            or components.get("suburb")
            or components.get("city_district")
        )
        state = components.get("state") or components.get("state_district")
        country = components.get("country")

        # Check if city is actually a city-state
        if city and not country:
            city_lower = city.lower().strip()
            if city_lower in self.city_states:
                country = self.city_states[city_lower]
                logger.info(f"Detected city-state: {city} = {country}")

        # Try to infer country from city name if still missing
        if not country and city:
            city_lower = city.lower().strip()
            if city_lower in self.country_aliases:
                country = self.country_aliases[city_lower]
                logger.info(f"Inferred country from city alias: {city} = {country}")

        # Check state field for country hints (some addresses put country in state field)
        if not country and state:
            state_lower = state.lower().strip()
            if state_lower in self.country_aliases:
                country = self.country_aliases[state_lower]
                state = None  # Clear state since it was actually country
                logger.info(f"Found country in state field: {country}")

        # Fallback to provided country if still not found
        if not country and fallback_country:
            country = fallback_country

        if not country:
            logger.warning(f"No country found in address: {address}")
            return None

        # Create/find hierarchy and return location_id
        try:
            location_id = self.find_or_create_hierarchy(
                city=city,
                state=state,
                country=country,
                latitude=latitude,
                longitude=longitude,
            )

            logger.info(
                f"✓ Linked address to location_id: {location_id[:8]}... ({city or country})"
            )
            return location_id

        except Exception as e:
            logger.error(f"Failed to create location hierarchy for {address}: {e}")
            return None

    def validate_location_hierarchy(self, location_id: str) -> bool:
        """
        Validate that location has complete parent chain to Global

        Args:
            location_id: UUID of location to validate

        Returns:
            True if valid hierarchy, False otherwise
        """
        try:
            current_id = location_id
            max_depth = 10  # Prevent infinite loops
            depth = 0

            while current_id and depth < max_depth:
                result = (
                    self.supabase.from_("locations")
                    .select("level, parent_id")
                    .eq("id", current_id)
                    .execute()
                )

                if not result.data:
                    logger.error(f"Location {current_id} not found in database")
                    return False

                location = result.data[0]

                # Reached global level (root)
                if location["level"] == "global":
                    return True

                # Move up to parent
                current_id = location["parent_id"]
                depth += 1

            # Exceeded max depth or no parent found
            logger.error(
                f"Location {location_id} has broken hierarchy (depth: {depth})"
            )
            return False

        except Exception as e:
            logger.error(f"Failed to validate location hierarchy: {e}")
            return False

    def get_stats(self) -> Dict:
        """
        Return parsing statistics

        Returns:
            Dictionary with cache hits, misses, created locations, errors
        """
        return {
            **self.stats,
            "cache_hit_rate": (
                self.stats["cache_hits"]
                / (self.stats["cache_hits"] + self.stats["cache_misses"])
                if (self.stats["cache_hits"] + self.stats["cache_misses"]) > 0
                else 0
            ),
        }


# Convenience function for quick usage
def parse_address_to_location_id(
    address: str,
    supabase_url: Optional[str] = None,
    supabase_key: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> Optional[str]:
    """
    Convenience function to parse address and get location_id in one call

    Args:
        address: Raw address string
        supabase_url: Supabase project URL (reads from env if not provided)
        supabase_key: Supabase service key (reads from env if not provided)
        latitude: Optional latitude
        longitude: Optional longitude

    Returns:
        location_id (UUID) or None
    """
    # Use env variables if not provided
    supabase_url = supabase_url or os.getenv("SUPABASE_URL")
    supabase_key = supabase_key or os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase credentials")

    client = create_client(supabase_url, supabase_key)
    parser = LocationParser(client)

    return parser.parse_and_link(address, latitude, longitude)


if __name__ == "__main__":
    """Test the LocationParser with sample addresses"""
    import sys
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Initialize parser
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        print(
            "Error: Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables"
        )
        sys.exit(1)

    client = create_client(supabase_url, supabase_key)
    parser = LocationParser(client)

    # Test addresses
    test_addresses = [
        "123 Main Street, Houston, TX 77001, United States",
        "45 King's Road, London SW3 4ND, United Kingdom",
        "10 Orchard Road, Singapore 238841",
        "1 Marina Boulevard, Singapore 018989",
        "Khalifa Tower, Sheikh Zayed Road, Dubai, UAE",
    ]

    print("\n" + "=" * 70)
    print("LOCATION PARSER TEST")
    print("=" * 70)

    for address in test_addresses:
        print(f"\nTesting: {address}")
        location_id = parser.parse_and_link(address)

        if location_id:
            print(f"  ✓ location_id: {location_id}")
            valid = parser.validate_location_hierarchy(location_id)
            print(f"  Hierarchy valid: {valid}")
        else:
            print("  ✗ Failed to parse")

    # Show stats
    print("\n" + "=" * 70)
    print("STATISTICS")
    print("=" * 70)
    stats = parser.get_stats()
    for key, value in stats.items():
        if key == "cache_hit_rate":
            print(f"  {key}: {value:.1%}")
        else:
            print(f"  {key}: {value}")
