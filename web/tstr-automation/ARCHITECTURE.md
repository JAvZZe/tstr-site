# TSTR.directory Custom Build Architecture
## Lean MVP for Global Testing Directory

**Decision: Custom build with Cloudflare Pages + Supabase**
- Zero monthly costs during MVP phase
- Complete control over structure and monetisation
- Fast static generation with dynamic data
- Scales to millions of listings

---

## Technology Stack (All Free Tier)

### Frontend & Hosting
- **Cloudflare Pages**: Free hosting, unlimited bandwidth, global CDN, automatic HTTPS
- **Astro 4.x**: Static site generator, partial hydration, 0kb JavaScript by default
- **React 18**: Interactive components (search filters, submission forms)
- **Tailwind CSS**: Rapid styling, mobile-first

### Backend & Database
- **Supabase Free Tier**: 500MB PostgreSQL database, 2GB bandwidth/month, 50k MAU
- **Supabase Auth**: Email/password login for listing owners
- **Supabase Storage**: 1GB free for listing images
- **Row Level Security**: Owners can only edit their listings

### Payments (Manual → Automated)
- **Phase 1 (MVP)**: Bank transfer instructions, manual verification
- **Phase 2**: PayPal Business (£0.20 + 2.9% per transaction)
- **Phase 3**: BTCPay Server (self-hosted Bitcoin, zero fees)
- **Phase 4**: Stripe (when revenue justifies 2.9% + £0.20)

### Automation & Scraping
- **Python 3.11**: Scraping scripts
- **Google Maps API**: Free £200/month credit
- **GitHub Actions**: Free CI/CD, scheduled scraping (2,000 minutes/month)

---

## Database Schema (PostgreSQL)
### Core Tables

```sql
-- Global → Region → Country → City hierarchy
CREATE TABLE locations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  parent_id UUID REFERENCES locations(id),
  level TEXT NOT NULL CHECK (level IN ('global', 'region', 'country', 'city')),
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Industry categories (Oil & Gas, Pharma, Biotech, Environmental, Materials)
CREATE TABLE categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  parent_id UUID REFERENCES categories(id),
  description TEXT,
  icon TEXT, -- Icon identifier
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Industry-specific custom fields definition
CREATE TABLE custom_fields (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category_id UUID REFERENCES categories(id),
  field_name TEXT NOT NULL, -- e.g., "iso_17025_certified"
  field_label TEXT NOT NULL, -- e.g., "ISO 17025 Certified"
  field_type TEXT NOT NULL CHECK (field_type IN ('text', 'number', 'boolean', 'select', 'multi_select', 'date', 'url')),
  options JSONB, -- For select/multi_select: ["Option 1", "Option 2"]
  is_required BOOLEAN DEFAULT FALSE,
  is_searchable BOOLEAN DEFAULT TRUE,
  display_order INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Business listings
CREATE TABLE listings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  owner_id UUID REFERENCES auth.users(id),
  category_id UUID REFERENCES categories(id) NOT NULL,
  location_id UUID REFERENCES locations(id) NOT NULL,
  
  -- Core details
  business_name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  description TEXT,
  website TEXT,
  email TEXT,
  phone TEXT,
  address TEXT,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  
  -- Monetisation
  plan_type TEXT DEFAULT 'free' CHECK (plan_type IN ('free', 'basic', 'featured', 'premium')),
  is_featured BOOLEAN DEFAULT FALSE,
  featured_until TIMESTAMPTZ,
  
  -- Status
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'active', 'expired', 'suspended')),
  verified BOOLEAN DEFAULT FALSE,
  claimed BOOLEAN DEFAULT FALSE,
  
  -- Metadata
  views INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ
);

-- Custom field values per listing
CREATE TABLE listing_custom_fields (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  custom_field_id UUID REFERENCES custom_fields(id),
  value JSONB NOT NULL, -- Stores any data type
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(listing_id, custom_field_id)
);

-- Listing images
CREATE TABLE listing_images (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  is_primary BOOLEAN DEFAULT FALSE,
  display_order INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Payment tracking (manual verification for MVP)
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES listings(id),
  owner_id UUID REFERENCES auth.users(id),
  
  amount DECIMAL(10, 2) NOT NULL,
  currency TEXT DEFAULT 'GBP',
  payment_method TEXT CHECK (payment_method IN ('bank_transfer', 'paypal', 'bitcoin', 'stripe')),
  
  -- Bank transfer verification
  reference_number TEXT,
  proof_image_url TEXT,
  
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'rejected', 'refunded')),
  verified_by UUID REFERENCES auth.users(id),
  verified_at TIMESTAMPTZ,
  
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Search analytics
CREATE TABLE search_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  query TEXT,
  filters JSONB,
  results_count INTEGER,
  ip_hash TEXT, -- Anonymised
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_listings_category ON listings(category_id);
CREATE INDEX idx_listings_location ON listings(location_id);
CREATE INDEX idx_listings_status ON listings(status) WHERE status = 'active';
CREATE INDEX idx_listings_featured ON listings(is_featured, featured_until) WHERE is_featured = TRUE;
CREATE INDEX idx_locations_parent ON locations(parent_id);
CREATE INDEX idx_locations_slug ON locations(slug);
CREATE INDEX idx_categories_parent ON categories(parent_id);
CREATE INDEX idx_custom_field_values ON listing_custom_fields(custom_field_id);
```

