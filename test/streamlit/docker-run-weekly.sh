#!/bin/bash

# Script to run Weekly Report Generator with Docker Compose

echo "🚀 Starting Weekly Report Generator with Docker Compose..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ .env file created. Please edit it with your API credentials."
        echo ""
        exit 1
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed!"
    echo "Please install Docker Compose first."
    exit 1
fi

# Use docker compose (new) or docker-compose (old)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo "🔨 Building and starting Weekly Report Generator..."
$DOCKER_COMPOSE -f docker-compose.weekly.yml up --build -d

echo ""
echo "✅ Weekly Report Generator is starting..."
echo ""
echo "📊 Access the app at: http://localhost:8523"
echo ""
echo "📝 Useful commands:"
echo "   View logs:    $DOCKER_COMPOSE -f docker-compose.weekly.yml logs -f"
echo "   Stop app:     $DOCKER_COMPOSE -f docker-compose.weekly.yml down"
echo "   Restart app:  $DOCKER_COMPOSE -f docker-compose.weekly.yml restart"
echo ""
