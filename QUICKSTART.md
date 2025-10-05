# 🚀 Quick Start Guide - Task Management API

Guía rápida para empezar a usar la API en menos de 5 minutos.

## ⚡ Inicio Ultra Rápido con Docker

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd task-back

# 2. Dar permisos al script helper
chmod +x docker.sh

# 3. Setup automático
./docker.sh setup

# 4. ¡Listo!
```

La API estará en: **http://localhost:8000/docs**

---

## 📝 Primeros Pasos en la API

### 1. Registrar un usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "password": "password123"
  }'
```

### 2. Iniciar sesión y obtener token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "password123"
  }'
```

Copia el `access_token` de la respuesta.

### 3. Crear una tarea

```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer TU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera tarea",
    "description": "Descripción de la tarea",
    "category": "Trabajo",
    "status": "planificado",
    "start_date": "2025-10-10T09:00:00",
    "deadline": "2025-10-15T18:00:00"
  }'
```

### 4. Listar todas las tareas

```bash
curl -X GET "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

---

## 🎯 Usar Swagger UI (Recomendado)

1. Abre: **http://localhost:8000/docs**
2. Click en **"Authorize" 🔓** (esquina superior derecha)
3. Pega tu `access_token`
4. Click en "Authorize"
5. ¡Ahora puedes probar todos los endpoints interactivamente!

---

## 🐳 Comandos Docker Útiles

```bash
# Ver logs en tiempo real
./docker.sh logs

# Reiniciar servicios
./docker.sh restart

# Detener todo
./docker.sh stop

# Ver estado
./docker.sh status

# Acceder al shell del contenedor
./docker.sh shell

# Crear backup de BD
./docker.sh backup

# Ver todos los comandos
./docker.sh help
```

---

## 🔑 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Registrar usuario |
| POST | `/api/v1/auth/login` | Iniciar sesión |
| POST | `/api/v1/auth/refresh` | Renovar token |
| GET | `/api/v1/tasks/` | Listar tareas (con filtros) |
| POST | `/api/v1/tasks/` | Crear tarea |
| POST | `/api/v1/tasks/bulk` | Crear múltiples tareas |
| GET | `/api/v1/tasks/categories` | Listar categorías |
| GET | `/api/v1/tasks/calendar/{year}/{month}` | Vista calendario |
| GET | `/api/v1/tasks/{id}` | Obtener tarea por ID |
| PUT | `/api/v1/tasks/{id}` | Actualizar tarea |
| DELETE | `/api/v1/tasks/{id}` | Eliminar tarea |

---

## 🎨 Ejemplos de Filtros

```bash
# Tareas en progreso
GET /api/v1/tasks/?status=en_progreso

# Tareas de categoría "Trabajo"
GET /api/v1/tasks/?category=Trabajo

# Tareas que vencen esta semana
GET /api/v1/tasks/?deadline_from=2025-10-07T00:00:00&deadline_to=2025-10-13T23:59:59

# Buscar "informe"
GET /api/v1/tasks/?search=informe

# Combinar filtros
GET /api/v1/tasks/?status=planificado&category=Trabajo&sort_by=deadline&order=asc
```

---

## 🐛 Problemas Comunes

### Puerto 8000 ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Ahora usará puerto 8001
```

### Docker no responde
```bash
# Reconstruir todo
docker-compose down
docker-compose up --build
```

### Base de datos no conecta
```bash
# Ver logs de la BD
./docker.sh logs-db

# Reiniciar solo la BD
docker-compose restart db
```

---

## 📚 Documentación Completa

- **README Principal**: [README.md](README.md) - Documentación completa de la API
- **Guía Docker**: [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Guía detallada de Docker
- **Seguridad**: Ver sección de seguridad en README.md
- **Swagger**: http://localhost:8000/docs - Documentación interactiva
- **ReDoc**: http://localhost:8000/redoc - Documentación alternativa

---

## 🎓 Recursos Adicionales

### Importar tareas desde CSV
Ver sección "Importación de Tareas desde CSV" en [README.md](README.md)

### Ejemplos de scripts Python/JavaScript
Ver ejemplos completos en la documentación principal

### Migraciones de base de datos
```bash
# Crear nueva migración
./docker.sh makemigration "Descripción del cambio"

# Aplicar migraciones
./docker.sh migrate
```

---

¿Necesitas ayuda? Abre un issue en el repositorio.
