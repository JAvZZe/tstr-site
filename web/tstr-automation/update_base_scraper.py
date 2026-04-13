
file_path = "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/base_scraper.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Add import
new_lines = []
imported = False
for line in lines:
    new_lines.append(line)
    if "from url_validator import URLValidator" in line and not imported:
        new_lines.append("from conglomerates import detect_parent\n")
        imported = True

# Add helper method
helper_method = """
    def _get_or_create_parent_id(self, parent_name: str) -> Optional[str]:
        if not parent_name:
            return None
            
        try:
            # Check if parent exists (must be a top-level listing)
            result = self.supabase.from_("listings").select("id").eq("business_name", parent_name).is_("parent_listing_id", "null").execute()
            
            if result.data:
                return result.data[0]["id"]
                
            # Create parent listing
            import re
            slug = re.sub(r"[^a-z0-9]+", "-", parent_name.lower()).strip("-")
            
            parent_data = {
                "business_name": parent_name,
                "slug": slug,
                "category_id": self.category_id,
                "status": "active",
                "description": f"Parent brand for {parent_name} group of testing facilities."
            }
            
            result = self.supabase.from_("listings").insert(parent_data).execute()
            if result.data:
                logger.info(f"Created new parent listing: {parent_name}")
                return result.data[0]["id"]
        except Exception as e:
            logger.error(f"Failed to get/create parent ID for {parent_name}: {e}")
            
        return None
"""

# Insert helper before save_listing
final_lines = []
for i, line in enumerate(new_lines):
    if "def save_listing" in line:
        final_lines.append(helper_method)
    final_lines.append(line)

# Update save_listing
# Find where listing_data is defined
for i, line in enumerate(final_lines):
    if '"status": "active",' in line:
        # Check if we already added it
        if "parent_listing_id" not in final_lines[i+1]:
            # Insert parent_listing_id detection logic before listing_data
            pass

# This is getting complex with line-based editing. 
# Let's do a more robust string replacement approach for the listing_data dict.

content = "".join(final_lines)

# Add parent detection logic inside save_listing
old_block = '            # Prepare listing data'
new_block = '''            # Detect parent brand
            parent_name = detect_parent(business_name)
            parent_id = self._get_or_create_parent_id(parent_name) if parent_name else None

            # Prepare listing data'''
content = content.replace(old_block, new_block)

# Add to dict
old_dict = '"status": "active",'
new_dict = '"status": "active",\\n                "parent_listing_id": parent_id,'
content = content.replace(old_dict, new_dict)

with open(file_path, 'w') as f:
    f.write(content)

print("Successfully updated base_scraper.py with hierarchy logic.")
