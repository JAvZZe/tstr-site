-- Allow anonymous users to submit listings (will go to 'pending' status for review)
CREATE POLICY "Allow public submissions to pending listings"
ON listings FOR INSERT
TO anon
WITH CHECK (status = 'pending');

-- Ensure status column defaults to 'pending' for safety
ALTER TABLE listings ALTER COLUMN status SET DEFAULT 'pending';
