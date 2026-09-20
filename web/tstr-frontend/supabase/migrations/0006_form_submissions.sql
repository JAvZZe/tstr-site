-- form_submissions: backup log for all form submissions
-- If email fails, we have a searchable record and can resend.
-- Applied manually via Supabase dashboard SQL editor (cloud DB is firewalled from this host).

create table if not exists public.form_submissions (
  uuid uuid primary key default gen_random_uuid(),
  form_type text not null check (form_type in ('claim','submit','contact','rfq')),
  payload jsonb not null default '{}',
  ip text,
  user_agent text,
  referrer text,
  status text not null default 'received' check (status in ('received','emailed','bounced','resent')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Index for triaging by type + recency
create index idx_form_submissions_type_created on public.form_submissions (form_type, created_at desc);

-- RLS: only service_role can read/write (internal log)
alter table public.form_submissions enable row level security;

create policy "service_role only"
  on public.form_submissions
  for all
  to service_role
  using (true)
  with check (true);

-- Trigger to keep updated_at fresh
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists trg_form_submissions_updated_at on public.form_submissions;
create trigger trg_form_submissions_updated_at
  before update on public.form_submissions
  for each row execute function public.touch_updated_at();
