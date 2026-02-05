#!/bin/bash
# Quick script to run Docker container

set -e

echo "🐳 Slide Prompt Generator - Docker Runner"
echo "=========================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "📝 Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env created. Please edit it with your API credentials:"
        echo "   nano .env"
        exit 1
    else
        echo "❌ .env.example not found either!"
        exit 1
    fi
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

# Parse command line arguments
MODE=${1:-dev}

case $MODE in
    dev|development)
        echo "🚀 Starting in DEVELOPMENT mode..."
        docker-compose up -d
        echo ""
        echo "✅ App is running!"
        echo "📍 URL: http://localhost:8501"
        echo ""
        echo "📋 Useful commands:"
        echo "   View logs:    docker-compose logs -f"
        echo "   Stop:         docker-compose down"
        echo "   Restart:      docker-compose restart"
        echo "   Shell:        docker-compose exec streamlit-app bash"
        ;;
    
    prod|production)
        echo "🚀 Starting in PRODUCTION mode..."
        docker-compose -f docker-compose.prod.yml up -d
        echo ""
        echo "✅ App is running!"
        echo "📍 URL: http://localhost:80"
        echo "📍 Direct: http://localhost:8501"
        echo ""
        echo "📋 Useful commands:"
        echo "   View logs:    docker-compose -f docker-compose.prod.yml logs -f"
        echo "   Stop:         docker-compose -f docker-compose.prod.yml down"
        echo "   Restart:      docker-compose -f docker-compose.prod.yml restart"
        ;;
    
    build)
        echo "🔨 Building Docker image..."
        docker-compose build
        echo "✅ Build complete!"
        ;;
    
    stop)
        echo "🛑 Stopping containers..."
        docker-compose down
        docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
        echo "✅ Stopped!"
        ;;
    
    logs)
        echo "📋 Showing logs (Ctrl+C to exit)..."
        docker-compose logs -f
        ;;
    
    clean)
        echo "🧹 Cleaning up..."
        docker-compose down -v
        docker-compose -f docker-compose.prod.yml down -v 2>/dev/null || true
        docker rmi slide-prompt-generator:latest 2>/dev/null || true
        echo "✅ Cleaned!"
        ;;
    
    *)
        echo "Usage: $0 {dev|prod|build|stop|logs|clean}"
        echo ""
        echo "Commands:"
        echo "  dev     - Run in development mode (default)"
        echo "  prod    - Run in production mode with nginx"
        echo "  build   - Build Docker image"
        echo "  stop    - Stop all containers"
        echo "  logs    - View logs"
        echo "  clean   - Remove containers and images"
        exit 1
        ;;
esac
