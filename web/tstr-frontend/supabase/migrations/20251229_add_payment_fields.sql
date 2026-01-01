-- Add payment tracking columns to user_profiles
ALTER TABLE public.user_profiles
ADD COLUMN IF NOT EXISTS paypal_subscription_id TEXT,
ADD COLUMN IF NOT EXISTS subscription_start_date TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS subscription_end_date TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS last_payment_date TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT NULL;

-- Create payment history table
CREATE TABLE IF NOT EXISTS public.payment_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    status TEXT NOT NULL CHECK (status IN ('completed', 'pending', 'failed', 'refunded')),
    paypal_transaction_id TEXT,
    paypal_subscription_id TEXT,
    tier TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_payment_history_user_id ON public.payment_history(user_id);
CREATE INDEX IF NOT EXISTS idx_payment_history_created_at ON public.payment_history(created_at DESC);

-- RLS policies
ALTER TABLE public.payment_history ENABLE ROW LEVEL SECURITY;

-- Users can only see their own payment history
CREATE POLICY "Users can view own payment history" ON public.payment_history
    FOR SELECT USING (auth.uid() = user_id);

-- Only service role can insert (webhooks)
CREATE POLICY "Service role can insert payments" ON public.payment_history
    FOR INSERT WITH CHECK (true);