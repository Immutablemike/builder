-- Toy Soldiers Database Schema
-- PostgreSQL 15.x

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('creator', 'fan', 'admin')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Creators table
CREATE TABLE IF NOT EXISTS creators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    payout_account TEXT,
    bio TEXT,
    tiers JSONB DEFAULT '{}',
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_creators_user_id ON creators(user_id);

-- Content table
CREATE TABLE IF NOT EXISTS content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    creator_id UUID NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    media_url TEXT,
    stream_url TEXT,
    thumbnail_url TEXT,
    tags TEXT[] DEFAULT '{}',
    visibility TEXT DEFAULT 'public' CHECK (visibility IN ('public', 'unlisted', 'private')),
    duration INTEGER,
    file_size BIGINT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_content_creator_id ON content(creator_id);
CREATE INDEX idx_content_visibility ON content(visibility);
CREATE INDEX idx_content_created_at ON content(created_at DESC);
CREATE INDEX idx_content_tags ON content USING GIN(tags);

-- Comments table
CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL REFERENCES content(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_comments_content_id ON comments(content_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_parent_id ON comments(parent_id);

-- Tips table
CREATE TABLE IF NOT EXISTS tips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_user UUID REFERENCES users(id),
    to_creator UUID REFERENCES creators(id),
    amount NUMERIC(10, 2) NOT NULL,
    stripe_txn TEXT,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tips_from_user ON tips(from_user);
CREATE INDEX idx_tips_to_creator ON tips(to_creator);
CREATE INDEX idx_tips_created_at ON tips(created_at DESC);

-- Analytics views table
CREATE TABLE IF NOT EXISTS analytics_views (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    user_id UUID REFERENCES users(id),
    content_id UUID REFERENCES content(id),
    view_count INTEGER DEFAULT 1,
    duration NUMERIC(8, 2),
    device_type TEXT,
    referrer TEXT
);

CREATE INDEX idx_analytics_views_date ON analytics_views(date);
CREATE INDEX idx_analytics_views_user_id ON analytics_views(user_id);
CREATE INDEX idx_analytics_views_content_id ON analytics_views(content_id);

-- Dashboard view for creators
CREATE OR REPLACE VIEW dashboard_creator AS
SELECT 
    c.id AS creator_id,
    c.user_id,
    COUNT(DISTINCT ct.id) AS total_content,
    COUNT(DISTINCT av.id) AS total_views,
    COALESCE(SUM(av.duration), 0) AS total_watch_time,
    COALESCE(SUM(t.amount), 0) AS total_tips,
    COUNT(DISTINCT co.id) AS total_comments
FROM creators c
LEFT JOIN content ct ON ct.creator_id = c.id
LEFT JOIN analytics_views av ON av.content_id = ct.id
LEFT JOIN tips t ON t.to_creator = c.id AND t.status = 'completed'
LEFT JOIN comments co ON co.content_id = ct.id
GROUP BY c.id, c.user_id;

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for users table
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Trigger for content table
CREATE TRIGGER update_content_updated_at
BEFORE UPDATE ON content
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE content ENABLE ROW LEVEL SECURITY;
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE tips ENABLE ROW LEVEL SECURITY;

-- Public content is viewable by everyone
CREATE POLICY "Public content is viewable by everyone" ON content
    FOR SELECT
    USING (visibility = 'public');

-- Creators can view their own content
CREATE POLICY "Creators can view their own content" ON content
    FOR SELECT
    USING (creator_id IN (SELECT id FROM creators WHERE user_id = auth.uid()));

-- Creators can insert their own content
CREATE POLICY "Creators can insert their own content" ON content
    FOR INSERT
    WITH CHECK (creator_id IN (SELECT id FROM creators WHERE user_id = auth.uid()));

-- Creators can update their own content
CREATE POLICY "Creators can update their own content" ON content
    FOR UPDATE
    USING (creator_id IN (SELECT id FROM creators WHERE user_id = auth.uid()));

-- Creators can delete their own content
CREATE POLICY "Creators can delete their own content" ON content
    FOR DELETE
    USING (creator_id IN (SELECT id FROM creators WHERE user_id = auth.uid()));

-- Anyone can view comments on public content
CREATE POLICY "Anyone can view comments" ON comments
    FOR SELECT
    USING (true);

-- Authenticated users can insert comments
CREATE POLICY "Authenticated users can insert comments" ON comments
    FOR INSERT
    WITH CHECK (auth.uid() IS NOT NULL);

-- Users can update their own comments
CREATE POLICY "Users can update their own comments" ON comments
    FOR UPDATE
    USING (user_id = auth.uid());

-- Users can delete their own comments
CREATE POLICY "Users can delete their own comments" ON comments
    FOR DELETE
    USING (user_id = auth.uid());
