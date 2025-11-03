# Toy Soldiers MVP Platform - Test Backend

Basic FastAPI backend structure for the Toy Soldiers platform based on the architecture defined in `ToySoldiers_Stack.yaml`.

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Start the development server
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

Once running, the API will be available at `http://localhost:8000`

- **Root**: `GET /` - Welcome message
- **Health Check**: `GET /health` - Service health status
- **Platform Info**: `GET /info` - Platform architecture overview
- **API Status**: `GET /api/status` - API version and planned services
- **Interactive Docs**: `http://localhost:8000/docs` - Swagger UI
- **ReDoc**: `http://localhost:8000/redoc` - Alternative documentation

## Architecture Overview

This is a minimal implementation showcasing the foundation for:

### Core Services (Planned)
- **auth_service**: Supabase JWT verification, session management
- **payments_service**: Stripe Connect integration
- **analytics_service**: PostHog + metrics ingestion
- **content_api**: CRUD for content + streaming URLs
- **chat_service**: Comments + live chat

### Creator Services (Planned)
- **upload_service**: Media upload to Cloudflare R2
- **dashboard_service**: Analytics and earnings
- **profile_service**: Creator profile management

### Fan Services (Planned)
- **discovery_service**: Content feed and recommendations
- **interaction_service**: Comments, tips, subscriptions

## Technology Stack

- **Framework**: FastAPI
- **Runtime**: Python 3.11+
- **ASGI Server**: Uvicorn
- **Validation**: Pydantic v2
- **Documentation**: OpenAPI 3.1 (auto-generated)

## Next Steps

1. Implement authentication with Supabase
2. Add database models and connections
3. Create service-specific routers
4. Integrate Cloudflare R2 for storage
5. Add PostHog analytics tracking
6. Implement Stripe payment processing

## Configuration

Environment variables will be needed for:
- `SUPABASE_URL` and `SUPABASE_KEY`
- `STRIPE_SECRET_KEY`
- `CLOUDFLARE_*` credentials
- `POSTHOG_API_KEY`

See `ToySoldiers_Stack.yaml` for complete environment variable requirements.