---

## Row Level Security (RLS) Policies

```sql
-- Enable RLS
ALTER TABLE listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE listing_custom_fields ENABLE ROW LEVEL SECURITY;
ALTER TABLE listing_images ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- Public can read active listings
CREATE POLICY "Public can view active listings"
ON listings FOR SELECT
USING (status = 'active');

-- Owners can CRUD their own listings
CREATE POLICY "Owners can manage own listings"
ON listings FOR ALL
USING (auth.uid() = owner_id);

-- Admin override (you'll create admin role)
CREATE POLICY "Admins can manage all listings"
ON listings FOR ALL
USING (
  EXISTS (
    SELECT 1 FROM auth.users
    WHERE auth.uid() = id AND raw_user_meta_data->>'role' = 'admin'
  )
);
```

---

## Frontend Architecture

### File Structure
```
tstr.directory/
├── src/
│   ├── pages/
│   │   ├── index.astro              # Homepage
│   │   ├── [category]/
│   │   │   ├── index.astro          # Category listing
│   │   │   └── [location]/
│   │   │       └── index.astro      # Filtered by location
│   │   ├── listing/
│   │   │   └── [slug].astro         # Individual listing page
│   │   ├── submit.astro             # Submit new listing
│   │   ├── dashboard.astro          # Owner dashboard
│   │   └── api/
│   │       ├── search.ts            # Search endpoint
│   │       └── submit.ts            # Form handler
│   ├── components/
│   │   ├── SearchFilters.tsx        # React component
│   │   ├── ListingCard.astro
│   │   ├── LocationBreadcrumb.astro
│   │   └── PaymentInstructions.tsx
│   ├── layouts/
│   │   └── Base.astro
│   └── lib/
│       ├── supabase.ts              # Client setup
│       └── utils.ts
├── public/
│   └── images/
├── astro.config.mjs
├── package.json
└── tailwind.config.mjs
```

### Key Pages

**Homepage (`index.astro`)**
- Hero with global search
- Featured listings carousel
- Browse by industry category (Oil & Gas, Pharma, etc.)
- Browse by location (top countries/cities)
- Recent listings
- SEO: Title "TSTR - Global Testing & Laboratory Services Directory"

**Category Page (`/oil-gas-testing/`)**
- Breadcrumb: Home > Oil & Gas Testing
- Filter sidebar (location, custom fields specific to oil & gas)
- Grid of listings
- SEO: "Oil & Gas Testing Laboratories - Pipeline Testing, Corrosion Analysis"

**Location + Category Page (`/oil-gas-testing/united-states/texas/`)**
- Breadcrumb: Home > Oil & Gas Testing > United States > Texas
- Listings in Texas
- SEO: "Oil & Gas Testing Labs in Texas - Pipeline Integrity, Weld Testing"

**Listing Page (`/listing/acme-testing-lab-houston/`)**
- Business name, description
- Contact details (click-to-reveal for lead tracking)
- Custom fields (certifications, turnaround time)
- Location map
- Enquiry form
- Related listings
- SEO: "Acme Testing Lab Houston - ISO 17025 Pipeline Testing"

**Submit Listing (`/submit/`)**
- Multi-step form:
  1. Choose category
  2. Choose location (cascading selects: country → region → city)
  3. Business details
  4. Custom fields (dynamic based on category)
  5. Upload images
  6. Choose plan (Free, Featured £50/month)
  7. Payment (show bank transfer details)
