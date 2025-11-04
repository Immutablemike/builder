# Toy Soldiers MVP Platform

Full-stack modular content streaming and monetization platform combining Spotify (audio), YouTube (video), and Patreon (creator funding) paradigms.

## Architecture

- **Backend**: FastAPI microservices with modular separation between Creator and Fan workflows
- **Frontend**: Expo (React Native) for cross-platform mobile apps
- **Database**: PostgreSQL via Supabase with realtime capabilities
- **Storage**: Cloudflare R2 for media, Cloudflare Stream for video transcoding
- **Live Streaming**: LiveKit for real-time video/audio rooms
- **Analytics**: PostHog for product analytics, Grafana for system monitoring
- **Payments**: Stripe Connect for creator payouts and tipping

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ and Yarn
- Python 3.11+
- Terraform (for infrastructure)
- Make

### Local Development

```bash
# Copy environment variables
cp .env.example .env

# Install dependencies and setup
make setup

# Start all services
docker-compose up -d

# Run database migrations
make migrate

# Seed sample data
make seed

# Start backend services
make dev-backend

# Start frontend (in another terminal)
make dev-frontend
```

## Project Structure

```
toysoldiers/
├── backend/
│   ├── core/          # Shared services (auth, payments, analytics, content, chat)
│   ├── creator/       # Creator-specific workflows (upload, dashboard, profile)
│   ├── fan/           # Fan-specific workflows (discovery, interaction)
│   └── gateway/       # API gateway and routing
├── frontend/
│   ├── creator_app/   # Expo app for creators
│   ├── fan_app/       # Expo app for fans
│   ├── shared_ui/     # Reusable components
│   └── web/           # Next.js web dashboard
├── database/          # SQL schemas and migrations
├── infra/             # Terraform and Docker configs
├── clients/           # Auto-generated TypeScript and Python SDKs
└── docs/              # Documentation and architecture diagrams
```

## Workflows

### Creator Workflow
1. Sign up and create creator profile
2. Upload audio/video content → Cloudflare R2/Stream
3. View dashboard with analytics (views, tips, engagement)
4. Interact with fans via comments and live chat
5. Manage earnings and request payouts

### Fan Workflow
1. Sign up and browse content feed
2. Discover creators and content
3. Watch/listen to content with adaptive streaming
4. Tip creators and subscribe to premium tiers
5. Comment and participate in live chat

## Deployment

### Staging
```bash
make deploy-staging
```

### Production
```bash
make deploy-production
```

## Testing

```bash
# Run all tests
make test

# Run backend tests
make test-backend

# Run frontend tests
make test-frontend

# Run integration tests
make test-integration
```

## Documentation

- [Architecture Overview](./docs/ToySoldiers_Stack.yaml)
- [API Documentation](./docs/ToySoldiers_API_OpenAPI.yaml)
- [Creator Workflow](./docs/creator_flow.md)
- [Fan Workflow](./docs/fan_flow.md)

## License

Proprietary - Immutability.Space / Toy.Soldiers
