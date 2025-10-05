from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, verify_password
from app.core.jwt import create_access_token, create_refresh_token, verify_refresh_token
from app.core.exceptions import BadRequestException, UnauthorizedException, ConflictException
from app.core.response import success_response
from app.models.models import User
from app.schemas.schemas import UserCreate, UserResponse, LoginRequest, TokenResponse, RefreshTokenRequest

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise ConflictException(message="El correo electrónico ya está registrado")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    user_response = UserResponse.model_validate(new_user)
    
    return success_response(
        message="Usuario registrado exitosamente",
        data=user_response.model_dump()
    )


@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Login user and return access and refresh tokens"""
    
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise UnauthorizedException(message="Correo electrónico o contraseña incorrectos")
    
    # Create tokens (sub debe ser string)
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    token_response = TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
    
    return success_response(
        message="Inicio de sesión exitoso",
        data=token_response.model_dump()
    )


@router.post("/refresh")
def refresh_token(token_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    
    # Verify refresh token
    payload = verify_refresh_token(token_data.refresh_token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise UnauthorizedException(message="Token inválido")
    
    # Verify user exists (convertir user_id a int si es string)
    user_id_int = int(user_id) if isinstance(user_id, str) else user_id
    user = db.query(User).filter(User.id == user_id_int).first()
    if not user:
        raise UnauthorizedException(message="Usuario no encontrado")
    
    # Create new access token (sub debe ser string)
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return success_response(
        message="Token renovado exitosamente",
        data={"access_token": access_token, "token_type": "bearer"}
    )
