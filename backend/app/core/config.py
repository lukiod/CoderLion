from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str  # Used by database.py
    postgres_url: str
    postgres_user: str
    postgres_host: str
    postgres_password: str
    postgres_database: str
    postgres_prisma_url: str
    postgres_url_non_pooling: str
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Security
    secret_key: str  # Used by auth.py
    algorithm: str = "HS256"  # Used by auth.py
    access_token_expire_minutes: int = 30  # Used by auth.py
    
    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    supabase_jwt_secret: str
    
    # Frontend
    next_public_supabase_url: str
    next_public_supabase_anon_key: str
    
    # GitHub OAuth
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    
    # Gemini AI
    gemini_api_key: Optional[str] = None  # Used by gemini.py
    
    # App
    app_name: str = "CodeLion"
    debug: bool = False
    node_env: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
