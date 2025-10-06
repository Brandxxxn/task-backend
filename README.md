# Task Management API - Backend

API REST para gestión de tareas con autenticación JWT, desarrollada con FastAPI y PostgreSQL (Neon).

---

## 📑 Índice

- [🚀 Características](#-características)
- [📋 Requisitos Previos](#-requisitos-previos)
- [🔧 Instalación](#-instalación)
  - [🐳 Opción 1: Usando Docker (Recomendado)](#-opción-1-usando-docker-recomendado)
    - [Inicio Rápido con Docker (3 pasos)](#-inicio-rápido-con-docker-3-pasos)
    - [Comandos Útiles de Docker](#-comandos-útiles-de-docker)
    - [Configuración con PostgreSQL Local](#-configuración-con-postgresql-local-sin-neon)
    - [Troubleshooting](#-troubleshooting-problemas-comunes)
    - [Script Helper Opcional](#-script-helper-opcional-dockersh)
  - [💻 Opción 2: Instalación Local (Sin Docker)](#-opción-2-instalación-local-sin-docker)
- [📖 Documentación API](#-documentación-api)
- [🔑 Endpoints](#-endpoints)
  - [Autenticación](#autenticación)
  - [Tareas](#tareas)
- [🗂️ Estructura del Proyecto](#️-estructura-del-proyecto)
- [🔒 Seguridad](#-seguridad)
  - [Autenticación y Autorización](#-autenticación-y-autorización)
  - [Protección de Datos](#️-protección-de-datos)
  - [Validación de Datos](#-validación-de-datos)
  - [Recomendaciones para Producción](#️-recomendaciones-adicionales-para-producción)
- [🌐 Formato de Respuestas](#-formato-de-respuestas)
- [🧪 Códigos de Estado HTTP](#-códigos-de-estado-http)
- [📝 Notas Adicionales](#-notas-adicionales)
  - [Modelo de Datos de Tareas](#modelo-de-datos-de-tareas)
  - [Estados de Tareas](#estados-de-tareas)
  - [Características de Filtrado y Ordenamiento](#características-de-filtrado-y-ordenamiento)
  - [Importación de Tareas desde CSV](#importación-de-tareas-desde-csv)
  - [Consideraciones de Producción](#consideraciones-de-producción)
- [🐳 Deployment con Docker](#-deployment-con-docker)
- [📁 Archivos de Docker](#-archivos-de-docker)
- [🤝 Contribución](#-contribución)
- [📄 Licencia](#-licencia)

---

## 🚀 Características

- ✅ Registro e inicio de sesión de usuarios
- 🔐 Autenticación JWT con access token y refresh token
- 📝 CRUD completo de tareas
- 📦 Creación masiva de tareas (bulk create)
- 🏷️ Categorización de tareas
- 📊 Estados de tareas (planificado, en_progreso, completado)
- 📅 Fechas de inicio y deadlines
- 🔍 Filtrado avanzado (por estado, categoría, fechas)
- 🔄 Ordenamiento personalizado
- 📈 Endpoint de categorías con conteo de tareas
- 📆 Vista de calendario mensual
- 🚨 Manejo de errores estructurado con success/message
- 🗄️ Base de datos PostgreSQL en Neon
- 📚 Documentación automática con Swagger UI interactiva
- 🐳 **Docker & Docker Compose** para fácil deployment
- 🔒 **Seguridad robusta**: bcrypt, JWT, validación de ownership, protección SQL injection

## 📋 Requisitos Previos

### Opción A: Desarrollo Local
- Python 3.9 o superior
- Cuenta en [Neon](https://neon.tech/) (PostgreSQL serverless)
- pip o virtualenv

### Opción B: Con Docker (Recomendado) 🐳
- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado
- Docker Compose (incluido con Docker Desktop)
- **No necesitas instalar Python ni PostgreSQL localmente**

## 🔧 Instalación

## 🐳 Opción 1: Usando Docker (Recomendado)

Docker permite que la aplicación funcione **exactamente igual** en cualquier máquina sin configurar Python, PostgreSQL ni dependencias.

### 📦 Requisitos Previos
- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y ejecutándose
- Cuenta en [Neon](https://neon.tech/) para obtener el DATABASE_URL (o usa PostgreSQL local)

---

### 🚀 Inicio Rápido con Docker (3 pasos)

#### **Paso 1: Configurar Variables de Entorno**

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar el archivo .env con tus credenciales
nano .env  # o usa tu editor favorito (code .env, vim .env, etc.)
```

**Debes configurar estas variables en el archivo `.env`:**

```env
# Database - OBLIGATORIO
# Opción A: Con Neon (PostgreSQL en la nube)
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Opción B: Con PostgreSQL local en Docker
# DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb

# JWT Settings - OBLIGATORIO
SECRET_KEY=genera-una-clave-secreta-aqui-32-caracteres-minimo
JWT_SECRET_KEY=genera-otra-clave-secreta-diferente-aqui
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Settings - Opcional (valores por defecto)
API_V1_STR=/api/v1
PROJECT_NAME=Task Management API
```

**💡 Generar SECRET_KEY segura:**
```bash
# Opción 1: Con Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Opción 2: Con OpenSSL
openssl rand -base64 32

# Opción 3: Online (usar solo para desarrollo)
# https://randomkeygen.com/
```

**🔹 Obtener DATABASE_URL de Neon:**
1. Ve a [https://neon.tech/](https://neon.tech/) y crea una cuenta
2. Crea un nuevo proyecto
3. En "Connection Details", selecciona "Connection string"
4. Copia el string (incluye `?sslmode=require` al final)
5. Pégalo en `.env` en la variable `DATABASE_URL`

---

#### **Paso 2: Construir e Iniciar los Contenedores**

```bash
# Construir la imagen e iniciar los servicios
docker-compose up --build

# O ejecutar en segundo plano (detached mode)
docker-compose up --build -d
```

**Verás algo como:**
```
[+] Building 45.2s (14/14) FINISHED
[+] Running 1/1
 ✔ Container task-back-api-1  Started
```

---

#### **Paso 3: Ejecutar Migraciones de Base de Datos**

```bash
# En otra terminal (o si ejecutaste con -d)
docker-compose exec api alembic upgrade head
```

**Deberías ver:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade -> abc123, Initial migration
```

**¡Listo!** 🎉 La API está corriendo en **http://localhost:8000**

---

### 📋 Comandos Útiles de Docker

#### **Ver Logs en Tiempo Real**
```bash
# Ver todos los logs
docker-compose logs -f

# Solo logs de la API
docker-compose logs -f api

# Últimas 50 líneas
docker-compose logs --tail=50 api
```

#### **Detener los Servicios**
```bash
# Detener contenedores (mantiene datos)
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener y eliminar TODO (contenedores + volúmenes + imágenes)
docker-compose down -v --rmi all
```

#### **Reiniciar los Servicios**
```bash
# Reiniciar todos los servicios
docker-compose restart

# Reiniciar solo la API
docker-compose restart api

# Reconstruir y reiniciar (si cambiaste código)
docker-compose up --build
```

#### **Ver Estado de Contenedores**
```bash
# Ver contenedores corriendo
docker-compose ps

# Ver todos los contenedores
docker ps -a

# Ver imágenes creadas
docker images | grep task
```

#### **Acceder al Contenedor (Shell)**
```bash
# Abrir bash dentro del contenedor
docker-compose exec api /bin/bash

# O ejecutar comandos directos
docker-compose exec api python --version
docker-compose exec api pip list
```

#### **Ejecutar Migraciones (Alembic)**
```bash
# Ver estado de migraciones
docker-compose exec api alembic current

# Aplicar migraciones pendientes
docker-compose exec api alembic upgrade head

# Crear nueva migración (después de cambiar modelos)
docker-compose exec api alembic revision --autogenerate -m "Descripción del cambio"

# Revertir última migración
docker-compose exec api alembic downgrade -1

# Ver historial de migraciones
docker-compose exec api alembic history
```

#### **Limpiar y Empezar de Nuevo**
```bash
# 1. Detener y eliminar todo
docker-compose down -v

# 2. Eliminar imagen antigua
docker rmi task-back-api

# 3. Reconstruir desde cero
docker-compose up --build

# 4. Aplicar migraciones
docker-compose exec api alembic upgrade head
```

---

### 🔧 Configuración con PostgreSQL Local (sin Neon)

Si prefieres usar PostgreSQL localmente dentro de Docker en vez de Neon:

#### **Paso 1: Editar `.env`**
```env
# Cambiar DATABASE_URL a PostgreSQL local
DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb

# Resto de variables igual...
SECRET_KEY=tu-clave-secreta
JWT_SECRET_KEY=otra-clave-secreta
```

#### **Paso 2: Iniciar Servicios (API + PostgreSQL)**
```bash
docker-compose up --build -d
```

#### **Paso 3: Esperar a que PostgreSQL esté listo**
```bash
# Ver logs hasta que veas "database system is ready to accept connections"
docker-compose logs -f db
```

#### **Paso 4: Ejecutar Migraciones**
```bash
docker-compose exec api alembic upgrade head
```

#### **Paso 5 (Opcional): Usar PgAdmin**
```bash
# Iniciar con PgAdmin incluido
docker-compose --profile tools up -d

# Abrir PgAdmin en: http://localhost:5050
# Email: admin@admin.com
# Password: admin
```

**Configurar conexión en PgAdmin:**
- Host: `db`
- Port: `5432`
- Database: `taskdb`
- Username: `taskuser`
- Password: `taskpass`

---

### 🐛 Troubleshooting (Problemas Comunes)

#### **Error: "Cannot connect to Docker daemon"**
```bash
# Solución: Iniciar Docker Desktop
open -a Docker  # En macOS
# O busca Docker Desktop en Aplicaciones
```

#### **Error: "Port 8000 already in use"**
```bash
# Solución 1: Detener proceso que usa el puerto
lsof -ti:8000 | xargs kill -9

# Solución 2: Cambiar puerto en docker-compose.yml
# Editar: ports: - "8001:8000"  # Usar puerto 8001
```

#### **Error: "Field required: SECRET_KEY"**
```bash
# Solución: Verifica que .env tenga todas las variables
cat .env

# Debe incluir SECRET_KEY y JWT_SECRET_KEY
```

#### **Error: "Database connection failed"**
```bash
# Solución 1: Si usas Neon, verifica DATABASE_URL
echo $DATABASE_URL

# Solución 2: Si usas PostgreSQL local, verifica que esté corriendo
docker-compose logs db

# Solución 3: Reiniciar todo
docker-compose down -v
docker-compose up --build
```

#### **Los cambios en código no se reflejan**
```bash
# Solución: Reconstruir la imagen
docker-compose up --build

# O forzar rebuild sin cache
docker-compose build --no-cache
docker-compose up
```

#### **Contenedor se detiene inmediatamente**
```bash
# Ver logs para identificar el error
docker-compose logs api

# Problemas comunes:
# 1. Falta .env o variables incorrectas
# 2. DATABASE_URL inválido
# 3. Puerto 8000 ocupado
```

---

### 📊 Verificar que Todo Funciona

#### **1. Ver logs del contenedor**
```bash
docker-compose logs api

# Deberías ver:
# INFO:     Started server process [1]
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### **2. Verificar endpoints**
```bash
# Probar documentación
curl http://localhost:8000/docs

# O abrir en navegador
open http://localhost:8000/docs
```

#### **3. Health check**
```bash
# Verificar estado de salud
docker-compose ps

# Deberías ver "healthy" en STATE
```

---

### 🚀 Script Helper Opcional (docker.sh)

Para simplificar los comandos, puedes usar el script helper:

```bash
# Dar permisos de ejecución
chmod +x docker.sh

# Ver comandos disponibles
./docker.sh help

# Setup automático (configura .env y ejecuta todo)
./docker.sh setup

# Iniciar servicios
./docker.sh start

# Ver logs
./docker.sh logs

# Ejecutar migraciones
./docker.sh migrate

# Detener servicios
./docker.sh stop

# Limpiar todo
./docker.sh clean
```

---

### 📚 Documentación Adicional

Para más detalles sobre Docker, consulta:
- 📖 [DOCKER_GUIDE.md](DOCKER_GUIDE.md) - Guía completa con ejemplos avanzados
- 📖 [DOCKER_FILES_EXPLANATION.md](DOCKER_FILES_EXPLANATION.md) - Explicación de cada archivo Docker
- ⚡ [QUICKSTART.md](QUICKSTART.md) - Inicio ultra-rápido en 5 minutos
- 🧪 [TEST_DOCKERFILE.md](TEST_DOCKERFILE.md) - Cómo verificar que el Dockerfile funciona

---

### 🎯 Resumen de Comandos Esenciales

```bash
# Setup inicial
cp .env.example .env
nano .env  # Configurar variables

# Iniciar
docker-compose up --build -d

# Migraciones
docker-compose exec api alembic upgrade head

# Ver logs
docker-compose logs -f api

# Detener
docker-compose down

# Reconstruir (después de cambios)
docker-compose up --build
```

**✅ Con esto tu aplicación estará corriendo en Docker lista para desarrollo o producción.**

---

## 💻 Opción 2: Instalación Local (Sin Docker)

### 1. Clonar el repositorio

```bash
cd task-back
```

### 2. Crear y activar entorno virtual

```bash
# En macOS/Linux
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:

```env
# Database - Obtén tu connection string de Neon
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# JWT Settings - Genera una clave secreta segura
SECRET_KEY=tu-clave-secreta-aqui-usa-algo-seguro
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=Task Management API
```

#### 🔹 Cómo obtener el DATABASE_URL de Neon:

1. Ve a [https://neon.tech/](https://neon.tech/)
2. Crea una cuenta o inicia sesión
3. Crea un nuevo proyecto
4. En la sección "Connection Details", copia el connection string
5. Asegúrate de que incluya `?sslmode=require` al final

#### 🔹 Cómo generar un SECRET_KEY seguro:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Ejecutar migraciones de base de datos

**IMPORTANTE**: Este proyecto usa Alembic para migraciones (recomendado para producción).

#### Si es la primera vez (base de datos nueva):

```bash
# 1. Crear migración inicial (detecta automáticamente todos los modelos)
alembic revision --autogenerate -m "Initial migration with all features"

# 2. Aplicar la migración a la base de datos
alembic upgrade head

# 3. Verificar que se aplicó correctamente
alembic current
```

#### Si necesitas resetear las migraciones:

```bash
# 1. Eliminar migración anterior (si existe)
rm alembic/versions/*.py
rm -rf alembic/versions/__pycache__

# 2. Crear nueva migración
alembic revision --autogenerate -m "Initial migration with all features"

# 3. Aplicar migración
alembic upgrade head
```

**Nota:** La migración inicial incluye:
- ✅ Tabla `users` (id, name, email, password, created_at)
- ✅ Tabla `tasks` con todos los campos:
  - Campos básicos: id, title, description, deadline
  - Campos avanzados: **category**, **status**, **start_date**
  - Relaciones: user_id, created_at, updated_at
- ✅ Índices en campos clave para optimizar búsquedas

Para más detalles sobre migraciones, consulta [ALEMBIC_GUIDE.md](ALEMBIC_GUIDE.md)

### 6. Ejecutar la aplicación

```bash
python main.py
```

O usando uvicorn directamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: `http://localhost:8000`

## 📖 Documentación API

Una vez que la aplicación esté corriendo, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs (Interfaz interactiva con autenticación)
- **ReDoc**: http://localhost:8000/redoc

### 🔐 Cómo autenticarse en Swagger:

1. Haz login en el endpoint `POST /api/v1/auth/login`
2. Copia el `access_token` de la respuesta
3. Haz clic en el botón **"Authorize" 🔓** (esquina superior derecha)
4. Pega SOLO el token (sin "Bearer")
5. Haz clic en "Authorize"
6. ¡Ahora puedes probar todos los endpoints protegidos!

📝 Para una guía detallada con imágenes, consulta [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md)

## 🔑 Endpoints

### Autenticación

#### Registro de Usuario
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "name": "Juan Pérez",
  "email": "juan@example.com",
  "password": "password123"
}
```

**NOTA:** Todos los campos son obligatorios. Si falta alguno, recibirás un mensaje específico indicando qué campo es requerido.

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "data": {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "created_at": "2025-10-05T10:00:00"
  }
}
```

**Respuesta de error (campo faltante):**
```json
{
  "success": false,
  "message": "Errores de validación: El campo 'name' es obligatorio y no puede estar vacío",
  "data": {
    "errors": [
      "El campo 'name' es obligatorio y no puede estar vacío"
    ]
  }
}
```

#### Inicio de Sesión
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "juan@example.com",
  "password": "password123"
}
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "message": "Inicio de sesión exitoso",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "name": "Juan Pérez",
      "email": "juan@example.com",
      "created_at": "2025-10-05T10:00:00"
    }
  }
}
```

#### Renovar Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Tareas

**Nota:** Todos los endpoints de tareas requieren autenticación. Incluye el header:
```
Authorization: Bearer {access_token}
```

#### Crear Tarea
```http
POST /api/v1/tasks/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Completar proyecto",
  "description": "Finalizar el backend de la aplicación",
  "category": "Trabajo",
  "status": "planificado",
  "start_date": "2025-10-10T09:00:00",
  "deadline": "2025-10-15T23:59:59"
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Tarea creada exitosamente",
  "data": {
    "id": 1,
    "title": "Completar proyecto",
    "description": "Finalizar el backend de la aplicación",
    "category": "Trabajo",
    "status": "planificado",
    "start_date": "2025-10-10T09:00:00",
    "deadline": "2025-10-15T23:59:59",
    "user_id": 1,
    "created_at": "2025-10-05T15:30:00",
    "updated_at": null
  }
}
```

#### Crear Tareas Masivas (Bulk Create)
```http
POST /api/v1/tasks/bulk
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "tasks": [
    {
      "title": "Tarea 1",
      "description": "Descripción 1",
      "category": "Trabajo",
      "status": "planificado",
      "start_date": "2025-10-10T09:00:00",
      "deadline": "2025-10-10T12:00:00"
    },
    {
      "title": "Tarea 2",
      "description": "Descripción 2",
      "category": "Personal",
      "status": "planificado",
      "start_date": "2025-10-11T10:00:00",
      "deadline": "2025-10-11T12:00:00"
    }
  ]
}
```

**📋 Notas sobre Bulk Create:**
- ✅ Acepta un array de tareas en formato JSON
- ❌ **NO soporta archivos CSV directamente**
- 💡 Para importar desde CSV: Parsea el CSV en el cliente (frontend/script) y envía como JSON
- 📊 Formato CSV recomendado si usas scripts de importación:
  ```csv
  title,description,category,status,start_date,deadline
  "Tarea 1","Descripción 1","Trabajo","planificado","2025-10-10T09:00:00","2025-10-15T18:00:00"
  "Tarea 2","Descripción 2","Personal","en_progreso","2025-10-11T10:00:00","2025-10-16T17:00:00"
  ```
- 🐍 Ejemplo Python para convertir CSV a JSON:
  ```python
  import csv
  import json
  import requests
  
  # Leer CSV
  tasks = []
  with open('tasks.csv', 'r') as file:
      reader = csv.DictReader(file)
      for row in reader:
          tasks.append(row)
  
  # Enviar a API
  response = requests.post(
      'http://localhost:8000/api/v1/tasks/bulk',
      headers={'Authorization': f'Bearer {access_token}'},
      json={'tasks': tasks}
  )
  ```

#### Listar Tareas (con filtros y ordenamiento)
```http
GET /api/v1/tasks/?sort_by=created_at&order=desc&search=proyecto
Authorization: Bearer {access_token}
```

**Parámetros de consulta opcionales:**
- `sort_by`: Campo por el cual ordenar
  - `created_at` (por defecto)
  - `start_date`
  - `deadline`
  - `title`
  - `status`
  - `updated_at`
- `order`: Orden de resultados
  - `asc` - Ascendente
  - `desc` - Descendente (por defecto)
- **Filtros por estado:**
  - `status`: Filtrar por estado (`planificado`, `en_progreso`, `completado`)
- **Filtros por categoría:**
  - `category`: Filtrar por categoría exacta (ej: `Trabajo`, `Personal`)
- **Filtros por fechas de inicio:**
  - `start_date_from`: Tareas con fecha de inicio desde (ISO 8601)
  - `start_date_to`: Tareas con fecha de inicio hasta (ISO 8601)
- **Filtros por deadline:**
  - `deadline_from`: Tareas con deadline desde (ISO 8601)
  - `deadline_to`: Tareas con deadline hasta (ISO 8601)
- **Filtros por fecha de creación:**
  - `created_from`: Tareas creadas desde (ISO 8601)
  - `created_to`: Tareas creadas hasta (ISO 8601)
- **Búsqueda:**
  - `search`: Buscar en título o descripción (case-insensitive)

**Ejemplos de uso:**
```http
# Tareas en progreso ordenadas por deadline
GET /api/v1/tasks/?status=en_progreso&sort_by=deadline&order=asc

# Tareas de categoría "Trabajo" creadas esta semana
GET /api/v1/tasks/?category=Trabajo&created_from=2025-10-01T00:00:00

# Buscar "proyecto" en tareas completadas
GET /api/v1/tasks/?search=proyecto&status=completado

# Tareas que vencen esta semana
GET /api/v1/tasks/?deadline_from=2025-10-07T00:00:00&deadline_to=2025-10-13T23:59:59
```

#### Obtener Categorías con Conteo
```http
GET /api/v1/tasks/categories
Authorization: Bearer {access_token}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Se encontraron 3 categorías",
  "data": [
    {
      "category": "Trabajo",
      "count": 15
    },
    {
      "category": "Personal",
      "count": 8
    },
    {
      "category": "Urgente",
      "count": 3
    }
  ]
}
```

#### Vista de Calendario Mensual
```http
GET /api/v1/tasks/calendar/2025/10
Authorization: Bearer {access_token}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Se encontraron 12 tareas para 10/2025",
  "data": {
    "year": 2025,
    "month": 10,
    "total_tasks": 12,
    "tasks": [
      {
        "id": 1,
        "title": "Reunión de equipo",
        "description": "Revisión semanal",
        "category": "Trabajo",
        "status": "completado",
        "start_date": "2025-10-05T10:00:00",
        "deadline": "2025-10-05T11:00:00",
        "user_id": 1,
        "created_at": "2025-10-01T08:00:00",
        "updated_at": "2025-10-05T11:00:00"
      }
    ]
  }
}
```

#### Obtener Tarea por ID
```http
GET /api/v1/tasks/{task_id}
Authorization: Bearer {access_token}
```

#### Actualizar Tarea
```http
PUT /api/v1/tasks/{task_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Título actualizado",
  "description": "Nueva descripción",
  "category": "Trabajo",
  "status": "en_progreso",
  "start_date": "2025-10-12T09:00:00",
  "deadline": "2025-10-20T23:59:59"
}
```

**Nota:** Todos los campos son opcionales. Solo actualiza los campos enviados.

#### Eliminar Tarea
```http
DELETE /api/v1/tasks/{task_id}
Authorization: Bearer {access_token}
```

## 🗂️ Estructura del Proyecto

```
task-back/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # Endpoints de autenticación
│   │   └── tasks.py         # Endpoints de tareas
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuración de la app
│   │   ├── database.py      # Conexión a base de datos
│   │   ├── exceptions.py    # Excepciones personalizadas
│   │   ├── jwt.py           # Manejo de JWT
│   │   ├── response.py      # Formatos de respuesta
│   │   └── security.py      # Hash de contraseñas
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py        # Modelos SQLAlchemy
│   └── schemas/
│       ├── __init__.py
│       └── schemas.py       # Schemas Pydantic
├── main.py                  # Archivo principal
├── requirements.txt         # Dependencias
├── .env.example            # Ejemplo de variables de entorno
├── .gitignore
└── README.md
```

## 🔒 Seguridad

Este backend implementa múltiples capas de seguridad para proteger los datos y la aplicación:

### 🔐 Autenticación y Autorización

#### 1. **JWT (JSON Web Tokens)**
- ✅ **Access Tokens**: Expiran en 30 minutos (configurable)
- ✅ **Refresh Tokens**: Expiran en 7 días (configurable)
- ✅ Tokens firmados con algoritmo HS256
- ✅ Secret key robusta generada de forma segura
- ✅ Validación de tokens en cada request protegido

#### 2. **Hash de Contraseñas**
- ✅ **bcrypt** con salt automático
- ✅ Factor de costo 12 (2^12 iteraciones)
- ✅ Las contraseñas NUNCA se almacenan en texto plano
- ✅ Protección contra ataques de fuerza bruta offline
- ✅ Password hashing antes de comparar en login

**Ejemplo de implementación:**
```python
import bcrypt

# Al registrar
password_bytes = password.encode('utf-8')
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password_bytes, salt)

# Al verificar login
bcrypt.checkpw(password.encode('utf-8'), stored_hash)
```

### 🛡️ Protección de Datos

#### 3. **Protección contra Inyección SQL**
- ✅ **SQLAlchemy ORM** en todas las consultas
- ✅ Parámetros vinculados automáticamente
- ✅ Sin concatenación directa de strings SQL
- ✅ Validación de tipos con Pydantic

#### 4. **Validación de Ownership**
- ✅ Cada tarea verifica que pertenezca al usuario autenticado
- ✅ Endpoints GET, PUT, DELETE validan `task.user_id == current_user.id`
- ✅ Protección contra acceso no autorizado a recursos ajenos
- ✅ Error 403 Forbidden si intenta acceder a tareas de otros usuarios

**Ejemplo de implementación:**
```python
task = db.query(Task).filter(Task.id == task_id).first()
if task.user_id != current_user.id:
    raise ForbiddenException(message="No tienes permiso...")
```

#### 5. **CORS (Cross-Origin Resource Sharing)**
- ✅ Middleware CORS configurado
- ⚠️ Actualmente permite todos los orígenes (`*`) - **CAMBIAR EN PRODUCCIÓN**
- ✅ Permite credenciales (cookies, headers de autorización)
- ✅ Métodos HTTP permitidos configurables

**Configuración recomendada para producción:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tudominio.com"],  # Dominios específicos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### 📋 Validación de Datos

#### 6. **Schemas de Pydantic**
- ✅ Validación automática de tipos de datos
- ✅ Validación de longitudes (ej: título máximo 255 caracteres)
- ✅ Validación de formatos (emails, fechas ISO 8601)
- ✅ Enums estrictos para estados de tareas
- ✅ Mensajes de error descriptivos en español

**Validaciones implementadas:**
- Email: Formato válido requerido
- Passwords: Longitud mínima, no pueden exceder 72 bytes (bcrypt)
- Títulos: 1-255 caracteres
- Status: Solo `planificado`, `en_progreso`, `completado`
- Fechas: Formato ISO 8601 con timezone

#### 7. **Manejo de Errores Personalizado**
- ✅ Excepciones personalizadas (`NotFoundException`, `ForbiddenException`, etc.)
- ✅ Mensajes de error claros sin exponer información sensible
- ✅ No se revelan detalles internos del servidor
- ✅ Formato de respuesta consistente

### 🔐 Conexión a Base de Datos

#### 8. **PostgreSQL con SSL (Neon)**
- ✅ Conexión SSL requerida (`?sslmode=require`)
- ✅ Credenciales en variables de entorno (`.env`)
- ✅ Connection string no se expone en código
- ✅ Base de datos serverless con encriptación en reposo

#### 9. **Variables de Entorno**
- ✅ Secretos almacenados en `.env` (no versionado)
- ✅ `.env.example` como plantilla sin datos sensibles
- ✅ `.gitignore` configurado para proteger `.env`
- ✅ Validación de configuración al iniciar

### 🚨 Headers de Seguridad

#### 10. **Headers HTTP Recomendados** (implementar en producción):
```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Protección contra Host Header Injection
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["tudominio.com", "*.tudominio.com"]
)

# Headers de seguridad adicionales
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

### 📊 Auditoría y Monitoreo

#### 11. **Campos de Auditoría**
- ✅ `created_at`: Timestamp de creación automático
- ✅ `updated_at`: Timestamp de última modificación automático
- ✅ `user_id`: Trazabilidad de propietario de cada recurso

### ⚠️ Recomendaciones Adicionales para Producción

#### **ALTA PRIORIDAD:**
1. 🔴 **Cambiar CORS** de `allow_origins=["*"]` a dominios específicos
2. 🔴 **SECRET_KEY fuerte** y única por entorno (usar `secrets.token_urlsafe(32)`)
3. 🔴 **HTTPS obligatorio** en producción (nunca HTTP)
4. 🔴 **Rate Limiting** para prevenir ataques de fuerza bruta
5. 🔴 **Logging** de intentos de acceso no autorizado

#### **MEDIA PRIORIDAD:**
6. 🟡 **Timeout de sesión** configurable
7. 🟡 **Política de contraseñas** (complejidad mínima)
8. 🟡 **2FA (Autenticación de dos factores)** opcional
9. 🟡 **Blacklist de tokens** para invalidar refresh tokens
10. 🟡 **Limitar intentos de login** (3-5 intentos)

#### **BAJA PRIORIDAD:**
11. 🟢 **Auditoría de acciones** (logs detallados)
12. 🟢 **Versionado de API** para retrocompatibilidad
13. 🟢 **Sanitización adicional** de inputs HTML/JS

### 🔧 Ejemplo: Implementar Rate Limiting

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# En endpoints de login
@router.post("/login")
@limiter.limit("5/minute")  # Máximo 5 intentos por minuto
async def login(request: Request, ...):
    ...
```

### 🛠️ Testing de Seguridad Recomendado

1. **OWASP Top 10** - Verificar vulnerabilidades comunes
2. **Pruebas de penetración** - Simulación de ataques
3. **Auditoría de dependencias** - `pip audit` o `safety check`
4. **Escaneo de secretos** - Evitar commits con credenciales
5. **Análisis estático de código** - Herramientas como `bandit`

```bash
# Auditar dependencias
pip install pip-audit
pip-audit

# Escanear código Python
pip install bandit
bandit -r app/
```

---

### 📚 Recursos de Seguridad

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

## 🌐 Formato de Respuestas

Todas las respuestas de la API siguen este formato:

### Respuesta Exitosa
```json
{
  "success": true,
  "message": "Mensaje descriptivo",
  "data": { /* datos de respuesta */ }
}
```

### Respuesta de Error
```json
{
  "success": false,
  "message": "Mensaje de error descriptivo",
  "data": null
}
```

## 🧪 Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `400 Bad Request` - Solicitud inválida
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - Sin permisos
- `404 Not Found` - Recurso no encontrado
- `409 Conflict` - Conflicto (ej: email ya registrado)
- `500 Internal Server Error` - Error del servidor

## 📝 Notas Adicionales

### Modelo de Datos de Tareas

Cada tarea tiene los siguientes campos:

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `id` | Integer | Auto | ID único de la tarea |
| `title` | String (255) | ✅ | Título de la tarea |
| `description` | Text | ✅ | Descripción detallada |
| `category` | String (100) | ❌ | Categoría (Trabajo, Personal, etc.) |
| `status` | Enum | ✅ | Estado: `planificado`, `en_progreso`, `completado` (default: `planificado`) |
| `start_date` | DateTime | ❌ | Fecha y hora de inicio |
| `deadline` | DateTime | ✅ | Fecha y hora límite |
| `user_id` | Integer | Auto | ID del usuario propietario |
| `created_at` | DateTime | Auto | Fecha de creación |
| `updated_at` | DateTime | Auto | Fecha de última actualización |

### Estados de Tareas

Las tareas pueden tener tres estados:

1. **`planificado`** - Tarea creada pero no iniciada (estado por defecto)
2. **`en_progreso`** - Tarea actualmente en desarrollo
3. **`completado`** - Tarea finalizada

### Características de Filtrado y Ordenamiento

#### Ejemplos de Consultas Complejas

**Dashboard de tareas pendientes:**
```http
GET /api/v1/tasks/?status=en_progreso&sort_by=deadline&order=asc
```

**Tareas urgentes de hoy:**
```http
GET /api/v1/tasks/?category=Urgente&deadline_from=2025-10-05T00:00:00&deadline_to=2025-10-05T23:59:59
```

**Planificación semanal:**
```http
GET /api/v1/tasks/?start_date_from=2025-10-07T00:00:00&start_date_to=2025-10-13T23:59:59&sort_by=start_date&order=asc
```

**Tareas completadas del proyecto:**
```http
GET /api/v1/tasks/?category=Proyecto X&status=completado
```

**Búsqueda con múltiples filtros:**
```http
GET /api/v1/tasks/?search=informe&category=Trabajo&status=planificado&sort_by=deadline&order=asc
```

### Importación de Tareas desde CSV

Aunque la API no soporta CSV directamente, puedes importar tareas usando scripts:

#### Script Python de Ejemplo
```python
import csv
import json
import requests

# Configuración
API_URL = "http://localhost:8000/api/v1/tasks/bulk"
ACCESS_TOKEN = "tu_access_token_aqui"

# Leer CSV
tasks = []
with open('tareas.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        tasks.append({
            "title": row['title'],
            "description": row['description'],
            "category": row.get('category', ''),
            "status": row.get('status', 'planificado'),
            "start_date": row.get('start_date', None),
            "deadline": row['deadline']
        })

# Enviar a API
response = requests.post(
    API_URL,
    headers={
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    },
    json={'tasks': tasks}
)

if response.status_code == 201:
    result = response.json()
    print(f"✅ {result['message']}")
else:
    print(f"❌ Error: {response.json()}")
```

#### Script JavaScript/Node.js de Ejemplo
```javascript
const fs = require('fs');
const csv = require('csv-parser');
const axios = require('axios');

const API_URL = 'http://localhost:8000/api/v1/tasks/bulk';
const ACCESS_TOKEN = 'tu_access_token_aqui';

const tasks = [];

fs.createReadStream('tareas.csv')
  .pipe(csv())
  .on('data', (row) => {
    tasks.push({
      title: row.title,
      description: row.description,
      category: row.category || '',
      status: row.status || 'planificado',
      start_date: row.start_date || null,
      deadline: row.deadline
    });
  })
  .on('end', async () => {
    try {
      const response = await axios.post(
        API_URL,
        { tasks },
        {
          headers: {
            'Authorization': `Bearer ${ACCESS_TOKEN}`,
            'Content-Type': 'application/json'
          }
        }
      );
      console.log(`✅ ${response.data.message}`);
    } catch (error) {
      console.error('❌ Error:', error.response.data);
    }
  });
```

### Consideraciones de Producción

Para producción, considera:

1. **Cambiar `allow_origins=["*"]`** en CORS a dominios específicos
2. **SECRET_KEY robusta** y única por entorno
3. **HTTPS obligatorio** (nunca HTTP en producción)
4. **Rate limiting** para prevenir ataques
5. **Implementar logging** apropiado
6. **Añadir validaciones** adicionales
7. **Backups automáticos** de base de datos en Neon
8. **Monitoreo y alertas** (ej: Sentry, DataDog)
9. **Health checks** configurados
10. **Docker en modo producción** (ver DOCKER_GUIDE.md)

---

## 🐳 Deployment con Docker

Esta aplicación está completamente dockerizada y lista para deployment:

### Para Desarrollo

```bash
# Setup automático
chmod +x docker.sh
./docker.sh setup

# O manual
docker-compose up --build
docker-compose exec api alembic upgrade head
```

### Para Producción

```bash
# 1. Usar docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml up -d

# 2. O construir imagen para registry
docker build -t task-api:latest .
docker tag task-api:latest registry.example.com/task-api:latest
docker push registry.example.com/task-api:latest
```

📚 **Guías de Deployment:**
- Ver [DOCKER_GUIDE.md](DOCKER_GUIDE.md) para instrucciones detalladas
- Ver [QUICKSTART.md](QUICKSTART.md) para inicio rápido
- Script helper: `./docker.sh help`

---

## 📁 Archivos de Docker

- `Dockerfile` - Imagen Docker optimizada con multi-stage
- `docker-compose.yml` - Orchestración de servicios (API + PostgreSQL)
- `.dockerignore` - Archivos ignorados en build
- `docker.sh` - Script helper para comandos comunes

---

## 🤝 Contribución

Este proyecto es un ejemplo educativo. Siéntete libre de hacer fork y adaptarlo a tus necesidades.

## 📄 Licencia

MIT License

---

**Desarrollado por Kevin Azua usando FastAPI y Neon PostgreSQL**
