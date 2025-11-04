#!/bin/bash

set -e

echo "Running linters on all code..."

echo "Linting backend Python code..."
cd backend
find . -name "*.py" -not -path "*/venv/*" -not -path "*/.venv/*" | xargs flake8 --max-line-length=120 --ignore=E501,W503

echo "Linting frontend TypeScript code..."
cd ../frontend/creator_app
yarn lint

cd ../fan_app
yarn lint

echo "Linting completed successfully!"
