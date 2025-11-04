from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from pydantic_settings import BaseSettings
from posthog import Posthog
import os

class Settings(BaseSettings):
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    posthog_api_key: str = os.getenv("POSTHOG_API_KEY", "")
    
    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI(
    title="Toy Soldiers Auth Service",
    description="Authentication and authorization service for Toy Soldiers platform",
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
posthog_client = Posthog(settings.posthog_api_key, host='https://app.posthog.com')

from routes import signup, login, profile

app.include_router(signup.router, prefix="/auth", tags=["authentication"])
app.include_router(login.router, prefix="/auth", tags=["authentication"])
app.include_router(profile.router, prefix="/auth", tags=["profile"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "auth_service",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "service": "Toy Soldiers Auth Service",
        "status": "running",
        "endpoints": ["/auth/signup", "/auth/login", "/auth/profile", "/auth/logout"]
    }
