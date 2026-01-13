-- Add pending subscription storage to user_profiles
ALTER TABLE user_profiles
ADD COLUMN IF NOT EXISTS pending_subscription_data JSONB,
ADD COLUMN IF NOT EXISTS pending_subscription_token TEXT,
ADD COLUMN IF NOT EXISTS pending_subscription_expires_at TIMESTAMPTZ;

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_user_profiles_pending_token
ON user_profiles(pending_subscription_token)
WHERE pending_subscription_token IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_user_profiles_pending_expires
ON user_profiles(pending_subscription_expires_at)
WHERE pending_subscription_expires_at IS NOT NULL;

-- Cleanup function
CREATE OR REPLACE FUNCTION cleanup_expired_pending_subscriptions()
RETURNS void AS $$
BEGIN
  UPDATE user_profiles
  SET
    pending_subscription_data = NULL,
    pending_subscription_token = NULL,
    pending_subscription_expires_at = NULL
  WHERE pending_subscription_expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- RLS Policy (users can only access their own pending data)
CREATE POLICY "Users can manage own pending subscriptions" ON user_profiles
  FOR ALL USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);