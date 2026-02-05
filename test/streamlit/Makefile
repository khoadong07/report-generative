.PHONY: help build run stop restart logs clean shell test

# Default target
help:
	@echo "Available commands:"
	@echo "  make build       - Build Docker image"
	@echo "  make run         - Run container (development)"
	@echo "  make run-prod    - Run container (production with nginx)"
	@echo "  make stop        - Stop container"
	@echo "  make restart     - Restart container"
	@echo "  make logs        - View container logs"
	@echo "  make logs-f      - Follow container logs"
	@echo "  make shell       - Open shell in container"
	@echo "  make clean       - Remove container and image"
	@echo "  make clean-all   - Remove everything including volumes"
	@echo "  make test        - Test the application"

# Build Docker image
build:
	@echo "🔨 Building Docker image..."
	docker-compose build

# Run container (development)
run:
	@echo "🚀 Starting Streamlit app (development)..."
	docker-compose up -d
	@echo "✅ App running at http://localhost:8501"

# Run container (production)
run-prod:
	@echo "🚀 Starting Streamlit app (production)..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✅ App running at http://localhost:80"

# Stop container
stop:
	@echo "🛑 Stopping container..."
	docker-compose down

# Restart container
restart:
	@echo "🔄 Restarting container..."
	docker-compose restart

# View logs
logs:
	docker-compose logs

# Follow logs
logs-f:
	docker-compose logs -f

# Open shell in container
shell:
	docker-compose exec streamlit-app /bin/bash

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down
	docker rmi slide-prompt-generator:latest || true

# Clean everything
clean-all:
	@echo "🧹 Cleaning everything..."
	docker-compose down -v
	docker rmi slide-prompt-generator:latest || true
	rm -rf uploads/*

# Test
test:
	@echo "🧪 Testing application..."
	docker-compose exec streamlit-app python -m pytest || echo "No tests found"

# Check status
status:
	@echo "📊 Container status:"
	docker-compose ps

# View resource usage
stats:
	docker stats slide-prompt-generator

# Rebuild and run
rebuild: clean build run
	@echo "✅ Rebuild complete"
