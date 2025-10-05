# 📋 Guía de Archivos Docker - Task Management API

## 📁 Archivos Docker en el Proyecto

### ✅ ARCHIVOS QUE SÍ FUNCIONAN Y DEBES USAR:

#### 1. **`Dockerfile`** ⭐ PRINCIPAL
- **Propósito**: Define cómo se construye la imagen Docker de la aplicación
- **Estado**: ✅ FUNCIONAL Y OPTIMIZADO
- **Características**:
  - Imagen base Python 3.11-slim
  - Usuario no-root para seguridad
  - Health check configurado
  - Variables de entorno optimizadas
  - Cache de capas eficiente
- **Uso**: Automático con docker-compose
- **🎯 ESTE ES EL DEFINITIVO - NO TOCAR**

```dockerfile
# Este archivo define la imagen Docker de tu aplicación
# Se usa automáticamente cuando ejecutas docker-compose
```

---

#### 2. **`docker-compose.yml`** ⭐ PRINCIPAL
- **Propósito**: Orquestación completa con PostgreSQL local
- **Estado**: ✅ FUNCIONAL Y COMPLETO
- **Características**:
  - Servicio API (FastAPI)
  - Servicio DB (PostgreSQL 15)
  - Servicio PgAdmin (opcional con --profile tools)
  - Health checks
  - Volúmenes persistentes
  - Red interna
- **Uso**: Para desarrollo con PostgreSQL local
- **🎯 USA ESTE SI NO TIENES NEON O QUIERES BD LOCAL**

```bash
# Iniciar todo (API + PostgreSQL + PgAdmin)
docker-compose --profile tools up

# Solo API + PostgreSQL
docker-compose up
```

---

#### 3. **`docker-compose.neon.yml`** ⭐ ALTERNATIVO
- **Propósito**: Solo API, sin PostgreSQL (usa Neon externo)
- **Estado**: ✅ FUNCIONAL
- **Características**:
  - Solo servicio API
  - Más ligero (no incluye PostgreSQL)
  - Usa DATABASE_URL de Neon desde .env
- **Uso**: Para desarrollo cuando YA TIENES Neon configurado
- **🎯 USA ESTE SI YA TIENES NEON EN LA NUBE**

```bash
# Iniciar solo la API (conecta a Neon)
docker-compose -f docker-compose.neon.yml up
```

---

#### 4. **`.dockerignore`** ⭐ IMPORTANTE
- **Propósito**: Define qué archivos NO copiar a la imagen Docker
- **Estado**: ✅ FUNCIONAL
- **Características**:
  - Ignora __pycache__
  - Ignora venv/
  - Ignora .env
  - Ignora archivos temporales
- **Uso**: Automático durante build
- **🎯 NO MODIFICAR - FUNCIONA BIEN**

---

#### 5. **`docker.sh`** ⭐ HELPER SCRIPT
- **Propósito**: Script auxiliar para comandos Docker comunes
- **Estado**: ✅ FUNCIONAL
- **Características**:
  - Comandos simplificados
  - Setup automático
  - Logs, restart, backup, etc.
- **Uso**: Facilita el uso de Docker
- **🎯 MUY ÚTIL - DARLE PERMISOS CON `chmod +x docker.sh`**

```bash
# Ver comandos disponibles
./docker.sh help

# Setup inicial
./docker.sh setup

# Ver logs
./docker.sh logs
```

---

### ⚠️ ARCHIVOS OPCIONALES/SECUNDARIOS:

#### 6. **`docker-migrate.sh`**
- **Propósito**: Script específico solo para migraciones
- **Estado**: ✅ Funcional pero redundante
- **Recomendación**: ⚠️ OPCIONAL - Las funciones ya están en docker.sh
- **Puedes**: Usarlo o eliminarlo (docker.sh ya tiene comandos de migración)

```bash
# Mejor usar:
./docker.sh migrate
./docker.sh makemigration "mensaje"

# En vez de:
./docker-migrate.sh
```

---

#### 7. **`.env.docker.example`**
- **Propósito**: Ejemplo de .env para PostgreSQL local
- **Estado**: ✅ Funcional pero redundante
- **Recomendación**: ⚠️ OPCIONAL - Ya existe .env.example
- **Diferencia**: 
  - `.env.example` → Para Neon (producción)
  - `.env.docker.example` → Para PostgreSQL local (desarrollo)

