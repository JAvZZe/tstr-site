-- Add RLS policies for reference tables (categories, locations)
-- These tables need to be readable by anonymous users for form submissions

-- Categories table: Allow anonymous SELECT (public reference data)
DROP POLICY IF EXISTS "Allow anonymous read access to categories" ON public.categories;

CREATE POLICY "Allow anonymous read access to categories"
  ON public.categories
  FOR SELECT
  TO public
  USING (true);

-- Locations table: Allow anonymous SELECT (public reference data)
DROP POLICY IF EXISTS "Allow anonymous read access to locations" ON public.locations;

CREATE POLICY "Allow anonymous read access to locations"
  ON public.locations
  FOR SELECT
  TO public
  USING (true);