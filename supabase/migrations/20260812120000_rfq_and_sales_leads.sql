-- Migration: RFQ capture + sales leads
-- Purpose: (1) stop losing buyer intent — capture quote/RFQ requests against a
-- listing so we can prove demand to labs ("buyers are asking for you"), and
-- (2) give the scraper/lead-gen pipeline a real table to write into.
--
-- Revenue rationale: the funnel is `search -> listing -> RFQ -> claim/upgrade`.
-- Before this migration the RFQ step did not exist, so buyer intent was lost and
-- there was no evidence to sell a paid listing with. sales_leads replaces the
-- non-existent sales_leads.csv that generate_outreach.py expects.
--
-- APPLY: run in the Supabase dashboard SQL editor (or `supabase db push` when the
-- CLI tunnel is available). Additive only, no data loss.

-- ---------------------------------------------------------------------------
-- 1. RFQ / quote requests (buyer side)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.rfq_requests (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id        uuid REFERENCES public.listings (id) ON DELETE SET NULL,
  -- buyer details
  buyer_name        text NOT NULL,
  buyer_email       text NOT NULL,
  buyer_company     text,
  buyer_phone       text,
  country           text,
  -- what they need
  service_needed    text NOT NULL,
  standard          text,
  quantity          text,
  deadline          date,
  message           text,
  -- pipeline
  status            text NOT NULL DEFAULT 'new'
                      CHECK (status IN ('new','reviewed','forwarded','answered','closed','spam')),
  forwarded_at      timestamptz,
  source            text NOT NULL DEFAULT 'web'
                      CHECK (source IN ('web','email','api','manual')),
  -- anti-spam / audit
  ip_hash           text,
  user_agent        text,
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS rfq_requests_listing_idx ON public.rfq_requests (listing_id);
CREATE INDEX IF NOT EXISTS rfq_requests_status_idx  ON public.rfq_requests (status);
CREATE INDEX IF NOT EXISTS rfq_requests_created_idx ON public.rfq_requests (created_at DESC);

-- RLS: anonymous visitors may INSERT an RFQ, but never read others' requests.
ALTER TABLE public.rfq_requests ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS rfq_insert_public ON public.rfq_requests;
CREATE POLICY rfq_insert_public ON public.rfq_requests
  FOR INSERT TO anon, authenticated
  WITH CHECK (true);

-- No SELECT policy for anon on purpose: reads are service-role only.

-- ---------------------------------------------------------------------------
-- 2. Sales leads (our outreach side)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.sales_leads (
  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id        uuid REFERENCES public.listings (id) ON DELETE SET NULL,
  company_name      text NOT NULL,
  website           text,
  contact_name      text,
  role              text,
  email             text,
  phone             text,
  linkedin_url      text,
  country           text,
  category_slug     text,
  -- why we think they're a lead
  signal            text,
  intent_score      integer NOT NULL DEFAULT 0 CHECK (intent_score BETWEEN 0 AND 100),
  -- compliance: never treat a scraped address as confirmed
  is_verified       boolean NOT NULL DEFAULT false,
  opted_out         boolean NOT NULL DEFAULT false,
  -- pipeline
  status            text NOT NULL DEFAULT 'new'
                      CHECK (status IN ('new','queued','contacted','replied','claimed','paid','bounced','rejected')),
  contacted_at      timestamptz,
  replied_at        timestamptz,
  source            text NOT NULL DEFAULT 'scraped'
                      CHECK (source IN ('scraped','manual','referral','inbound','import')),
  notes             text,
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now()
);

-- one lead row per email (case-insensitive) so re-runs upsert instead of duplicating
CREATE UNIQUE INDEX IF NOT EXISTS sales_leads_email_uniq
  ON public.sales_leads (lower(email)) WHERE email IS NOT NULL;
CREATE INDEX IF NOT EXISTS sales_leads_status_idx  ON public.sales_leads (status);
CREATE INDEX IF NOT EXISTS sales_leads_listing_idx ON public.sales_leads (listing_id);

-- RLS: leads are internal only — no anon access at all.
ALTER TABLE public.sales_leads ENABLE ROW LEVEL SECURITY;
-- (no policies => service-role only, which is what we want)

-- ---------------------------------------------------------------------------
-- 3. updated_at triggers
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.touch_updated_at()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS rfq_requests_touch ON public.rfq_requests;
CREATE TRIGGER rfq_requests_touch BEFORE UPDATE ON public.rfq_requests
  FOR EACH ROW EXECUTE FUNCTION public.touch_updated_at();

DROP TRIGGER IF EXISTS sales_leads_touch ON public.sales_leads;
CREATE TRIGGER sales_leads_touch BEFORE UPDATE ON public.sales_leads
  FOR EACH ROW EXECUTE FUNCTION public.touch_updated_at();
