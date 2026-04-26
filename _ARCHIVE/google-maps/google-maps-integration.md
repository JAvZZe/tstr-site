# 🗺️ TSTR.directory — Google Maps Platform Integration Plan
## Version 1.0 | Prepared by Antigravity (Claude Sonnet) | 2026-04-22

> **Execution Agent:** Gemini Flash (new Antigravity session)
> **Skill to invoke at session start:** `executing-plans`
> **Workflow:** Git Checkpoint → Local Build → DevTools Verify → Success Log → Git Commit

---

## 🎯 Goal

Add Google Maps Platform to TSTR.directory to create a premium visual moat:
- **Free listings**: Static map thumbnail on listing page
- **Premium listings**: Interactive map with Advanced Markers + service radius polygon
- **Browse/Category pages**: Static map cluster overview with zero client-side JS

Free Tier First. Zero client-side JS for non-premium pages. Full Obsidian design alignment.

---

## 📊 Current State (Do Not Repeat These Steps)

| What | Status |
|------|--------|
| `latitude`/`longitude` on `locations` table | ✅ Already in schema + TS types |
| `latitude`/`longitude` on `listings` TS types | ✅ Already exists |
| `listing_premium_data` table | ✅ Exists |
| `subscription_tier` / `billing_tier` fields | ✅ Exists |
| `map_tier` column | ❌ Missing — needs migration |
| `coverage_radius_km` column | ❌ Missing — needs migration |
| Google Maps API key in `.env` | ❌ Missing — needs setup |
| Geocoded lat/lng data for listings | ❌ NULL for most — needs backfill |
| Any Map UI component | ❌ Not built yet |

---

## ⚙️ Prerequisites (Before Phase 1)

### Add API Key to Environment
```bash
# In web/tstr-frontend/.env  AND  web/tstr-frontend/.dev.vars
PUBLIC_GOOGLE_MAPS_API_KEY=your_key_here
GOOGLE_MAPS_API_KEY=your_key_here   # for Python geocoder (server-side, not PUBLIC_)
```
Then add `PUBLIC_GOOGLE_MAPS_API_KEY` to **Cloudflare Pages dashboard** → Environment Variables (both Preview and Production).

**API Key Restrictions** (set in Google Cloud Console):
- Application restrictions: **HTTP referrers**
- Allowed referrers: `tstr.directory/*`, `*.tstr.directory/*`, `localhost:4321/*`
- API restrictions: Enable only — Geocoding API, Maps JavaScript API, Maps Static API

> South Africa billing account — standard GMP Terms apply, no EEA restrictions.

---

## 📋 Tasks

### Phase 1: DB Schema Enhancement
**Goal:** Add `map_tier` and `coverage_radius_km` to `listing_premium_data`.

- [ ] **1.1** Create `supabase/migrations/20260422_add_map_fields.sql`:
  ```sql
  ALTER TABLE listing_premium_data
    ADD COLUMN IF NOT EXISTS map_tier TEXT NOT NULL DEFAULT 'static'
      CHECK (map_tier IN ('none', 'static', 'premium')),
    ADD COLUMN IF NOT EXISTS coverage_radius_km INTEGER DEFAULT NULL;

  COMMENT ON COLUMN listing_premium_data.map_tier IS
    'none=no map, static=Static Maps API img, premium=interactive JS map';
  COMMENT ON COLUMN listing_premium_data.coverage_radius_km IS
    'Service area radius in km for premium map polygon. NULL = no polygon.';
  ```
  → Verify: file exists, SQL is valid

- [ ] **1.2** Apply via Supabase MCP `apply_migration` tool
  → Verify: Supabase table editor shows new columns with correct constraints

- [ ] **1.3** Regenerate TypeScript types:
  ```bash
  cd web/tstr-frontend && npx supabase gen types typescript \
    --project-id haimjeaetrsaauitrhfy > src/types/supabase.ts
  ```
  → Verify: `supabase.ts` contains `map_tier` and `coverage_radius_km`

