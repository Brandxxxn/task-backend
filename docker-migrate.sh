#!/bin/bash

# Script para ejecutar migraciones dentro del contenedor Docker

echo "🔄 Esperando a que la base de datos esté lista..."
sleep 3

echo "📋 Generando migración inicial..."
docker-compose exec api alembic revision --autogenerate -m "Initial migration with all features"

echo "⬆️  Aplicando migraciones..."
docker-compose exec api alembic upgrade head

echo "✅ Migraciones completadas!"
echo ""
echo "📊 Estado actual de migraciones:"
docker-compose exec api alembic current
