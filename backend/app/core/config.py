from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/workflow_db"
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    SERPAPI_API_KEY: Optional[str] = None
    
    # ChromaDB Configuration
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Upload
    MAX_FILE_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"

settings = Settings()

