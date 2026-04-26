from base_scraper import BaseNicheScraper
import logging
logging.basicConfig(level=logging.ERROR)

scraper = type('Dummy', (BaseNicheScraper,), {
    'extract_standard_fields': lambda s, soup, url: {}, 
    'extract_custom_fields': lambda s, soup, url: {}, 
    'get_listing_urls': lambda s, limit: []
})('materials-testing', 'A2LA')

# Print category ID for sanity
print(f"Category ID: {scraper.category_id}")

# Get ALL listings for this category to see what we have
response = scraper.supabase.from_('listings').select('id, business_name, updated_at, website').eq('category_id', scraper.category_id).execute()
data = response.data

print(f"Total listings in category: {len(data)}")

found_any = 0
for listing in data:
    lid = listing['id']
    name = listing['business_name']
    cf_response = scraper.supabase.from_('listing_custom_fields').select('*, custom_fields(field_label)').eq('listing_id', lid).execute()
    cf_data = cf_response.data
    if cf_data:
        found_any += 1
        print(f"\n[{found_any}] Checking listing: {name} ({lid}) [Updated: {listing['updated_at']}]")
        for row in cf_data:
            label = row.get('custom_fields', {}).get('field_label', 'Unknown')
            print(f"  Field: {label} -> Value: {row['value']}")

if found_any == 0:
    print("\nNo custom fields found in ANY listings for this category.")
