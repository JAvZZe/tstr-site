-- Migration: add certificate_url to certifications
-- Purpose: let listings link directly to a downloadable/viewable accreditation
-- certificate (PDF or hosted page) so paying customers can verify scope on-site.
--
-- APPLY: run this in the Supabase dashboard SQL editor (or `supabase db push`
-- once the CLI tunnel is available). Safe, additive, no data loss.
--
-- NOTE (2026-08-11): direct TCP to the DB is firewalled from the build host and
-- the Supabase CLI `remote psql` tunnel would not accept stdin in that shell, so
-- this was NOT auto-applied. Until applied, the listing UI falls back to linking
-- the lab's public accreditations page (which hosts the PDFs).

ALTER TABLE public.certifications
  ADD COLUMN IF NOT EXISTS certificate_url text;

-- Optional index if we later filter/list by URL (not required now).
-- CREATE INDEX IF NOT EXISTS certifications_certificate_url_idx
--   ON public.certifications (certificate_url);
