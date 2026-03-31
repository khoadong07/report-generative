#!/bin/bash

# Script to manage Masan Weekly Report Docker service

set -e

COMPOSE_FILE="docker-compose.weekly.yml"
SERVICE_NAME="streamlit-masan"

case "$1" in
    start)
        echo "Starting Masan service..."
        docker-compose -f $COMPOSE_FILE up -d $SERVICE_NAME
        echo "Masan service started at http://localhost:8524"
        ;;
    stop)
        echo "Stopping Masan service..."
        docker-compose -f $COMPOSE_FILE stop $SERVICE_NAME
        echo "Masan service stopped"
        ;;
    restart)
        echo "Restarting Masan service..."
        docker-compose -f $COMPOSE_FILE restart $SERVICE_NAME
        echo "Masan service restarted"
        ;;
    logs)
        echo "Showing Masan service logs..."
        docker-compose -f $COMPOSE_FILE logs -f $SERVICE_NAME
        ;;
    build)
        echo "Building Masan service..."
        docker-compose -f $COMPOSE_FILE build $SERVICE_NAME
        echo "Build complete"
        ;;
    rebuild)
        echo "Rebuilding and restarting Masan service..."
        docker-compose -f $COMPOSE_FILE up -d --build $SERVICE_NAME
        echo "Masan service rebuilt and started at http://localhost:8524"
        ;;
    status)
        echo "Checking Masan service status..."
        docker-compose -f $COMPOSE_FILE ps $SERVICE_NAME
        ;;
    shell)
        echo "Opening shell in Masan container..."
        docker exec -it slide-prompt-generator-masan /bin/bash
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|build|rebuild|status|shell}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the Masan service"
        echo "  stop     - Stop the Masan service"
        echo "  restart  - Restart the Masan service"
        echo "  logs     - Show service logs (follow mode)"
        echo "  build    - Build the Docker image"
        echo "  rebuild  - Rebuild and restart the service"
        echo "  status   - Check service status"
        echo "  shell    - Open bash shell in container"
        exit 1
        ;;
esac

exit 0
