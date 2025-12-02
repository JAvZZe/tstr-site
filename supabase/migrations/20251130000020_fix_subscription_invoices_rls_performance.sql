-- Fix Auth RLS Initialization Plan issue on subscription_invoices table
-- Wrap auth.uid() in subquery to avoid per-row re-evaluation

-- Drop the existing policy
DROP POLICY IF EXISTS "Users can view own invoices" ON public.subscription_invoices;

-- Recreate with optimized auth call
CREATE POLICY "Users can view own invoices" ON public.subscription_invoices
  FOR SELECT TO authenticated
  USING (user_id = (SELECT auth.uid()));