from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


# Enum para estados de tareas
class TaskStatus(str, Enum):
    PLANIFICADO = "planificado"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario", examples=["juan.perez@example.com"])
    name: str = Field(..., min_length=1, max_length=255, description="Nombre completo del usuario", examples=["Juan Pérez"])


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Contraseña mínimo 6 caracteres", examples=["MiPassword123!"])


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Auth Schemas
class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["juan.perez@example.com"])
    password: str = Field(..., examples=["MiPassword123!"])


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Task Schemas
class TaskBase(BaseModel):
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=255, 
        description="Título de la tarea",
        examples=["Completar informe mensual"]
    )
    description: Optional[str] = Field(
        None, 
        description="Descripción detallada de la tarea",
        examples=["Elaborar y enviar el informe de ventas del mes de octubre"]
    )
    category: Optional[str] = Field(
        None, 
        max_length=100,
        description="Categoría de la tarea",
        examples=["Trabajo", "Personal", "Urgente", "Proyecto X"]
    )
    status: TaskStatus = Field(
        default=TaskStatus.PLANIFICADO,
        description="Estado de la tarea: planificado, en_progreso, completado"
    )
    start_date: Optional[datetime] = Field(
        None,
        description="Fecha y hora de inicio de la tarea",
        examples=["2025-10-10T09:00:00"]
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Fecha y hora límite de la tarea",
        examples=["2025-10-15T18:00:00"]
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    status: Optional[TaskStatus] = None
    start_date: Optional[datetime] = None
    deadline: Optional[datetime] = None


class TaskResponse(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class TaskBulkCreate(BaseModel):
    tasks: list[TaskCreate] = Field(..., min_length=1)


class CategoryResponse(BaseModel):
    category: str
    count: int
    
    model_config = ConfigDict(from_attributes=True)