- Requires login (Supabase Auth)
- Auto-creates pending listing
- Admin email notification

**Dashboard (`/dashboard/`)**
- Protected route (must be logged in)
- My listings table
- Edit/renew options
- View statistics (views, enquiries)
- Payment history
- Upgrade to featured

---

## Search & Filtering Logic

```typescript
// src/lib/search.ts
import { supabase } from './supabase'

export async function searchListings(params: {
  query?: string
  categoryId?: string
  locationId?: string
  customFilters?: Record<string, any>
  planType?: string[]
  page?: number
  limit?: number
}) {
  let query = supabase
    .from('listings')
    .select(`
      *,
      category:categories(*),
      location:locations(*),
      images:listing_images(*),
      custom_fields:listing_custom_fields(
        *,
        field:custom_fields(*)
      )
    `)
    .eq('status', 'active')
    .order('is_featured', { ascending: false })
    .order('created_at', { ascending: false })

  if (params.query) {
    query = query.or(`business_name.ilike.%${params.query}%,description.ilike.%${params.query}%`)
  }

  if (params.categoryId) {
    query = query.eq('category_id', params.categoryId)
  }

  if (params.locationId) {
    // Include all child locations
    const childLocations = await getChildLocationIds(params.locationId)
    query = query.in('location_id', childLocations)
  }

  if (params.planType) {
    query = query.in('plan_type', params.planType)
  }

  // Pagination
  const from = ((params.page || 1) - 1) * (params.limit || 20)
  query = query.range(from, from + (params.limit || 20) - 1)

  const { data, error, count } = await query

  return { listings: data, total: count, error }
}

async function getChildLocationIds(parentId: string): Promise<string[]> {
  // Recursive fetch of all child locations
  const { data } = await supabase
    .from('locations')
    .select('id')
    .or(`id.eq.${parentId},parent_id.eq.${parentId}`)
  
  return data?.map(l => l.id) || [parentId]
}
```

---

## Monetisation Implementation

### Plan Types
1. **Free Listing**
   - Appears in search results
   - Basic business details
   - 1 image
   - No highlighting

2. **Featured Listing** (£50/month)
   - Appears at top of search results
   - Badge: "Featured"
   - Unlimited images
   - Priority in homepage carousel
   - 2x larger card in grid

3. **Premium** (£150/month) - Future
   - All Featured benefits
   - Lead form enquiries forwarded
   - Analytics dashboard
   - Remove "Powered by TSTR" footer

### Payment Flow (MVP - Bank Transfer)

1. User submits listing → selects "Featured"
2. System shows bank details:
   ```
   Bank Transfer Details:
   Account Name: TSTR Services Ltd
   Sort Code: XX-XX-XX
   Account Number: XXXXXXXX
   Reference: TSTR-{LISTING_ID}
   Amount: £50.00
   
   Important: Use reference TSTR-{LISTING_ID} exactly
   Upload proof of payment below.
   ```
3. User uploads bank transfer screenshot
4. Admin receives email notification
5. Admin verifies payment in dashboard
6. System activates featured status for 30 days
7. Auto-expiry after 30 days with renewal reminder email

---

## Scraping & Automation

