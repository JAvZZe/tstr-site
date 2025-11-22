-- Create clicks table for tracking outbound link clicks
-- Provides analytics on listing engagement and helps identify dead links

CREATE TABLE clicks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  listing_id UUID REFERENCES listings(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  user_agent TEXT,
  referrer TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common query patterns
CREATE INDEX idx_clicks_listing ON clicks(listing_id);
CREATE INDEX idx_clicks_created ON clicks(created_at DESC);

-- RLS policies: Anonymous users can create clicks (logging), authenticated users can read all
ALTER TABLE clicks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can log clicks"
  ON clicks FOR INSERT
  TO anon
  WITH CHECK (true);

CREATE POLICY "Authenticated users can view all clicks"
  ON clicks FOR SELECT
  TO authenticated
  USING (true);

-- Comment for documentation
COMMENT ON TABLE clicks IS 'Tracks outbound clicks to listing websites. Used for engagement analytics and dead link detection.';
