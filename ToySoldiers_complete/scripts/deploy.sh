#!/bin/bash

set -e

ENVIRONMENT=${1:-staging}

echo "Deploying to $ENVIRONMENT environment..."

if [ "$ENVIRONMENT" == "production" ]; then
  DOMAIN="app.toysoldiers.space"
  BACKEND_URL="https://api.toysoldiers.space"
elif [ "$ENVIRONMENT" == "staging" ]; then
  DOMAIN="staging.toysoldiers.space"
  BACKEND_URL="https://api-staging.toysoldiers.space"
else
  echo "Invalid environment. Use 'staging' or 'production'"
  exit 1
fi

echo "Building backend Docker images..."
docker-compose build

echo "Pushing images to registry..."
docker-compose push

echo "Deploying to Hetzner servers..."
ssh deploy@${DOMAIN} "cd /opt/toysoldiers && docker-compose pull && docker-compose up -d"

echo "Running database migrations..."
ssh deploy@${DOMAIN} "cd /opt/toysoldiers && docker-compose exec -T auth_service python -m alembic upgrade head"

echo "Building frontend..."
cd frontend/creator_app
yarn build
npx wrangler pages deploy dist --project-name toysoldiers-creator-${ENVIRONMENT}

cd ../fan_app
yarn build
npx wrangler pages deploy dist --project-name toysoldiers-fan-${ENVIRONMENT}

echo "Deployment to $ENVIRONMENT completed successfully!"

if [ "$ENVIRONMENT" == "production" ]; then
  echo "Notifying team..."
  curl -X POST $DISCORD_WEBHOOK \
    -H "Content-Type: application/json" \
    -d "{\"content\": \"🚀 Toy Soldiers deployed to production successfully!\"}"
fi