### Google Maps Scraper (Enhanced)
```python
# scraper_v2.py - Enhanced for global + industry-specific scraping

import os
import googlemaps
from datetime import datetime
import json
from supabase import create_client, Client

# Supabase setup
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Google Maps API
gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAPS_API_KEY"))

# Industry-specific search terms
INDUSTRY_QUERIES = {
    "oil_gas": [
        "pipeline testing laboratory",
        "corrosion testing lab",
        "weld testing services",
        "NDT inspection company",
        "petroleum testing laboratory"
    ],
    "pharma": [
        "pharmaceutical testing laboratory",
        "GMP testing lab",
        "stability testing services",
        "pharmaceutical analytical testing"
    ],
    "biotech": [
        "bioanalytical testing laboratory",
        "cell culture testing",
        "biocompatibility testing lab"
    ],
    "environmental": [
        "environmental testing laboratory",
        "water quality testing lab",
        "soil testing services",
        "air quality testing"
    ],
    "materials": [
        "materials testing laboratory",
        "metallurgical testing lab",
        "polymer testing services"
    ]
}

# Priority cities for initial scraping
PRIORITY_CITIES = [
    {"name": "Houston", "country": "United States", "category": "oil_gas"},
    {"name": "Singapore", "country": "Singapore", "category": "oil_gas"},
    {"name": "Basel", "country": "Switzerland", "category": "pharma"},
    {"name": "San Francisco", "country": "United States", "category": "biotech"},
    {"name": "London", "country": "United Kingdom", "category": "environmental"}
]

def get_or_create_location(city_name, country_name):
    """Get location ID or create hierarchy"""
    # Check if city exists
    city = supabase.table("locations").select("*").eq("name", city_name).eq("level", "city").execute()
    if city.data:
        return city.data[0]['id']
    
    # Get or create country
    country = supabase.table("locations").select("*").eq("name", country_name).eq("level", "country").execute()
    if not country.data:
        # Create global → region → country hierarchy
        # (Simplified for MVP - you'll expand this)
        country = supabase.table("locations").insert({
            "name": country_name,
            "slug": country_name.lower().replace(" ", "-"),
            "level": "country"
        }).execute()
    
    country_id = country.data[0]['id']
    
    # Create city
    city = supabase.table("locations").insert({
        "name": city_name,
        "slug": f"{country_name.lower().replace(' ', '-')}-{city_name.lower().replace(' ', '-')}",
        "level": "city",
        "parent_id": country_id
    }).execute()
    
    return city.data[0]['id']

def get_category_id(category_slug):
    """Get category ID by slug"""
    result = supabase.table("categories").select("id").eq("slug", category_slug).execute()
    return result.data[0]['id'] if result.data else None

def scrape_city_industry(city, industry_key):
    """Scrape specific industry in specific city"""
    print(f"\n🔍 Scraping {industry_key} in {city['name']}, {city['country']}")
    
    location_id = get_or_create_location(city['name'], city['country'])
    category_id = get_category_id(industry_key.replace("_", "-"))
    
    all_results = []
    
    for query in INDUSTRY_QUERIES[industry_key]:
        full_query = f"{query} in {city['name']}, {city['country']}"
        print(f"  Query: {full_query}")
        
        try:
            places = gmaps.places(query=full_query)
            
            for place in places.get('results', [])[:10]:  # Limit per query
                place_id = place['place_id']
                details = gmaps.place(place_id=place_id, fields=[
                    'name', 'formatted_address', 'formatted_phone_number',
                    'website', 'geometry', 'rating', 'business_status'
                ])['result']
                
                # Check if already exists
                existing = supabase.table("listings").select("id").eq("business_name", details['name']).execute()
                if existing.data:
                    print(f"    ⏭️  Skip: {details['name']} (exists)")
                    continue
                
                # Insert listing
                listing_data = {
                    "category_id": category_id,
                    "location_id": location_id,
                    "business_name": details['name'],
                    "slug": f"{details['name'].lower().replace(' ', '-').replace('/', '-')}-{city['name'].lower()}",
                    "address": details.get('formatted_address'),
                    "phone": details.get('formatted_phone_number'),
                    "website": details.get('website'),
                    "latitude": details['geometry']['location']['lat'],
                    "longitude": details['geometry']['location']['lng'],
                    "status": "pending",  # Requires manual verification
                    "verified": False
                }
                
                result = supabase.table("listings").insert(listing_data).execute()
                print(f"    ✅ Added: {details['name']}")
                all_results.append(result.data[0])
                
        except Exception as e:
            print(f"    ❌ Error: {str(e)}")
            continue
    
    print(f"  Total scraped: {len(all_results)}")
    return all_results

def scrape_all_priority():
    """Scrape all priority city+industry combinations"""
    total_scraped = 0
    
    for city in PRIORITY_CITIES:
        results = scrape_city_industry(city, city['category'])
        total_scraped += len(results)
    
    print(f"\n🎉 Total listings scraped: {total_scraped}")
    print(f"💾 Saved to Supabase database")

if __name__ == "__main__":
    scrape_all_priority()
```

### GitHub Actions Automation

```yaml
# .github/workflows/scrape.yml
name: Automated Scraping

on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2am UTC
  workflow_dispatch:  # Manual trigger

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install googlemaps supabase
      
      - name: Run scraper
        env:
          GOOGLE_MAPS_API_KEY: ${{ secrets.GOOGLE_MAPS_API_KEY }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
        run: python scraper_v2.py
      
      - name: Notify completion
        run: echo "✅ Scraping complete"
```

