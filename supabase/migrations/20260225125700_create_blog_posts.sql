-- Migration: Create blog_posts table for TSTR.directory
-- Date: 2026-02-25

CREATE TABLE IF NOT EXISTS blog_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT UNIQUE NOT NULL,

  -- Display fields
  title TEXT NOT NULL,
  excerpt TEXT NOT NULL,
  body TEXT NOT NULL,                       -- Markdown content
  category TEXT NOT NULL,                   -- 'Lab Spotlight'|'Industry Trends'|'Accreditation'|'Regulatory'|'Guide'|'Press'
  author TEXT DEFAULT 'TSTR Editorial',
  cover_image_url TEXT,
  reading_time_mins INTEGER DEFAULT 3,

  -- SEO & relationships
  meta_title TEXT,                          -- Optional override for title tag
  meta_description TEXT,                    -- Optional override for meta description
  canonical_url TEXT,                       -- Useful if syndicating content
  related_listings UUID[],                  -- Array of listing IDs mentioned in the article

  -- Publishing state
  is_published BOOLEAN DEFAULT false,
  published_at TIMESTAMPTZ DEFAULT now(),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Public read access
ALTER TABLE blog_posts ENABLE ROW LEVEL SECURITY;

DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'blog_posts' AND policyname = 'public read published posts'
    ) THEN
        CREATE POLICY "public read published posts"
          ON blog_posts FOR SELECT
          USING (is_published = true);
    END IF;
END $$;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX IF NOT EXISTS idx_blog_posts_category ON blog_posts(category);
