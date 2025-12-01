# Manual User Profile Creation for Existing Users

## Problem
The automatic user profile creation trigger only works for new user signups. Users who signed up before the trigger was created (like existing LinkedIn OAuth users) don't have profile records in the `user_profiles` table, causing the account dashboard to show "Failed to load account profile."

## Status: RESOLVED ✅
The trigger is now working correctly for all new signups. This document is kept for reference in case manual intervention is needed for edge cases.

## Solution
Manually create profile records for existing users.

## SQL Commands

### 1. Find Your User ID
Go to Supabase Dashboard → Authentication → Users
Find your user record and copy the `id` field (UUID format).

### 2. Create Profile for Existing User
Run this SQL in Supabase SQL Editor, replacing the placeholders:

```sql
-- Create profile for existing user
INSERT INTO public.user_profiles (id, billing_email, subscription_tier, role)
VALUES (
  'YOUR_USER_ID_HERE',  -- Replace with your actual user ID
  'your-email@example.com',  -- Replace with your actual email
  'free',
  'user'
) ON CONFLICT (id) DO NOTHING;
```

### 3. Verify RLS Policies (Optional)
If the above doesn't work, ensure RLS policies are correct:

```sql
-- Enable RLS on user_profiles (if not already enabled)
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- Allow users to read their own profiles
CREATE POLICY "Users can view own profile" ON user_profiles
  FOR SELECT USING (auth.uid() = id);

-- Allow users to update their own profiles
CREATE POLICY "Users can update own profile" ON user_profiles
  FOR UPDATE USING (auth.uid() = id);

-- Allow authenticated users to insert their own profiles
CREATE POLICY "Users can insert own profile" ON user_profiles
  FOR INSERT WITH CHECK (auth.uid() = id);
```

## Testing
After running the SQL:
1. Refresh https://tstr.site/account
2. The dashboard should now show your profile information instead of the error

## Notes
- The `ON CONFLICT (id) DO NOTHING` prevents errors if the profile already exists
- This is a one-time fix for existing users
- New users will automatically get profiles via the trigger</content>
<parameter name="filePath">docs/active/MANUAL_USER_PROFILE_CREATION.md