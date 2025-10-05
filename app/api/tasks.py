from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func, extract
from typing import List, Optional
from datetime import datetime
from calendar import monthrange

from app.core.database import get_db
from app.core.jwt import get_current_user
from app.core.exceptions import NotFoundException, ForbiddenException, BadRequestException
from app.core.response import success_response
from app.models.models import User, Task
from app.schemas.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskBulkCreate, CategoryResponse, TaskStatus

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        category=task_data.category,
        status=task_data.status.value,
        start_date=task_data.start_date,
        deadline=task_data.deadline,
        user_id=current_user.id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    task_response = TaskResponse.model_validate(new_task)
    
    return success_response(
        message="Tarea creada exitosamente",
        data=task_response.model_dump()
    )


@router.post("/bulk", status_code=status.HTTP_201_CREATED)
def create_tasks_bulk(
    bulk_data: TaskBulkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create multiple tasks at once
    
    **Note:** This endpoint accepts JSON only. CSV files are NOT directly supported.
    If you want to import from CSV, parse it on the client-side and send as JSON array.
    
    Example request body:
    ```json
    {
        "tasks": [
            {
                "title": "Tarea 1",
                "description": "Primera tarea del día",
                "category": "Trabajo",
                "status": "planificado",
                "start_date": "2025-10-10T09:00:00",
                "deadline": "2025-10-15T18:00:00"
            },
            {
                "title": "Tarea 2",
                "description": "Segunda tarea importante",
                "category": "Personal",
                "status": "planificado",
                "start_date": "2025-10-11T10:00:00",
                "deadline": "2025-10-16T17:00:00"
            }
        ]
    }
    ```
    """
    
    if len(bulk_data.tasks) == 0:
        raise BadRequestException(message="Debe proporcionar al menos una tarea")
    
    new_tasks = []
    for task_data in bulk_data.tasks:
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            category=task_data.category,
            status=task_data.status.value,
            start_date=task_data.start_date,
            deadline=task_data.deadline,
            user_id=current_user.id
        )
        new_tasks.append(new_task)
    
    db.add_all(new_tasks)
    db.commit()
    
    # Refresh all tasks to get their IDs
    for task in new_tasks:
        db.refresh(task)
    
    tasks_response = [TaskResponse.model_validate(task).model_dump() for task in new_tasks]
    
    return success_response(
        message=f"{len(new_tasks)} tareas creadas exitosamente",
        data=tasks_response
    )


@router.get("/")
def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    sort_by: Optional[str] = Query("created_at", description="Campo por el cual ordenar: created_at, start_date, deadline, title, status"),
    order: Optional[str] = Query("desc", description="Orden: asc o desc"),
    status: Optional[TaskStatus] = Query(None, description="Filtrar por estado: planificado, en_progreso, completado"),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    start_date_from: Optional[datetime] = Query(None, description="Filtrar tareas con fecha de inicio desde"),
    start_date_to: Optional[datetime] = Query(None, description="Filtrar tareas con fecha de inicio hasta"),
    deadline_from: Optional[datetime] = Query(None, description="Filtrar tareas con deadline desde esta fecha"),
    deadline_to: Optional[datetime] = Query(None, description="Filtrar tareas con deadline hasta esta fecha"),
    created_from: Optional[datetime] = Query(None, description="Filtrar tareas creadas desde esta fecha"),
    created_to: Optional[datetime] = Query(None, description="Filtrar tareas creadas hasta esta fecha"),
    search: Optional[str] = Query(None, description="Buscar en título o descripción")
):
    """Get all tasks for the current user with advanced filtering and sorting options"""
    
    # Base query
    query = db.query(Task).filter(Task.user_id == current_user.id)
    
    # Apply search filter
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Task.title.ilike(search_filter)) | 
            (Task.description.ilike(search_filter))
        )
    
    # Apply status filter
    if status:
        query = query.filter(Task.status == status.value)
    
    # Apply category filter
    if category:
        query = query.filter(Task.category == category)
    
    # Apply start_date filters
    if start_date_from:
        query = query.filter(Task.start_date >= start_date_from)
    
    if start_date_to:
        query = query.filter(Task.start_date <= start_date_to)
    
    # Apply deadline filters
    if deadline_from:
        query = query.filter(Task.deadline >= deadline_from)
    
    if deadline_to:
        query = query.filter(Task.deadline <= deadline_to)
    
    # Apply created_at filters
    if created_from:
        query = query.filter(Task.created_at >= created_from)
    
    if created_to:
        query = query.filter(Task.created_at <= created_to)
    
    # Apply sorting
    valid_sort_fields = {"created_at", "start_date", "deadline", "title", "status", "updated_at"}
    if sort_by not in valid_sort_fields:
        sort_by = "created_at"
    
    sort_column = getattr(Task, sort_by)
    
    if order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))
    
    tasks = query.all()
    
    tasks_response = [TaskResponse.model_validate(task).model_dump() for task in tasks]
    
    return success_response(
        message=f"Se encontraron {len(tasks)} tareas",
        data=tasks_response
    )


@router.get("/categories")
def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all categories with task count for the current user"""
    
    # Query para obtener categorías y contar tareas
    categories = db.query(
        Task.category,
        func.count(Task.id).label('count')
    ).filter(
        Task.user_id == current_user.id,
        Task.category.isnot(None),
        Task.category != ''
    ).group_by(Task.category).order_by(desc('count')).all()
    
    categories_response = [
        {"category": cat.category, "count": cat.count}
        for cat in categories
    ]
    
    return success_response(
        message=f"Se encontraron {len(categories_response)} categorías",
        data=categories_response
    )


@router.get("/calendar/{year}/{month}")
def get_calendar_tasks(
    year: int,
    month: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tasks for a specific month (by start_date, deadline, or created_at)"""
    
    # Validar mes y año
    if month < 1 or month > 12:
        raise BadRequestException(message="El mes debe estar entre 1 y 12")
    
    if year < 2000 or year > 2100:
        raise BadRequestException(message="El año debe estar entre 2000 y 2100")
    
    # Obtener el primer y último día del mes
    from datetime import datetime, timezone
    first_day = datetime(year, month, 1, 0, 0, 0, tzinfo=timezone.utc)
    
    # Calcular el último día del mes
    if month == 12:
        last_day = datetime(year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    else:
        last_day = datetime(year, month + 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    
    # Query: tareas que tengan start_date, deadline o created_at en este mes
    tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        (
            (Task.start_date >= first_day) & (Task.start_date < last_day) |
            (Task.deadline >= first_day) & (Task.deadline < last_day) |
            (Task.created_at >= first_day) & (Task.created_at < last_day)
        )
    ).order_by(asc(Task.start_date)).all()
    
    tasks_response = [TaskResponse.model_validate(task).model_dump() for task in tasks]
    
    return success_response(
        message=f"Se encontraron {len(tasks)} tareas para {month}/{year}",
        data={
            "year": year,
            "month": month,
            "total_tasks": len(tasks),
            "tasks": tasks_response
        }
    )


@router.get("/{task_id}")
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task by ID"""
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise NotFoundException(message="Tarea no encontrada")
    
    # Check if task belongs to current user
    if task.user_id != current_user.id:
        raise ForbiddenException(message="No tienes permiso para acceder a esta tarea")
    
    task_response = TaskResponse.model_validate(task)
    
    return success_response(
        message="Tarea obtenida exitosamente",
        data=task_response.model_dump()
    )


@router.put("/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task"""
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise NotFoundException(message="Tarea no encontrada")
    
    # Check if task belongs to current user
    if task.user_id != current_user.id:
        raise ForbiddenException(message="No tienes permiso para editar esta tarea")
    
    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise BadRequestException(message="No se proporcionaron campos para actualizar")
    
    for field, value in update_data.items():
        # Convertir el enum status a su valor string
        if field == "status" and value is not None:
            setattr(task, field, value.value if hasattr(value, 'value') else value)
        else:
            setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    
    task_response = TaskResponse.model_validate(task)
    
    return success_response(
        message="Tarea actualizada exitosamente",
        data=task_response.model_dump()
    )


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task"""
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise NotFoundException(message="Tarea no encontrada")
    
    # Check if task belongs to current user
    if task.user_id != current_user.id:
        raise ForbiddenException(message="No tienes permiso para eliminar esta tarea")
    
    db.delete(task)
    db.commit()
    
    return success_response(
        message="Tarea eliminada exitosamente",
        data={"id": task_id}
    )

