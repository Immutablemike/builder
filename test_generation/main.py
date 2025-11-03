"""
Toy Soldiers MVP Platform - FastAPI Backend
Main application entry point with basic health check and info endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

app = FastAPI(
    title="Toy Soldiers API",
    description="Full-stack modular content streaming and monetization platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str


class PlatformInfo(BaseModel):
    name: str
    description: str
    version: str
    services: List[str]
    deployment_targets: List[str]


@app.get("/", tags=["General"])
async def root() -> Dict[str, str]:
    """Root endpoint - Welcome message"""
    return {
        "message": "Welcome to Toy Soldiers API",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse, tags=["General"])
async def health_check() -> HealthResponse:
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="0.1.0"
    )


@app.get("/info", response_model=PlatformInfo, tags=["General"])
async def platform_info() -> PlatformInfo:
    """Get platform information and architecture overview"""
    return PlatformInfo(
        name="Toy Soldiers MVP Platform",
        description="Full-stack modular content streaming and monetization platform combining Spotify (audio), YouTube (video), and Patreon (creator funding) paradigms.",
        version="0.1.0",
        services=[
            "auth_service",
            "payments_service",
            "analytics_service",
            "content_api",
            "chat_service",
            "upload_service",
            "dashboard_service",
            "discovery_service",
            "interaction_service"
        ],
        deployment_targets=[
            "Hetzner (Core Backend)",
            "Cloudflare (CDN, R2, Workers, Stream)",
            "Supabase (PostgreSQL, Auth, Realtime)",
            "LiveKit (Live Streaming)"
        ]
    )


@app.get("/api/status", tags=["API"])
async def api_status():
    """API status with basic service information"""
    return {
        "api_version": "0.1.0",
        "framework": "FastAPI",
        "runtime": "Python 3.11+",
        "environment": "development",
        "endpoints": {
            "health": "/health",
            "info": "/info",
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        "core_services_planned": [
            "/api/auth",
            "/api/payments",
            "/api/analytics",
            "/api/content",
            "/api/chat"
        ],
        "creator_services_planned": [
            "/api/creator/upload",
            "/api/creator/dashboard",
            "/api/creator/profile"
        ],
        "fan_services_planned": [
            "/api/fan/discovery",
            "/api/fan/interaction"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