---

## MVP Development Phases

### Phase 1: Foundation (Week 1)
**Goal: Database + basic frontend deployed**

1. **Supabase Setup** (Day 1)
   - Create tables from schema above
   - Set up RLS policies
   - Create seed categories:
     * Oil & Gas Testing
     * Pharmaceutical Testing
     * Biotech Testing
     * Environmental Testing
     * Materials Testing
   - Create seed locations:
     * Global → North America → United States → Texas → Houston
     * Global → Europe → United Kingdom → England → London
     * Global → Asia → Singapore

2. **Frontend Scaffold** (Days 2-3)
   - Initialize Astro project
   - Install Tailwind, React
   - Create base layout with header/footer
   - Homepage with search bar
   - Category listing page
   - Individual listing page template

3. **Deploy** (Day 4)
   - Connect GitHub repo
   - Deploy to Cloudflare Pages
   - Configure custom domain (tstr.directory)
   - Test end-to-end

**Deliverable: Live site with static content**

---

### Phase 2: Core Functionality (Week 2)
**Goal: Search, filtering, listing submission working**

1. **Search Implementation** (Days 5-6)
   - Build search API endpoint
   - React search component with filters
   - Location cascade selector
   - Custom field filters (dynamic based on category)
   - Pagination

2. **Listing Submission** (Days 7-8)
   - Multi-step form
   - Supabase Auth integration
   - Image upload to Supabase Storage
   - Create pending listing

3. **Admin Dashboard** (Day 9)
   - Simple admin panel
   - Approve/reject pending listings
   - Manual payment verification
   - Featured listing activation

**Deliverable: Full CRUD + search working**

---

### Phase 3: Monetisation (Week 3)
**Goal: Featured listings, payment tracking**

1. **Pricing Plans** (Day 10)
   - Upgrade flow
   - Bank transfer instructions
   - Payment proof upload
   - Email notifications

2. **Featured Listings Display** (Day 11)
   - Featured badge
   - Priority sorting
   - Homepage carousel
   - Auto-expiry after 30 days

3. **Owner Dashboard** (Day 12)
   - View my listings
   - Analytics (views, clicks)
   - Renew featured status
   - Edit details

**Deliverable: Complete monetisation flow**

---

### Phase 4: Content & Launch (Week 4)
**Goal: Seed database, go live**

1. **Initial Scraping** (Days 13-14)
   - Run scraper for 5 priority cities
   - Manual verification of scraped data
   - Enrich with industry-specific custom fields
   - Target: 200-500 seed listings

2. **SEO & Content** (Days 15-16)
   - Meta descriptions for all pages
   - Schema.org markup (LocalBusiness)
   - XML sitemap generation
   - Blog template for content marketing

3. **Launch Preparation** (Day 17)
   - Test all user flows
   - Mobile testing
   - Performance optimization (image compression, lazy loading)
   - Analytics setup (Cloudflare Web Analytics - free)

**Deliverable: Public launch with 200+ listings**

---

## Capacity Planning

### Supabase Free Tier Limits
- **Database**: 500MB
  - 10,000 listings × 20KB avg = 200MB
  - Room for 25,000 listings before upgrade needed
- **Bandwidth**: 2GB/month
  - 1,000 visitors × 2MB avg = 2GB
  - Upgrade at 50,000 monthly visitors
- **Storage**: 1GB
  - 10,000 images × 100KB avg = 1GB
  - Use Cloudflare R2 (10GB free) for overflow

### When to Upgrade
- Supabase Pro ($25/month): At 20,000 listings or 40,000 monthly visitors
- Cloudflare Pages Pro: Never needed (unlimited bandwidth on free tier)
- Custom domain: £10/year

### Revenue Projections
- 10 featured listings × £50/month = £500/month
- Break-even: 1 featured listing
- Target: 50 featured listings = £2,500/month by Month 6

---

## Next Immediate Steps

1. **Set up Supabase database** (I'll generate SQL script)
2. **Initialize Astro project locally**
3. **Create category + location seed data**
4. **Deploy "Coming Soon" page to tstr.directory**
5. **Run first scraping session** (Houston oil & gas labs)

Should I proceed with generating the complete Supabase setup SQL script now?
