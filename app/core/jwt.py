from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import UnauthorizedException
from app.models.models import User

# Configurar HTTPBearer con auto_error=False para manejar errores personalizados
security = HTTPBearer(
    scheme_name="Bearer",
    description="Ingrese el token JWT en el formato: Bearer {token}",
    auto_error=True
)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException(message="El token ha expirado. Por favor inicie sesión nuevamente.")
    except JWTError as e:
        raise UnauthorizedException(message=f"Token inválido: {str(e)}")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    
    # Decodificar el token (esto ya maneja las excepciones)
    payload = decode_token(token)
    
    # Verify it's an access token
    if payload.get("type") != "access":
        raise UnauthorizedException(message="Tipo de token inválido")
    
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise UnauthorizedException(message="Token inválido: no contiene ID de usuario")
    
    # Convertir sub (string) a int
    try:
        user_id = int(user_id_str)
    except (ValueError, TypeError):
        raise UnauthorizedException(message="Token inválido: ID de usuario no válido")
    
    # Buscar usuario en la base de datos
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise UnauthorizedException(message="Usuario no encontrado")
    
    return user


def verify_refresh_token(token: str) -> Dict[str, Any]:
    """Verify refresh token and return payload"""
    payload = decode_token(token)
    
    # Verify it's a refresh token
    if payload.get("type") != "refresh":
        raise UnauthorizedException(message="Tipo de token inválido")
    
    return payload
