#!/bin/bash

# Social Listening Report Generator - Deployment Script
# Usage: ./deploy.sh [command] [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.prod.yml"
PROJECT_NAME="social-listening-app"
APP_CONTAINER="social-listening-app"
NGINX_CONTAINER="social-listening-nginx"

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Commands
cmd_help() {
    cat << EOF
Social Listening Report Generator - Deployment Script

Usage: ./deploy.sh [command] [options]

Commands:
    help              Show this help message
    build             Build Docker images
    up                Start services
    down              Stop services
    restart           Restart services
    logs              View service logs
    status            Show service status
    health            Check service health
    backup            Backup data and reports
    restore           Restore from backup
    clean             Clean up containers and images
    update            Update and restart services
    shell             Open shell in app container
    nginx-reload      Reload Nginx configuration
    ssl-generate      Generate self-signed SSL certificate
    ssl-check         Check SSL certificate validity

Examples:
    ./deploy.sh build
    ./deploy.sh up
    ./deploy.sh logs -f
    ./deploy.sh backup
    ./deploy.sh ssl-generate

EOF
}

cmd_build() {
    print_header "Building Docker Images"
    docker-compose -f $COMPOSE_FILE build --no-cache
    print_success "Images built successfully"
}

cmd_up() {
    print_header "Starting Services"
    docker-compose -f $COMPOSE_FILE up -d
    print_success "Services started"
    sleep 3
    cmd_status
}

cmd_down() {
    print_header "Stopping Services"
    docker-compose -f $COMPOSE_FILE down
    print_success "Services stopped"
}

cmd_restart() {
    print_header "Restarting Services"
    docker-compose -f $COMPOSE_FILE restart
    print_success "Services restarted"
    sleep 3
    cmd_status
}

cmd_logs() {
    print_header "Service Logs"
    docker-compose -f $COMPOSE_FILE logs "$@"
}

cmd_status() {
    print_header "Service Status"
    docker-compose -f $COMPOSE_FILE ps
}

cmd_health() {
    print_header "Health Check"
    
    # Check app container
    if docker-compose -f $COMPOSE_FILE exec app curl -s http://localhost:8501/_stcore/health > /dev/null; then
        print_success "App container is healthy"
    else
        print_error "App container is unhealthy"
    fi
    
    # Check Nginx container
    if docker-compose -f $COMPOSE_FILE exec nginx curl -s http://localhost > /dev/null; then
        print_success "Nginx container is healthy"
    else
        print_error "Nginx container is unhealthy"
    fi
    
    # Show resource usage
    print_info "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
}

cmd_backup() {
    print_header "Backing Up Data"
    
    BACKUP_DIR="backups"
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    
    mkdir -p $BACKUP_DIR
    
    # Backup reports
    if [ -d "reports" ]; then
        print_info "Backing up reports..."
        tar -czf $BACKUP_DIR/reports_$TIMESTAMP.tar.gz reports/
        print_success "Reports backed up: $BACKUP_DIR/reports_$TIMESTAMP.tar.gz"
    fi
    
    # Backup data
    if [ -d "data" ]; then
        print_info "Backing up data..."
        tar -czf $BACKUP_DIR/data_$TIMESTAMP.tar.gz data/
        print_success "Data backed up: $BACKUP_DIR/data_$TIMESTAMP.tar.gz"
    fi
    
    # Backup uploads
    if [ -d "uploads" ]; then
        print_info "Backing up uploads..."
        tar -czf $BACKUP_DIR/uploads_$TIMESTAMP.tar.gz uploads/
        print_success "Uploads backed up: $BACKUP_DIR/uploads_$TIMESTAMP.tar.gz"
    fi
    
    # Clean old backups (keep last 7 days)
    print_info "Cleaning old backups..."
    find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
    print_success "Old backups cleaned"
}

cmd_restore() {
    print_header "Restoring From Backup"
    
    if [ -z "$1" ]; then
        print_error "Please specify backup file"
        echo "Usage: ./deploy.sh restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Backup file not found: $1"
        exit 1
    fi
    
    print_warning "This will overwrite existing data. Continue? (y/n)"
    read -r response
    
    if [ "$response" != "y" ]; then
        print_info "Restore cancelled"
        return
    fi
    
    print_info "Restoring from $1..."
    tar -xzf "$1"
    print_success "Restore completed"
}

cmd_clean() {
    print_header "Cleaning Up"
    
    print_warning "This will remove stopped containers and unused images. Continue? (y/n)"
    read -r response
    
    if [ "$response" != "y" ]; then
        print_info "Cleanup cancelled"
        return
    fi
    
    print_info "Removing stopped containers..."
    docker container prune -f
    
    print_info "Removing unused images..."
    docker image prune -f
    
    print_info "Removing unused volumes..."
    docker volume prune -f
    
    print_success "Cleanup completed"
}

cmd_update() {
    print_header "Updating Application"
    
    print_info "Pulling latest code..."
    git pull origin main
    
    print_info "Building new images..."
    cmd_build
    
    print_info "Restarting services..."
    cmd_restart
    
    print_success "Update completed"
}

cmd_shell() {
    print_header "Opening Shell in App Container"
    docker-compose -f $COMPOSE_FILE exec app /bin/bash
}

cmd_nginx_reload() {
    print_header "Reloading Nginx Configuration"
    docker-compose -f $COMPOSE_FILE exec nginx nginx -s reload
    print_success "Nginx reloaded"
}

cmd_ssl_generate() {
    print_header "Generating Self-Signed SSL Certificate"
    
    mkdir -p ssl
    
    print_info "Generating certificate..."
    openssl req -x509 -newkey rsa:4096 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -days 365 \
        -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    
    chmod 600 ssl/key.pem
    chmod 644 ssl/cert.pem
    
    print_success "SSL certificate generated"
    print_info "Certificate: ssl/cert.pem"
    print_info "Key: ssl/key.pem"
}

cmd_ssl_check() {
    print_header "Checking SSL Certificate"
    
    if [ ! -f "ssl/cert.pem" ]; then
        print_error "Certificate not found: ssl/cert.pem"
        return
    fi
    
    print_info "Certificate Details:"
    openssl x509 -in ssl/cert.pem -text -noout
}

# Main
main() {
    if [ $# -eq 0 ]; then
        cmd_help
        exit 0
    fi
    
    COMMAND=$1
    shift
    
    case $COMMAND in
        help)
            cmd_help
            ;;
        build)
            cmd_build
            ;;
        up)
            cmd_up
            ;;
        down)
            cmd_down
            ;;
        restart)
            cmd_restart
            ;;
        logs)
            cmd_logs "$@"
            ;;
        status)
            cmd_status
            ;;
        health)
            cmd_health
            ;;
        backup)
            cmd_backup
            ;;
        restore)
            cmd_restore "$@"
            ;;
        clean)
            cmd_clean
            ;;
        update)
            cmd_update
            ;;
        shell)
            cmd_shell
            ;;
        nginx-reload)
            cmd_nginx_reload
            ;;
        ssl-generate)
            cmd_ssl_generate
            ;;
        ssl-check)
            cmd_ssl_check
            ;;
        *)
            print_error "Unknown command: $COMMAND"
            cmd_help
            exit 1
            ;;
    esac
}

main "$@"
