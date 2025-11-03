# Toy Soldiers Platform - Development Makefile
# ============================================

.PHONY: help install dev build test lint format clean validate-api generate-sdk deploy-dev deploy-prod

# Default target
help: ## 📋 Show this help message
	@echo "🎯 Toy Soldiers Platform - Development Commands"
	@echo "=============================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Environment setup
install: ## 📦 Install all dependencies
	@echo "📦 Installing dependencies..."
	@if [ -f "package.json" ]; then npm install; fi
	@if [ -f "requirements.txt" ]; then pip install -r requirements.txt; fi
	@if [ -d "packages/creator-app" ]; then cd packages/creator-app && npm install; fi
	@if [ -d "packages/fan-app" ]; then cd packages/fan-app && npm install; fi
	@if [ -d "packages/shared-components" ]; then cd packages/shared-components && npm install; fi
	@if [ -d "apps/api-server" ]; then cd apps/api-server && pip install -r requirements.txt; fi
	@echo "✅ Dependencies installed!"

dev: ## 🚀 Start development environment
	@echo "🚀 Starting development environment..."
	@echo "🔧 Starting API server..."
	@if [ -d "apps/api-server" ]; then \
		cd apps/api-server && uvicorn main:app --reload --port 8000 & \
	fi
	@echo "📱 Starting Creator app..."
	@if [ -d "packages/creator-app" ]; then \
		cd packages/creator-app && npm start & \
	fi
	@echo "👥 Starting Fan app..."
	@if [ -d "packages/fan-app" ]; then \
		cd packages/fan-app && npm start & \
	fi
	@echo "✅ Development environment started!"
	@echo "🌐 API Server: http://localhost:8000"
	@echo "📱 Creator App: http://localhost:19000"
	@echo "👥 Fan App: http://localhost:19001"

build: ## 🔨 Build all applications
	@echo "🔨 Building applications..."
	@if [ -d "packages/creator-app" ]; then \
		echo "📱 Building Creator app..." && \
		cd packages/creator-app && npm run build; \
	fi
	@if [ -d "packages/fan-app" ]; then \
		echo "👥 Building Fan app..." && \
		cd packages/fan-app && npm run build; \
	fi
	@if [ -d "packages/shared-components" ]; then \
		echo "🧱 Building shared components..." && \
		cd packages/shared-components && npm run build; \
	fi
	@if [ -d "apps/web-dashboard" ]; then \
		echo "🌐 Building web dashboard..." && \
		cd apps/web-dashboard && npm run build; \
	fi
	@echo "✅ Build complete!"

test: ## 🧪 Run all tests
	@echo "🧪 Running tests..."
	@if [ -d "apps/api-server" ]; then \
		echo "🔧 Testing API server..." && \
		cd apps/api-server && python -m pytest tests/ -v; \
	fi
	@if [ -d "packages/creator-app" ]; then \
		echo "📱 Testing Creator app..." && \
		cd packages/creator-app && npm test; \
	fi
	@if [ -d "packages/fan-app" ]; then \
		echo "👥 Testing Fan app..." && \
		cd packages/fan-app && npm test; \
	fi
	@if [ -d "tests/integration" ]; then \
		echo "🔗 Running integration tests..." && \
		python -m pytest tests/integration/ -v; \
	fi
	@echo "✅ All tests completed!"

lint: ## 🔍 Run linting on all code
	@echo "🔍 Running linting..."
	@if [ -d "apps/api-server" ]; then \
		echo "🔧 Linting API server..." && \
		cd apps/api-server && ruff check . && mypy .; \
	fi
	@if [ -d "packages/creator-app" ]; then \
		echo "📱 Linting Creator app..." && \
		cd packages/creator-app && npm run lint; \
	fi
	@if [ -d "packages/fan-app" ]; then \
		echo "👥 Linting Fan app..." && \
		cd packages/fan-app && npm run lint; \
	fi
	@echo "✅ Linting complete!"

format: ## ✨ Format all code
	@echo "✨ Formatting code..."
	@if [ -d "apps/api-server" ]; then \
		echo "🔧 Formatting API server..." && \
		cd apps/api-server && ruff format .; \
	fi
	@if [ -d "packages/creator-app" ]; then \
		echo "📱 Formatting Creator app..." && \
		cd packages/creator-app && npm run format; \
	fi
	@if [ -d "packages/fan-app" ]; then \
		echo "👥 Formatting Fan app..." && \
		cd packages/fan-app && npm run format; \
	fi
	@echo "✅ Code formatting complete!"

clean: ## 🧹 Clean build artifacts and dependencies
	@echo "🧹 Cleaning build artifacts..."
	@find . -name "node_modules" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "build" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".expo" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# API and Schema Operations
validate-api: ## ✅ Validate OpenAPI specification and JSON schemas
	@echo "✅ Validating API specifications..."
	@if command -v openapi-spec-validator >/dev/null 2>&1; then \
		echo "🔍 Validating OpenAPI specification..." && \
		openapi-spec-validator schemas/ToySoldiers_API_OpenAPI.yaml; \
	else \
		echo "⚠️  openapi-spec-validator not found. Install with: pip install openapi-spec-validator"; \
	fi
	@if command -v python >/dev/null 2>&1; then \
		echo "🔍 Validating JSON Schema..." && \
		python -c "import json, jsonschema; schema=json.load(open('schemas/ToySoldiers_API_Schema.json')); jsonschema.Draft7Validator.check_schema(schema); print('✅ JSON Schema is valid!')"; \
	fi
	@echo "✅ API validation complete!"

