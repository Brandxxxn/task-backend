#!/bin/bash

# Script de gestión para Task Management API con Docker

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de ayuda
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Verificar que Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Instala Docker Desktop desde https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker no está corriendo. Inicia Docker Desktop."
        exit 1
    fi
    
    print_success "Docker está instalado y corriendo"
}

# Verificar archivo .env
check_env() {
    if [ ! -f .env ]; then
        print_warning "Archivo .env no encontrado"
        print_info "Copiando .env.example a .env..."
        cp .env.example .env
        print_warning "Por favor edita .env con tus credenciales antes de continuar"
        exit 1
    fi
    print_success "Archivo .env encontrado"
}

# Función: Setup inicial
setup() {
    print_info "🚀 Iniciando setup de Task Management API..."
    check_docker
    check_env
    
    print_info "Construyendo imagen Docker..."
    docker-compose build
    
    print_info "Iniciando servicios..."
    docker-compose up -d
    
    print_info "Esperando que la base de datos esté lista..."
    sleep 5
    
    print_info "Ejecutando migraciones..."
    docker-compose exec api alembic upgrade head
    
    print_success "Setup completado!"
    print_info "La API está corriendo en: http://localhost:8000"
    print_info "Documentación Swagger: http://localhost:8000/docs"
}

# Función: Iniciar servicios
start() {
    print_info "Iniciando servicios..."
    docker-compose up -d
    print_success "Servicios iniciados"
    print_info "API: http://localhost:8000"
    print_info "Docs: http://localhost:8000/docs"
}

# Función: Detener servicios
stop() {
    print_info "Deteniendo servicios..."
    docker-compose down
    print_success "Servicios detenidos"
}

# Función: Ver logs
logs() {
    print_info "Mostrando logs (Ctrl+C para salir)..."
    docker-compose logs -f
}

# Función: Reiniciar servicios
restart() {
    print_info "Reiniciando servicios..."
    docker-compose restart
    print_success "Servicios reiniciados"
}

# Función: Limpiar todo
clean() {
    print_warning "Esto eliminará todos los contenedores, volúmenes y datos"
    read -p "¿Estás seguro? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Limpiando..."
        docker-compose down -v
        docker system prune -f
        print_success "Limpieza completa"
    else
        print_info "Cancelado"
    fi
}

# Función: Ejecutar migraciones
migrate() {
    print_info "Ejecutando migraciones..."
    docker-compose exec api alembic upgrade head
    print_success "Migraciones aplicadas"
}

# Función: Crear nueva migración
makemigration() {
    if [ -z "$1" ]; then
        print_error "Debes proporcionar un mensaje para la migración"
        print_info "Uso: ./docker.sh makemigration 'Descripción del cambio'"
        exit 1
    fi
    
    print_info "Creando nueva migración..."
    docker-compose exec api alembic revision --autogenerate -m "$1"
    print_success "Migración creada"
}

# Función: Shell dentro del contenedor
shell() {
    print_info "Abriendo shell en el contenedor..."
    docker-compose exec api bash
}

# Función: Ver estado
status() {
    print_info "Estado de los servicios:"
    docker-compose ps
}

# Función: Ver logs de un servicio específico
service_logs() {
    if [ -z "$1" ]; then
        print_error "Debes especificar un servicio (api, db, pgadmin)"
        exit 1
    fi
    docker-compose logs -f "$1"
}

# Función: Backup de base de datos
backup() {
    print_info "Creando backup de la base de datos..."
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    docker-compose exec -T db pg_dump -U taskuser taskdb > "$BACKUP_FILE"
    print_success "Backup creado: $BACKUP_FILE"
}

# Función: Ayuda
help() {
    echo "Task Management API - Docker Helper Script"
    echo ""
    echo "Uso: ./docker.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  setup           - Configuración inicial (primera vez)"
    echo "  start           - Iniciar servicios"
    echo "  stop            - Detener servicios"
    echo "  restart         - Reiniciar servicios"
    echo "  logs            - Ver logs de todos los servicios"
    echo "  logs-api        - Ver logs solo de la API"
    echo "  logs-db         - Ver logs solo de la BD"
    echo "  status          - Ver estado de servicios"
    echo "  migrate         - Ejecutar migraciones pendientes"
    echo "  makemigration   - Crear nueva migración"
    echo "  shell           - Abrir shell en el contenedor"
    echo "  clean           - Limpiar todo (contenedores, volúmenes, datos)"
    echo "  backup          - Crear backup de la base de datos"
    echo "  help            - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./docker.sh setup"
    echo "  ./docker.sh start"
    echo "  ./docker.sh makemigration 'Agregar campo email a usuarios'"
    echo "  ./docker.sh logs-api"
}

# Main
case "$1" in
    setup)
        setup
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    logs)
        logs
        ;;
    logs-api)
        service_logs "api"
        ;;
    logs-db)
        service_logs "db"
        ;;
    status)
        status
        ;;
    migrate)
        migrate
        ;;
    makemigration)
        makemigration "$2"
        ;;
    shell)
        shell
        ;;
    clean)
        clean
        ;;
    backup)
        backup
        ;;
    help|--help|-h)
        help
        ;;
    *)
        print_error "Comando no reconocido: $1"
        echo ""
        help
        exit 1
        ;;
esac
