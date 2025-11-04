from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from supabase import create_client, Client
import boto3
import os

class Settings(BaseSettings):
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_service_role_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    cloudflare_account_id: str = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    cloudflare_r2_access_key: str = os.getenv("CLOUDFLARE_R2_ACCESS_KEY", "")
    cloudflare_r2_secret_key: str = os.getenv("CLOUDFLARE_R2_SECRET_KEY", "")
    r2_bucket_audio: str = os.getenv("R2_BUCKET_AUDIO", "toysoldiers-audio")
    r2_bucket_video: str = os.getenv("R2_BUCKET_VIDEO", "toysoldiers-video")
    r2_bucket_thumbnails: str = os.getenv("R2_BUCKET_THUMBNAILS", "toysoldiers-thumbnails")
    
    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI(
    title="Toy Soldiers Content API",
    description="Content management, upload, and streaming service",
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

r2_client = boto3.client(
    's3',
    endpoint_url=f'https://{settings.cloudflare_account_id}.r2.cloudflarestorage.com',
    aws_access_key_id=settings.cloudflare_r2_access_key,
    aws_secret_access_key=settings.cloudflare_r2_secret_key
)

from routes import upload, feed, player, analytics

app.include_router(upload.router, prefix="/content", tags=["content"])
app.include_router(feed.router, prefix="/content", tags=["feed"])
app.include_router(player.router, prefix="/content", tags=["player"])
app.include_router(analytics.router, prefix="/content", tags=["analytics"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "content_api",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "service": "Toy Soldiers Content API",
        "status": "running",
        "endpoints": ["/content/upload", "/content/feed", "/content/player", "/content/analytics"]
    }