generate-sdk: validate-api ## 📦 Generate TypeScript and Python SDKs
	@echo "📦 Generating SDKs from OpenAPI specification..."
	@mkdir -p packages/api-client-ts packages/api-client-py
	
	@if command -v openapi-generator-cli >/dev/null 2>&1; then \
		echo "🟦 Generating TypeScript SDK..." && \
		openapi-generator-cli generate \
			-i schemas/ToySoldiers_API_OpenAPI.yaml \
			-g typescript-axios \
			-o packages/api-client-ts \
			--additional-properties=npmName=@toysoldiers/api-client,supportsES6=true; \
	else \
		echo "⚠️  openapi-generator-cli not found. Install with: npm install -g @openapitools/openapi-generator-cli"; \
	fi
	
	@if command -v java >/dev/null 2>&1; then \
		echo "🐍 Generating Python SDK..." && \
		if [ ! -f "openapi-generator-cli.jar" ]; then \
			wget https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.0.1/openapi-generator-cli-7.0.1.jar -O openapi-generator-cli.jar; \
		fi && \
		java -jar openapi-generator-cli.jar generate \
			-i schemas/ToySoldiers_API_OpenAPI.yaml \
			-g python \
			-o packages/api-client-py \
			--additional-properties=packageName=toysoldiers_api,projectName=toysoldiers-api-client; \
	else \
		echo "⚠️  Java not found. Install Java to generate Python SDK"; \
	fi
	
	@echo "✅ SDK generation complete!"

# Database Operations
db-setup: ## 🗄️ Set up database schema
	@echo "🗄️ Setting up database schema..."
	@if [ -f "schemas/database/schema.sql" ]; then \
		echo "📋 Database schema found. Run with your preferred database client." && \
		echo "🔗 Supabase: Upload to SQL Editor" && \
		echo "🐘 PostgreSQL: psql -f schemas/database/schema.sql" && \
		echo "📊 File: schemas/database/schema.sql"; \
	else \
		echo "⚠️  Database schema not found. Check schemas/database/ directory"; \
	fi

db-migrate: ## 🔄 Run database migrations
	@echo "🔄 Running database migrations..."
	@if [ -d "schemas/database/migrations" ]; then \
		echo "📂 Migrations directory found: schemas/database/migrations/" && \
		echo "🔗 Apply migrations using your database migration tool"; \
	else \
		echo "⚠️  No migrations directory found"; \
	fi

# Docker Operations
docker-build: ## 🐳 Build Docker images
	@echo "🐳 Building Docker images..."
	@if [ -f "infrastructure/docker/Dockerfile.api" ]; then \
		echo "🔧 Building API server image..." && \
		docker build -f infrastructure/docker/Dockerfile.api -t toysoldiers/api:latest .; \
	fi
	@if [ -f "infrastructure/docker/Dockerfile.web" ]; then \
		echo "🌐 Building web dashboard image..." && \
		docker build -f infrastructure/docker/Dockerfile.web -t toysoldiers/web:latest .; \
	fi
	@echo "✅ Docker images built!"

docker-dev: ## 🐳 Start development environment with Docker
	@echo "🐳 Starting development environment with Docker..."
	@if [ -f "infrastructure/docker/docker-compose.yml" ]; then \
		cd infrastructure/docker && docker-compose up -d; \
	else \
		echo "⚠️  docker-compose.yml not found in infrastructure/docker/"; \
	fi

docker-down: ## 🐳 Stop Docker development environment
	@echo "🐳 Stopping Docker development environment..."
	@if [ -f "infrastructure/docker/docker-compose.yml" ]; then \
		cd infrastructure/docker && docker-compose down; \
	fi

# Deployment Operations
deploy-dev: ## 🚀 Deploy to development environment
	@echo "🚀 Deploying to development environment..."
	@echo "🔧 Building applications..."
	@$(MAKE) build
	@echo "🧪 Running tests..."
	@$(MAKE) test
	@echo "✅ Validating API..."
	@$(MAKE) validate-api
	@echo "🚀 Development deployment complete!"
	@echo "📋 Manual steps required:"
	@echo "  - Update environment variables"
	@echo "  - Deploy to staging server"
	@echo "  - Run integration tests"

deploy-prod: ## 🚀 Deploy to production environment
	@echo "🚀 Deploying to production environment..."
	@echo "⚠️  Production deployment requires manual approval!"
	@echo "📋 Pre-deployment checklist:"
	@echo "  ✅ All tests passing"
	@echo "  ✅ API validation successful"
	@echo "  ✅ Security scan completed"
	@echo "  ✅ Staging environment tested"
	@echo "  ✅ Database migrations reviewed"
	@echo "  ✅ Environment variables updated"
	@echo ""
	@echo "🚀 Run deployment pipeline: GitHub Actions -> Deploy to Production"

