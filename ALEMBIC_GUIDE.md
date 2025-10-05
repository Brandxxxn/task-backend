# 🔄 Guía de Uso de Alembic

## 📋 Comandos Principales

### 1. Crear una nueva migración (automática)
```bash
alembic revision --autogenerate -m "Descripción del cambio"
```
Ejemplo:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic revision --autogenerate -m "Add phone to users"
```

### 2. Aplicar migraciones (upgrade)
```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar solo una migración específica
alembic upgrade +1
```

### 3. Revertir migraciones (downgrade)
```bash
# Revertir la última migración
alembic downgrade -1

# Volver a una migración específica
alembic downgrade <revision_id>

# Revertir TODAS las migraciones
alembic downgrade base
```

### 4. Ver estado de migraciones
```bash
# Ver migración actual
alembic current

# Ver historial de migraciones
alembic history

# Ver migraciones pendientes
alembic heads
```

### 5. Crear migración manual (vacía)
```bash
alembic revision -m "Custom migration"
```

## 🚀 Flujo de Trabajo

### Setup Inicial (Primera vez)

1. **Instalar Alembic:**
```bash
pip install alembic==1.13.0
```

2. **Crear migración inicial:**
```bash
alembic revision --autogenerate -m "Initial migration: users and tasks tables"
```

3. **Aplicar migración:**
```bash
alembic upgrade head
```

### Modificar Modelos Existentes

1. **Modificar el modelo en `app/models/models.py`**
```python
# Ejemplo: Agregar campo avatar a User
class User(Base):
    # ...existing code...
    avatar = Column(String(255), nullable=True)
```

2. **Generar migración automática:**
```bash
alembic revision --autogenerate -m "Add avatar field to users"
```

3. **Revisar el archivo de migración generado** en `alembic/versions/`

4. **Aplicar la migración:**
```bash
alembic upgrade head
```

### Rollback (Revertir cambios)

Si algo sale mal:
```bash
# Revertir última migración
alembic downgrade -1

# Ver qué se revertiría
alembic show <revision_id>
```

## 📁 Estructura de Archivos

```
task-back/
├── alembic/
│   ├── versions/          # Carpeta con archivos de migración
│   │   └── 20251005_1234-abc123_initial_migration.py
│   ├── env.py            # Configuración de Alembic
│   └── script.py.mako    # Template para nuevas migraciones
├── alembic.ini           # Configuración principal
└── app/
    └── models/
        └── models.py     # Tus modelos SQLAlchemy
```

## 🔍 Verificar Migraciones

### Ver contenido de una migración:
```bash
cat alembic/versions/<nombre_archivo>.py
```

### Verificar qué cambios detecta Alembic:
```bash
alembic revision --autogenerate -m "test" --sql
```

## ⚠️ Notas Importantes

1. **Siempre revisa** las migraciones autogeneradas antes de aplicarlas
2. **En producción**, haz backup de la BD antes de aplicar migraciones
3. **No modifiques** migraciones ya aplicadas - crea una nueva
4. **En equipo**, coordina las migraciones para evitar conflictos
5. **Commitea** los archivos de migración al repositorio

## 🐛 Troubleshooting

### Error: "Target database is not up to date"
```bash
alembic stamp head
```

### Error: "Can't locate revision"
```bash
alembic history
alembic stamp <revision_id>
```

### Resetear TODO (⚠️ CUIDADO - Borra datos)
```bash
alembic downgrade base
# Luego vuelve a aplicar
alembic upgrade head
```

## 📝 Ejemplo Completo

```bash
# 1. Primera configuración
alembic revision --autogenerate -m "Initial: users and tasks"
alembic upgrade head

# 2. Agregar campo
# Editar app/models/models.py...
alembic revision --autogenerate -m "Add avatar to users"
alembic upgrade head

# 3. Ver estado
alembic current
alembic history

# 4. Si necesitas revertir
alembic downgrade -1
```

## 🎯 Best Practices

- ✅ Usa nombres descriptivos para las migraciones
- ✅ Una migración = un cambio lógico
- ✅ Revisa el código generado antes de aplicar
- ✅ Prueba en desarrollo antes de producción
- ✅ Mantén backups antes de migraciones en producción
- ❌ No edites migraciones ya aplicadas
- ❌ No borres archivos de migración del historial
