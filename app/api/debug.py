from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.jwt import get_current_user, decode_token
from app.core.response import success_response
from app.models.models import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()


@router.get("/debug/token")
def debug_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Endpoint de debug para verificar el token"""
    token = credentials.credentials
    
    try:
        # Decodificar sin verificar expiración
        from jose import jwt
        from app.core.config import settings
        
        payload_no_verify = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": False}
        )
        
        # Información del token
        exp_timestamp = payload_no_verify.get("exp")
        exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc) if exp_timestamp else None
        now = datetime.now(timezone.utc)
        
        token_info = {
            "token_preview": token[:30] + "...",
            "payload": payload_no_verify,
            "current_time_utc": str(now),
            "token_expires_utc": str(exp_time) if exp_time else None,
            "is_expired": (exp_time < now) if exp_time else None,
            "time_remaining_minutes": ((exp_time - now).total_seconds() / 60) if exp_time else None,
        }
        
        # Intentar decodificar con verificación
        try:
            payload_verified = decode_token(token)
            token_info["verification"] = "✅ Token válido"
            token_info["verified_payload"] = payload_verified
            
            # Buscar usuario
            user_id = payload_verified.get("sub")
            if user_id:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    token_info["user_found"] = True
                    token_info["user_id"] = user.id
                    token_info["user_email"] = user.email
                else:
                    token_info["user_found"] = False
                    token_info["error"] = "Usuario no encontrado en BD"
        except Exception as e:
            token_info["verification"] = f"❌ Error: {str(e)}"
        
        return success_response(
            message="Información de debug del token",
            data=token_info
        )
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error al decodificar token: {str(e)}",
            "data": None
        }


@router.get("/debug/me")
def debug_me(current_user: User = Depends(get_current_user)):
    """Endpoint de debug que usa get_current_user"""
    return success_response(
        message="Usuario autenticado correctamente",
        data={
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email
        }
    )


@router.get("/debug/config")
def debug_config():
    """Ver configuración JWT"""
    from app.core.config import settings
    
    return success_response(
        message="Configuración JWT",
        data={
            "algorithm": settings.ALGORITHM,
            "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "refresh_token_expire_days": settings.REFRESH_TOKEN_EXPIRE_DAYS,
            "secret_key_length": len(settings.SECRET_KEY)
        }
    )