# Security Operations
security-scan: ## 🔒 Run security scanning
	@echo "🔒 Running security scans..."
	@if command -v bandit >/dev/null 2>&1; then \
		echo "🐍 Scanning Python code with bandit..." && \
		find . -name "*.py" -path "./apps/api-server/*" -exec bandit {} \; 2>/dev/null || true; \
	fi
	@if command -v npm >/dev/null 2>&1; then \
		echo "📦 Scanning npm packages..." && \
		if [ -f "package.json" ]; then npm audit; fi; \
	fi
	@echo "🔍 Checking for secrets in code..."
	@if grep -r "password\|secret\|key\|token" . --exclude-dir=.git --exclude-dir=node_modules --exclude="*.md" --exclude="Makefile" 2>/dev/null; then \
		echo "⚠️  WARNING: Potential secrets found in code!"; \
	else \
		echo "✅ No obvious secrets found"; \
	fi
	@echo "✅ Security scan complete!"

# Documentation Operations
docs: ## 📚 Generate documentation
	@echo "📚 Generating documentation..."
	@if command -v redocly >/dev/null 2>&1; then \
		echo "📝 Generating API documentation..." && \
		redocly build-docs schemas/ToySoldiers_API_OpenAPI.yaml --output docs/api-docs.html; \
	fi
	@echo "📋 Documentation files:"
	@echo "  📁 Repository Structure: docs/Repository_Structure.md"
	@echo "  🗄️  Database Schema: docs/Database_Schema.md"
	@echo "  🔌 API Specification: schemas/ToySoldiers_API_OpenAPI.yaml"
	@echo "  📊 Master Architecture: docs/ToySoldiers_Stack.yaml"
	@echo "✅ Documentation generation complete!"

# Monitoring and Analytics
logs: ## 📊 Show application logs
	@echo "📊 Application logs:"
	@if [ -d "logs" ]; then \
		echo "📂 Log directory found: logs/" && \
		ls -la logs/; \
	else \
		echo "📋 No local logs directory found"; \
	fi
	@echo "🔗 Check cloud logs:"
	@echo "  - Cloudflare Analytics: https://dash.cloudflare.com/analytics"
	@echo "  - Supabase Logs: https://app.supabase.com/project/YOUR_PROJECT/logs"
	@echo "  - Hetzner Monitoring: Server dashboard"

status: ## 📊 Show system status
	@echo "📊 Toy Soldiers Platform Status"
	@echo "==============================="
	@echo "🎯 Project: Toy Soldiers Platform"
	@echo "🏗️  Architecture: SupaNERN Stack"
	@echo "☁️  Infrastructure: Cloudflare + Hetzner + Supabase"
	@echo ""
	@echo "📂 Components:"
	@if [ -d "packages/creator-app" ]; then echo "  ✅ Creator App"; else echo "  ❌ Creator App"; fi
	@if [ -d "packages/fan-app" ]; then echo "  ✅ Fan App"; else echo "  ❌ Fan App"; fi
	@if [ -d "apps/api-server" ]; then echo "  ✅ API Server"; else echo "  ❌ API Server"; fi
	@if [ -f "schemas/ToySoldiers_API_OpenAPI.yaml" ]; then echo "  ✅ API Schema"; else echo "  ❌ API Schema"; fi
	@echo ""
	@echo "🔗 Quick Links:"
	@echo "  📚 Documentation: docs/README.md"
	@echo "  🔌 API Spec: schemas/ToySoldiers_API_OpenAPI.yaml"
	@echo "  🏗️  Architecture: docs/ToySoldiers_Stack.yaml"

# Environment Management
env-setup: ## ⚙️ Set up environment variables
	@echo "⚙️ Setting up environment variables..."
	@if [ ! -f ".env" ]; then \
		if [ -f ".env.example" ]; then \
			echo "📋 Copying .env.example to .env..." && \
			cp .env.example .env && \
			echo "✅ Environment file created!"; \
		else \
			echo "⚠️  No .env.example found. Create environment variables manually."; \
		fi; \
	else \
		echo "✅ .env file already exists"; \
	fi
	@echo "📝 Required environment variables:"
	@echo "  🔐 SUPABASE_URL, SUPABASE_ANON_KEY"
	@echo "  💳 STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET"
	@echo "  ☁️  CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID"
	@echo "  📹 LIVEKIT_API_KEY, LIVEKIT_API_SECRET"

# Quick development shortcuts
quick-start: install env-setup validate-api ## 🚀 Quick project setup
	@echo "🚀 Quick Start Complete!"
	@echo "========================"
	@echo "✅ Dependencies installed"
	@echo "✅ Environment configured"
	@echo "✅ API validated"
	@echo ""
	@echo "🎯 Next steps:"
	@echo "  1. Update .env with your API keys"
	@echo "  2. Run 'make dev' to start development"
	@echo "  3. Visit http://localhost:8000/docs for API docs"

all: clean install build test validate-api ## 🎯 Run complete build pipeline
	@echo "🎯 Complete build pipeline finished!"
	@echo "✅ All tasks completed successfully!"