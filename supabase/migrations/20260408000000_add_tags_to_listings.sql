
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS tags text[] DEFAULT '{}';
COMMENT ON COLUMN public.listings.tags IS 'Descriptive tags or service highlights, extracted from business name or added manually.';