- [ ] **1.4** Run `get_advisors` (security) via Supabase MCP — confirm RLS not broken

**Success Log 1:**
```
[Phase 1] map_tier + coverage_radius_km added to listing_premium_data.
DevTools: N/A (DB migration). Budget: $0. Git Hash: [TBD]
```

---

### Phase 2: Geocoding Backfill (Python Script)
**Goal:** Populate lat/lng for all listings with address data but NULL coordinates.

- [ ] **2.1** Create `web/tstr-automation/geocode_listings.py`:
  ```python
  """
  Geocode backfill: reads listings with no lat/lng, calls Google Geocoding API,
  writes coordinates back to Supabase listings table.
  Rate limited to 20 req/sec — well under 50/sec quota.
  Cost: ~596 requests = $0.003 total (free tier = 40,000/month).
  """
  import os, time, argparse
  import requests
  from supabase import create_client
  from dotenv import load_dotenv

  load_dotenv()
  supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
  GMAPS_KEY = os.environ["GOOGLE_MAPS_API_KEY"]
  GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

  def geocode(address, city, state, country):
      query = ", ".join(filter(None, [address, city, state, country]))
      r = requests.get(GEOCODE_URL, params={"address": query, "key": GMAPS_KEY})
      data = r.json()
      if data["status"] == "OK":
          loc = data["results"][0]["geometry"]["location"]
          return loc["lat"], loc["lng"]
      return None

  parser = argparse.ArgumentParser()
  parser.add_argument("--dry-run", action="store_true")
  parser.add_argument("--limit", type=int, default=600)
  args = parser.parse_args()

  rows = supabase.table("listings").select(
      "id, address, city, state, country"
  ).is_("latitude", "null").limit(args.limit).execute().data

  print(f"{'DRY RUN — ' if args.dry_run else ''}Geocoding {len(rows)} listings...")
  success, failed = 0, 0

  for row in rows[:5 if args.dry_run else len(rows)]:
      coords = geocode(row.get("address",""), row.get("city",""),
                       row.get("state",""), row.get("country",""))
      if coords:
          if not args.dry_run:
              supabase.table("listings").update(
                  {"latitude": coords[0], "longitude": coords[1]}
              ).eq("id", row["id"]).execute()
          print(f"  ✅ {row.get('city','?')}: {coords}")
          success += 1
      else:
          print(f"  ❌ Failed: {row.get('city','?')}")
          failed += 1
      time.sleep(0.05)

  print(f"Done. {success} geocoded, {failed} failed.")
  ```

- [ ] **2.2** Dry run:
  ```bash
  cd web/tstr-automation && python geocode_listings.py --dry-run --limit 5
  ```
  → Verify: 5 lat/lng pairs printed, no Supabase writes

- [ ] **2.3** Full backfill:
  ```bash
  python geocode_listings.py --limit 600
  ```
  → Verify: `SELECT COUNT(*) FROM listings WHERE latitude IS NOT NULL` returns 500+

**Cost: 596 requests × $0.005/1000 = $0.003 one-time. Free tier: 40,000/month.**

**Success Log 2:**
```
[Phase 2] 596 listings geocoded. lat/lng populated in database.
DevTools: N/A (Python script). Budget: $0.003 one-time. Git Hash: [TBD]
```

---

### Phase 3: Static Maps (Browse & Category Pages)
**Goal:** Zero-JS static map images on `/browse` and `/[category]/[region]/` pages.

