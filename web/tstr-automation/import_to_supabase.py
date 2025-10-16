
import os
import csv
from supabase import create_client, Client
from dotenv import load_dotenv
import re

def create_slug(text):
    if text is None:
        return ''
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace spaces and repeated hyphens with a single hyphen
    text = re.sub(r'[\s-]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text

def import_data():
    """
    Imports listings from a CSV file to the Supabase database.
    """
    load_dotenv(dotenv_path='../../.env')
    
    supabase_url = "https://haimjeaetrsaauitrhfy.supabase.co"
    supabase_key = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

    if not supabase_url or not supabase_key:
        print("Error: Supabase URL or Key not found. Make sure they are in web/tstr-frontend/.env")
        return

    supabase: Client = create_client(supabase_url, supabase_key)

    # 1. Fetch categories and locations from Supabase
    try:
        categories_response = supabase.table('categories').select('id, name').execute()
        locations_response = supabase.table('locations').select('id, name').execute()

        if not categories_response.data:
            print("No categories found in the database. Please seed the database first.")
            return
        if not locations_response.data:
            print("No locations found in the database. Please seed the database first.")
            return

        categories = {cat['name']: cat['id'] for cat in categories_response.data}
        locations = {loc['name']: loc['id'] for loc in locations_response.data}
        
        print("Successfully fetched categories and locations.")

    except Exception as e:
        print(f"Error fetching categories or locations: {e}")
        return

    # 2. Read CSV and import data
    csv_file_path = 'tstr_directory_import.csv'
    
    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            listings_to_insert = []
            
            for row in reader:
                # Generate slug
                slug = create_slug(row.get('listing_title'))

                # Get category_id and location_id
                category_name = row.get('listing_category')
                location_name = row.get('listing_location')
                
                category_id = categories.get(category_name)
                location_id = locations.get(location_name)

                if not category_id:
                    print(f"Warning: Category '{category_name}' not found for listing '{row.get('listing_title')}'. Skipping.")
                    continue
                if not location_id:
                    print(f"Warning: Location '{location_name}' not found for listing '{row.get('listing_title')}'. Skipping.")
                    continue

                listing_data = {
                    'business_name': row.get('listing_title'),
                    'description': row.get('listing_content'),
                    'website': row.get('website'),
                    'email': row.get('email'),
                    'phone': row.get('phone'),
                    'address': row.get('address'),
                    'latitude': float(row['latitude']) if row.get('latitude') else None,
                    'longitude': float(row['longitude']) if row.get('longitude') else None,
                    'slug': slug,
                    'category_id': category_id,
                    'location_id': location_id,
                    'status': 'active', # Default status to active
                }
                listings_to_insert.append(listing_data)

            if listings_to_insert:
                print(f"Attempting to insert {len(listings_to_insert)} listings...")
                insert_response = supabase.table('listings').insert(listings_to_insert).execute()
                
                if len(insert_response.data) > 0:
                    print(f"Successfully inserted {len(insert_response.data)} listings.")
                else:
                    print("Error inserting listings.")
                    print(insert_response)

    except FileNotFoundError:
        print(f"Error: The file '{csv_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import_data()
