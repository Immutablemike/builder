#!/bin/bash

set -e

echo "Running database migrations..."

ENVIRONMENT=${1:-development}

if [ "$ENVIRONMENT" == "production" ]; then
  DB_URL=$SUPABASE_URL_PRODUCTION
elif [ "$ENVIRONMENT" == "staging" ]; then
  DB_URL=$SUPABASE_URL_STAGING
else
  DB_URL=$SUPABASE_URL
fi

echo "Environment: $ENVIRONMENT"
echo "Database: $DB_URL"

echo "Applying schema..."
psql $DB_URL < ./database/schema.sql

if [ "$ENVIRONMENT" == "development" ]; then
  echo "Seeding database with sample data..."
  psql $DB_URL < ./database/seed_data.sql
fi

echo "Running migration scripts..."
for migration in ./database/migrations/*.sql; do
  if [ -f "$migration" ]; then
    echo "Applying migration: $migration"
    psql $DB_URL < "$migration"
  fi
done

echo "Database migrations completed successfully!"
