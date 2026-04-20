#!/usr/bin/env python3
# ruff: noqa: E402
"""
Tests for LocationParser
Verifies geographic hierarchy resolution and address parsing
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file in the same directory as this script
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

import sys
import unittest
from supabase import create_client

# Add root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from location_parser import LocationParser


class TestLocationParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not supabase_url or not supabase_key:
            raise unittest.SkipTest("Supabase credentials not found in environment")
            
        cls.client = create_client(supabase_url, supabase_key)
        cls.parser = LocationParser(cls.client)

    def test_us_address_parsing(self):
        """Test parsing a standard US address"""
        address = "123 Main St, Houston, TX 77001, USA"
        location_id = self.parser.parse_and_link(address)
        
        self.assertIsNotNone(location_id, "Should return a location_id")
        
        # Verify hierarchy
        is_valid = self.parser.validate_location_hierarchy(location_id)
        self.assertTrue(is_valid, "Hierarchy should be valid (linked to Global)")
        
        # Check details
        result = self.client.from_("locations").select("*").eq("id", location_id).single().execute()
        self.assertEqual(result.data["level"], "city")
        self.assertEqual(result.data["name"].lower(), "houston")

    def test_international_address_parsing(self):
        """Test parsing an international address (UK)"""
        address = "45 King's Road, London SW3 4ND, United Kingdom"
        location_id = self.parser.parse_and_link(address)
        
        self.assertIsNotNone(location_id)
        
        is_valid = self.parser.validate_location_hierarchy(location_id)
        self.assertTrue(is_valid)
        
        result = self.client.from_("locations").select("*").eq("id", location_id).single().execute()
        self.assertEqual(result.data["level"], "city")
        self.assertEqual(result.data["name"].lower(), "london")

    def test_partial_address(self):
        """Test parsing an address with missing components"""
        # City and Country only
        address = "Berlin, Germany"
        location_id = self.parser.parse_and_link(address)
        
        self.assertIsNotNone(location_id)
        
        result = self.client.from_("locations").select("*").eq("id", location_id).single().execute()
        self.assertEqual(result.data["level"], "city")
        self.assertEqual(result.data["name"].lower(), "berlin")

    def test_invalid_address(self):
        """Test behavior with nonsense address"""
        address = "This is not an address 1234567890"
        # Should either return None or a very high-level fallback if it finds anything
        self.parser.parse_and_link(address)
        # Currently, if it can't parse anything, it returns None or falls back to global if it finds country
        # Let's see what it does.
        pass

    def test_hierarchy_uniqueness(self):
        """Test that we don't create duplicate cities in the same state"""
        address1 = "100 First St, Austin, TX, USA"
        address2 = "200 Second St, Austin, TX, USA"
        
        id1 = self.parser.parse_and_link(address1)
        id2 = self.parser.parse_and_link(address2)
        
        self.assertEqual(id1, id2, "Should reuse the same location_id for the same city")

if __name__ == "__main__":
    unittest.main()
