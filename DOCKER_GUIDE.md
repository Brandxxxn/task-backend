# 🐳 Docker - Guía de Uso

Esta guía explica cómo ejecutar la aplicación Task Management API usando Docker.

## 📋 Requisitos

- Docker Desktop instalado ([Descargar](https://www.docker.com/products/docker-desktop))
- Docker Compose incluido con Docker Desktop

## 🚀 Opción 1: Usar con Neon (Base de Datos en la Nube)

### Paso 1: Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tu connection string de Neon
nano .env  # o usa tu editor favorito
```

Tu `.env` debe tener:
```env
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require
SECRET_KEY=tu-secret-key-generada
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
API_V1_STR=/api/v1
PROJECT_NAME=Task Management API
```

### Paso 2: Comentar el servicio `db` en docker-compose.yml

Edita `docker-compose.yml` y comenta o elimina la sección del servicio `db` ya que usarás Neon:

```yaml
# db:
#   image: postgres:15-alpine
#   ...
```

### Paso 3: Construir y ejecutar

```bash
# Construir imagen Docker
docker-compose build

# Ejecutar migraciones (primera vez)
docker-compose run --rm api alembic upgrade head

# Iniciar aplicación
docker-compose up
```

La API estará disponible en: **http://localhost:8000**

---

## 🐘 Opción 2: Usar con PostgreSQL Local (Docker)

### Paso 1: Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y usa esta DATABASE_URL para PostgreSQL local:
```env
DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb
SECRET_KEY=tu-secret-key-generada
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
API_V1_STR=/api/v1
PROJECT_NAME=Task Management API
```

**Nota:** El host es `db` (nombre del servicio en docker-compose), no `localhost`.

### Paso 2: Iniciar todos los servicios

```bash
# Construir e iniciar API + PostgreSQL
docker-compose up --build
```

### Paso 3: Ejecutar migraciones

En otra terminal:
```bash
docker-compose exec api alembic upgrade head
```

La API estará en: **http://localhost:8000**
PostgreSQL estará en: **localhost:5432**

---

## 🛠️ Comandos Útiles

### Ver logs
```bash
# Logs de todos los servicios
docker-compose logs -f

# Logs solo de la API
docker-compose logs -f api

# Logs solo de la BD
docker-compose logs -f db
```

### Ejecutar comandos dentro del contenedor
```bash
# Ejecutar migraciones
docker-compose exec api alembic upgrade head

# Generar nueva migración
docker-compose exec api alembic revision --autogenerate -m "Descripción"

# Abrir shell en el contenedor
docker-compose exec api bash

# Ejecutar Python
docker-compose exec api python
```

### Reiniciar servicios
```bash
# Reiniciar todo
docker-compose restart

# Reiniciar solo la API
docker-compose restart api
```

### Detener y limpiar
```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: elimina datos de BD)
docker-compose down -v

# Limpiar imágenes no usadas
docker system prune -a
```

---

## 🗄️ PgAdmin (Interfaz Web para PostgreSQL)

Si quieres una interfaz gráfica para gestionar PostgreSQL:

```bash
# Iniciar con PgAdmin
docker-compose --profile tools up
```

Accede a: **http://localhost:5050**
- Email: `admin@task.com`
- Password: `admin123`

**Conectar a PostgreSQL desde PgAdmin:**
1. Add New Server
2. General → Name: `Task DB`
3. Connection:
   - Host: `db` (nombre del servicio)
   - Port: `5432`
   - Database: `taskdb`
   - Username: `taskuser`
   - Password: `taskpass`

---

## 🔧 Desarrollo con Hot Reload

El `docker-compose.yml` está configurado para desarrollo:

```yaml
volumes:
  - .:/app  # Código montado en tiempo real
command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Los cambios en el código se reflejan automáticamente** sin reiniciar el contenedor.

---

## 📦 Producción

Para producción, crea un `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: task-api-prod
    ports:
      - "8000:8000"
    env_file:
      - .env.production
    restart: always
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
    # Sin volúmenes montados
    # Sin --reload
```

Ejecutar en producción:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🐛 Troubleshooting

### Error: "Port already in use"
```bash
# Ver qué usa el puerto 8000
lsof -i :8000

# Cambiar puerto en docker-compose.yml
ports:
  - "8001:8000"  # Usar 8001 externamente
```

### Error: "Database connection failed"
```bash
# Verificar que la BD esté corriendo
docker-compose ps

# Ver logs de la BD
docker-compose logs db

# Reiniciar servicios
docker-compose restart
```

### Error: "Permission denied"
```bash
# Dar permisos al directorio
chmod -R 755 .

# O ejecutar como root (no recomendado)
docker-compose exec --user root api bash
```

### Contenedor no se actualiza con cambios de código
```bash
# Reconstruir imagen
docker-compose build --no-cache api

# Reiniciar
docker-compose up --force-recreate
```

---

## 📊 Monitoreo y Health Checks

### Verificar health del contenedor
```bash
docker-compose ps
docker inspect task-api | grep Health
```

### Acceder a métricas
```bash
# Ver uso de recursos
docker stats
```

---

## ✅ Checklist de Deployment

Antes de desplegar a producción:

- [ ] Cambiar `SECRET_KEY` por una única y segura
- [ ] Configurar CORS con dominios específicos
- [ ] Usar HTTPS (certificado SSL)
- [ ] Quitar `--reload` del comando
- [ ] Aumentar workers: `--workers 4`
- [ ] Configurar logs persistentes
- [ ] Backup automático de base de datos
- [ ] Monitoring y alertas
- [ ] Rate limiting activado
- [ ] Eliminar servicios de desarrollo (PgAdmin)

---

¿Dudas? Revisa la documentación completa en el [README.md](README.md)
