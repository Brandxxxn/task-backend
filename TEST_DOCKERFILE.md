# 🧪 Verificación del Dockerfile

## 1️⃣ Esperar a que Docker Desktop inicie
```bash
# Verificar que Docker está corriendo
docker ps
```

Si ves una tabla (aunque esté vacía), Docker está funcionando ✅

---

## 2️⃣ Validar sintaxis del Dockerfile
```bash
# Verificar sintaxis básica
docker build -t task-api-test --no-cache .
```

### ✅ Si funciona correctamente verás:
```
[+] Building 45.2s (14/14) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 1.23kB
 => [internal] load .dockerignore
 => [1/8] FROM docker.io/library/python:3.11-slim
 => [2/8] WORKDIR /app
 => [3/8] RUN apt-get update && apt-get install...
 => [4/8] COPY requirements.txt .
 => [5/8] RUN pip install --no-cache-dir -r requirements.txt
 => [6/8] COPY . .
 => [7/8] RUN useradd -m -u 1000 appuser...
 => exporting to image
 => => naming to docker.io/library/task-api-test
```

### ❌ Si hay errores verás:
```
ERROR [4/8] COPY requirements.txt .
# O errores de sintaxis en el Dockerfile
```

---

## 3️⃣ Verificar que la imagen se creó
```bash
# Listar imágenes
docker images | grep task-api

# Deberías ver:
# task-api-test   latest   abc123def456   2 minutes ago   450MB
```

---

## 4️⃣ Probar que la imagen funciona
```bash
# Ejecutar un contenedor de prueba
docker run -d \
  --name test-container \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@localhost:5432/db" \
  -e JWT_SECRET_KEY="test-secret-key" \
  -e JWT_ALGORITHM="HS256" \
  -e ACCESS_TOKEN_EXPIRE_MINUTES="30" \
  task-api-test
```

---

## 5️⃣ Verificar que el contenedor está corriendo
```bash
# Ver contenedores en ejecución
docker ps

# Ver logs del contenedor
docker logs test-container

# Deberías ver:
# INFO:     Started server process [1]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 6️⃣ Probar la API
```bash
# Verificar que responde
curl http://localhost:8000/docs

# O abrir en navegador:
open http://localhost:8000/docs
```

---

## 7️⃣ Limpiar después de probar
```bash
# Detener contenedor
docker stop test-container

# Eliminar contenedor
docker rm test-container

# (Opcional) Eliminar imagen de prueba
docker rmi task-api-test
```

---

## 🔍 Checklist de Verificación

- [ ] Docker Desktop está corriendo (`docker ps` funciona)
- [ ] Build del Dockerfile exitoso (sin errores)
- [ ] Imagen creada (`docker images` la muestra)
- [ ] Contenedor inicia correctamente
- [ ] Logs muestran "Uvicorn running"
- [ ] API responde en http://localhost:8000/docs
- [ ] Health check funciona (después de 5s)

---

## 🐛 Problemas Comunes

### Error: "requirements.txt not found"
**Solución**: Asegúrate de tener el archivo requirements.txt en el mismo directorio

### Error: "psycopg2 compilation failed"
**Solución**: El Dockerfile ya instala las dependencias necesarias (gcc, libpq-dev)

### Error: "Permission denied"
**Solución**: El Dockerfile ya crea un usuario no-root (appuser)

### Contenedor se detiene inmediatamente
**Solución**: Revisa los logs con `docker logs test-container`

---

## ✅ Resultado Esperado

Si todos los pasos funcionan:
- ✅ **Dockerfile es válido y está bien configurado**
- ✅ **La imagen se construye correctamente**
- ✅ **La aplicación inicia sin errores**
- ✅ **La API responde correctamente**

**Conclusión**: Tu Dockerfile está listo para usar en producción 🚀
