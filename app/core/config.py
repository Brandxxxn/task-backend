from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT Configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task Management API"
    DEBUG: bool = True
    
    # CORS - Variable opcional para override desde .env
    BACKEND_CORS_ORIGINS: Optional[str] = None
    
    @property
    def cors_origins(self) -> list[str]:
        """
        Obtener lista de orígenes CORS permitidos.
        Si BACKEND_CORS_ORIGINS está definido en .env, parsear la cadena separada por comas.
        Si no, usar valores por defecto.
        """
        if self.BACKEND_CORS_ORIGINS:
            # Parsear desde variable de entorno (separado por comas)
            return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",")]
        else:
            # Valores por defecto
            return [
                "http://localhost:3000",
                "http://localhost:8000", 
                "https://task-front-iota.vercel.app",
                "https://task-backend-production-f92e.up.railway.app"
            ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'  # Cambiado de 'forbid' a 'ignore'
    )

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()