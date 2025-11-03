# ToySoldiers Creator Economy Platform

A complete modular monorepo for the ToySoldiers creator economy platform, featuring FastAPI microservices, Expo React Native apps, and production-ready infrastructure.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repo-url>
cd Toy_Soldiers_completedly_agentic
./quickstart.sh
```

## 📁 Project Structure

```
Toy_Soldiers_completedly_agentic/
├── backend/                    # FastAPI microservices
│   ├── core/                  # Core platform services
│   ├── creator/               # Creator-specific services
│   ├── fan/                   # Fan-specific services
│   └── gateway/               # API gateway configuration
├── frontend/                  # React Native & Web apps
│   ├── creator_app/           # Creator mobile app (Expo)
│   ├── fan_app/              # Fan mobile app (Expo)
│   ├── shared_ui/            # Shared UI components
│   └── web/                  # Web dashboard (Next.js)
├── database/                  # Database schemas & migrations
├── infra/                    # Infrastructure as code
├── scripts/                  # Deployment & utility scripts
└── docs/                     # Documentation
```

## 🛠️ Development

```bash
# Start local development environment
make dev

# Run tests
make test

# Build for production
make build

# Deploy to production
make deploy
```

## 🏗️ Architecture

The platform is built as a modular monorepo with:

- **Backend**: FastAPI microservices with async PostgreSQL
- **Frontend**: Expo React Native apps + Next.js web dashboard
- **Database**: PostgreSQL with Redis caching
- **Infrastructure**: Docker containers with Kubernetes deployment
- **CI/CD**: GitHub Actions with automated testing & deployment

## 📊 Services

### Core Services
- **Auth Service**: Authentication & authorization
- **Payment Service**: Stripe integration for tips & subscriptions
- **Analytics Service**: User behavior & platform metrics
- **Content API**: Video & media management
- **Chat Service**: Real-time messaging

### Creator Services
- **Dashboard Service**: Creator analytics & management
- **Upload Service**: Video upload & processing

### Fan Services
- **Discovery Service**: Content recommendation engine
- **Interaction Service**: Likes, comments, tips, follows

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://localhost/toysoldiers
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=your-jwt-secret
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-key

# Payments
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Storage
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET=toysoldiers-content

# External APIs
CLOUDFLARE_API_TOKEN=your-cf-token
TWILIO_SID=your-twilio-sid
```

## 📱 Mobile Apps

Both creator and fan apps are built with Expo React Native:

```bash
cd frontend/creator_app
npm start

cd frontend/fan_app  
npm start
```

## 🌐 Web Dashboard

Next.js web application for advanced creator management:

```bash
cd frontend/web
npm run dev
```

## 🗄️ Database

PostgreSQL with Redis caching:

```bash
# Run migrations
make migrate

# Seed sample data
make seed

# Reset database
make reset-db
```

## 🚀 Deployment

Production deployment with Docker & Kubernetes:

```bash
# Deploy to staging
make deploy-staging

# Deploy to production
make deploy-production

# Monitor deployment
make logs
```

## 📈 Monitoring

- **Health Checks**: `/health` endpoint on all services
- **Metrics**: Prometheus metrics exported
- **Logging**: Structured JSON logging
- **Tracing**: OpenTelemetry integration

## 🧪 Testing

```bash
# Run all tests
make test

# Backend tests
make test-backend

# Frontend tests
make test-frontend

# Integration tests
make test-integration

# Load tests
make test-load
```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Database Schema](docs/database.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing Guide](docs/contributing.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Platform Goals

ToySoldiers empowers creators to:
- **Monetize Content**: Direct fan support through tips & subscriptions
- **Build Community**: Real-time chat & interaction features
- **Grow Audience**: Advanced discovery & recommendation engine
- **Analyze Performance**: Comprehensive analytics & insights
- **Scale Easily**: Cloud-native architecture for global reach

Built with ❤️ for the creator economy.