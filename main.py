from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import APIException
from app.api import auth, tasks, debug


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Las tablas se crean con Alembic migrations
    # Base.metadata.create_all(bind=engine)  # Comentado - usar Alembic
    yield
    # Shutdown: Add cleanup code here if needed


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="API para gestión de tareas con autenticación JWT",
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,  # Mantiene el token entre recargas
    }
)

# Configure CORS - Usar orígenes específicos desde settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # Orígenes específicos desde config.py
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


# Exception handler for custom API exceptions
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": exc.success,
            "message": exc.message,
            "data": exc.data
        }
    )


# Exception handler for Pydantic validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
        error_type = error["type"]
        
        # Personalizar mensajes según el tipo de error
        if error_type == "missing":
            message = f"El campo '{field}' es obligatorio y no puede estar vacío"
        elif error_type == "string_too_short":
            min_length = error.get("ctx", {}).get("min_length", "")
            message = f"El campo '{field}' debe tener al menos {min_length} caracteres"
        elif error_type == "value_error.email":
            message = f"El campo '{field}' debe ser un correo electrónico válido"
        elif error_type == "string_type":
            message = f"El campo '{field}' debe ser texto"
        else:
            message = f"El campo '{field}' tiene un error: {error.get('msg', 'valor inválido')}"
        
        errors.append(message)
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Errores de validación: " + "; ".join(errors),
            "data": {"errors": errors}
        }
    )


# Exception handler for HTTPException (FastAPI default)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Personalizar mensajes de autenticación
    message = exc.detail
    
    if exc.status_code == 401:
        if isinstance(exc.detail, str):
            if "Not authenticated" in exc.detail:
                message = "No autenticado. Por favor inicie sesión."
            elif "token" in exc.detail.lower():
                message = "Token inválido o expirado. Por favor inicie sesión nuevamente."
            else:
                message = exc.detail
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": message,
            "data": None
        }
    )


# Exception handler for general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Error interno del servidor",
            "data": None
        }
    )


# Health check endpoint
@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Task Management API is running",
        "data": {
            "version": "1.0.0",
            "api_prefix": settings.API_V1_STR
        }
    }


@app.get("/health")
async def health_check():
    return {
        "success": True,
        "message": "API is healthy",
        "data": {"status": "ok"}
    }


# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Authentication"]
)

app.include_router(
    tasks.router,
    prefix=f"{settings.API_V1_STR}/tasks",
    tags=["Tasks"]
)

# Debug router (temporal - remover en producción)
app.include_router(
    debug.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["Debug"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
