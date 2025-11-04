-- Migration 002: Add followers table for creator following
-- Enables fans to follow creators and get personalized feeds

CREATE TABLE IF NOT EXISTS followers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fan_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    creator_id UUID NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(fan_id, creator_id)
);

CREATE INDEX idx_followers_fan_id ON followers(fan_id);
CREATE INDEX idx_followers_creator_id ON followers(creator_id);

-- Add RLS policies
ALTER TABLE followers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own follows" ON followers
    FOR SELECT
    USING (fan_id = auth.uid());

CREATE POLICY "Users can follow creators" ON followers
    FOR INSERT
    WITH CHECK (fan_id = auth.uid());

CREATE POLICY "Users can unfollow creators" ON followers
    FOR DELETE
    USING (fan_id = auth.uid());

SELECT 'Migration 002 completed successfully' AS status;
