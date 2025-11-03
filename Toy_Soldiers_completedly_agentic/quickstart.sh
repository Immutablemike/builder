#!/bin/bash
set -e

echo "🚀 ToySoldiers Platform Quick Start"
echo "=================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration before continuing!"
    echo "   Required: DATABASE_URL, STRIPE keys, SUPABASE credentials"
    echo ""
    echo "📖 Run './quickstart.sh' again after configuring .env"
    exit 1
fi

echo "✅ Environment file found"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Load environment variables
source .env

# Start PostgreSQL and Redis
echo "🗄️  Starting database services..."
docker-compose -f infra/docker-compose.yml up -d postgres redis

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run database migrations
echo "📊 Setting up database..."
if command -v psql > /dev/null; then
    psql $DATABASE_URL -f database/schema.sql
    echo "✅ Database schema created"
    
    psql $DATABASE_URL -f database/seed_data.sql
    echo "✅ Sample data loaded"
else
    echo "⚠️  psql not found. Please install PostgreSQL client or run migrations manually:"
    echo "   psql $DATABASE_URL -f database/schema.sql"
    echo "   psql $DATABASE_URL -f database/seed_data.sql"
fi

# Start backend services
echo "🔧 Starting backend services..."
docker-compose -f infra/docker-compose.yml up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 15

# Health check
echo "🏥 Checking service health..."
services=("auth:8001" "payments:8002" "analytics:8003" "content_api:8004" "chat:8005")

for service in "${services[@]}"; do
    name=${service%:*}
    port=${service#*:}
    if curl -f http://localhost:$port/health > /dev/null 2>&1; then
        echo "✅ $name service healthy"
    else
        echo "⚠️  $name service not responding (this is normal on first startup)"
    fi
done

echo ""
echo "🎉 ToySoldiers Platform Started Successfully!"
echo "==========================================="
echo ""
echo "🌐 Web Interfaces:"
echo "   API Gateway:     http://localhost:8000"
echo "   Creator App:     http://localhost:19006"
echo "   Fan App:         http://localhost:19007"
echo "   Web Dashboard:   http://localhost:3000"
echo ""
echo "🔧 Backend Services:"
echo "   Auth Service:    http://localhost:8001"
echo "   Payment Service: http://localhost:8002"
echo "   Analytics:       http://localhost:8003"
echo "   Content API:     http://localhost:8004"
echo "   Chat Service:    http://localhost:8005"
echo ""
echo "🗄️  Database:"
echo "   PostgreSQL:      localhost:5432"
echo "   Redis:           localhost:6379"
echo ""
echo "📚 Next Steps:"
echo "   1. Install frontend dependencies:"
echo "      cd frontend/creator_app && npm install"
echo "      cd frontend/fan_app && npm install"
echo "      cd frontend/web && npm install"
echo ""
echo "   2. Start mobile apps:"
echo "      cd frontend/creator_app && npm start"
echo "      cd frontend/fan_app && npm start"
echo ""
echo "   3. Start web dashboard:"
echo "      cd frontend/web && npm run dev"
echo ""
echo "   4. View logs:"
echo "      make logs"
echo ""
echo "   5. Stop everything:"
echo "      make clean"
echo ""
echo "🚀 Happy coding!"