import os
import logging
from typing import Optional
from supabase import create_client
from dotenv import load_dotenv
from conglomerates import detect_parent
import re

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Need service role for updates

if not supabase_url or not supabase_key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(supabase_url, supabase_key)

def get_or_create_parent(parent_name: str, category_id: str) -> Optional[str]:
    # Check if parent exists
    result = supabase.from_("listings").select("id").eq("business_name", parent_name).is_("parent_listing_id", "null").execute()
    
    if result.data:
        return result.data[0]["id"]
        
    # Create parent listing
    slug = re.sub(r"[^a-z0-9]+", "-", parent_name.lower()).strip("-")
    parent_data = {
        "business_name": parent_name,
        "slug": f"group-{slug}", # Distinguish from branches
        "category_id": category_id,
        "status": "active",
        "description": f"Parent brand for {parent_name} group of testing facilities."
    }
    
    result = supabase.from_("listings").insert(parent_data).execute()
    if result.data:
        logger.info(f"Created new parent listing: {parent_name}")
        return result.data[0]["id"]
    return None

def run_fix():
    # Fetch all active listings without a parent
    result = supabase.from_("listings").select("id, business_name, category_id").is_("parent_listing_id", "null").execute()
    
    if not result.data:
        logger.info("No listings to process.")
        return

    listings = result.data
    logger.info(f"Processing {len(listings)} listings...")

    for listing in listings:
        name = listing["business_name"]
        parent_name = detect_parent(name)
        
        # Don't link a listing to itself if it's already the parent name
        if parent_name and parent_name.upper() != name.upper():
            logger.info(f"Linking '{name}' to parent '{parent_name}'")
            parent_id = get_or_create_parent(parent_name, listing["category_id"])
            
            if parent_id:
                supabase.from_("listings").update({"parent_listing_id": parent_id}).eq("id", listing["id"]).execute()
                logger.info(f"✓ Updated '{name}'")

if __name__ == "__main__":
    run_fix()
