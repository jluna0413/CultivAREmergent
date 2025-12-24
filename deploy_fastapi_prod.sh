#!/bin/bash

# Production Deployment Script for CultivAR FastAPI Backend
# This script handles the deployment of the FastAPI application to production

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="cultivar"
COMPOSE_FILE="docker-compose.fastapi.prod.yml"
ENV_FILE=".env.production"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f "$ENV_FILE" ]; then
        print_warning "Environment file $ENV_FILE not found. Creating from template..."
        cat > "$ENV_FILE" << EOF
# Production Environment Configuration for CultivAR FastAPI
# IMPORTANT: Change all default values before deploying to production

# Database Configuration
POSTGRES_PASSWORD=CHANGE_ME_BEFORE_PRODUCTION

# Application Secrets (Generate strong secrets for production)
SECRET_KEY=CHANGE_ME_TO_A_LONG_RANDOM_STRING
JWT_SECRET_KEY=CHANGE_ME_TO_ANOTHER_LONG_RANDOM_STRING
SESSION_SECRET_KEY=CHANGE_ME_TO_A_THIRD_RANDOM_STRING
CSRF_SECRET_KEY=CHANGE_ME_TO_A_FOURTH_RANDOM_STRING
FLASH_SECRET_KEY=CHANGE_ME_TO_A_FIFTH_RANDOM_STRING

# Application Environment
ENVIRONMENT=production
LOG_LEVEL=INFO
EOF
        print_warning "Please update $ENV_FILE with production values before continuing."
        exit 1
    fi
    
    print_success "Prerequisites check completed"
}

# Function to build and deploy
deploy() {
    print_status "Building and deploying CultivAR FastAPI..."
    
    # Pull latest images
    docker-compose -f "$COMPOSE_FILE" pull db
    
    # Build the FastAPI application
    docker-compose -f "$COMPOSE_FILE" build --no-cache
    
    # Stop existing containers (if any)
    print_status "Stopping existing containers..."
    docker-compose -f "$COMPOSE_FILE" down --remove-orphans || true
    
    # Start services
    print_status "Starting services..."
    docker-compose -f "$COMPOSE_FILE" up -d
    
    # Wait for services to be healthy
    print_status "Waiting for services to be healthy..."
    sleep 10
    
    # Check service health
    check_health
    
    print_success "Deployment completed successfully!"
}

# Function to check service health
check_health() {
    print_status "Checking service health..."
    
    # Check database
    if docker-compose -f "$COMPOSE_FILE" exec -T db pg_isready -U cultivar; then
        print_success "Database is healthy"
    else
        print_error "Database health check failed"
        return 1
    fi
    
    # Check FastAPI application
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
            print_success "FastAPI application is healthy"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - Waiting for FastAPI application..."
        sleep 2
        ((attempt++))
    done
    
    print_error "FastAPI application health check failed after $max_attempts attempts"
    return 1
}

# Function to run migrations
run_migrations() {
    print_status "Running database migrations..."
    
    docker-compose -f "$COMPOSE_FILE" exec -T cultivar-fastapi alembic upgrade head
    
    print_success "Database migrations completed"
}

# Function to show logs
show_logs() {
    print_status "Showing recent logs..."
    docker-compose -f "$COMPOSE_FILE" logs --tail=50 -f
}

# Function to restart services
restart() {
    print_status "Restarting services..."
    docker-compose -f "$COMPOSE_FILE" restart
    print_success "Services restarted"
}

# Function to stop services
stop() {
    print_status "Stopping services..."
    docker-compose -f "$COMPOSE_FILE" down
    print_success "Services stopped"
}

# Function to backup database
backup_db() {
    print_status "Creating database backup..."
    
    local backup_file="backup_$(date +%Y%m%d_%H%M%S).sql"
    
    docker-compose -f "$COMPOSE_FILE" exec -T db pg_dump -U cultivar cultivardb > "backups/$backup_file"
    
    print_success "Database backup created: backups/$backup_file"
}

# Function to show deployment status
status() {
    print_status "Deployment Status:"
    docker-compose -f "$COMPOSE_FILE" ps
}

# Function to cleanup
cleanup() {
    print_status "Cleaning up old images and containers..."
    
    # Remove unused images
    docker image prune -f
    
    # Remove unused volumes (be careful with this)
    # docker volume prune -f
    
    # Remove unused networks
    docker network prune -f
    
    print_success "Cleanup completed"
}

# Main script logic
main() {
    case "${1:-deploy}" in
        "deploy")
            check_prerequisites
            deploy
            run_migrations
            status
            ;;
        "health"|"check")
            check_health
            ;;
        "logs")
            show_logs
            ;;
        "restart")
            restart
            ;;
        "stop")
            stop
            ;;
        "backup")
            backup_db
            ;;
        "status")
            status
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|*)
            echo "CultivAR FastAPI Production Deployment Script"
            echo ""
            echo "Usage: $0 [COMMAND]"
            echo ""
            echo "Commands:"
            echo "  deploy    - Full deployment (default)"
            echo "  health    - Check service health"
            echo "  logs      - Show service logs"
            echo "  restart   - Restart all services"
            echo "  stop      - Stop all services"
            echo "  backup    - Create database backup"
            echo "  status    - Show deployment status"
            echo "  cleanup   - Clean up old Docker resources"
            echo "  help      - Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 deploy    # Deploy the application"
            echo "  $0 health    # Check if everything is working"
            echo "  $0 logs      # View recent logs"
            ;;
    esac
}

# Run main function with all arguments
main "$@"