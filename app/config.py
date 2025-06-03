"""Application configuration management"""

from typing import List
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_keys: List[str] = Field(default_factory=list, description="Valid API keys")
    environment: str = Field(default="production", description="Environment (development/production)")
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Host to bind to")
    port: int = Field(default=8000, description="Port to bind to")
    
    # Security
    allowed_origins: List[str] = Field(default=["*"], description="CORS allowed origins")
    allowed_hosts: List[str] = Field(default=["*"], description="Trusted hosts")
    
    # File handling
    upload_dir: str = Field(default="uploads", description="Upload directory")
    output_dir: str = Field(default="outputs", description="Output directory")
    max_file_size: int = Field(default=10485760, description="Max file size in bytes (10MB)")
    allowed_extensions: List[str] = Field(
                                            default=[".jpg", ".jpeg", ".png", ".bmp", ".webp"],
                                            description="Allowed file extensions"
                                        )

    class Config:
        env_file = ".env"
        case_sensitive = False
        
    def validate_api_key(self, api_key: str) -> bool:
        """Validate API key"""
        return api_key in self.api_keys if self.api_keys else True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
