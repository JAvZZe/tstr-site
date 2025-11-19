  image_url TEXT NOT NULL,
  is_primary BOOLEAN DEFAULT FALSE,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Payment tracking
CREATE TABLE IF NOT EXISTS payments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  listing_id UUID REFERENCES listings(id) ON DELETE SET NULL,
  owner_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  
  amount DECIMAL(10, 2) NOT NULL,
  currency TEXT DEFAULT 'GBP',
  payment_method TEXT CHECK (payment_method IN ('bank_transfer', 'paypal', 'bitcoin', 'stripe')),
  
  reference_number TEXT,
  proof_image_url TEXT,
  
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'verified', 'rejected', 'refunded')),
  verified_by UUID REFERENCES auth.users(id),
  verified_at TIMESTAMPTZ,
  
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Search analytics
CREATE TABLE IF NOT EXISTS search_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  query TEXT,
  filters JSONB,
  results_count INTEGER,
  ip_hash TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- SUCCESS: Once complete, proceed to STEP_3_INDEXES.sql
