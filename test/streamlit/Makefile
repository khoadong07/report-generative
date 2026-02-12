.PHONY: help build run stop restart logs clean shell test build-weekly run-weekly stop-weekly logs-weekly

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Daily Report (default):"
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
	@echo ""
	@echo "Weekly Report:"
	@echo "  make build-weekly   - Build Weekly Docker image"
	@echo "  make run-weekly     - Run Weekly container (development)"
	@echo "  make run-weekly-prod - Run Weekly container (production)"
	@echo "  make stop-weekly    - Stop Weekly container"
	@echo "  make restart-weekly - Restart Weekly container"
	@echo "  make logs-weekly    - View Weekly container logs"
	@echo "  make logs-weekly-f  - Follow Weekly container logs"
	@echo "  make shell-weekly   - Open shell in Weekly container"
	@echo "  make clean-weekly   - Remove Weekly container and image"

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

# ============================================
# WEEKLY REPORT COMMANDS
# ============================================

# Build Weekly Docker image
build-weekly:
	@echo "🔨 Building Weekly Docker image..."
	docker-compose -f docker-compose.weekly.yml build

# Run Weekly container (development)
run-weekly:
	@echo "🚀 Starting Weekly Streamlit app (development)..."
	docker-compose -f docker-compose.weekly.yml up -d
	@echo "✅ Weekly app running at http://localhost:8523"

# Run Weekly container (production)
run-weekly-prod:
	@echo "🚀 Starting Weekly Streamlit app (production)..."
	docker-compose -f docker-compose.prod.weekly.yml up -d
	@echo "✅ Weekly app running at http://localhost:8523"

# Stop Weekly container
stop-weekly:
	@echo "🛑 Stopping Weekly container..."
	docker-compose -f docker-compose.weekly.yml down

# Restart Weekly container
restart-weekly:
	@echo "🔄 Restarting Weekly container..."
	docker-compose -f docker-compose.weekly.yml restart

# View Weekly logs
logs-weekly:
	docker-compose -f docker-compose.weekly.yml logs

# Follow Weekly logs
logs-weekly-f:
	docker-compose -f docker-compose.weekly.yml logs -f

# Open shell in Weekly container
shell-weekly:
	docker-compose -f docker-compose.weekly.yml exec streamlit-weekly /bin/bash

# Clean up Weekly
clean-weekly:
	@echo "🧹 Cleaning up Weekly..."
	docker-compose -f docker-compose.weekly.yml down
	docker rmi streamlit_streamlit-weekly:latest || true

# Check Weekly status
status-weekly:
	@echo "📊 Weekly container status:"
	docker-compose -f docker-compose.weekly.yml ps

# Rebuild and run Weekly
rebuild-weekly: clean-weekly build-weekly run-weekly
	@echo "✅ Weekly rebuild complete"

