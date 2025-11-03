.PHONY: help dev build test clean deploy-staging deploy-production

# Default target
help:
	@echo "ToySoldiers Creator Economy Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  dev              - Start local development environment"
	@echo "  build            - Build all services for production"
	@echo "  test             - Run all tests"
	@echo "  test-backend     - Run backend tests only"
	@echo "  test-frontend    - Run frontend tests only"
	@echo "  clean            - Clean up containers and build artifacts"
	@echo "  migrate          - Run database migrations"
	@echo "  seed             - Seed database with sample data"
	@echo "  reset-db         - Reset database (WARNING: destroys data)"
	@echo "  logs             - Show container logs"
	@echo "  deploy-staging   - Deploy to staging environment"
	@echo "  deploy-production - Deploy to production environment"

# Development
dev:
	@echo "🚀 Starting ToySoldiers development environment..."
	docker-compose -f infra/docker-compose.yml up -d
	@echo "✅ Development environment started!"
	@echo "📱 Creator App: http://localhost:19006"
	@echo "📱 Fan App: http://localhost:19007"
	@echo "🌐 Web Dashboard: http://localhost:3000"
	@echo "🔧 API Gateway: http://localhost:8000"

# Build
build:
	@echo "🔨 Building all services..."
	docker-compose -f infra/docker-compose.yml build
	cd frontend/creator_app && npm run build
	cd frontend/fan_app && npm run build
	cd frontend/web && npm run build
	@echo "✅ All services built successfully!"

# Testing
test: test-backend test-frontend

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend/core/auth && python -m pytest
	cd backend/core/payments && python -m pytest
	cd backend/core/analytics && python -m pytest
	cd backend/core/content_api && python -m pytest
	cd backend/core/chat && python -m pytest
	@echo "✅ Backend tests completed!"

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd frontend/creator_app && npm test
	cd frontend/fan_app && npm test
	cd frontend/web && npm test
	@echo "✅ Frontend tests completed!"

# Database operations
migrate:
	@echo "📊 Running database migrations..."
	cd database && ./migrate_db.sh
	@echo "✅ Database migrations completed!"

seed:
	@echo "🌱 Seeding database with sample data..."
	cd database && psql $(DATABASE_URL) -f seed_data.sql
	@echo "✅ Database seeded successfully!"

reset-db:
	@echo "⚠️  WARNING: This will destroy all data!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	cd database && psql $(DATABASE_URL) -f reset.sql
	$(MAKE) migrate
	$(MAKE) seed
	@echo "✅ Database reset completed!"

# Deployment
deploy-staging:
	@echo "🚀 Deploying to staging environment..."
	./scripts/deploy.sh staging
	@echo "✅ Staging deployment completed!"

deploy-production:
	@echo "🚀 Deploying to production environment..."
	@echo "⚠️  WARNING: Production deployment!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	./scripts/deploy.sh production
	@echo "✅ Production deployment completed!"

# Monitoring
logs:
	@echo "📋 Showing container logs..."
	docker-compose -f infra/docker-compose.yml logs -f

health:
	@echo "🏥 Checking service health..."
	curl -f http://localhost:8001/health && echo "✅ Auth service healthy"
	curl -f http://localhost:8002/health && echo "✅ Payment service healthy"
	curl -f http://localhost:8003/health && echo "✅ Analytics service healthy"
	curl -f http://localhost:8004/health && echo "✅ Content API healthy"
	curl -f http://localhost:8005/health && echo "✅ Chat service healthy"

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	docker-compose -f infra/docker-compose.yml down -v
	docker system prune -f
	@echo "✅ Cleanup completed!"

# Quick start
quickstart:
	@echo "⚡ Quick start - setting up everything..."
	cp .env.example .env
	@echo "📝 Please edit .env with your configuration"
	@echo "⚡ After editing .env, run: make dev"

# Development tools
format:
	@echo "💅 Formatting code..."
	cd backend && black . && isort .
	cd frontend && npm run format
	@echo "✅ Code formatted!"

lint:
	@echo "🔍 Linting code..."
	cd backend && flake8 . && mypy .
	cd frontend && npm run lint
	@echo "✅ Linting completed!"

# Documentation
docs:
	@echo "📚 Generating documentation..."
	cd docs && mkdocs build
	@echo "✅ Documentation generated!"

docs-serve:
	@echo "📚 Serving documentation locally..."
	cd docs && mkdocs serve

# SDK generation
generate-sdk:
	@echo "🔧 Generating client SDKs..."
	./scripts/generate_sdk.sh
	@echo "✅ SDKs generated!"

# Backup
backup:
	@echo "💾 Creating database backup..."
	pg_dump $(DATABASE_URL) > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created!"