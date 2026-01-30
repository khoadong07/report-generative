.PHONY: help build up down restart logs status health backup clean update shell ssl-generate ssl-check

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help:
	@echo "$(BLUE)Social Listening Report Generator - Makefile$(NC)"
	@echo ""
	@echo "$(GREEN)Development Commands:$(NC)"
	@echo "  make dev-up          Start development environment"
	@echo "  make dev-down        Stop development environment"
	@echo "  make dev-logs        View development logs"
	@echo ""
	@echo "$(GREEN)Production Commands:$(NC)"
	@echo "  make build           Build Docker images"
	@echo "  make up              Start production services"
	@echo "  make down            Stop production services"
	@echo "  make restart         Restart services"
	@echo "  make logs            View service logs"
	@echo "  make status          Show service status"
	@echo "  make health          Check service health"
	@echo ""
	@echo "$(GREEN)Maintenance Commands:$(NC)"
	@echo "  make backup          Backup data and reports"
	@echo "  make clean           Clean up containers and images"
	@echo "  make update          Update and restart services"
	@echo "  make shell           Open shell in app container"
	@echo ""
	@echo "$(GREEN)SSL Commands:$(NC)"
	@echo "  make ssl-generate    Generate self-signed SSL certificate"
	@echo "  make ssl-check       Check SSL certificate validity"
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@echo "  make install         Install dependencies"
	@echo "  make lint            Run code linting"
	@echo "  make format          Format code"

# Development
dev-up:
	@echo "$(BLUE)Starting development environment...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Development environment started$(NC)"
	@echo "Access at: http://localhost:8501"

dev-down:
	@echo "$(BLUE)Stopping development environment...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Development environment stopped$(NC)"

dev-logs:
	docker-compose logs -f app

# Production
build:
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose -f docker-compose.prod.yml build --no-cache
	@echo "$(GREEN)✓ Images built successfully$(NC)"

up:
	@echo "$(BLUE)Starting production services...$(NC)"
	docker-compose -f docker-compose.prod.yml up -d
	@sleep 3
	@make status
	@echo "$(GREEN)✓ Services started$(NC)"

down:
	@echo "$(BLUE)Stopping production services...$(NC)"
	docker-compose -f docker-compose.prod.yml down
	@echo "$(GREEN)✓ Services stopped$(NC)"

restart:
	@echo "$(BLUE)Restarting services...$(NC)"
	docker-compose -f docker-compose.prod.yml restart
	@sleep 3
	@make status
	@echo "$(GREEN)✓ Services restarted$(NC)"

logs:
	docker-compose -f docker-compose.prod.yml logs -f

status:
	@echo "$(BLUE)Service Status:$(NC)"
	docker-compose -f docker-compose.prod.yml ps

health:
	@echo "$(BLUE)Checking service health...$(NC)"
	@docker-compose -f docker-compose.prod.yml exec app curl -s http://localhost:8501/_stcore/health > /dev/null && echo "$(GREEN)✓ App is healthy$(NC)" || echo "$(RED)✗ App is unhealthy$(NC)"
	@docker-compose -f docker-compose.prod.yml exec nginx curl -s http://localhost > /dev/null && echo "$(GREEN)✓ Nginx is healthy$(NC)" || echo "$(RED)✗ Nginx is unhealthy$(NC)"

# Maintenance
backup:
	@echo "$(BLUE)Backing up data...$(NC)"
	@bash deploy.sh backup
	@echo "$(GREEN)✓ Backup completed$(NC)"

clean:
	@echo "$(BLUE)Cleaning up...$(NC)"
	docker container prune -f
	docker image prune -f
	docker volume prune -f
	@echo "$(GREEN)✓ Cleanup completed$(NC)"

update:
	@echo "$(BLUE)Updating application...$(NC)"
	git pull origin main
	@make build
	@make restart
	@echo "$(GREEN)✓ Update completed$(NC)"

shell:
	@echo "$(BLUE)Opening shell in app container...$(NC)"
	docker-compose -f docker-compose.prod.yml exec app /bin/bash

# SSL
ssl-generate:
	@echo "$(BLUE)Generating SSL certificate...$(NC)"
	@mkdir -p ssl
	@openssl req -x509 -newkey rsa:4096 \
		-keyout ssl/key.pem \
		-out ssl/cert.pem \
		-days 365 \
		-nodes \
		-subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
	@chmod 600 ssl/key.pem
	@chmod 644 ssl/cert.pem
	@echo "$(GREEN)✓ SSL certificate generated$(NC)"
	@echo "Certificate: ssl/cert.pem"
	@echo "Key: ssl/key.pem"

ssl-check:
	@echo "$(BLUE)Checking SSL certificate...$(NC)"
	@openssl x509 -in ssl/cert.pem -text -noout

# Utilities
install:
	@echo "$(BLUE)Installing dependencies...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

lint:
	@echo "$(BLUE)Running linting...$(NC)"
	pylint app.py main.py data_loader.py slides.py prompt_builder.py prompt_template.py
	@echo "$(GREEN)✓ Linting completed$(NC)"

format:
	@echo "$(BLUE)Formatting code...$(NC)"
	black app.py main.py data_loader.py slides.py prompt_builder.py prompt_template.py
	@echo "$(GREEN)✓ Code formatted$(NC)"

# Default
.DEFAULT_GOAL := help
