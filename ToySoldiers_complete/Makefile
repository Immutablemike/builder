.PHONY: help setup dev-backend dev-frontend test migrate seed deploy-staging deploy-production

help:
	@echo "Toy Soldiers MVP Platform - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup              - Install all dependencies"
	@echo "  make migrate            - Run database migrations"
	@echo "  make seed               - Seed database with sample data"
	@echo ""
	@echo "Development:"
	@echo "  make dev-backend        - Start backend services"
	@echo "  make dev-frontend       - Start frontend development"
	@echo "  make dev                - Start all services"
	@echo ""
	@echo "Testing:"
	@echo "  make test               - Run all tests"
	@echo "  make test-backend       - Run backend tests"
	@echo "  make test-frontend      - Run frontend tests"
	@echo "  make lint               - Run linters"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy-staging     - Deploy to staging"
	@echo "  make deploy-production  - Deploy to production"
	@echo "  make build-backend      - Build backend Docker images"
	@echo "  make build-frontend     - Build frontend applications"

setup:
	@echo "Installing backend dependencies..."
	cd backend/core/auth && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend/creator_app && yarn install
	cd frontend/fan_app && yarn install
	@echo "Setup complete!"

dev-backend:
	docker-compose up -d

dev-frontend:
	cd frontend/creator_app && yarn start

dev:
	docker-compose up -d
	cd frontend/creator_app && yarn start

migrate:
	@echo "Running database migrations..."
	cd database && psql $(SUPABASE_URL) -f schema.sql

seed:
	@echo "Seeding database..."
	cd database && psql $(SUPABASE_URL) -f seed_data.sql

test:
	make test-backend
	make test-frontend

test-backend:
	cd backend/core/auth && pytest
	cd backend/core/payments && pytest
	cd backend/core/content_api && pytest

test-frontend:
	cd frontend/creator_app && yarn test
	cd frontend/fan_app && yarn test

lint:
	cd backend && flake8 .
	cd frontend/creator_app && yarn lint
	cd frontend/fan_app && yarn lint

build-backend:
	docker-compose build

build-frontend:
	cd frontend/creator_app && yarn build
	cd frontend/fan_app && yarn build

deploy-staging:
	./scripts/deploy.sh staging

deploy-production:
	./scripts/deploy.sh production

generate-sdk:
	./scripts/generate_sdk.sh

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name ".expo" -exec rm -rf {} +
