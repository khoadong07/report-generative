#!/bin/bash
# Quick start script for Slide Prompt Generator (Docker)

echo "🚀 Starting Slide Prompt Generator (Streamlit + API)..."
echo ""

# Check if .env exists in root directory
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found in root directory"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "❗ Please edit .env and add your API credentials"
    echo ""
fi

# Copy .env to deployment directory for docker-compose
cp .env deployment/.env 2>/dev/null || echo "Warning: Could not copy .env to deployment directory"

# Create directories if they don't exist
mkdir -p uploads logs

# Check if user wants to include nginx
if [ "$1" = "--with-nginx" ]; then
    echo "🌐 Starting with Nginx reverse proxy..."
    docker-compose -f deployment/docker-compose.yml --profile with-nginx up --build
else
    echo "🐳 Starting Docker containers..."
    echo ""
    echo "Services:"
    echo "  📊 Streamlit App: http://localhost:8522"
    echo "  🚀 FastAPI Server: http://localhost:8524"
    echo "  📚 API Docs: http://localhost:8524/docs"
    echo ""
    
    # Start containers
    docker-compose -f deployment/docker-compose.yml up --build
fi
