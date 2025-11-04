-- Seed data for Toy Soldiers platform
-- Sample creators, content, and interactions

-- Insert sample users (passwords are hashed with bcrypt)
INSERT INTO users (id, email, password_hash, role) VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'creator1@toysoldiers.space', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eX.dQvK3JkKe', 'creator'),
    ('b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'creator2@toysoldiers.space', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eX.dQvK3JkKe', 'creator'),
    ('c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'fan1@toysoldiers.space', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eX.dQvK3JkKe', 'fan'),
    ('d3eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'fan2@toysoldiers.space', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5eX.dQvK3JkKe', 'fan')
ON CONFLICT (email) DO NOTHING;

-- Insert sample creators
INSERT INTO creators (id, user_id, bio, tiers, verified) VALUES
    ('e4eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Music producer and beatmaker', '{"basic": 4.99, "premium": 9.99}', true),
    ('f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'b1eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'Podcast host and storyteller', '{"supporter": 2.99, "vip": 7.99}', true)
ON CONFLICT (user_id) DO NOTHING;

-- Insert sample content
INSERT INTO content (id, creator_id, title, description, tags, visibility) VALUES
    ('10eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'e4eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'Late Night Beats Vol. 1', 'Chill beats for coding and relaxation', ARRAY['beats', 'lofi', 'instrumental'], 'public'),
    ('11eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', 'e4eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'Morning Energy Mix', 'Upbeat tracks to start your day', ARRAY['beats', 'upbeat', 'energetic'], 'public'),
    ('12eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'Tech Talk Episode 1', 'Discussion about the future of AI', ARRAY['podcast', 'tech', 'ai'], 'public'),
    ('13eebc99-9c0b-4ef8-bb6d-6bb9bd380a20', 'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 'Behind the Scenes', 'Exclusive content for supporters', ARRAY['podcast', 'exclusive'], 'unlisted')
ON CONFLICT (id) DO NOTHING;

-- Insert sample comments
INSERT INTO comments (content_id, user_id, text) VALUES
    ('10eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'This is amazing! Perfect for late night coding sessions.'),
    ('10eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'd3eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'Love the vibe! Keep them coming.'),
    ('12eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'Great insights on AI. Looking forward to more episodes.')
ON CONFLICT DO NOTHING;

-- Insert sample tips
INSERT INTO tips (from_user, to_creator, amount, status) VALUES
    ('c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'e4eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 5.00, 'completed'),
    ('d3eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 'e4eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 10.00, 'completed'),
    ('c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'f5eebc99-9c0b-4ef8-bb6d-6bb9bd380a16', 3.00, 'completed')
ON CONFLICT DO NOTHING;

-- Insert sample analytics views
INSERT INTO analytics_views (content_id, user_id, view_count, duration, device_type) VALUES
    ('10eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 1, 180.5, 'mobile'),
    ('10eebc99-9c0b-4ef8-bb6d-6bb9bd380a17', 'd3eebc99-9c0b-4ef8-bb6d-6bb9bd380a14', 1, 250.0, 'desktop'),
    ('11eebc99-9c0b-4ef8-bb6d-6bb9bd380a18', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 1, 120.0, 'mobile'),
    ('12eebc99-9c0b-4ef8-bb6d-6bb9bd380a19', 'c2eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 1, 1800.0, 'desktop')
ON CONFLICT DO NOTHING;
