from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from supabase import create_client, Client
import stripe
import os

class Settings(BaseSettings):
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    stripe_connect_client_id: str = os.getenv("STRIPE_CONNECT_CLIENT_ID", "")
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    class Config:
        env_file = ".env"

settings = Settings()

stripe.api_key = settings.stripe_secret_key

app = FastAPI(
    title="Toy Soldiers Payments Service",
    description="Payment processing, tipping, and subscription management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase: Client = create_client(settings.supabase_url, settings.supabase_service_role_key)

from routes import checkout, webhook, payouts

app.include_router(checkout.router, prefix="/payments", tags=["payments"])
app.include_router(webhook.router, prefix="/payments", tags=["webhooks"])
app.include_router(payouts.router, prefix="/payments", tags=["payouts"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "payments_service",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "service": "Toy Soldiers Payments Service",
        "status": "running",
        "endpoints": ["/payments/checkout", "/payments/webhook", "/payments/payouts"]
    }
