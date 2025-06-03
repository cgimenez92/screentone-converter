"""
Color Blindness Assistance API
A FastAPI application providing screentone processing and color inspection services.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from app.config import get_settings
from app.api.v1 import screentone, color_inspector
from app.core.exceptions import APIException

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""

    settings = get_settings()
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.output_dir, exist_ok=True)
    yield


def create_app() -> FastAPI:
    """Application factory"""
    settings = get_settings()
    
    app = FastAPI(
                    title="Color Blindness Assistance API",
                    description="API for screentone processing and color inspection to assist color blind users",
                    version="1.0.0",
                    docs_url="/docs" if settings.environment == "development" else None,
                    redoc_url="/redoc" if settings.environment == "development" else None,
                    lifespan=lifespan
                )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts
    )

    # Exception handlers
    app.add_exception_handler(APIException)

    # Routers
    app.include_router(screentone.router, prefix="/api/v1/screentone", tags=["screentone"])
    app.include_router(color_inspector.router, prefix="/api/v1/colors", tags=["colors"])

    return app

app = create_app()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
                "app.main:app",
                host=settings.host,
                port=settings.port,
                reload=settings.environment == "development"                
                )