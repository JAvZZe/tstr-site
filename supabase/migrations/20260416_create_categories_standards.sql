-- Create categories_standards join table
CREATE TABLE IF NOT EXISTS public.categories_standards (
    category_id uuid REFERENCES public.categories(id) ON DELETE CASCADE,
    standard_id uuid REFERENCES public.standards(id) ON DELETE CASCADE,
    PRIMARY KEY (category_id, standard_id)
);

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_categories_standards_category_id ON public.categories_standards(category_id);
CREATE INDEX IF NOT EXISTS idx_categories_standards_standard_id ON public.categories_standards(standard_id);

-- Enable RLS
ALTER TABLE public.categories_standards ENABLE ROW LEVEL SECURITY;

-- Allow read access to everyone
CREATE POLICY "Allow public read access" ON public.categories_standards FOR SELECT USING (true);
