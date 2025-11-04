# Database Documentation

## Schema Overview

The Toy Soldiers database uses PostgreSQL 15.x with the following main tables:

### Core Tables

#### users
Stores all user accounts (fans, creators, admins)
- `id` (UUID, PK): Unique user identifier
- `email` (TEXT, UNIQUE): User email address
- `password_hash` (TEXT): Bcrypt hashed password
- `role` (TEXT): User role (creator, fan, admin)
- `created_at`, `updated_at` (TIMESTAMPTZ): Timestamps

#### creators
Creator-specific profile information
- `id` (UUID, PK): Creator profile ID
- `user_id` (UUID, FK → users.id): Link to user account
- `payout_account` (TEXT): Stripe Connect account ID
- `bio` (TEXT): Creator biography
- `tiers` (JSONB): Subscription tier configuration
- `verified` (BOOLEAN): Verification status

#### content
All uploaded content (audio/video)
- `id` (UUID, PK): Content identifier
- `creator_id` (UUID, FK → creators.id): Content owner
- `title`, `description` (TEXT): Content metadata
- `media_url`, `stream_url`, `thumbnail_url` (TEXT): Storage URLs
- `tags` (TEXT[]): Searchable tags
- `visibility` (TEXT): public/unlisted/private
- `duration`, `file_size` (INTEGER/BIGINT): Media properties

#### comments
User comments on content
- `id` (UUID, PK): Comment identifier
- `content_id` (UUID, FK → content.id): Referenced content
- `user_id` (UUID, FK → users.id): Comment author
- `parent_id` (UUID, FK → comments.id): For threaded replies
- `text` (TEXT): Comment content

#### tips
Creator monetization via tipping
- `id` (UUID, PK): Transaction identifier
- `from_user` (UUID, FK → users.id): Tipper
- `to_creator` (UUID, FK → creators.id): Recipient
- `amount` (NUMERIC): Tip amount in USD
- `stripe_txn` (TEXT): Stripe transaction ID
- `status` (TEXT): pending/completed/failed/refunded

#### analytics_views
Content view tracking
- `id` (SERIAL, PK): View record ID
- `date` (DATE): View date
- `user_id` (UUID, FK → users.id): Viewer
- `content_id` (UUID, FK → content.id): Viewed content
- `view_count` (INTEGER): Number of views
- `duration` (NUMERIC): Watch time in seconds
- `device_type`, `referrer` (TEXT): Analytics metadata

### Views

#### dashboard_creator
Aggregated creator analytics
```sql
SELECT 
  creator_id,
  total_content,
  total_views,
  total_watch_time,
  total_tips,
  total_comments
FROM dashboard_creator;
```

## Migrations

Migrations are stored in `database/migrations/` and applied sequentially.

### Running Migrations

```bash
./scripts/migrate_db.sh [environment]
```

### Creating a Migration

1. Create new file: `database/migrations/00X_description.sql`
2. Add migration SQL
3. Test locally
4. Commit and deploy

## Row Level Security (RLS)

RLS policies ensure data access control:

- **Content**: Public content viewable by all, private only by creator
- **Comments**: All can view, authenticated users can create
- **Tips**: Users can only see their own transactions

## Indexing Strategy

Optimized indexes for common queries:
- `users.email` (unique)
- `content.creator_id`, `content.visibility`, `content.created_at`
- `content.tags` (GIN index for array operations)
- `comments.content_id`, `comments.user_id`
- `tips.to_creator`, `tips.created_at`
- `analytics_views.content_id`, `analytics_views.date`

## Backup and Recovery

- **Automated backups**: Daily via Supabase
- **Retention**: 30 days
- **Point-in-time recovery**: Available for production
- **Manual backup**: `pg_dump` via scripts

## Performance Optimization

1. **Connection pooling**: PgBouncer (managed by Supabase)
2. **Read replicas**: For analytics queries (future)
3. **Materialized views**: For complex aggregations (future)
4. **Partitioning**: analytics_views by date (when needed)