- [ ] **3.1** Create `web/tstr-frontend/src/components/StaticLabMap.astro`:
  ```astro
  ---
  /**
   * StaticLabMap.astro — Zero client-side JS.
   * Uses Google Maps Static API (a simple <img> URL).
   * No SDK loaded. Cloudflare CDN-cacheable.
   */
  interface Props {
    listings: Array<{ latitude: number | null; longitude: number | null; name: string }>;
    width?: number;
    height?: number;
    zoom?: number;
  }
  const { listings, width = 640, height = 300, zoom = 5 } = Astro.props;
  const API_KEY = import.meta.env.PUBLIC_GOOGLE_MAPS_API_KEY;

  const geoListings = listings.filter(l => l.latitude && l.longitude);
  const markers = geoListings.slice(0, 50)
    .map(l => `markers=color:0x4F46E5%7C${l.latitude},${l.longitude}`)
    .join('&');
  const center = geoListings.length > 0
    ? `${geoListings[0].latitude},${geoListings[0].longitude}`
    : "39.5,-98.35";

  const mapUrl = `https://maps.googleapis.com/maps/api/staticmap?`
    + `center=${center}&zoom=${zoom}&size=${width}x${height}&maptype=roadmap`
    + `&style=feature:all|element:geometry|color:0x1a1a2e`
    + `&style=feature:road|element:geometry|color:0x0f3460`
    + `&style=feature:poi|visibility:off`
    + `&${markers}&key=${API_KEY}`;
  ---

  {geoListings.length > 0 && (
    <div class="static-map-container">
      <img
        src={mapUrl}
        alt={`Map showing ${geoListings.length} testing lab locations`}
        width={width}
        height={height}
        loading="lazy"
        decoding="async"
        class="static-map-img"
      />
      <p class="static-map-label">{geoListings.length} labs mapped</p>
    </div>
  )}

  <style>
    .static-map-container {
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid rgba(255,255,255,0.08);
      background: #111;
      margin-bottom: 2rem;
    }
    .static-map-img { width: 100%; height: auto; display: block; opacity: 0.85; }
    .static-map-label {
      position: absolute; bottom: 8px; right: 12px;
      font-size: 11px; color: rgba(255,255,255,0.5); margin: 0;
    }
  </style>
  ```

- [ ] **3.2** Add to `src/pages/browse.astro` — import and place above the listing grid

- [ ] **3.3** Add to `src/pages/[category]/[region]/index.astro` — filtered to category listings

- [ ] **3.4** DevTools check (Chrome DevTools MCP or manual):
  - Network tab on `/browse` → `staticmap` request → 200 OK ✅
  - Network tab filter `maps/api/js` → **zero results** ✅
  - Console → zero errors ✅

**Cost: Static Maps = $2/1000 requests. ~30 real API calls/day (Cloudflare CDN caches rest). = $0 (free tier: 100,000/month).**

**Success Log 3:**
```
[Phase 3] StaticLabMap live on /browse and category/region pages.
DevTools: 200 OK staticmap. Zero JS map SDK loaded. Zero console errors.
Budget: $0 (100k free tier, ~30 real req/day). Git Hash: [TBD]
```

---

### Phase 4: Premium Interactive Map (Listing Pages)
**Goal:** React Island with Maps JS API — Advanced Markers + optional service radius. Gated by `map_tier`.

- [ ] **4.1** Install:
  ```bash
  cd web/tstr-frontend && npm install @googlemaps/js-api-loader
  ```

- [ ] **4.2** Create `src/components/PremiumLabMap.tsx`:
  ```tsx
  /**
   * PremiumLabMap.tsx — Astro Island (client:load)
   * Interactive Google Maps for premium listings only.
   * Obsidian-themed dark map. Advanced Markers. Optional service radius.
   */
  import { useEffect, useRef } from 'react';
  import { Loader } from '@googlemaps/js-api-loader';

  interface Props {
    lat: number;
    lng: number;
    labName: string;
    coverageRadiusKm?: number | null;
  }

  const DARK_STYLES = [
    { elementType: "geometry", stylers: [{ color: "#111827" }] },
    { elementType: "labels.text.fill", stylers: [{ color: "#6B7280" }] },
    { featureType: "road", elementType: "geometry", stylers: [{ color: "#1F2937" }] },
    { featureType: "water", elementType: "geometry", stylers: [{ color: "#050505" }] },
    { featureType: "poi", stylers: [{ visibility: "off" }] },
  ];

  export default function PremiumLabMap({ lat, lng, labName, coverageRadiusKm }: Props) {
    const mapRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
      const loader = new Loader({
        apiKey: import.meta.env.PUBLIC_GOOGLE_MAPS_API_KEY,
        version: 'weekly',
        libraries: ['marker'],
      });

      loader.load().then(async () => {
        const { Map } = await google.maps.importLibrary('maps') as google.maps.MapsLibrary;
        const { AdvancedMarkerElement } = await google.maps.importLibrary('marker') as google.maps.MarkerLibrary;
        if (!mapRef.current) return;

        const map = new Map(mapRef.current, {
          center: { lat, lng }, zoom: 13,
          mapId: 'DEMO_MAP_ID',
          styles: DARK_STYLES,
          disableDefaultUI: true, zoomControl: true,
        });

        // Indigo pin — matches Obsidian design system
        const pin = document.createElement('div');
        pin.style.cssText = `
          width:36px;height:36px;border-radius:50%;background:#4F46E5;
          border:2px solid rgba(255,255,255,0.2);display:flex;
          align-items:center;justify-content:center;
          box-shadow:0 0 16px rgba(79,70,229,0.5);cursor:pointer;
        `;
        pin.innerHTML = `<svg width="18" height="18" fill="white" viewBox="0 0 24 24">
          <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
        </svg>`;
        pin.setAttribute('title', labName);

        new AdvancedMarkerElement({ map, position: { lat, lng }, title: labName, content: pin });

        // Emerald service radius — premium feature
        if (coverageRadiusKm && coverageRadiusKm > 0) {
          new google.maps.Circle({
            map, center: { lat, lng }, radius: coverageRadiusKm * 1000,
            strokeColor: '#10B981', strokeOpacity: 0.6, strokeWeight: 2,
            fillColor: '#10B981', fillOpacity: 0.05,
          });
        }
      });
    }, [lat, lng]);

    return (
      <div ref={mapRef} aria-label={`Interactive map for ${labName}`}
        style={{ width:'100%', height:'380px', borderRadius:'12px',
                 border:'1px solid rgba(255,255,255,0.08)', overflow:'hidden' }} />
    );
  }
  ```

- [ ] **4.3** Create `src/components/ListingMap.astro` — tier gate:
  ```astro
  ---
  import PremiumLabMap from './PremiumLabMap.tsx';
  import StaticLabMap from './StaticLabMap.astro';
  interface Props {
    listing: {
      latitude: number | null; longitude: number | null; name: string;
      listing_premium_data?: { map_tier?: string; coverage_radius_km?: number | null } | null;
    };
  }
  const { listing } = Astro.props;
  const tier = listing.listing_premium_data?.map_tier ?? 'static';
  const hasCoords = listing.latitude && listing.longitude;
  ---
  {hasCoords && tier === 'premium' && (
    <PremiumLabMap client:load lat={listing.latitude!} lng={listing.longitude!}
      labName={listing.name} coverageRadiusKm={listing.listing_premium_data?.coverage_radius_km} />
  )}
  {hasCoords && tier === 'static' && (
    <StaticLabMap listings={[listing]} zoom={13} height={220} />
  )}
  {hasCoords && tier === 'static' && (
    <div class="map-upgrade-cta">
      <span>🗺️ Show your service area with an interactive map</span>
      <a href="/lab-manager#upgrade">Upgrade Plan →</a>
    </div>
  )}
  {!hasCoords && <div class="map-unavailable">📍 Location not yet mapped</div>}
  ```

- [ ] **4.4** Integrate `ListingMap.astro` into `src/pages/testing/[industry]/[slug].astro`

- [ ] **4.5** DevTools verification (use Chrome DevTools MCP):
  - Premium listing: `maps/api/js` → 200 OK, Advanced Marker visible, no 403/429
  - Free listing: `maps/api/js` → **zero requests** (static img only)
  - Console: zero errors on both

**Cost: Maps JS API = 28,500 free loads/month. ~3,000 premium views/month = $0.**

**Success Log 4:**
```
[Phase 4] PremiumLabMap live on premium listing pages.
DevTools: 200 OK maps/api/js (premium). Zero JS on free listings. No 403/429.
Budget: $0 (28,500 free tier, ~3,000 premium views/month). Git Hash: [TBD]
```

---

### Phase 5: Monetization Gate Wiring
**Goal:** Auto-sync `map_tier` when `subscription_tier` changes.

- [ ] **5.1** Create `supabase/migrations/20260422_map_tier_trigger.sql`:
  ```sql
  CREATE OR REPLACE FUNCTION sync_map_tier_on_subscription()
  RETURNS TRIGGER AS $$
  BEGIN
    -- Adjust table/column names to match actual subscription table schema
    UPDATE listing_premium_data
    SET map_tier = CASE
      WHEN NEW.subscription_tier IN ('pro', 'enterprise') THEN 'premium'
      ELSE 'static'
    END
    WHERE listing_id = NEW.listing_id;
    RETURN NEW;
  END;
  $$ LANGUAGE plpgsql SECURITY DEFINER;

  -- Note: Verify the correct table name before applying
  -- DROP TRIGGER IF EXISTS trigger_sync_map_tier ON listing_premium_data;
  -- CREATE TRIGGER trigger_sync_map_tier
  --   AFTER UPDATE OF subscription_tier ON listing_premium_data
  --   FOR EACH ROW EXECUTE FUNCTION sync_map_tier_on_subscription();
  ```

  > ⚠️ **Check first:** Query `information_schema.columns` to confirm which table holds `subscription_tier` before creating trigger. May need adjustment.

- [ ] **5.2** Test gate manually: update one listing's `map_tier` to `'premium'`, verify interactive map loads; set back to `'static'`, verify static map only

- [ ] **5.3** Update `PROJECT_STATUS.md` to v2.5.0

**Success Log 5:**
```
[Phase 5] Monetization gate live. subscription_tier drives map_tier automatically.
Budget: $0. Git Hash: [TBD]
```

---

## ✅ Done When

- [ ] `map_tier` + `coverage_radius_km` in schema + TS types regenerated
- [ ] 500+ listings have lat/lng populated in database
- [ ] `/browse` shows static map cluster with indigo pins, zero JS SDK loaded
- [ ] Category/region pages show filtered static map
- [ ] Premium listing page shows Obsidian dark interactive map with Advanced Markers
- [ ] Free listing page shows static thumbnail + upsell CTA
- [ ] All DevTools checks passed (200 OK, 0 console errors, 0 403/429)
- [ ] `PROJECT_STATUS.md` updated to v2.5.0

---

## 💰 Total Cost Summary

| API | Usage | Free Tier | Monthly Cost |
|-----|-------|-----------|--------------|
| Geocoding API | 596 one-time | 40,000/month | **$0** |
| Maps Static API | ~30 real/day (CDN caches rest) | 100,000/month | **$0** |
| Maps JS API | ~3,000/month (premium only) | 28,500/month | **$0** |
| **TOTAL** | | | **$0/month** |

---

## 🤖 Agent Handoff Instructions

**To execute this plan, open a new Antigravity session in Gemini Flash mode:**
1. Run global bootstrap: `cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh`
2. Read this file: `google-maps-integration.md` (project root)
3. Invoke skill: `executing-plans`
4. Execute phases **in order 1 → 2 → 3 → 4 → 5**
5. After each phase: write Success Log entry to `SUCCESS_LOG.md`, then `git commit`
6. **Do NOT skip DevTools verification** — use Chrome DevTools MCP for Phases 3 and 4

---

*Google Maps Platform Terms of Service: https://cloud.google.com/maps-platform/terms*
*Map renders include attribution automatically via the GMP SDK.*