---

## 🎯 RESUMEN: ¿Qué Archivo Usar?

### Escenario 1: Desarrollo Local con PostgreSQL en Docker
```bash
# 1. Usar docker-compose.yml
# 2. Copiar .env.docker.example → .env
cp .env.docker.example .env

# 3. Iniciar
docker-compose up --build

# 4. Migraciones
docker-compose exec api alembic upgrade head
```

### Escenario 2: Desarrollo con Neon (BD en la nube)
```bash
# 1. Usar docker-compose.neon.yml
# 2. Copiar .env.example → .env (con tu DATABASE_URL de Neon)
cp .env.example .env
nano .env  # Editar con tu conexión de Neon

# 3. Iniciar
docker-compose -f docker-compose.neon.yml up --build

# 4. Migraciones
docker-compose exec api alembic upgrade head
```

### Escenario 3: Sin Docker (Instalación tradicional)
```bash
# Seguir README.md sección "Instalación Local (Sin Docker)"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 🗂️ Estructura de Archivos Docker (Orden de Importancia)

```
📁 task-back/
├── 1️⃣ Dockerfile                    ⭐ PRINCIPAL - Define imagen
├── 2️⃣ docker-compose.yml            ⭐ PRINCIPAL - Con PostgreSQL local
├── 3️⃣ docker-compose.neon.yml       ⭐ ALTERNATIVO - Solo para Neon
├── 4️⃣ .dockerignore                 ✅ Importante - Optimiza build
├── 5️⃣ docker.sh                     ✅ Útil - Helper script
├── 6️⃣ docker-migrate.sh             ⚠️  Opcional - Redundante
└── 7️⃣ .env.docker.example           ⚠️  Opcional - Redundante
```

---

## ❌ Archivos que PUEDES ELIMINAR (sin afectar funcionalidad):

1. **`docker-migrate.sh`** → Redundante (docker.sh ya hace esto)
2. **`.env.docker.example`** → Redundante (basta con .env.example)

```bash
# Si quieres limpiar:
rm docker-migrate.sh
rm .env.docker.example
```

---

## ✅ Archivos que DEBES MANTENER:

1. ✅ **Dockerfile** → ESENCIAL
2. ✅ **docker-compose.yml** → ESENCIAL
3. ✅ **docker-compose.neon.yml** → ÚTIL (alternativa para Neon)
4. ✅ **.dockerignore** → IMPORTANTE
5. ✅ **docker.sh** → MUY ÚTIL

---

## 🔧 Configuración Recomendada Final

### Para Producción con Neon:
```yaml
Archivos necesarios:
- Dockerfile
- docker-compose.neon.yml (o crear docker-compose.prod.yml)
- .env (con credenciales de Neon)
- .dockerignore
```

### Para Desarrollo Local:
```yaml
Archivos necesarios:
- Dockerfile
- docker-compose.yml
- .env (con PostgreSQL local)
- .dockerignore
- docker.sh (opcional pero útil)
```

---

## 🚀 Comandos Finales Recomendados

### Opción A: Con Neon (Producción-like)
```bash
# 1. Configurar
cp .env.example .env
nano .env  # Agregar DATABASE_URL de Neon

# 2. Iniciar
docker-compose -f docker-compose.neon.yml up -d

# 3. Migraciones
docker-compose -f docker-compose.neon.yml exec api alembic upgrade head
```

### Opción B: Con PostgreSQL Local (Desarrollo)
```bash
# 1. Configurar
cp .env.docker.example .env
# O editar DATABASE_URL=postgresql://taskuser:taskpass@db:5432/taskdb

# 2. Iniciar
docker-compose up -d

# 3. Migraciones
docker-compose exec api alembic upgrade head
```

### Opción C: Con Script Helper (Más fácil)
```bash
chmod +x docker.sh
./docker.sh setup  # Hace todo automáticamente
```

---

## 📝 Notas Finales

- **Dockerfile**: Es la "receta" de tu aplicación → NO TOCAR
- **docker-compose.yml**: Orquesta servicios → USAR para desarrollo local
- **docker-compose.neon.yml**: Versión ligera → USAR para Neon
- **docker.sh**: Facilita comandos → USAR para comodidad

**Conclusión**: Todos los archivos principales funcionan correctamente. Solo hay 2 archivos redundantes que puedes eliminar si quieres limpiar el proyecto.
